from financialInfo import financialInfo
"""
Written by Aaron Shah
6 / 29 / 2019
Class that test financialInfo methods
to see if they are working properly
"""
months =  ["Jan", "Feb", "Mar",
           "Apr", "May", "Jun",
           "Jul","Aug","Sep",
           "Oct","Nov","Dec"] #months in year
def testInitialization():
    """
    Test to see if financialInfo object
    is properly initializaed
    """
    test1 = financialInfo()
    print(test1)

def testAccessorMethods():
    """
    Test accessor methods of
    financialInfo object
    """
    test2 = financialInfo(2019, 100000)
    print(test2.get_income()) #test to see if proper income is displayed
    print(test2.get_year()) #test to see if proper year is displayed
    global months
    for month in months:
        print(test2.get_monthly_budget(month)) #test to see if proper
        # monthly budget is displayed at the end of each month
        print(test2.get_monthly_purchase(month)) #test to see if method
        # returns empty list
def testMutatorMethods():
    """
    Test mutator methods of
    financialInfo object
    """
    test3 = financialInfo(2019, 100000)
    test3.set_income(90000)
    print(test3.get_income())
    for month in months:
        test3.set_monthly_budget(month, 2000)
        print(test3.get_monthly_budget(month))
def testAddRemove():
    """
    Test adding and removing items to
    monthly purchases
    """
    test4 = financialInfo(2019, 100000)
    for month in months:
        test4.add_monthly_purchase(month, "Shaving Cream", 200)
        print(test4.get_monthly_purchase(month))
        test4.remove_monthly_purchase(month, "Shaving Cream")
        print(test4.get_monthly_purchase(month))

def testMonthCalculations():
    """
    Test if methods calculates
    numbers correctly
    """
    test5 = financialInfo(2019, 1000)
    test5.add_monthly_purchase("Jan", "Game", 200)
    test5.add_monthly_purchase("Jan", "Cap", 150)
    test5.add_monthly_purchase("Jan", "Ball", 27)
    print(test5.calc_monthly_spending("Jan"))
    print(test5.calc_net_monthly_profit("Jan"))
    for month in months:
        test5.add_monthly_purchase(month, "Shoe", 20)
    print(test5.calc_yearly_spending())
    print(test5.calc_net_yearly_profit())
#Test calls
"""
testInitialization()
testAccessorMethods()
testMutatorMethods()
testAddRemove()
"""
testMonthCalculations()
