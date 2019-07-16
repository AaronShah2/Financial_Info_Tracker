from collections import defaultdict
"""
Written by Aaron Shah
6 / 27 / 2019
Class that helps with basic financial management
"""
class financialInfo:
    def __init__(self, year = 0, income = 0.0):
        """
        Constructor
        (year) - int variable representing year user
        wants to budget for
        (income) - double variable representing user's
        yearly income
        """
        self.year = year #inputted year
        self.income = float('%.2f'%income) #inputted income
        self.months = ["Jan", "Feb", "Mar",
                       "Apr", "May", "Jun",
                       "Jul","Aug","Sep",
                       "Oct","Nov","Dec"] #months in year
        #sets monthly budget to 1/12 of yearly income by default
        mb = '%.2f'%(income / 12)
        self.monthly_budget = {k:mb for k in self.months} #monthly budget
        self.monthly_purchases = {k:defaultdict(float) for k in self.months} #monthly puchases

    """
    Accessor and Mutator Functions
    """
    def get_monthly_budget(self, month):
        """
        Returns monthly budget of inputted month
        (month) - string variable representing month
        user wants monthly budget of
        """
        if month in self.months:
            return self.monthly_budget[month]
        return 0

    def set_monthly_budget(self, month, mb):
        """
        Modifies monthly budget of inputted month
        (month) - string variable representing month
        user wants monthly budget of
        (mb) - int variable representing new monthly
        budget
        """
        if month in self.months:
            self.monthly_budget[month] = float('%.2f'%mb)

    def get_income(self):
        """
        Returns yearly income
        """
        return self.income

    def set_income(self, income):
        """
        Modifies yearly income
        (income) - double variable representing
        new yearly income
        """
        self.income = income
        
    def get_year(self):
        """
        return year
        """
        return self.year

    def set_year(self, year):
        """
        modifies year
        year - new year
        """
        self.year = year
        
    def get_monthly_purchase(self, month):
        """
        Returns monthly purchases of inputted month
        (month) - string variable representing month
        user wants monthly purchases of
        """
        if month in self.months:
            return [(k,v)for k,v in self.monthly_purchases[month].items()]

    """
    Utility Functions
    """
    def add_monthly_purchase(self, month, name, price):
        """
        Adds item to monthly purchases for inputted month
        if name is not inputted, else modifies existing price
        associated with name
        (month) - string varaible representing month
        user want to input new monthly purchase
        (name) - string variable representing name
        of new purchase
        (price) - price of inputted variable
        """
        if month in self.months:
            self.monthly_purchases[month][name] = float('%.2f'%price)

    def remove_monthly_purchase(self, month, name):
        """
        Removes item from monthly purchases for inputted
        name and month assuming name is in monthly
        purchases
        (month) - string varaible representing month
        user want to remove monthly purchase from
        (name) - string variable representing name
        of purchase that user wants removed
        """
        if month in self.months and name in self.monthly_purchases[month]:
            del self.monthly_purchases[month][name]

    def calc_monthly_spending(self, month):
        """
        Calculates total amount of money spent
        during month
        (month) - string variable representing month
        the user wants to calculate the total monthly
        spending of
        """
        if month in self.months:
            return sum(self.monthly_purchases[month].values())

    def calc_yearly_spending(self):
        """
        Calculates total amount of money spent
        during the year
        """
        total = 0
        for _,mv in self.monthly_purchases.items():
            total+=sum(mv.values())
        return total

    def calc_net_monthly_profit(self, month):
        """
        Calculates the net gain or loss of the
        monthly expenses
        (month) - string variable representing
        month
        """
        if month in self.months:
            return float(self.monthly_budget[month]) - self.calc_monthly_spending(month)

    def calc_net_yearly_profit(self):
        """
        Calculates the net gain or loss of the
        yearly expenses
        """
        return self.income - self.calc_yearly_spending()


