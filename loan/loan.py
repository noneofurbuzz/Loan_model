from tabulate import tabulate
from matplotlib import pyplot as plt
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Dictionary to store users
users = {}
is_logged_in = False
loans = {}
 
try:
    with open('users.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}
try:
    with open('loans.json', 'r') as f:
        loans = json.load(f)
except FileNotFoundError:
    loans = {}

def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    if username in users:
        print("Username already exists. Please choose a different one.")
    else:
        users[username] = password
        loans[username] = 0
        print("User registered successfully!\n")
        
def login():
    global is_logged_in
    username = input("Enter your username: ")
    fill = []
    password = input("Enter your password: ")
    if username in users and users[username] == password:
        print("Login successful!\n")
        is_logged_in = True
        # After a successful login, the user can manage their loans
        print(tabulate(fill,headers=[f'Welcome {username}!"'], tablefmt="grid"))
        repayment_loan(username)
        # After the loan repayment, only show the exit option
    else:
        print("Invalid username or password.\n")
        
def company_data():
    total_borrowed = sum(loans.values())
    fill = []
    print(tabulate(fill,headers=["Company Data!"], tablefmt="grid"))
    print(f"Total amount of money loaned by the company: ${total_borrowed}")

def start():
    global is_logged_in
    while True:
        if is_logged_in == True:
            print("1. Logout")
            print("2. Show Company Data")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                is_logged_in = False
                print("Logout successful!\n")
                start()
            elif choice == '2':
                company_data()
            elif choice == '3':
                # Save users to file before exiting
                with open('users.json', 'w') as f:
                    json.dump(users, f)
                with open('loans.json', 'w') as f:
                    json.dump(loans, f)
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        else:       
            print("1. Register")
            print("2. Login")
            print("3. Show Company Data")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                register()
            elif choice == '2':
                login()
            elif choice == '3':
                company_data()
            elif choice == '4':
                 # Save users to file before exiting
                with open('users.json', 'w') as f:
                    json.dump(users, f)
                with open('loans.json', 'w') as f:
                    json.dump(loans, f)
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")

def repayment_loan(username):
    loan = int(input("Enter your loan amount: $"))
    if username not in loans:
        loans[username] = 0
    loans[username] += loan
    rate = float(input("Enter the interest rate in decimal: "))
    data = []
    new_loan = loan;
    paymentArr = []
    month = 0;
    is_fixed = input("do you want to pay at fixed intervals (y/n): ").lower()
    if (is_fixed == "y"):
        payment = float(input("Enter the amount you want to pay each month: $"))
        while new_loan > 0:
            month = month + 1
            loan = (new_loan * rate) + new_loan
            new_loan = loan - payment
            if new_loan < 0:
                new_loan = 0
                data.append([month, loan, payment, new_loan])
                paymentArr.append(payment)
            else:
                data.append([month, loan, payment, new_loan])
                paymentArr.append(payment)
        print(tabulate(data, headers=['month','amount to pay (with accumulated interest)','payment','remaining amount'], floatfmt=('.2f'), tablefmt="grid"))
    else:
        while new_loan > 0:
            month = month + 1
            loan = (new_loan * rate) + new_loan
            payment = float(input(f"Enter the amount you want to pay in month {month}: $"))
            new_loan = loan - payment
            if new_loan < 0:
                new_loan = 0
                data.append([month, loan, payment, new_loan])
                paymentArr.append(payment)
            else:
                data.append([month, loan, payment, new_loan])
                paymentArr.append(payment)
        print(tabulate(data, headers=['month','amount to pay (with accumulated interest)','payment','remaining amount'], floatfmt=('.2f'), tablefmt="grid"))
    print("\nCongratulations! You've paid off the loan.\n")
 
    #visualize loan repayment schedule
    monthly_range = range(1, month + 1)
    loan_balance = [loan - sum(paymentArr[:i]) for i in monthly_range]
    plt.plot(monthly_range, loan_balance, marker='o', linestyle='-')
    plt.xlabel('Months')
    plt.ylabel('Loan Balance')
    plt.title('Loan Repayment Schedule')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("Welcome to my simple loan calculator!\n")
    start()
    