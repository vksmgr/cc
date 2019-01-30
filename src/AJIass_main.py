import tkinter as tk
from tkinter import *
from tkinter import messagebox

from pylab import plot, show, xlabel, ylabel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt

from src.moneymanager import MoneyManager

# Path to the file
file_path = "/home/hp/PycharmProjects/cc/data/"

win = tk.Tk()

# Set window size here to '540 x 640'
win.geometry("540x640")

# Set the window title to 'FedUni Money Manager'
win.title("FedUni Money Manager")

# The user number and associated variable
user_number_var = tk.StringVar()

# This is set as a default for ease of testing
user_number_var.set('123456')
user_number_entry = tk.Entry(win, textvariable=user_number_var)
user_number_entry.focus_set()

# The pin number entry and associated variables
pin_number_var = tk.StringVar()

# This is set as a default for ease of testing
pin_number_var.set('7890')

# Modify the following to display a series of * rather than the pin ie **** not 1234
user_pin_entry = tk.Entry(win, text='PIN Number', textvariable=pin_number_var, show='*')
PIN_number = ''

# set the user file by default to an empty string
user_file = ''

# The balance label and associated variable
balance_var = tk.StringVar()
balance_var.set('0.00')
balance_label = tk.Label(win, textvariable=balance_var)

# The Entry widget to accept a numerical value to deposit or withdraw
amount_var = tk.StringVar()
tkVar = StringVar(win)
amount_entry = tk.Entry(win, textvariable=amount_var)
entry_type = tk.Entry(win)

# The transaction text widget holds text of the transactions
transaction_text_widget = tk.Text(win, height=10, width=48)

# The money manager object we will work with
user = MoneyManager()


# ---------------Button Handlers for Login Screen--------------

def clear_pin_entry(event):
    '''Function to clear the PIN number entry when the Clear / Cancel button is clicked.'''
    # Clear the pin number entry here
    global PIN_number
    pin_number_var.set('')
    PIN_number = ''
    user_pin_entry.focus_set()


def handle_pin_button(event):
    '''Function to add the number of the button clicked to the PIN number entry.'''

    global PIN_number
    Value = event.widget.cget("text")

    # Limit to 4 chars in length
    if len(pin_number_var.get()) < 4:
        PIN_number = PIN_number + Value

    # Set the new pin number on the pin_number_var
    pin_number_var.set(PIN_number)


def log_in(event):
    '''Function to log in to the banking system using a known user number and PIN.'''
    global user
    global pin_number_var
    global user_file
    global user_num_entry
    global PIN_number

    # Create the filename from the entered account number with '.txt' on the end

    # Try to open the account file for reading
    try:
        user_file = open(file_path + user_number_var.get() + ".txt", 'r+')

        # Open the account file for reading
        file_data = user_file.readlines()
        file_data = [data.strip('\n') for data in file_data]

        # First line is account number
        user.user_number = file_data[0]

        # Second line is PIN number, raise exceptionk if the PIN entered doesn't match account PIN read
        if pin_number_var.get() != file_data[1]:
            raise messagebox.showerror("Error", "Wrong PIN Number")

        # Read third and fourth lines (balance and interest rate) 
        else:
            user.user_pin = file_data[1]
            user.currentBalance = file_data[2]
            balance_var.set(file_data[2])
         # user.interest_rate = file_data[3]

        # Section to read account transactions from file - start an infinite 'do-while' loop here
        transaction_data = file_data[3:]
        i = 0
        while (i < len(transaction_data)):
            # Attempt to read a line from the account file, break if we've hit the end of the file. If we
            # read a line then it's the transaction type, so read the next line which will be the transaction amount.
            # and then create a tuple from both lines and add it to the account's transaction_list 
            user.transaction_list.append((transaction_data[i], transaction_data[i + 1]))
            i = i + 2

        # Close the file now we're finished with it
        user_file.close()

    # Catch exception if we couldn't open the file or PIN entered did not match account PIN
    except IOError:

        # Show error messagebox and & reset BankAccount object to default...
        messagebox.showerror("Error", "Try Again!")

        #  ...also clear PIN entry and change focus to account number entry
        pin_number_var.set('')
        PIN_number = ''
        user_number_entry.focus_set()

    # Got here without raising an exception? Then we can log in - so remove the widgets and display the account screen
    if pin_number_var.get() == file_data[1]:
        remove_all_widgets()
        create_user_screen()


# ----------------Button Handlers for User Screen----------------------


def save_and_log_out():
    '''Function  to overwrite the user file with the current state of
       the user object (i.e. including any new transactions), remove
       all widgets and display the login screen.'''
    global user
    global PIN_number

    # Save the account with any new transactions
    user.save_to_file()

    # Reset the bank acount object
    user = MoneyManager()

    # Reset the account number and pin to blank
    user_number_var.set('')
    pin_number_var.set('')
    PIN_number = ''

    # Remove all widgets and display the login screen again
    remove_all_widgets()
    create_login_screen()


def perform_deposit():
    '''Function to add a deposit for the amount in the amount entry to the
       user's transaction list.'''
    global user
    global amount_entry
    global balance_label
    global balance_var

    # Try to increase the account balance and append the deposit to the account file
    try:

        # Get the cash amount to deposit. Note: We check legality inside account's deposit method
        user.deposit_funds(amount_var.get())

        # Deposit funds

        # Update the transaction widget with the new transaction by calling account.get_transaction_string()
        # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
        #       contents, and finally configure back to state='disabled' so it cannot be user edited.
        user.get_transaction_string()
        user.transaction_list.append(("Deposit", float(amount_var.get())))

        transaction_text_widget = tk.Text(win, height=10, width=48)
        text_scrollbar = tk.Scrollbar(win, command=transaction_text_widget.yview, orient='vertical')
        z = [[i for i in vall] for vall in user.transaction_list]

        for i in z:
            for a in i:
                transaction_text_widget.config(state='normal')
                transaction_text_widget.insert('end', str(a) + '\n')
        transaction_text_widget.config(state='disabled')
        transaction_text_widget.grid(row=4, columnspan=4, sticky='NESW')
        transaction_text_widget.config(yscrollcommand=text_scrollbar.set)

        # Change the balance label to reflect the new balance
        balance_var.set(str(user.currentBalance))
        balance_label = tk.Label(win, text="Balance: $" + balance_var.get())
        balance_label.grid(row=1, column=1, sticky="NESW")

        # Clear the amount entry
        amount_var.set('')

        # Update the interest graph with our new balance
        plot_spending_graph()


    # Catch and display exception as a 'showerror' messagebox with a title of 'Transaction Error' and the text of the exception
    except ValueError:
        messagebox.showerror("Error", "Invalid Transaction!!!")


def perform_transaction():
    '''Function to add the entry the amount in the amount entry from the user balance and add an entry to the transaction list.'''
    global user
    global amount_entry
    global balance_label
    global balance_var
    global entry_type

    # Try to decrease the account balance and append the deposit to the account file
    try:

        # Get the cash amount to use. Note: We check legality inside account's withdraw_funds method
        amount_var.get()
        # user.add_entry(amount_var.get())

        # Get the type of entry that will be added ie rent etc
        tkVar.get()
        # user.add_entry(tkVar.get())

        # Withdraw funds from the balance
        if float(amount_var.get()) < float(user.currentBalance):
            user.add_entry(amount_var.get(), tkVar.get())

            # Update the transaction widget with the new transaction by calling user.get_transaction_string()
            # Note: Configure the text widget to be state='normal' first, then delete contents, then instert new
            #       contents, and finally configure back to state='disabled' so it cannot be user edited.
            user.get_transaction_string()
            user.transaction_list.append((tkVar.get(), float(amount_var.get())))

            transaction_text_widget = tk.Text(win, height=10, width=48)
            text_scrollbar = tk.Scrollbar(win, command=transaction_text_widget.yview, orient='vertical')
            z = [[i for i in vall] for vall in user.transaction_list]

            for i in z:
                for a in i:
                    transaction_text_widget.config(state='normal')
                    transaction_text_widget.insert('end', str(a) + '\n')
            transaction_text_widget.config(state='disabled')
            transaction_text_widget.grid(row=4, columnspan=4, sticky='NESW')
            transaction_text_widget.config(yscrollcommand=text_scrollbar.set)
        else:
            messagebox.showerror("Error", "Insufficient Balance!!!")

        # Change the balance label to reflect the new balance
        balance_var.set(str(user.currentBalance))
        balance_label = tk.Label(win, text="Balance: $" + balance_var.get())
        balance_label.grid(row=1, column=1, sticky="NESW")

        # Clear the amount entry
        amount_var.set('')

        # Update the graph
        plot_spending_graph()


    # Catch and display any returned exception as a messagebox 'showerror'
    except ValueError:
        messagebox.showerror("Transaction Error", "Invalid Transaction!!!")


def remove_all_widgets():
    '''Function to remove all the widgets from the window.'''
    global win
    for widget in win.winfo_children():
        widget.grid_remove()


def read_line_from_user_file():
    '''Function to read a line from the users file but not the last newline character.
       Note: The user_file must be open to read from for this function to succeed.'''
    global user_file
    return user_file.readline()[0:-1]


def plot_spending_graph():
    '''Function to plot the user spending here'''

 # Your code to generate the x and y lists here which will be plotted
    tx_list = user.transaction_list
    dict_value = {}
    for i in tx_list:
        if i[0] in dict_value.keys():
            dict_value[i[0]] = float(dict_value[i[0]])+float(i[1])
        else:
            dict_value[i[0]] = float(i[1])

 # Your code to display the graph on the screen here - do this last
    f = Figure(figsize=(1, 2), dpi=100)
    a = f.add_subplot(111)

    a.set_title("User Spending Chart")
    a.bar(range(len(dict_value)), list(dict_value.values()), align='center')
    a.plot(dict_value.keys(), dict_value.values(), dashes=[1, 60], color='w')
    canvas = FigureCanvasTkAgg(f, win)
    canvas.draw()

    graph_widget = canvas.get_tk_widget()
    graph_widget.grid(row=6,  columnspan=5, sticky='nsew')


# -----------------UI Drawing Functions------------------

def create_login_screen():
    '''Function to create the login screen.'''

    # ----- Row 0 -----

    # 'FedUni Money Manager' label here. Font size is 28.
    tk.Label(win, text="FedUni Money Manager", font='Arial 28 bold').grid(row=0, columnspan=3)

    # ----- Row 1 -----

    # Account Number / Pin label here
    tk.Label(win, text="User Number / Pin").grid(row=1, column=0)

    # Account number entry here
    user_number_entry.grid(row=1, column=1, sticky="NESW")
    user_number_entry.focus_set()

    # Account pin entry here
    user_pin_entry.grid(row=1, column=2, sticky="NESW")

    # ----- Row 2 -----

    # Buttons 1, 2 and 3 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button1 = tk.Button(win, text="1", padx=30, pady=30)
    button1.bind('<Button-1>', handle_pin_button)
    button1.grid(row=2, column=0, sticky="NESW")

    button2 = tk.Button(win, text="2", padx=30, pady=30)
    button2.bind('<Button-1>', handle_pin_button)
    button2.grid(row=2, column=1, sticky="NESW")

    button3 = tk.Button(win, text="3", padx=30, pady=30)
    button3.bind('<Button-1>', handle_pin_button)
    button3.grid(row=2, column=2, sticky="NESW")

    # ----- Row 3 -----

    # Buttons 4, 5 and 6 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button4 = tk.Button(win, text="4", padx=30, pady=30)
    button4.bind('<Button-1>', handle_pin_button)
    button4.grid(row=3, column=0, sticky="NESW")

    button5 = tk.Button(win, text="5", padx=30, pady=30)
    button5.bind('<Button-1>', handle_pin_button)
    button5.grid(row=3, column=1, sticky="NESW")

    button6 = tk.Button(win, text="6", padx=30, pady=30)
    button6.bind('<Button-1>', handle_pin_button)
    button6.grid(row=3, column=2, sticky="NESW")

    # ----- Row 4 -----

    # Buttons 7, 8 and 9 here. Buttons are bound to 'handle_pin_button' function via '<Button-1>' event.
    button7 = tk.Button(win, text="7", padx=30, pady=30)
    button7.bind('<Button-1>', handle_pin_button)
    button7.grid(row=4, column=0, sticky="NESW")

    button8 = tk.Button(win, text="8", padx=30, pady=30)
    button8.bind('<Button-1>', handle_pin_button)
    button8.grid(row=4, column=1, sticky="NESW")

    button9 = tk.Button(win, text="9", padx=30, pady=30)
    button9.bind('<Button-1>', handle_pin_button)
    button9.grid(row=4, column=2, sticky="NESW")

    # ----- Row 5 -----

    # Cancel/Clear button here. 'bg' and 'activebackground' should be 'red'. But calls 'clear_pin_entry' function.
    clear_button = tk.Button(win, text="Cancel/Clear", bg="red", activebackground="red", padx=30, pady=30)
    clear_button.bind('<Button-1>', clear_pin_entry)
    clear_button.grid(row=5, column=0, sticky="NESW")

    # Button 0 here
    button0 = tk.Button(win, text="0", padx=30, pady=30)
    button0.bind('<Button-1>', handle_pin_button)
    button0.grid(row=5, column=1, sticky="NESW")

    # Login button here. 'bg' and 'activebackground' should be 'green'). Button calls 'log_in' function.
    login_button = tk.Button(win, text="Log In", bg="green", activebackground="green", padx=30, pady=30)
    login_button.bind('<Button-1>', log_in)
    login_button.grid(row=5, column=2, sticky="NESW")

    # ----- Set column & row weights -----

    # Set column and row weights. There are 5 columns and 6 rows (0..4 and 0..5 respectively)
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)
    win.rowconfigure(4, weight=1)
    win.rowconfigure(5, weight=1)
    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.columnconfigure(3, weight=0)
    win.columnconfigure(4, weight=0)


def create_user_screen():
    '''Function to create the user screen.'''
    global amount_text
    global amount_label
    global transaction_text_widget
    global balance_var

    # ----- Row 0 -----

    # FedUni Banking label here. Font size should be 24.
    tk.Label(win, text="FedUni Money Manager", font='Arial 24 bold').grid(row=0, columnspan=5)

    # ----- Row 1 -----

    # Account number label here
    tk.Label(win, text="User Number: " + user.user_number).grid(row=1, column=0, sticky="NESW")

    # Balance label here
    tk.Label(win, text="Balance: $" + user.currentBalance).grid(row=1, column=1, sticky="NESW")

    # Log out button here
    logout_button = tk.Button(win, text="Log Out", command=save_and_log_out)
    logout_button.grid(row=1, column=2, sticky="NESW")

    # ----- Row 2 -----

    # Amount label here
    amount_label = tk.Label(win, text="Amount($)").grid(row=2, column=0, sticky="NESW")

    # Amount entry here
    amount_entry.grid(row=2, column=1, sticky="NESW")

    # Deposit button here
    deposit_button = tk.Button(win, text="Deposit", command=perform_deposit)
    deposit_button.grid(row=2, column=2, sticky="NESW")

    # NOTE: Bind Deposit and Withdraw buttons via the command attribute to the relevant deposit and withdraw
    #       functions in this file. If we "BIND" these buttons then the button being pressed keeps looking as
    #       if it is still pressed if an exception is raised during the deposit or withdraw operation, which is
    #       offputting.

    # ----- Row 3 -----

    # Entry type label here
    tk.Label(win, text="Entry Type").grid(row=3, column=0)

    # Entry drop list here
    OPTIONS = ["Rent", "Bills", "Food", "Entertainment", "Other"]
    tkVar.set(OPTIONS[0])

    e = OptionMenu(win, tkVar, *OPTIONS)
    e.grid(row=3, column=1)

    # Add entry button here
    entry_button = tk.Button(win, text="Add Entry", command=perform_transaction)
    entry_button.grid(row=3, column=2, sticky="NESW")

    # ----- Row 4 -----

    # Declare scrollbar (text_scrollbar) here (BEFORE transaction text widget)

    transaction_text_widget = tk.Text(win, height=10, width=48)
    text_scrollbar = tk.Scrollbar(win, command=transaction_text_widget.yview, orient='vertical')
    z = [[i for i in vall] for vall in user.transaction_list]

    for i in z:
        for a in i:
            transaction_text_widget.insert('end', str(a) + '\n')
    transaction_text_widget.config(state='disabled')
    transaction_text_widget.grid(row=4, columnspan=4, sticky="NESW")

    # Add transaction Text widget and configure to be in 'disabled' mode so it cannot be edited.
    # Note: Set the yscrollcommand to be 'text_scrollbar.set' here so that it actually scrolls the Text widget
    # Note: When updating the transaction text widget it must be set back to 'normal mode' (i.e. state='normal') for it to be edited

    # Now add the scrollbar and set it to change with the yview of the text widget

    text_scrollbar.grid(row=4, column=4, sticky="NS")
    transaction_text_widget.config(yscrollcommand=text_scrollbar.set)

    # ----- Row 5 - Graph -----

    # Call plot_interest_graph() here to display the graph
    plot_spending_graph()

    # ----- Set column & row weights -----

    # Set column and row weights here - there are 6 rows and 5 columns (numbered 0 through 4 not 1 through 5!)
    win.rowconfigure(0, weight=1)
    win.rowconfigure(1, weight=1)
    win.rowconfigure(2, weight=1)
    win.rowconfigure(3, weight=1)
    win.rowconfigure(4, weight=1)
    win.rowconfigure(5, weight=1)
    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=1)
    win.columnconfigure(2, weight=1)
    win.columnconfigure(3, weight=1)
    win.columnconfigure(4, weight=1)


# ----------------------- Display Login Screen & Start Main loop --------------------

create_login_screen()
win.mainloop()
