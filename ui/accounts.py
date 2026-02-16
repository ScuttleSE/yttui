"""Account management screen."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Button, Label
from textual.screen import ModalScreen
from textual.binding import Binding

from account_manager import AccountManager, Account


class AccountSwitcher(ModalScreen):
    """Modal screen for switching accounts."""

    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=True),
        Binding("q", "dismiss", "Close", show=False),
    ]

    CSS = """
    AccountSwitcher {
        align: center middle;
    }

    #account-dialog {
        width: 70;
        height: auto;
        max-height: 30;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }

    .account-item {
        height: auto;
        width: 100%;
        border: solid $panel;
        background: $panel;
        padding: 1 2;
        margin: 1 0;
    }

    .account-item:hover {
        border: solid $accent;
        background: $boost;
    }

    .account-item-active {
        border: solid $success;
        background: $success 30%;
    }

    .account-item-active:hover {
        border: solid $success;
        background: $success 50%;
    }

    .account-name {
        color: $text;
        text-style: bold;
    }

    .account-email {
        color: $text-muted;
    }

    .account-status {
        color: $success;
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
    """

    def __init__(self, account_manager: AccountManager):
        """Initialize account switcher."""
        super().__init__()
        self.account_manager = account_manager

    def compose(self) -> ComposeResult:
        """Compose the account switcher dialog."""
        with Vertical(id="account-dialog"):
            yield Static("Switch YouTube Account", classes="info")
            yield Static("Select an account or add a new one:", classes="account-email")

            with VerticalScroll():
                accounts = self.account_manager.get_all_accounts()
                if accounts:
                    for account in accounts:
                        with Container(
                            classes="account-item account-item-active" if account.is_active else "account-item",
                            id=f"account-{account.id}"
                        ):
                            yield Label(f"👤 {account.name}", classes="account-name")
                            yield Label(account.email, classes="account-email")
                            if account.is_active:
                                yield Label("✓ Active", classes="account-status")
                else:
                    yield Static("No accounts found. Add one below.", classes="account-email")

            with Horizontal(classes="dialog-buttons"):
                yield Button("Add Account", variant="primary", id="add-account")
                yield Button("Close", variant="default", id="close-dialog")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "close-dialog":
            self.dismiss(None)
        elif event.button.id == "add-account":
            self.dismiss("add_account")

    def on_container_click(self, event) -> None:
        """Handle account selection."""
        container = event.widget
        if container.id and container.id.startswith("account-"):
            account_id = container.id.replace("account-", "")

            # Switch to selected account
            if self.account_manager.switch_account(account_id):
                account = self.account_manager.get_account_by_id(account_id)
                self.dismiss(account)


class AccountInfoWidget(Static):
    """Widget showing current account info in the header."""

    def __init__(self, account_manager: AccountManager):
        """Initialize account info widget."""
        super().__init__()
        self.account_manager = account_manager
        self.update_display()

    def update_display(self):
        """Update the display with current account."""
        account = self.account_manager.get_active_account()
        if account:
            self.update(f"👤 {account.name} ({account.email})")
        else:
            self.update("👤 No account")

    def on_click(self) -> None:
        """Handle click - open account switcher."""
        self.app.push_screen(AccountSwitcher(self.account_manager), self.handle_account_switch)

    def handle_account_switch(self, result) -> None:
        """Handle account switch result."""
        if result == "add_account":
            # Trigger add account flow
            self.app.action_add_account()
        elif result:
            # Account switched
            self.update_display()
            self.app.notify(f"Switched to: {result.name}")
            # Reload the app with new account
            self.app.action_reload_with_account(result)
