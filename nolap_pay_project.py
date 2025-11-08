user_database = {
    "0241234567": {
        "pin": "4321",
        "balance": 259.87
    },
    "0557609273": {
        "pin": "2703",
        "balance": 1456.87
    },
    "0592498249": {
        "pin": "5281",
        "balance": 1987.665
    }
}

current_user_phone = None

def login_or_create_account():
    global current_user_phone

    print("Welcome to NOLAP Pay!")
    phone_number = input("Enter your 10-digit phone number: ").strip()

    # Step 1: Validate number
    if not (phone_number.isdigit() and len(phone_number) == 10):
        print("❌ Invalid phone number. Must be exactly 10 digits.")
        return

    # Step 2: Check if user exists
    if phone_number in user_database:
        # --- LOGIN FLOW ---
        pin = input("Enter your 4-digit PIN: ").strip()
        if pin == user_database[phone_number]["pin"]:
            current_user_phone = phone_number
            print("✅ Login successful!")
            main_menu()
            # Later this will take you to main menu
        else:
            print("❌ Incorrect PIN. Try again.")
    else:
        # --- ACCOUNT CREATION FLOW ---
        choice = input("This number is not registered. Create new account? (yes/no): ").strip().lower()
        if choice == "yes":
            new_pin = input("Create a 4-digit PIN: ").strip()
            confirm_pin = input("Confirm your PIN: ").strip()

            if new_pin != confirm_pin:
                print("❌ PINs do not match. Account not created.")
                return

            if not (new_pin.isdigit() and len(new_pin) == 4):
                print("❌ Invalid PIN format. Must be 4 digits.")
                return

            # Add new user to the database
            user_database[phone_number] = {"pin": new_pin, "balance": 0.00}
            current_user_phone = phone_number
            print("🎉 Account created successfully! Your starting balance is GHS 0.00")
        else:
            print("Okay, maybe next time.")

def buy_airtime(current_user_phone):
    print("\n--- Buy Airtime (Self) ---")

    amount = float(input("Please enter an amount GHS to buy..."))

    confirm = input(f"Buy GHS {amount:.2f} airtime for yourself. Enter'yes' to continue or 'no' to cancel: ").lower()
    if confirm != 'yes':
        print("Transaction cancelled..")
        return

    pin = input("Enter your PIN to confirm: ")

    # Check if PIN is correct
    if pin != user_database[current_user_phone]["pin"]:
        print("❌ Incorrect PIN.")
        return

    # Check if user has enough balance
    if amount > user_database[current_user_phone]["balance"]:
        print("❌ Insufficient balance.")
        return

    # Deduct the amount
    user_database[current_user_phone]["balance"] -= amount

    print(f"✅ You have successfully bought GHS {amount:.2f} airtime for yourself!")
    print(f"💰 New balance: GHS {user_database[current_user_phone]['balance']:.2f}")


def transfer_money(current_user_phone):
    print("\n=== Transfer Money ===")

    # Ask for recipient phone number
    recipient = input("Enter recipient's phone number: ")

    if recipient not in user_database:
        print("This number is not registered on NOLAP Pay.")
        return

    # Ask for amount
    amount = float(input("Enter amount to send: "))

    #Ask for reference
    reference = input("Enter a reference (e.g. 'food', 'transport' etc)")

    #Calculate Fee
    fee = 1.00
    total = amount + fee

    # Check balance
    if amount > user_database[current_user_phone]['balance']:
        print("Insufficient balance.")
        return
    
    #Show confirmation:
    print(f'\nTransfer GHS {amount:.2f} to {recipient} for {reference} .')
    print(f'Fee: GHS {fee:.2f}. Total: GHS {total:.2f}')
    pin = input("Enter your PIN to confirm: ")

    # Pin Validation:
    if pin != user_database[current_user_phone]['pin']:
        print("Incorrect PIN.")
        return

    # Do the transfer
    user_database[current_user_phone]['balance'] -= amount
    user_database[recipient]['balance'] += amount

    print(f"Transfer successful! You sent GHS {amount:.2f} to {recipient}.")
    print(f"Your new balance is: GHS {user_database[current_user_phone]['balance']:.2f}")  

import random

# --- Dynamic Charges ---

def calculate_transfer_fee(amount):
    """Calculates P2P transfer fee."""
    if amount >= 2000:
        return 15.00
    else:
        return round(amount * 0.0075, 2)  # 0.75%

def calculate_withdrawal_fee(amount):
    """Calculates withdrawal (cash out) fee."""
    if amount >= 2000:
        return 20.00
    else:
        return round(amount * 0.01, 2)  # 1%


# --- Withdraw & Deposit Feature ---

def withdraw_and_deposit(current_user_phone):
    global user_database

    print("\n--- Withdraw & Deposit ---")
    print("1. Withdraw Cash")
    print("2. Deposit Cash")
    print("0. Go Back")

    choice = input("Choose an option: ")

    # Withdraw Cash
    if choice == "1":
        amount = float(input("Enter amount to withdraw: "))
        fee = calculate_withdrawal_fee(amount)
        total = amount + fee

        print(f"\nWithdrawal Details:")
        print(f"Amount: GHS {amount:.2f}")
        print(f"Fee: GHS {fee:.2f}")
        print(f"Total to be deducted: GHS {total:.2f}")

        pin = input("Enter PIN to confirm: ")

        if pin == user_database[current_user_phone]["pin"]:
            if user_database[current_user_phone]["balance"] >= total:
                user_database[current_user_phone]["balance"] -= total
                token = random.randint(100000, 999999)
                print(f"\n✅ Withdrawal successful!")
                print(f"Withdrawal token: {token}")
                print(f"New Balance: GHS {user_database[current_user_phone]['balance']:.2f}")
            else:
                print("❌ Insufficient funds.")
        else:
            print("❌ Incorrect PIN.")

    # Deposit Cash
    elif choice == "2":
        amount = float(input("Enter amount to deposit: "))
        user_database[current_user_phone]["balance"] += amount
        print(f"\n✅ Deposit successful!")
        print(f"New Balance: GHS {user_database[current_user_phone]['balance']:.2f}")

    elif choice == "0":
        print("Returning to main menu...")

    else:
        print("❌ Invalid option. Please select again.")

def check_balance(current_user_phone):
    user = user_database[current_user_phone]
    pin = input("\nEnter your PIN to view balance: ")
    
    if pin == user_database[current_user_phone]["pin"]:
        print(f"\n💳 Your current balance is: GHS {user['balance']:.2f}")
    else:
        print("\n❌ Incorrect PIN. Access denied.")

def change_pin(current_user_phone):
    print("🔒 Change PIN")

    old_pin = input("Enter your OLD PIN: ")

    # Step 1: Verify old PIN
    if old_pin == user_database[current_user_phone]["pin"]:
        new_pin = input("Enter your NEW PIN: ")
        confirm_pin = input("Confirm your NEW PIN: ")

        # Step 2: Check if new PINs match
        if new_pin == confirm_pin:
            # Step 3: Update the user's PIN
            user_database[current_user_phone]["pin"] = new_pin
            print("✅ PIN changed successfully!")
        else:
            print("❌ PINs do not match. Try again.")
    else:
        print("❌ Incorrect OLD PIN.")      

# 🟤 Step 3: Main NOLAP Pay Menu
def main_menu():
    while True:
        print("\n--- Welcome to NOLAP Pay ---")
        print("1. Transfer Money")
        print("2. Buy Airtime (Self)")
        print("3. Withdraw & Deposit")
        print("4. Check Balance")
        print("5. Change PIN")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            print("💸 Transfer Money")
            transfer_money(current_user_phone)
            break
        elif choice == "2":
            print("📱 Buy Airtime")
            buy_airtime(current_user_phone)
            break
        elif choice == "3":
            print("🏧 Withdraw & Deposit")
            withdraw_and_deposit(current_user_phone)
            break
        elif choice == "4":
            print("💰 Check Balance ")
            check_balance(current_user_phone)
            break
        elif choice == "5":
            print("🔐 Change PIN")
            change_pin(current_user_phone)
            break
        elif choice == "0":
            print("👋 Thank you for using NOLAP Pay. Goodbye!")
            break
        else:
            print("❌ Invalid option, please try again.")
            break

login_or_create_account()
