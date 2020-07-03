import sys
from functools import partial
from financialInfo import financialInfo
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import re
import json
"""
Written by Aaron Shah
7 / 3 / 2019
Class meant to provide a working GUI for
the financialInfo class
"""
user = dict()
months = ["Jan", "Feb", "Mar",
          "Apr", "May", "Jun",
          "Jul","Aug","Sep",
          "Oct","Nov","Dec"] #months in year
v_p = re.compile("^[$]?[0-9]*[.]?[0-9]+$") #check for valid price
SAVE_FILE= "save_data.json"
"""
Global methods
"""
def init_label(window, text, x = 0, y = 0):
    """
    initializes QLabel objects
    window - window which label will be initialized on
    text - label text
    x - x-coordinate
    y - y-coordinate
    """
    label = QLabel(text, window)
    label.move(x,y)
    return label

def init_textbox(window, width = 0, height = 0, x = 0, y = 0):
    """
    initializes QLineEdit objects
    window - window which QLineEdit will be initialized on
    width - width of QLineEdit
    height - height of QLineEdit
    x - x-coordinate
    y - y-coordinate
    """
    textbox = QLineEdit(window)
    textbox.move(x,y)
    textbox.resize(width, height)
    return textbox

def init_button(window, text, func, x = 0, y = 0):
    """
    initializes QPushButton object
    window - window which QPushButton will be initialized on
    text - button text
    func - linked function to button
    x - x-coordinate
    y - y-coordinate
    """
    button = QPushButton(text, window)
    button.clicked.connect(func)
    button.move(x, y)
    return button

def save():
    """
    Saves data onto JSON file
    """
    save_dict = dict()
    save_dict["names"] = []
    print(save_dict)
    for k,v in user.items():
        save_dict["names"].append(v.save_data(k))
    print(save_dict)
    with open(SAVE_FILE, 'w') as save_file:
        json.dump(save_dict, save_file)
"""
Program classes
"""
class Registration(QWidget):
    """
    First page of app
    Registers new user into database
    based on information provided in
    textboxes
    """
    def __init__(self):
        """
        Initializes window dimmensions to 640 x 480
        """
        super().__init__()
        self.title = "Financial Info Tracker"
        
        #Window Dimmensions
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    def initUI(self):
        """
        Initializes UI components
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        # label and textbox for name
        self.name_label = init_label(self, "Name", 20, 20)
        self.name_textbox = init_textbox(self, 140, 40, 80, 20)
        
        # label and textbox for income
        self.income_label = init_label(self, "Income", 20, 80)
        self.income_textbox = init_textbox(self, 140, 40, 80, 80)
        
        # label and textbox for year
        self.year_label = init_label(self, "Year", 20, 140)
        self.year_textbox = init_textbox(self, 140, 40, 80, 140)
        
        # Create a button in the window
        self.button = init_button(self, 'Register', self.on_click, 80, 200)

        # Creates table to see all user information
        self.name_display = QTableWidget(self)
        self.name_display.move(260, 20)
        self.update_name_table()
        
        self.show()
    @pyqtSlot()
    def on_click(self):
        """
        Sends user to new page if inputted
        information is in the correct syntax.
        Otherwise, has them re-input their information.
        """
        #variables to be inputted in financialInfo object
        name = self.name_textbox.text().strip()
        income = self.income_textbox.text().strip()
        year = self.year_textbox.text().strip()
        global user, v_p

        #checks if user is already registered
        if(name in user):
            QMessageBox.question(self, 'Login - Successful!', "Welcome back " + name + ".", QMessageBox.Ok, QMessageBox.Ok)

            #hides current window and initializes new window displaying months
            self.display_account(name)

        #check to see if variables inputted are in the correct format
        elif(v_p.match(income) and year.isnumeric()):
            
            #initializes new object if check passes
            user[name] = financialInfo(int(year), float(income.strip("$")))
            QMessageBox.question(self, 'Registration - Successful!', "You are now registered " + name + ".", QMessageBox.Ok, QMessageBox.Ok)
            
            #hides current window and initializes new window displaying months
            self.display_account(name)
        else:
            QMessageBox.question(self, 'Registration - Fail!', "Please enter a valid year and income.", QMessageBox.Ok, QMessageBox.Ok)
            
    def display_account(self, name):
        """
        Displays user's account based on their name
        and closes their window
        """
        self.new_window = MonthManagement(name)
        self.new_window.show()
        self.close()
        
    def update_name_table(self):
        """
        Updates table of names to reflect current
        information better
        """
        global user
        
        #initializes table dimmensions
        self.name_display.setRowCount(len(user))
        self.name_display.setColumnCount(3)
        self.name_display.setHorizontalHeaderLabels(["Name", "Income", "Year"])
        
        #initializes table items
        for count, (name, fi) in enumerate(user.items()):
            self.name_display.setItem(count, 0, QTableWidgetItem(name))
            self.name_display.setItem(count, 1, QTableWidgetItem("$"+str(fi.get_income())))
            self.name_display.setItem(count, 2, QTableWidgetItem(str(fi.get_year())))
            
        
class MonthManagement(QWidget):
    """
    Lets users select which months they'd
    like to alter.
    Also displays yearly information
    """
    def __init__(self, name):
        """
        Initializes window to 640 x 480
        name - name of user who's information will be viewed
        """
        super().__init__()
        self.title = "Financial Info Tracker"
        
        #Window Dimmensions
        self.name = name
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
    def initUI(self):
        """
        Initializes UI components
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #initializes title label
        global user
        self.title = init_label(self, self.name + "'s "+ str(user[self.name].get_year()) + " spending")
        
        #initializes buttons for each month
        self.month_buttons = [init_button(self, month, self.month_window, 200 + (counter%2)*120, 70 + (counter//2)*40) for counter, month in enumerate(months)]
        """
        Simplified interpretation of above code
        self.month_buttons = [QPushButton(month, self) for month in months]
        for counter, button in enumerate(self.month_buttons):
            height = 70+(counter//2)*40
            width = 200+(counter%2)*120
            button.move(200 + width, 70+height)
            month = button.text()
            button.clicked.connect(self.month_window)
        """

        #initializes label to display yearly income
        yearly_income = "Current Yearly Income: $" + str(user[self.name].get_income())
        self.yearly_income = init_label(self, yearly_income, 200, 320)

        #initializes label to display yearly profit
        yearly_profit = "Current Yearly Profit: $" + str(user[self.name].calc_net_yearly_profit())
        self.yearly_profit = init_label(self, yearly_profit, 200, 340)

        #initializes button to go back to previous page
        self.gb_button = init_button(self, "Go Back", self.go_back, 200, 360)
        
        
    @pyqtSlot()
    def month_window(self):
        """
        Adds functionality to month buttons to
        display a new month
        """
        button = self.sender()
        if isinstance(button, QPushButton):
            month = button.text()
            
            #hides current window and initializes new window
            self.new_window = MonthlySpendingChecker(self.name, month)
            self.new_window.show()
            self.close()

    @pyqtSlot()
    def go_back(self):
        """
        Goes back to login page
        """
        self.new_window = Registration()
        self.new_window.show()
        self.close()

    def update_profits(self):
        """
        Updates profits label to match current values
        """
        global user
        yearly_profit = "Current Yearly Profit: $" + str(user[self.name].calc_net_yearly_profit())
        self.yearly_profit.setText(yearly_profit)

        # saves user data
        save()

class MonthlySpendingChecker(QWidget):
    """
    Lets users and add and remove items for each month
    """
    def __init__(self, name, month):
        """
        Initializes window to 640 x 480
        name - name of user who's information will be viewed
        month - month who's information will be viewed and modified
        mm - MonthManagement class component who's information
        will be observed later
        """
        super().__init__()
        self.title = "Financial Info Tracker"
        
        #Window Dimmensions
        self.name = name
        self.month = month
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        """
        Initializes UI components
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #initializes title label
        global user
        self.title = init_label(self, self.name + "'s "+ str(user[self.name].get_year()) + " spending")
        
        #Labels, textboxes, and buttons that adds new items to monthly spending
        self.add_labelN = init_label(self, "New Item Name:", 20, 30)
        self.add_textboxN = init_textbox(self, 140, 40, 130, 30)
        self.add_labelP = init_label(self, "New Item Price:", 20, 90)
        self.add_textboxP = init_textbox(self, 140, 40, 130, 90)
        self.add_button = init_button(self, "Add", self.add_item, 130, 150)

        #Button dedicated to removing item from list
        self.remove_button = init_button(self, "Remove", self.remove_item, 250, 150)

        #Button dedicated to going back to month page
        self.gb_button = init_button(self, "Go Back", self.go_back, 370, 150)

        #Label dedicated to showing monthly income
        monthly_income = "Current Monthly Income: $" + str(user[self.name].get_monthly_budget(self.month))
        self.monthly_income = init_label(self, monthly_income, 20, 190)

        #Label dedicated to showing net monthly profit
        monthly_profit = "Current Monthly Profit: $" +str(user[self.name].calc_net_monthly_profit(self.month))
        self.monthly_profit = init_label(self, monthly_profit, 20, 210)

        #Button and textbox dedicated to modifying monthly budget
        self.cb_box = init_textbox(self, 70, 40, 20, 240)
        self.change_budget = init_button(self, "Change Budget", self.change_mb, 20, 290)

        #Creates scrollable list of items
        self.itemDisplay = QTableWidget(self)
        self.itemDisplay.move(270, 230)
        self.update_item_table()

    @pyqtSlot()
    def add_item(self):
        """
        Adds new item to financial aid object list 
        """
        #variables that represent the name and price of the new object to be added
        global user, v_p
        item = self.add_textboxN.text().strip()
        price = self.add_textboxP.text().strip()
        
        #check to see if price is numeric
        if(v_p.match(price)):
            price = float(price.strip("$"))
            
            #checks to see if item is already in the monthly purchases and displays appropriate message
            items = [list(i) for i in zip(*user[self.name].get_monthly_purchase(self.month))]
            if(len(items)!=0 and item in items[0]):
                QMessageBox.question(self, "Item successfully changed.", "New Item was successfully changed.", QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.question(self, "Item successfully added.", "New Item was successfully added.", QMessageBox.Ok, QMessageBox.Ok)

            #add new item to list
            user[self.name].add_monthly_purchase(self.month, item, price)

            #updates table and labels
            self.update_item_table()
            self.update_labels()
        else:
            #displays error message if price is not correctly marked
            QMessageBox.question(self, "New Item could not be added.", "Please enter a valid price.",QMessageBox.Ok, QMessageBox.Ok)

    @pyqtSlot()
    def go_back(self):
        """
        Goes back to MonthManagement Page
        """
        self.new_window = MonthManagement(self.name)
        self.new_window.show()
        self.close()

    @pyqtSlot()
    def remove_item(self):
        """
        Removes item from list if it is in textbox
        """
        item = self.add_textboxN.text().strip()
        items = [list(i) for i in zip(*user[self.name].get_monthly_purchase(self.month))]
        
        #Checks if item was actually bought by the user
        if(len(items)!=0 and item in items[0]):
            QMessageBox.question(self, "Item successfully removed", "Item was successfully removed", QMessageBox.Ok, QMessageBox.Ok)
            
            #removes item from user object
            user[self.name].remove_monthly_purchase(self.month, item)

            #updates table and lables
            self.update_item_table()
            self.update_labels()
        else:
            QMessageBox.question(self, "Error", "The item was not purchased by the user.", QMessageBox.Ok, QMessageBox.Ok)
    
    @pyqtSlot()
    def change_mb(self):
        """
        Changes monthly budget
        """
        global user, v_p
        nb = self.cb_box.text().strip()
        
        #check to see if inputted string is valid number
        if(v_p.match(nb)):

            QMessageBox.question(self, "Change - Successful!", "Monthly budget successfully changed.", QMessageBox.Ok, QMessageBox.Ok)
            #modifies current monthly budget
            user[self.name].set_monthly_budget(self.month, float(nb.strip("$")))

            #updates labels
            self.update_labels()

    def update_labels(self):
        """
        updates labels & saves user data
        """
        monthly_profit = "Current Monthly Profit: $" + str(user[self.name].calc_net_monthly_profit(self.month))
        self.monthly_profit.setText(monthly_profit)
        monthly_income = "Current Monthly Income: $" + str(user[self.name].get_monthly_budget(self.month))
        self.monthly_income.setText(monthly_income)

        # saves user data
        save()
        
    def update_item_table(self):
        """
        Shows currently purchased items in table
        """
        global user
        items = user[self.name].get_monthly_purchase(self.month)
        self.itemDisplay.setHorizontalHeaderLabels(('Name', 'Price'))
        #modifies table dimmensions
        self.itemDisplay.setRowCount(len(items))
        self.itemDisplay.setColumnCount(2)

        #conditional to check that monthly list of purchased items is not empty
        if(len(items) != 0):

            #adds each item and its price to the table
            for count, item in enumerate(items):

                #adds name
                self.itemDisplay.setItem(count, 0, QTableWidgetItem(item[0]))

                #adds price
                self.itemDisplay.setItem(count, 1, QTableWidgetItem("$" + str(item[1])))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Registration()
    sys.exit(app.exec_())
