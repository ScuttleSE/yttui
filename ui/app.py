"""Main Textual application."""
import webbrowser
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, TabbedContent, TabPane, Static, DataTable, Input, Button
from textual.screen import Screen

from youtube_api import YouTubeAPI, YouTubeAPIError
from account_manager import AccountManager
from auth import get_authenticated_service
from ui.search import SearchScreen
from ui.subscriptions import SubscriptionsScreen
from ui.history import HistoryScreen
from ui.playlists import PlaylistsScreen, PlaylistVideosScreen
from ui.trending import TrendingScreen
from ui.accounts import AccountSwitcher, AccountInfoWidget


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

    #account-bar {
        height: 1;
        background: $boost;
        color: $text;
        dock: top;
        padding: 0 2;
    }

    #account-bar Static {
        width: auto;
        text-style: bold;
        margin-right: 2;
    }

    #account-bar Static:hover {
        background: $accent;
        text-style: bold underline;
    }

    #account-bar {
        layout: horizontal;
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
        Binding("a", "switch_account", "Accounts"),
        Binding("1", "switch_tab('search')", "Search", show=False),
        Binding("2", "switch_tab('trending')", "Trending", show=False),
        Binding("3", "switch_tab('subscriptions')", "Subscriptions", show=False),
        Binding("4", "switch_tab('history')", "History", show=False),
        Binding("5", "switch_tab('playlists')", "Playlists", show=False),
    ]

    def __init__(self, youtube_api: YouTubeAPI, account_manager: AccountManager = None):
        super().__init__()
        self.youtube = youtube_api
        self.account_manager = account_manager
        self.title = "YT-TUI - YouTube Terminal Client"
        self.sub_title = "Tab: switch | Enter: play | /: search | a: accounts | q: quit"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        # Show account info if account manager is available
        if self.account_manager:
            with Container(id="account-bar"):
                yield AccountInfoWidget(self.account_manager)

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

    def action_switch_account(self) -> None:
        """Open account switcher."""
        if not self.account_manager:
            self.notify("Account switching not available", severity="warning")
            return

        self.push_screen(AccountSwitcher(self.account_manager), self.handle_account_switch)

    def handle_account_switch(self, result) -> None:
        """Handle account switch result."""
        if result == "add_account":
            self.action_add_account()
        elif result:
            # Account switched, need to reload
            self.notify(f"Switched to: {result.name}")
            self.action_reload_with_account(result)

    def action_add_account(self) -> None:
        """Add a new account."""
        if not self.account_manager:
            return

        self.notify("Opening browser for authentication...")

        try:
            result = self.account_manager.authenticate_new_account()
            if result:
                account, creds = result
                self.notify(f"Added account: {account.name}")

                # Switch to new account
                self.account_manager.switch_account(account.id)
                self.action_reload_with_account(account)
            else:
                self.notify("Authentication cancelled", severity="warning")
        except Exception as e:
            self.notify(f"Failed to add account: {e}", severity="error")

    def action_reload_with_account(self, account) -> None:
        """Reload app with different account."""
        if not self.account_manager:
            return

        try:
            # Get new service with switched account
            from googleapiclient.discovery import build
            creds = self.account_manager.get_credentials(account)
            if not creds:
                self.notify("Failed to get credentials", severity="error")
                return

            service = build('youtube', 'v3', credentials=creds)
            self.youtube = YouTubeAPI(service)

            # Update all screens with new API
            for screen in self.query("SearchScreen, TrendingScreen, SubscriptionsScreen, HistoryScreen, PlaylistsScreen"):
                screen.youtube = self.youtube

            # Update account info widget
            account_widget = self.query_one(AccountInfoWidget)
            account_widget.update_display()

            # Refresh current view
            self.action_refresh()

        except Exception as e:
            self.notify(f"Failed to switch account: {e}", severity="error")
