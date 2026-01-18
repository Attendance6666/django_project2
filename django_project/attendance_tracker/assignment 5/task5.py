class BankAccount:
    def __init__(self, owner, balance=0):
        self.__owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
        else:
            print("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient funds")
        elif amount <= 0:
            print("Withdrawal amount must be positive")
        else:
            self.__balance -= amount

    def get_balance(self):
        return self.__balance


account = BankAccount("Aisultan", 1000)
account.deposit(500)
account.withdraw(1600)
print(account.get_balance())
