"""Trending videos screen."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable
from textual.reactive import reactive

from youtube_api import YouTubeAPI, YouTubeAPIError


class TrendingScreen(Static):
    """Trending videos screen widget."""

    videos: reactive[list] = reactive([])

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize trending screen."""
        super().__init__()
        self.youtube = youtube_api

    def compose(self) -> ComposeResult:
        """Compose the trending screen."""
        with Vertical():
            yield Static("🔥 Trending Videos", classes="info")
            yield DataTable(id="trending-table")

    def on_mount(self) -> None:
        """Set up the data table and load trending videos."""
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Title", "Channel", "Duration", "Views", "Published")

        self.refresh_data()

    def refresh_data(self) -> None:
        """Load trending videos."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading trending videos...", "", "", "", "")

        try:
            results = self.youtube.get_trending_videos(max_results=25)
            self.videos = results

            table.clear()

            if not results:
                table.add_row("No trending videos found", "", "", "", "")
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
            self.app.notify(f"Opening: {video['title'][:50]}...")
        except Exception as e:
            self.app.notify(f"Failed to open browser: {e}", severity="error")
