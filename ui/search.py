"""Search screen for videos."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, DataTable, Input, Button
from textual.reactive import reactive

from youtube_api import YouTubeAPI, YouTubeAPIError


class SearchScreen(Static):
    """Search screen widget."""

    current_query: reactive[str] = reactive("")
    videos: reactive[list] = reactive([])

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize search screen."""
        super().__init__()
        self.youtube = youtube_api

    def compose(self) -> ComposeResult:
        """Compose the search screen."""
        with Vertical():
            yield Static("🔍 Search YouTube", classes="info")
            with Horizontal():
                yield Input(placeholder="Enter search query...", id="search-input")
                yield Button("Search", variant="primary", id="search-btn")
            yield DataTable(id="search-results")

    def on_mount(self) -> None:
        """Set up the data table."""
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Title", "Channel", "Duration", "Views", "Published")

        # Show helpful message
        table.add_row("Type a query and press Enter or click Search", "", "", "", "")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search input submission."""
        if event.input.id == "search-input":
            self.perform_search()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "search-btn":
            self.perform_search()

    def perform_search(self) -> None:
        """Perform the search."""
        search_input = self.query_one("#search-input", Input)
        query = search_input.value.strip()

        if not query:
            return

        self.current_query = query
        table = self.query_one(DataTable)
        table.clear()

        # Show loading message
        row_key = table.add_row("Searching...", "", "", "", "")

        try:
            # Perform search
            results = self.youtube.search_videos(query, max_results=25)
            self.videos = results

            # Clear table and populate with results
            table.clear()

            if not results:
                table.add_row("No results found", "", "", "", "")
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
        if not self.videos or event.row_key.value >= len(self.videos):
            return

        video = self.videos[event.row_key.value]
        url = video['url']

        try:
            webbrowser.open(url)
            self.app.notify(f"Opening: {video['title'][:50]}...")
        except Exception as e:
            self.app.notify(f"Failed to open browser: {e}", severity="error")

    def refresh_data(self) -> None:
        """Refresh search results."""
        if self.current_query:
            self.perform_search()
