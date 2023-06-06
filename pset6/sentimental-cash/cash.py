# TODO
from cs50 import get_float


def main():
    # ask how many cents the customer is owed
    cents = get_cents()

    # calculate the number of quarters to give the customer
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 0.25
    cents = float(format(cents, '.2f'))

    # calculate the number of dimes to give the customer
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 0.10
    cents = float(format(cents, '.2f'))

    # calculate the number on nickels to give the customer
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 0.05
    cents = float(format(cents, '.2f'))

    # calculate the number of pennies to give the customer
    pennies = calculate_pennies(cents)
    cents = cents - pennies * 0.01
    cents = float(format(cents, '.2f'))

    # sum coins
    coins = quarters + dimes + nickels + pennies

    # print total number of coins to give the customer
    print(coins)


def get_cents():
    while True:
        cents = get_float("change owed: ")
        if cents > 0:
            break

    return cents


def calculate_quarters(cents):
    quarters = 0
    while cents >= 0.25:
        cents = cents - 0.25
        quarters += 1
    return quarters


def calculate_dimes(cents):
    dimes = 0
    while cents >= 0.10:
        cents = cents - 0.10
        dimes += 1
    return dimes


def calculate_nickels(cents):
    nickels = 0
    while cents >= 0.05:
        cents = cents - 0.05
        nickels += 1
    return nickels


def calculate_pennies(cents):
    pennies = 0
    while cents >= 0.01:
        cents = cents - 0.01
        pennies += 1
    return pennies


main()
