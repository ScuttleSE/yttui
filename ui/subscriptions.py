"""Subscriptions screen."""
import webbrowser
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable, Button
from textual.reactive import reactive

from youtube_api import YouTubeAPI, YouTubeAPIError


class SubscriptionsScreen(Static):
    """Subscriptions screen widget."""

    mode: reactive[str] = reactive("videos")  # "channels" or "videos"
    subscriptions: reactive[list] = reactive([])
    videos: reactive[list] = reactive([])

    def __init__(self, youtube_api: YouTubeAPI):
        """Initialize subscriptions screen."""
        super().__init__()
        self.youtube = youtube_api

    def compose(self) -> ComposeResult:
        """Compose the subscriptions screen."""
        with Vertical():
            yield Static("📺 Your Subscriptions - Latest Videos", classes="info")
            yield Button("Show Channels", variant="primary", id="toggle-mode")
            yield DataTable(id="subscriptions-table")

    def on_mount(self) -> None:
        """Set up the data table and load subscriptions."""
        self.setup_videos_view()
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
        import logging
        from pathlib import Path

        # Setup debug logging
        log_file = Path.home() / '.config' / 'yt-tui' / 'subscriptions_debug.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(log_file),
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s'
        )
        logger = logging.getLogger(__name__)

        logger.info("=== LOAD SUBSCRIPTION CHANNELS ===")

        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading subscriptions...", "", "")

        try:
            logger.info("Calling get_subscriptions(max_results=50)...")
            results = self.youtube.get_subscriptions(max_results=50)
            logger.info(f"Got {len(results)} subscriptions")
            self.subscriptions = results

            table.clear()

            if not results:
                logger.warning("No subscriptions found")
                table.add_row("No subscriptions found", "", "")
                return

            for i, sub in enumerate(results):
                logger.info(f"Subscription {i+1}: {sub['title'][:40]}")
                table.add_row(
                    sub['title'][:40],
                    sub['description'][:80],
                    sub['published_at']
                )

            logger.info(f"Successfully loaded {len(results)} subscriptions")
            logger.info("===================\n")

        except YouTubeAPIError as e:
            logger.error(f"YouTubeAPIError: {e}")
            import traceback
            logger.error(traceback.format_exc())
            table.clear()
            table.add_row(f"Error: {e}", "", "")
            table.add_row("Note: You need to be authenticated to view subscriptions", "", "")
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            table.clear()
            table.add_row(f"Unexpected error: {e}", "", "")

    def load_videos(self) -> None:
        """Load recent videos from subscriptions."""
        import logging
        from pathlib import Path

        # Setup debug logging
        log_file = Path.home() / '.config' / 'yt-tui' / 'subscriptions_debug.log'
        log_file.parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=str(log_file),
            level=logging.DEBUG,
            format='%(asctime)s - %(message)s'
        )
        logger = logging.getLogger(__name__)

        logger.info("=== LOAD SUBSCRIPTION VIDEOS ===")

        table = self.query_one(DataTable)
        table.clear()
        table.add_row("Loading videos from subscriptions...", "", "", "", "")

        try:
            logger.info("Calling get_subscription_videos(max_results=50)...")
            results = self.youtube.get_subscription_videos(max_results=50)
            logger.info(f"Got {len(results)} videos")
            self.videos = results

            table.clear()

            if not results:
                logger.warning("No videos found in results")
                table.add_row("No videos found", "", "", "", "")
                return

            for i, video in enumerate(results):
                logger.info(f"Video {i+1}: {video['title'][:40]} - {video['channel']}")
                table.add_row(
                    video['title'][:60],
                    video['channel'][:30],
                    video['duration'],
                    video['view_count'],
                    video['published_at']
                )

            logger.info(f"Successfully loaded {len(results)} videos")
            logger.info("===================\n")

        except YouTubeAPIError as e:
            logger.error(f"YouTubeAPIError: {e}")
            import traceback
            logger.error(traceback.format_exc())
            table.clear()
            table.add_row(f"Error: {e}", "", "", "", "")
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            table.clear()
            table.add_row(f"Unexpected error: {e}", "", "", "", "")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection."""
        row_index = event.cursor_row

        if self.mode == "videos":
            # Open video
            if not self.videos or row_index >= len(self.videos):
                return

            video = self.videos[row_index]
            url = video['url']

            try:
                webbrowser.open(url)
                self.app.notify(f"Opening: {video['title'][:50]}...")
            except Exception as e:
                self.app.notify(f"Failed to open browser: {e}", severity="error")
        else:
            # Open channel
            if not self.subscriptions or row_index >= len(self.subscriptions):
                return

            channel = self.subscriptions[row_index]
            url = f"https://www.youtube.com/channel/{channel['channel_id']}"

            try:
                webbrowser.open(url)
                self.app.notify(f"Opening: {channel['title'][:50]}...")
            except Exception as e:
                self.app.notify(f"Failed to open browser: {e}", severity="error")
