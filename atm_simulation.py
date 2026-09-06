"""A small command-line ATM simulation.

Run this file directly to try the interactive application:

    python atm_simulation.py
"""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from getpass import getpass
from typing import Dict, Optional


def money_to_cents(value: str) -> int:
    """Convert a user-entered amount into whole cents."""
    try:
        amount = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValueError("Enter a valid amount, for example 25.00.") from exc

    cents = int(amount * 100)
    if cents <= 0:
        raise ValueError("The amount must be greater than zero.")
    return cents


def format_money(cents: int) -> str:
    """Format cents as a currency value without using floating point math."""
    return f"${cents / 100:,.2f}"


@dataclass
class Account:
    """A bank account used by the simulation."""

    account_number: str
    pin: str
    balance_cents: int = 0

    def verify_pin(self, pin: str) -> bool:
        return self.pin == pin

    def deposit(self, amount_cents: int) -> None:
        if amount_cents <= 0:
            raise ValueError("The amount must be greater than zero.")
        self.balance_cents += amount_cents

    def withdraw(self, amount_cents: int) -> None:
        if amount_cents <= 0:
            raise ValueError("The amount must be greater than zero.")
        if amount_cents > self.balance_cents:
            raise ValueError("Insufficient funds.")
        self.balance_cents -= amount_cents


class ATM:
    """Coordinates authentication and transactions for a group of accounts."""

    MAX_PIN_ATTEMPTS = 3

    def __init__(self, accounts: Dict[str, Account]) -> None:
        self.accounts = accounts

    def authenticate(self, account_number: str, pin_attempts: list[str]) -> Optional[Account]:
        """Return an account after a successful PIN attempt, or None."""
        account = self.accounts.get(account_number)
        if account is None:
            return None

        for pin in pin_attempts[: self.MAX_PIN_ATTEMPTS]:
            if account.verify_pin(pin):
                return account
        return None

    def run(self) -> None:
        print("Welcome to the Python ATM")
        account_number = input("Account number (or 'q' to quit): ").strip()
        if account_number.lower() == "q":
            print("Goodbye!")
            return

        account = self.accounts.get(account_number)
        if account is None:
            print("Account not found.")
            return

        for attempt in range(self.MAX_PIN_ATTEMPTS):
            pin = getpass("PIN: ")
            if account.verify_pin(pin):
                break
            remaining = self.MAX_PIN_ATTEMPTS - attempt - 1
            if remaining:
                print(f"Incorrect PIN. {remaining} attempt(s) remaining.")
        else:
            print("Too many incorrect attempts. Your session has ended.")
            return

        print(f"\nSigned in as account {account.account_number}.")
        self._session(account)

    def _session(self, account: Account) -> None:
        while True:
            print(
                "\n1. Check balance\n"
                "2. Deposit\n"
                "3. Withdraw\n"
                "4. Log out"
            )
            choice = input("Choose an option: ").strip()

            if choice == "1":
                print(f"Available balance: {format_money(account.balance_cents)}")
            elif choice in {"2", "3"}:
                self._process_transaction(account, choice)
            elif choice == "4":
                print("You have been logged out.")
                return
            else:
                print("Please choose an option from 1 to 4.")

    @staticmethod
    def _process_transaction(account: Account, choice: str) -> None:
        try:
            amount_cents = money_to_cents(input("Amount: ").strip())
            if choice == "2":
                account.deposit(amount_cents)
                action = "Deposited"
            else:
                account.withdraw(amount_cents)
                action = "Withdrew"
            print(f"{action} {format_money(amount_cents)}.")
            print(f"New balance: {format_money(account.balance_cents)}")
        except ValueError as error:
            print(f"Transaction declined: {error}")


def create_demo_atm() -> ATM:
    """Create the demo accounts used when the app is run locally."""
    return ATM(
        {
            "1001": Account("1001", "1234", balance_cents=125_000),
            "1002": Account("1002", "2468", balance_cents=50_000),
        }
    )


if __name__ == "__main__":
    create_demo_atm().run()
