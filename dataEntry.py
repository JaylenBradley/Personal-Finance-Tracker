from datetime import datetime

dateFormat = "%m-%d-%Y" 
CATEGORIES = {'I': "Income", 'E': "Expense"}

def getDate(prompt, allowDefault=False): #default is current date 
    dateStr = input(prompt)
    if allowDefault and not dateStr:
        return datetime.today().strftime(dateFormat) #strftime = string format time; date-month-year; method returns todays date 
    
    try:
        validDate = datetime.strptime(dateStr, dateFormat) #convert string to datetime object
        return validDate.strftime(dateFormat)
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY")
        return getDate(prompt, allowDefault) #recursive call to getDate if invalid date format

def getAmount(): 
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative, non-zero value") #creates an error message with "raise" keyword 
        return amount
    except ValueError as e:
        print(e)
        return getAmount() #recursive call to getAmount if invalid amount format

def getCategory():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense")
    return getCategory()

def getDescription():
    return input("Enter a description (optional): ")