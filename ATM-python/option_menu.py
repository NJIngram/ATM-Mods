import json

from account import Account


class OptionMenu:
    """Handles user interaction and menu navigation for the ATM."""

    def __init__(self):
        self._data = {}  # dict mapping customer_number (int) -> Account

    @staticmethod
    def _format_money(amount):
        return "${:,.2f}".format(amount)

    # ------------------------------------------------------------------
    # Main Login Flow
    # ------------------------------------------------------------------

    def get_login(self):
        while True:
            try:
                customer_number = int(input("\nEnter your customer number: "))
                pin_number = int(input("\nEnter your PIN number: "))
                if customer_number in self._data:
                    acc = self._data[customer_number]
                    if pin_number == acc.get_pin_number():
                        self.get_account_type(acc)
                        self.save_accounts()
                        return
                print("\nWrong Customer Number or Pin Number")
            except ValueError:
                print("\nInvalid Character(s). Only Numbers.")

    # ------------------------------------------------------------------
    # Select Account Type (Checking or Savings)
    # ------------------------------------------------------------------
    def get_account_statement(self, acc_type):
        print("\n--- Account Statement ---")
        print("Checking Balance: " + self._format_money(acc_type.get_checking_balance()))
        print("Savings Balance: " + self._format_money(acc_type.get_saving_balance()))

    def get_account_type(self, acc):
        while True:
            try:
                print("\nSelect the account you want to access: ")
                print(" Type 1 - Checking Account")
                print(" Type 2 - Savings Account")
                print(" Type 3 - View Statement")
                print(" Type 4 - Exit")
                selection = int(input("\nChoice: "))
                if selection == 1:
                    self.get_checking(acc)
                elif selection == 2:
                    self.get_saving(acc)
                elif selection == 3:
                    self.get_account_statement(acc)
                elif selection == 4:
                    return
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

    # ------------------------------------------------------------------
    # Checking Account Operations Menu
    # ------------------------------------------------------------------

    def get_checking(self, acc):
        while True:
            try:
                print("\nChecking Account: ")
                print(" Type 1 - View Balance")
                print(" Type 2 - Withdraw Funds")
                print(" Type 3 - Deposit Funds")
                print(" Type 4 - Transfer Funds")
                print(" Type 5 - Exit")
                selection = int(input("\nChoice: "))
                if selection == 1:
                    print("\nChecking Account Balance: " + self._format_money(acc.get_checking_balance()))
                elif selection == 2:
                    acc.get_checking_withdraw_input()
                elif selection == 3:
                    acc.get_checking_deposit_input()
                elif selection == 4:
                    acc.get_transfer_input("Checking")
                elif selection == 5:
                    return
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

    # ------------------------------------------------------------------
    # Savings Account Operations Menu
    # ------------------------------------------------------------------

    def get_saving(self, acc):
        while True:
            try:
                print("\nSavings Account: ")
                print(" Type 1 - View Balance")
                print(" Type 2 - Withdraw Funds")
                print(" Type 3 - Deposit Funds")
                print(" Type 4 - Transfer Funds")
                print(" Type 5 - Exit")
                selection = int(input("\nChoice: "))
                if selection == 1:
                    print("\nSavings Account Balance: " + self._format_money(acc.get_saving_balance()))
                elif selection == 2:
                    acc.get_saving_withdraw_input()
                elif selection == 3:
                    acc.get_saving_deposit_input()
                elif selection == 4:
                    acc.get_transfer_input("Savings")
                elif selection == 5:
                    return
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

    # ------------------------------------------------------------------
    # Create New Account
    # ------------------------------------------------------------------

    def create_account(self):
        while True:
            try:
                cst_no = int(input("\nEnter your customer number "))
                if cst_no not in self._data:
                    break
                print("\nThis customer number is already registered")
            except ValueError:
                print("\nInvalid Choice.")

        try:
            pin = int(input("\nEnter PIN to be registered\n"))
        except ValueError:
            pin = 0

        self._data[cst_no] = Account(cst_no, pin)
        print("\nYour new account has been successfully registered!")
        self.save_accounts()
        print("\nRedirecting to login.............")
        self.get_login()

    #-------------------------------------------------------------------
    # Save accounts
    #-------------------------------------------------------------------
    def save_accounts(self):
        data = {}
        for cst_no, acc in self._data.items():
            data[str(cst_no)] = {
                "pin": acc.get_pin_number(),
                "checking_balance": acc.get_checking_balance(),
                "saving_balance": acc.get_saving_balance()
            }
        with open("accounts.json", "w") as f:
            json.dump(data, f)

    #------------------------------------------------------------------
    # Load accounts
    #------------------------------------------------------------------
    def load_accounts(self):
        try:
            with open("accounts.json", "r") as f:
                data = json.load(f)
                for cst_no, acc_data in data.items():
                    self._data[int(cst_no)] = Account(
                        int(cst_no),
                        acc_data["pin"],
                        acc_data["checking_balance"],
                        acc_data["saving_balance"]
                    )
        except FileNotFoundError:
            print("\nNo existing accounts found. Starting with an empty database.")

    # ------------------------------------------------------------------
    # Main Menu Entry Point
    # ------------------------------------------------------------------

    def main_menu(self):
        self.load_accounts()

        while True:
            try:
                print("\n Type 1 - Login")
                print(" Type 2 - Create Account")
                choice = int(input("\nChoice: "))
                if choice == 1:
                    self.get_login()
                    break
                elif choice == 2:
                    self.create_account()
                    break
                else:
                    print("\nInvalid Choice.")
            except ValueError:
                print("\nInvalid Choice.")

        print("\nThank You for using this ATM.\n")
