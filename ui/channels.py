"""Channel management and switching screen."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Button, Label
from textual.screen import ModalScreen
from textual.binding import Binding

from youtube_api import YouTubeAPI, YouTubeAPIError


class ChannelSwitcher(ModalScreen):
    """Modal screen for viewing and selecting channels."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=True),
        Binding("q", "dismiss", "Close", show=False),
    ]

    CSS = """
    ChannelSwitcher {
        align: center middle;
    }

    #channel-dialog {
        width: 80;
        height: auto;
        max-height: 35;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    .channel-item {
        height: auto;
        width: 100%;
        border: solid $panel;
        background: $panel;
        padding: 1 2;
        margin: 1 0;
    }

    .channel-item:hover {
        border: solid $accent;
        background: $boost;
    }

    .channel-name {
        color: $text;
        text-style: bold;
    }

    .channel-stats {
        color: $text-muted;
    }

    .channel-url {
        color: $accent;
        text-style: italic;
    }

    .dialog-buttons {
        height: auto;
        width: 100%;
        align: center middle;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
    }

    .loading {
        color: $text-muted;
        text-align: center;
        padding: 2;
    }

    .error {
        color: $error;
        text-align: center;
        padding: 2;
    }
    """

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize channel switcher."""
        super().__init__()
        self.youtube = youtube_api
        self.channels = []

    def compose(self) -> ComposeResult:
        """Compose the channel switcher dialog."""
        with Vertical(id="channel-dialog"):
            yield Static("📺 Your YouTube Channels", classes="info")
            yield Static("These are all channels associated with your account:", classes="channel-stats")

            with VerticalScroll(id="channels-list"):
                yield Static("Loading channels...", classes="loading")

            with Horizontal(classes="dialog-buttons"):
                yield Button("Close", variant="primary", id="close-dialog")

    def on_mount(self) -> None:
        """Load channels when mounted."""
        self.load_channels()

    def load_channels(self) -> None:
        """Load user's channels."""
        try:
            self.channels = self.youtube.get_my_channels()

            # Clear loading message
            scroll = self.query_one("#channels-list", VerticalScroll)
            scroll.remove_children()

            if not self.channels:
                with scroll:
                    scroll.mount(Static("No channels found for this account.", classes="channel-stats"))
                return

            # Display channels
            for channel in self.channels:
                with scroll:
                    with Container(classes="channel-item", id=f"channel-{channel['id']}"):
                        scroll.mount(Label(f"📺 {channel['title']}", classes="channel-name"))

                        stats = f"👥 {channel['subscriber_count']} subscribers • 🎥 {channel['video_count']} videos • 👁 {channel['view_count']} views"
                        scroll.mount(Label(stats, classes="channel-stats"))

                        if channel['custom_url']:
                            scroll.mount(Label(f"youtube.com/{channel['custom_url']}", classes="channel-url"))
                        else:
                            scroll.mount(Label(f"Channel ID: {channel['id'][:20]}...", classes="channel-url"))

        except YouTubeAPIError as e:
            scroll = self.query_one("#channels-list", VerticalScroll)
            scroll.remove_children()
            with scroll:
                scroll.mount(Static(f"Error loading channels: {e}", classes="error"))
        except Exception as e:
            scroll = self.query_one("#channels-list", VerticalScroll)
            scroll.remove_children()
            with scroll:
                scroll.mount(Static(f"Unexpected error: {e}", classes="error"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "close-dialog":
            self.dismiss(None)

    def on_container_click(self, event) -> None:
        """Handle channel selection."""
        container = event.widget
        if container.id and container.id.startswith("channel-"):
            channel_id = container.id.replace("channel-", "")

            # Find the channel
            for channel in self.channels:
                if channel['id'] == channel_id:
                    # Open channel in browser
                    try:
                        webbrowser.open(channel['url'])
                        self.app.notify(f"Opening channel: {channel['title']}")
                    except Exception as e:
                        self.app.notify(f"Failed to open browser: {e}", severity="error")
                    break


class ChannelInfoWidget(Static):
    """Widget showing channel count in the UI."""

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize channel info widget."""
        super().__init__()
        self.youtube = youtube_api
        self.channel_count = 0
        self.update_display()

    def update_display(self, count: int = None):
        """Update the display with channel count."""
        if count is not None:
            self.channel_count = count

        if self.channel_count == 0:
            self.update("📺 Channels: Loading...")
        elif self.channel_count == 1:
            self.update("📺 1 Channel")
        else:
            self.update(f"📺 {self.channel_count} Channels")

    def on_click(self) -> None:
        """Handle click - open channel switcher."""
        self.app.push_screen(ChannelSwitcher(self.youtube), self.handle_channel_result)

    def handle_channel_result(self, result) -> None:
        """Handle channel switcher result."""
        if result:
            self.app.notify(f"Channel selected: {result}")

    async def refresh_count(self):
        """Refresh channel count."""
        try:
            channels = self.youtube.get_my_channels()
            self.update_display(len(channels))
        except Exception:
            self.update_display(0)
