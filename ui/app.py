"""Main Textual application."""
import webbrowser
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, TabbedContent, TabPane, Static, DataTable, Input, Button
from textual.screen import Screen

from youtube_api import YouTubeAPI, YouTubeAPIError
from ui.search import SearchScreen
from ui.subscriptions import SubscriptionsScreen
from ui.history import HistoryScreen
from ui.playlists import PlaylistsScreen, PlaylistVideosScreen
from ui.trending import TrendingScreen


class YouTubeApp(App):
    """A Textual app for browsing YouTube."""

    CSS = """
    Screen {
        background: $surface;
    }

    Header {
        background: $primary;
        color: $text;
        dock: top;
    }

    Footer {
        background: $panel;
        color: $text;
        dock: bottom;
    }

    TabbedContent {
        height: 100%;
        border: solid $primary;
    }

    TabPane {
        padding: 1 2;
    }

    DataTable {
        height: 100%;
        border: none;
    }

    DataTable > .datatable--cursor {
        background: $accent;
        color: $text;
    }

    Input {
        margin: 1 0;
        border: solid $primary;
    }

    Button {
        margin: 0 1;
    }

    .error {
        background: $error;
        color: $text;
        padding: 1 2;
        margin: 1 0;
        border: solid red;
    }

    .info {
        background: $panel;
        color: $text-muted;
        padding: 1 2;
        margin: 1 0;
    }

    .video-info {
        padding: 1 2;
        background: $panel;
        border: solid $primary;
        margin: 1 0;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("r", "refresh", "Refresh"),
        Binding("/", "search", "Search"),
        Binding("1", "switch_tab('search')", "Search", show=False),
        Binding("2", "switch_tab('trending')", "Trending", show=False),
        Binding("3", "switch_tab('subscriptions')", "Subscriptions", show=False),
        Binding("4", "switch_tab('history')", "History", show=False),
        Binding("5", "switch_tab('playlists')", "Playlists", show=False),
    ]

    def __init__(self, youtube_api: YouTubeAPI):
        super().__init__()
        self.youtube = youtube_api
        self.title = "YT-TUI - YouTube Terminal Client"
        self.sub_title = "Navigate with Tab, Enter to play, / to search, q to quit"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with TabbedContent(initial="search"):
            with TabPane("Search", id="search"):
                yield SearchScreen(self.youtube)
            with TabPane("Trending", id="trending"):
                yield TrendingScreen(self.youtube)
            with TabPane("Subscriptions", id="subscriptions"):
                yield SubscriptionsScreen(self.youtube)
            with TabPane("History", id="history"):
                yield HistoryScreen(self.youtube)
            with TabPane("Playlists", id="playlists"):
                yield PlaylistsScreen(self.youtube)
        yield Footer()

    def action_refresh(self) -> None:
        """Refresh the current tab."""
        tabbed_content = self.query_one(TabbedContent)
        active_pane = tabbed_content.active

        # Find the screen widget in the active pane
        for widget in self.query("SearchScreen, TrendingScreen, SubscriptionsScreen, HistoryScreen, PlaylistsScreen"):
            if widget.ancestors and any(ancestor.id == active_pane for ancestor in widget.ancestors):
                if hasattr(widget, 'refresh_data'):
                    widget.refresh_data()
                break

    def action_search(self) -> None:
        """Focus on search tab and input."""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = "search"

        # Focus on the search input
        search_screen = self.query_one(SearchScreen)
        search_input = search_screen.query_one(Input)
        search_input.focus()

    def action_switch_tab(self, tab_id: str) -> None:
        """Switch to a specific tab."""
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.active = tab_id
