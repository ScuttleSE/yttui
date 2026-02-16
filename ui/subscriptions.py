"""Subscriptions screen."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable, Button
from textual.reactive import reactive

from youtube_api import YouTubeAPI, YouTubeAPIError


class SubscriptionsScreen(Static):
    """Subscriptions screen widget."""

    mode: reactive[str] = reactive("channels")  # "channels" or "videos"
    subscriptions: reactive[list] = reactive([])
    videos: reactive[list] = reactive([])

    def compose(self) -> ComposeResult:
        """Compose the subscriptions screen."""
        with Vertical():
            yield Static("📺 Your Subscriptions", classes="info")
            yield Button("Show Latest Videos", variant="primary", id="toggle-mode")
            yield DataTable(id="subscriptions-table")

    def on_mount(self) -> None:
        """Set up the data table and load subscriptions."""
        self.setup_channels_view()
        self.refresh_data()

    def setup_channels_view(self) -> None:
        """Set up table for channels view."""
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Channel", "Description", "Subscribed")

    def setup_videos_view(self) -> None:
        """Set up table for videos view."""
        table = self.query_one(DataTable)
        table.clear(columns=True)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("Title", "Channel", "Duration", "Views", "Published")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press to toggle between views."""
        if event.button.id == "toggle-mode":
            if self.mode == "channels":
                self.mode = "videos"
                event.button.label = "Show Channels"
                self.setup_videos_view()
                self.load_videos()
            else:
                self.mode = "channels"
                event.button.label = "Show Latest Videos"
                self.setup_channels_view()
                self.load_channels()

    def refresh_data(self) -> None:
        """Refresh current view."""
        if self.mode == "channels":
            self.load_channels()
        else:
            self.load_videos()

    def load_channels(self) -> None:
        """Load subscribed channels."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading subscriptions...", "", "")

        try:
            results = self.app.youtube.get_subscriptions(max_results=50)
            self.subscriptions = results

            table.clear()

            if not results:
                table.add_row("No subscriptions found", "", "")
                return

            for sub in results:
                table.add_row(
                    sub['title'][:40],
                    sub['description'][:80],
                    sub['published_at']
                )

        except YouTubeAPIError as e:
            table.clear()
            table.add_row(f"Error: {e}", "", "")
            table.add_row("Note: You need to be authenticated to view subscriptions", "", "")
        except Exception as e:
            table.clear()
            table.add_row(f"Unexpected error: {e}", "", "")

    def load_videos(self) -> None:
        """Load recent videos from subscriptions."""
        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading videos from subscriptions...", "", "", "", "")

        try:
            results = self.app.youtube.get_subscription_videos(max_results=50)
            self.videos = results

            table.clear()

            if not results:
                table.add_row("No videos found", "", "", "", "")
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
        """Handle row selection."""
        if self.mode == "videos":
            # Open video
            if not self.videos or event.row_key.value >= len(self.videos):
                return

            video = self.videos[event.row_key.value]
            url = video['url']

            try:
                webbrowser.open(url)
                self.app.notify(f"Opening: {video['title'][:50]}...")
            except Exception as e:
                self.app.notify(f"Failed to open browser: {e}", severity="error")
        else:
            # Open channel
            if not self.subscriptions or event.row_key.value >= len(self.subscriptions):
                return

            channel = self.subscriptions[event.row_key.value]
            url = f"https://www.youtube.com/channel/{channel['channel_id']}"

            try:
                webbrowser.open(url)
                self.app.notify(f"Opening: {channel['title'][:50]}...")
            except Exception as e:
                self.app.notify(f"Failed to open browser: {e}", severity="error")
