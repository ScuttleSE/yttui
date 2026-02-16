"""YouTube API wrapper with methods for each feature."""
from typing import List, Dict, Optional, Any
from datetime import datetime
import re

from googleapiclient.errors import HttpError


class YouTubeAPIError(Exception):
    """Custom exception for YouTube API errors."""
    pass


class YouTubeAPI:
    """Wrapper for YouTube Data API v3."""

    def __init__(self, service):
        """Initialize with authenticated service."""
        self.service = service

    def _parse_duration(self, duration: str) -> str:
        """Parse ISO 8601 duration to readable format."""
        try:
            import re
            match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
            if not match:
                return "Unknown"

            hours, minutes, seconds = match.groups()
            hours = int(hours) if hours else 0
            minutes = int(minutes) if minutes else 0
            seconds = int(seconds) if seconds else 0

            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
        except:
            return "Unknown"

    def _format_number(self, num: int) -> str:
        """Format large numbers to readable format."""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)

    def _parse_date(self, date_str: str) -> str:
        """Parse ISO date to readable format."""
        try:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d')
        except:
            return date_str

    def search_videos(self, query: str, max_results: int = 25) -> List[Dict[str, Any]]:
        """
        Search for videos.

        Args:
            query: Search query string
            max_results: Maximum number of results to return

        Returns:
            List of video dictionaries with metadata
        """
        try:
            request = self.service.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=max_results,
                order="relevance"
            )
            response = request.execute()

            # Get video IDs to fetch additional details
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]

            if not video_ids:
                return []

            # Get video details (duration, view count, etc.)
            videos_request = self.service.videos().list(
                part="snippet,contentDetails,statistics",
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()

            results = []
            for item in videos_response.get('items', []):
                results.append(self._parse_video(item))

            return results

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("API quota exceeded. Please try again later.")
            raise YouTubeAPIError(f"Search failed: {e}")

    def get_subscriptions(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's subscriptions.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List of subscription dictionaries
        """
        try:
            request = self.service.subscriptions().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results,
                order="alphabetical"
            )
            response = request.execute()

            subscriptions = []
            for item in response.get('items', []):
                snippet = item['snippet']
                subscriptions.append({
                    'channel_id': snippet['resourceId']['channelId'],
                    'title': snippet['title'],
                    'description': snippet['description'][:200] if snippet.get('description') else '',
                    'thumbnail': snippet['thumbnails']['default']['url'],
                    'published_at': self._parse_date(snippet['publishedAt'])
                })

            return subscriptions

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("API quota exceeded or insufficient permissions.")
            raise YouTubeAPIError(f"Failed to get subscriptions: {e}")

    def get_subscription_videos(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent videos from subscribed channels.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List of video dictionaries
        """
        try:
            request = self.service.activities().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            )
            response = request.execute()

            videos = []
            video_ids = []

            for item in response.get('items', []):
                if item['snippet']['type'] == 'upload':
                    video_id = item['contentDetails']['upload']['videoId']
                    video_ids.append(video_id)

            if video_ids:
                # Get full video details
                videos_request = self.service.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(video_ids)
                )
                videos_response = videos_request.execute()

                for item in videos_response.get('items', []):
                    videos.append(self._parse_video(item))

            return videos

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("API quota exceeded or insufficient permissions.")
            raise YouTubeAPIError(f"Failed to get subscription videos: {e}")

    def get_watch_history(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's watch history.

        Note: Watch history API access is restricted. This may not work for all users.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List of video dictionaries
        """
        try:
            # Note: This requires special API access for watch history
            # Using activities API as alternative
            request = self.service.activities().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            )
            response = request.execute()

            videos = []
            video_ids = []

            for item in response.get('items', []):
                content = item.get('contentDetails', {})
                if 'upload' in content:
                    video_ids.append(content['upload']['videoId'])
                elif 'recommendation' in content:
                    video_ids.append(content['recommendation']['resourceId']['videoId'])

            if video_ids:
                videos_request = self.service.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(video_ids[:50])  # API limit
                )
                videos_response = videos_request.execute()

                for item in videos_response.get('items', []):
                    videos.append(self._parse_video(item))

            return videos

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("Watch history not available. This may require special API access.")
            raise YouTubeAPIError(f"Failed to get watch history: {e}")

    def get_playlists(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get user's playlists.

        Args:
            max_results: Maximum number of results to return

        Returns:
            List of playlist dictionaries
        """
        try:
            request = self.service.playlists().list(
                part="snippet,contentDetails",
                mine=True,
                maxResults=max_results
            )
            response = request.execute()

            playlists = []
            for item in response.get('items', []):
                snippet = item['snippet']
                playlists.append({
                    'id': item['id'],
                    'title': snippet['title'],
                    'description': snippet.get('description', '')[:200],
                    'thumbnail': snippet['thumbnails']['default']['url'],
                    'video_count': item['contentDetails']['itemCount'],
                    'published_at': self._parse_date(snippet['publishedAt'])
                })

            return playlists

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("API quota exceeded or insufficient permissions.")
            raise YouTubeAPIError(f"Failed to get playlists: {e}")

    def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get videos from a playlist.

        Args:
            playlist_id: ID of the playlist
            max_results: Maximum number of results to return

        Returns:
            List of video dictionaries
        """
        try:
            request = self.service.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=max_results
            )
            response = request.execute()

            video_ids = []
            for item in response.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            if not video_ids:
                return []

            videos_request = self.service.videos().list(
                part="snippet,contentDetails,statistics",
                id=','.join(video_ids)
            )
            videos_response = videos_request.execute()

            videos = []
            for item in videos_response.get('items', []):
                videos.append(self._parse_video(item))

            return videos

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("API quota exceeded or insufficient permissions.")
            raise YouTubeAPIError(f"Failed to get playlist videos: {e}")

    def get_trending_videos(self, max_results: int = 25, region_code: str = "US") -> List[Dict[str, Any]]:
        """
        Get trending videos (no authentication required).

        Args:
            max_results: Maximum number of results to return
            region_code: ISO 3166-1 alpha-2 country code

        Returns:
            List of video dictionaries
        """
        try:
            request = self.service.videos().list(
                part="snippet,contentDetails,statistics",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=max_results
            )
            response = request.execute()

            videos = []
            for item in response.get('items', []):
                videos.append(self._parse_video(item))

            return videos

        except HttpError as e:
            if e.resp.status == 403:
                raise YouTubeAPIError("API quota exceeded.")
            raise YouTubeAPIError(f"Failed to get trending videos: {e}")

    def _parse_video(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Parse video item from API response."""
        snippet = item['snippet']
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})

        return {
            'id': item['id'],
            'title': snippet['title'],
            'channel': snippet['channelTitle'],
            'channel_id': snippet['channelId'],
            'description': snippet.get('description', '')[:200],
            'thumbnail': snippet['thumbnails']['high']['url'] if 'high' in snippet['thumbnails'] else snippet['thumbnails']['default']['url'],
            'published_at': self._parse_date(snippet['publishedAt']),
            'duration': self._parse_duration(content_details.get('duration', '')),
            'view_count': self._format_number(int(statistics.get('viewCount', 0))),
            'like_count': self._format_number(int(statistics.get('likeCount', 0))),
            'url': f"https://www.youtube.com/watch?v={item['id']}"
        }
