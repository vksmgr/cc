
file_path = "/home/hp/PycharmProjects/cc/data/"

class MoneyManager():
    def __init__(self):
        '''Constructor to set username to '', pin_number to an empty string,
           balance to 0.0, and transaction_list to an empty list.'''
        self.user_number = '0'
        self.user_pin = " "
        self.currentBalance = 0.0
#         self.interest_rate = 0.0
        self.transaction_list = []


    def add_entry(self, amount, entry_type):
        '''Function to add and entry an amount to the tool. Raises an
           exception if it receives a value for amount that cannot be cast to float. Raises an exception
           if the entry_type is not valid - i.e. not food, rent, bills, entertainment or other'''
        self.currentBalance = float(self.currentBalance)
        amount = float(amount)
        if self.currentBalance >= amount:
            self.currentBalance = str(self.currentBalance - amount)
            return str(self.currentBalance)
        else:
            return str(self.currentBalance)


    def deposit_funds(self, amount):
        '''Function to deposit an amount to the user balance. Raises an
           exception if it receives a value that cannot be cast to float. '''
        self.currentBalance = float(self.currentBalance)
        amount = float(amount)
        self.currentBalance = str(self.currentBalance + amount)
        return str(self.currentBalance)


    def get_transaction_string(self):
        '''Function to create and return a string of the transaction list. Each transaction
           consists of two lines - either the word "Deposit" or the entry type - food etc - on
           the first line, and then the amount deposited or entry amount on the next line.'''


    def save_to_file(self):
        '''Function to overwrite the user text file with the current user
           details. user number, pin number, and balance (in that
           precise order) are the first four lines - there are then two lines
           per transaction as outlined in the above 'get_transaction_string'
           function.'''
        ls = []
        ls.append(self.user_number)
        ls.append(self.user_pin)
        ls.append(float(self.currentBalance))
#         ls.append(float(self.interest_rate))

        final_file = open(file_path+self.user_number+".txt", 'w')
        z = [[i for i in vall] for vall in self.transaction_list]
        for i in z:
            for a in i:
                ls.append(a)
        i = 0
        for i in range(0,len(ls)):
            final_file.write(str(ls[i])+"\n")

        final_file.close()

