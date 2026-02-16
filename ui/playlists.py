"""Playlists screen."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable, Button
from textual.reactive import reactive
from textual.screen import Screen

from youtube_api import YouTubeAPI, YouTubeAPIError


class PlaylistVideosScreen(Screen):
    """Screen for displaying videos in a playlist."""

    def __init__(self, youtube_api: YouTubeAPI, playlist_id: str, playlist_title: str):
        super().__init__()
        self.youtube = youtube_api
        self.playlist_id = playlist_id
        self.playlist_title = playlist_title
        self.videos = []

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("q", "app.pop_screen", "Back"),
    ]

    CSS = """
    PlaylistVideosScreen {
        align: center middle;
    }

    #playlist-container {
        width: 90%;
        height: 90%;
        border: solid $primary;
        background: $surface;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the playlist videos screen."""
        with Vertical(id="playlist-container"):
            yield Static(f"📋 {self.playlist_title}", classes="info")
            yield Static("Press ESC or Q to go back", classes="info")
            yield DataTable(id="playlist-videos-table")

    def on_mount(self) -> None:
        """Set up the data table and load videos."""
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Title", "Channel", "Duration", "Views", "Published")

        self.load_videos()

    def load_videos(self) -> None:
        """Load videos from the playlist."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading playlist videos...", "", "", "", "")

        try:
            results = self.youtube.get_playlist_videos(self.playlist_id, max_results=50)
            self.videos = results

            table.clear()

            if not results:
                table.add_row("No videos in this playlist", "", "", "", "")
                return

            for video in results:
                table.add_row(
                    video['title'][:60],
                    video['channel'][:30],
                    video['duration'],
                    video['view_count'],
                    video['published_at']
                )

        except YouTubeAPIError as e:
            table.clear()
            table.add_row(f"Error: {e}", "", "", "", "")
        except Exception as e:
            table.clear()
            table.add_row(f"Unexpected error: {e}", "", "", "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection - open video in browser."""
        if not self.videos or event.row_key.value is None:
            return

        row_index = event.row_key.value
        if row_index >= len(self.videos):
            return

        video = self.videos[row_index]
        url = video['url']

        try:
            webbrowser.open(url)
            self.notify(f"Opening: {video['title'][:50]}...")
        except Exception as e:
            self.notify(f"Failed to open browser: {e}", severity="error")


class PlaylistsScreen(Static):
    """Playlists screen widget."""

    playlists: reactive[list] = reactive([])

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize playlists screen."""
        super().__init__()
        self.youtube = youtube_api

    def compose(self) -> ComposeResult:
        """Compose the playlists screen."""
        with Vertical():
            yield Static("📚 Your Playlists", classes="info")
            yield Static("Select a playlist to view its videos", classes="info")
            yield DataTable(id="playlists-table")

    def on_mount(self) -> None:
        """Set up the data table and load playlists."""
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Title", "Videos", "Description", "Created")

        self.refresh_data()

    def refresh_data(self) -> None:
        """Load playlists."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading playlists...", "", "", "")

        try:
            results = self.youtube.get_playlists(max_results=50)
            self.playlists = results

            table.clear()

            if not results:
                table.add_row("No playlists found", "", "", "")
                return

            for playlist in results:
                table.add_row(
                    playlist['title'][:40],
                    str(playlist['video_count']),
                    playlist['description'][:60],
                    playlist['published_at']
                )

        except YouTubeAPIError as e:
            table.clear()
            table.add_row(f"Error: {e}", "", "", "")
            table.add_row("You need to be authenticated to view playlists", "", "", "")
        except Exception as e:
            table.clear()
            table.add_row(f"Unexpected error: {e}", "", "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection - show playlist videos."""
        if not self.playlists or event.row_key.value is None:
            return

        row_index = event.row_key.value
        if row_index >= len(self.playlists):
            return

        playlist = self.playlists[row_index]

        # Push a new screen to show playlist videos
        screen = PlaylistVideosScreen(
            self.youtube,
            playlist['id'],
            playlist['title']
        )
        self.app.push_screen(screen)
