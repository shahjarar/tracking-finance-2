import sys
import os

# Add current folder to Python path
sys.path.append(os.path.abspath("."))

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# from features.transactions.transactions import manage_transactions
# from features.budgets.budgets import manage_budgets

console = Console()

def display_main_menu():
    console.print(
        Panel(
            Text("Personal Finance Tracker CLI", justify="center", style="bold blue"),
            title="[green]Welcome[/green]"
        )
    )
    
    choices = ["Manage Transactions", "Manage Budgets", "Exit"]
    
    choice = questionary.select(
        "What would you like to do?",
        choices=choices
    ).ask()
    
    return choice

def main():
    while True:
        choice = display_main_menu()

        # if choice == "Manage Transactions":
        #     manage_transactions()
        # if choice == "Manage Budgets":
        #     manage_budgets()
        if choice == "Exit":
            console.print(
                Panel(
                    Text("Thank you for using the Finance Tracker!", justify="center", style="bold green"),
                    title="[blue]Goodbye[/blue]"
                )
            )
            break

if __name__ == "__main__":
    main()
