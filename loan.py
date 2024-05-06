from tabulate import tabulate
from matplotlib import pyplot as plt

def repayment_loan():
    loan = int(input("Enter your loan amount: $"))
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
        print("\nCongratulations! You've paid off the loan.")
 
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
    repayment_loan()