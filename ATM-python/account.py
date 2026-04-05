import logging

logging.basicConfig(
    filename='atm_transactions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Account:
    """Represents a bank account with checking and savings balances."""

    def __init__(self, customer_number=0, pin_number=0, checking_balance=0.0, saving_balance=0.0, transaction_history=None):
        self._customer_number = customer_number
        self._pin_number = pin_number
        self._checking_balance = checking_balance
        self._saving_balance = saving_balance
        self._transaction_history = transaction_history if transaction_history is not None else []

    # ------------------------------------------------------------------
    # Getters and Setters
    # ------------------------------------------------------------------

    def set_customer_number(self, customer_number):
        self._customer_number = customer_number
        return customer_number

    def get_customer_number(self):
        return self._customer_number

    def set_pin_number(self, pin_number):
        self._pin_number = pin_number
        return pin_number

    def get_pin_number(self):
        return self._pin_number

    def get_checking_balance(self):
        return self._checking_balance

    def get_saving_balance(self):
        return self._saving_balance

    def get_transaction_history(self):
        return self._transaction_history

    # ------------------------------------------------------------------
    # Balance Calculation Methods
    # ------------------------------------------------------------------

    def _record(self, entry):
        self._transaction_history.append(entry)

    def calc_checking_withdraw(self, amount):
        self._checking_balance -= amount
        entry = f"Checking Withdraw | Amount: {self._format_money(amount)} | New Balance: {self._format_money(self._checking_balance)}"
        self._record(entry)
        logging.info(f"Customer {self._customer_number} withdrew {self._format_money(amount)} from checking account. New balance: {self._format_money(self._checking_balance)}")
        return self._checking_balance

    def calc_saving_withdraw(self, amount):
        self._saving_balance -= amount
        entry = f"Saving Withdraw | Amount: {self._format_money(amount)} | New Balance: {self._format_money(self._saving_balance)}"
        self._record(entry)
        logging.info(f"Customer {self._customer_number} withdrew {self._format_money(amount)} from savings account. New balance: {self._format_money(self._saving_balance)}")
        return self._saving_balance

    def calc_checking_deposit(self, amount):
        self._checking_balance += amount
        entry = f"Checking Deposit | Amount: {self._format_money(amount)} | New Balance: {self._format_money(self._checking_balance)}"
        self._record(entry)
        logging.info(f"Customer {self._customer_number} deposited {self._format_money(amount)} into checking account. New balance: {self._format_money(self._checking_balance)}")
        return self._checking_balance

    def calc_saving_deposit(self, amount):
        self._saving_balance += amount
        entry = f"Saving Deposit | Amount: {self._format_money(amount)} | New Balance: {self._format_money(self._saving_balance)}"
        self._record(entry)
        logging.info(f"Customer {self._customer_number} deposited {self._format_money(amount)} into savings account. New balance: {self._format_money(self._saving_balance)}")
        return self._saving_balance

    def calc_check_transfer(self, amount):
        self._checking_balance -= amount
        self._saving_balance += amount
        entry = f"Transfer Checking -> Saving | Amount: {self._format_money(amount)} | Checking: {self._format_money(self._checking_balance)} | Saving: {self._format_money(self._saving_balance)}"
        self._record(entry)
        logging.info(f"Customer {self._customer_number} transferred {self._format_money(amount)} from checking to savings account. New checking balance: {self._format_money(self._checking_balance)}, New savings balance: {self._format_money(self._saving_balance)}")

    def calc_saving_transfer(self, amount):
        self._saving_balance -= amount
        self._checking_balance += amount
        entry = f"Transfer Saving -> Checking | Amount: {self._format_money(amount)} | Saving: {self._format_money(self._saving_balance)} | Checking: {self._format_money(self._checking_balance)}"
        self._record(entry)
        logging.info(f"Customer {self._customer_number} transferred {self._format_money(amount)} from savings to checking account. New savings balance: {self._format_money(self._saving_balance)}, New checking balance: {self._format_money(self._checking_balance)}")

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------

    @staticmethod
    def _format_money(amount):
        return "${:,.2f}".format(amount)

    @staticmethod
    def _get_amount_input(prompt):
        """Prompt the user for a monetary amount, returning a float.

        Returns None when the user enters a non-numeric value.
        """
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            return None

    # ------------------------------------------------------------------
    # User Input Methods – Checking Account
    # ------------------------------------------------------------------

    def get_checking_withdraw_input(self):
        while True:
            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
            amount = self._get_amount_input("\nAmount you want to withdraw from Checking Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._checking_balance - amount) >= 0:
                self.calc_checking_withdraw(amount)
                print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                break
            else:
                print("\nBalance Cannot be Negative.")

    def get_checking_deposit_input(self):
        while True:
            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
            amount = self._get_amount_input("\nAmount you want to deposit into Checking Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._checking_balance + amount) >= 0:
                self.calc_checking_deposit(amount)
                print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                break
            else:
                print("\nBalance Cannot Be Negative.")

    # ------------------------------------------------------------------
    # User Input Methods – Savings Account
    # ------------------------------------------------------------------

    def get_saving_withdraw_input(self):
        while True:
            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
            amount = self._get_amount_input("\nAmount you want to withdraw from Savings Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._saving_balance - amount) >= 0:
                self.calc_saving_withdraw(amount)
                print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                break
            else:
                print("\nBalance Cannot Be Negative.")

    def get_saving_deposit_input(self):
        while True:
            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
            amount = self._get_amount_input("\nAmount you want to deposit into your Savings Account: ")
            if amount is None:
                print("\nInvalid Choice.")
                continue
            if amount >= 0 and (self._saving_balance + amount) >= 0:
                self.calc_saving_deposit(amount)
                print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                break
            else:
                print("\nBalance Cannot Be Negative.")

    # ------------------------------------------------------------------
    # Transfer Funds Between Accounts
    # ------------------------------------------------------------------

    def get_transfer_input(self, acc_type):
        while True:
            try:
                if acc_type == "Checking":
                    print("\nSelect an account you wish to transfer funds to:")
                    print("1. Savings")
                    print("2. Exit")
                    choice = int(input("\nChoice: "))
                    if choice == 1:
                        print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                        amount = self._get_amount_input("\nAmount you want to deposit into your Savings Account: ")
                        if amount is None:
                            print("\nInvalid Choice.")
                            continue
                        if amount >= 0 and (self._saving_balance + amount) >= 0 and (self._checking_balance - amount) >= 0:
                            self.calc_check_transfer(amount)
                            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                            break
                        else:
                            print("\nBalance Cannot Be Negative.")
                    elif choice == 2:
                        return
                    else:
                        print("\nInvalid Choice.")

                elif acc_type == "Savings":
                    print("\nSelect an account you wish to transfer funds to: ")
                    print("1. Checking")
                    print("2. Exit")
                    choice = int(input("\nChoice: "))
                    if choice == 1:
                        print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                        amount = self._get_amount_input("\nAmount you want to transfer to your Checking Account: ")
                        if amount is None:
                            print("\nInvalid Choice.")
                            continue
                        if amount >= 0 and (self._checking_balance + amount) >= 0 and (self._saving_balance - amount) >= 0:
                            self.calc_saving_transfer(amount)
                            print("\nCurrent Checking Account Balance: " + self._format_money(self._checking_balance))
                            print("\nCurrent Savings Account Balance: " + self._format_money(self._saving_balance))
                            break
                        else:
                            print("\nBalance Cannot Be Negative.")
                    elif choice == 2:
                        return
                    else:
                        print("\nInvalid Choice.")

            except ValueError:
                print("\nInvalid Choice.")
