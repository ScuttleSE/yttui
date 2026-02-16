"""Watch history screen."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable
from textual.reactive import reactive

from youtube_api import YouTubeAPI, YouTubeAPIError


class HistoryScreen(Static):
    """Watch history screen widget."""

    videos: reactive[list] = reactive([])

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize history screen."""
        super().__init__()
        self.youtube = youtube_api

    def compose(self) -> ComposeResult:
        """Compose the history screen."""
        with Vertical():
            yield Static("🕐 Watch History", classes="info")
            yield Static(
                "Note: Watch history API access is restricted. Showing activity feed instead.",
                classes="info"
            )
            yield DataTable(id="history-table")

    def on_mount(self) -> None:
        """Set up the data table and load history."""
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Title", "Channel", "Duration", "Views", "Published")

        self.refresh_data()

    def refresh_data(self) -> None:
        """Load watch history."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading history...", "", "", "", "")

        try:
            results = self.youtube.get_watch_history(max_results=50)
            self.videos = results

            table.clear()

            if not results:
                table.add_row("No history found", "", "", "", "")
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
            table.add_row("Watch history requires special API access", "", "", "", "")
        except Exception as e:
            table.clear()
            table.add_row(f"Unexpected error: {e}", "", "", "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection - open video in browser."""
        if not self.videos or event.row_key.value >= len(self.videos):
            return

        video = self.videos[event.row_key.value]
        url = video['url']

        try:
            webbrowser.open(url)
            self.app.notify(f"Opening: {video['title'][:50]}...")
        except Exception as e:
            self.app.notify(f"Failed to open browser: {e}", severity="error")
