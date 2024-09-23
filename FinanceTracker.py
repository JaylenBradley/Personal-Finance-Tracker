import pandas as pd
import csv
from datetime import datetime
from dataEntry import getDate, getAmount, getCategory, getDescription #imports functions from file "dateEntry.py"
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = 'finance_data.csv' #file you want to process, "comma separated values"
    COLUMNS = ['date', 'amount', 'category', 'description'] #define the column names
    FORMAT = "%m-%d-%Y"

    @classmethod
    def initializeCSV(cls): #cls passed as a class method, meaning it can be called directly on the class, not an instance of; same as using "self"
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS) #dataframe object accesses rows/columns from the CSV file
            df.to_csv(cls.CSV_FILE, index=False) #save the dataframe to the CSV file; index=False prevents pandas from adding an extra column of row numbers, not going to use indexing

    @classmethod
    def addEntry(cls, date, amount, category, description):
        newEntry = { #dictionary representing a new entry in the CSV file
            'date': date,
            'amount': amount,
            'category': category,
            'description': description
        } 
        with open(cls.CSV_FILE, 'a', newline='') as csvfile: #open the CSV, file is stored as 'csvfile'       
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS) #create a DictWriter object; CSVWriter takes a dict and writes it to a CSV file
            writer.writerow(newEntry) #write the new entry to the CSV file
        print(f'Added entry: {newEntry}')
    
    @classmethod
    def getTransactions(cls, startDate, endDate):
        df = pd.read_csv(cls.CSV_FILE) #read the CSV file into a pandas dataframe
        df['date'] = pd.to_datetime(df['date'], format=CSV.FORMAT) #to_datetime() function converts string to datetime object; converts all dates to the same format in the object
        df.sort_values(by='date', inplace=True) # sort the dataframe by the 'date' column

        startDate = datetime.strptime(startDate, CSV.FORMAT)
        endDate = datetime.strptime(endDate, CSV.FORMAT) #updates the start and end dates to datetime objects and converts them to the same format

        mask = (df['date'] >= startDate) & (df['date'] <= endDate) #checks if the date in the column is within the specified range; allowed bc they're datetime objects not strings; & is used w pandas
        filtered_df = df.loc[mask] #returns a new filtered dataframe containing only the rows that apply to the mask; the mask applies to every row in the df

        if filtered_df.empty:
            print("No transactions found in the specified date range.")
        else:
            print(f"Transactions from {startDate.strftime(CSV.FORMAT)} to {endDate.strftime(CSV.FORMAT)}:") #converting datetime objects back to strings
            print(filtered_df.to_string(index=False, formatters={'date': lambda x: x.strftime(CSV.FORMAT)})) 
            """converts the dataframe to a string, removing the index column; function gets called in dict to format; 
            lambda = one line anonymous function, passes parameter x (dt objects) and formats them"""

            totalIncome = filtered_df[filtered_df['category'] == 'Income']['amount'].sum() #gets all rows where category is 'Income' within the filtered dataframe; then gets the sum of the 'amount' column
            totalExpense = filtered_df[filtered_df['category'] == 'Expense']['amount'].sum() #same as above but for 'Expense' category
            print("\nSummary:") 
            print(f"Total Income: ${totalIncome:.2f}") #formats to 2 decimal places with ".2f"
            print(f"Total Expense: ${totalExpense:.2f}")
            print(f"Net Savings: ${(totalIncome - totalExpense):.2f}")

        return filtered_df #can now create plot with data

def add():
    CSV.initializeCSV()
    date = getDate(
        "Enter the date of the transaction (MM-DD-YYYY) or enter for today's date: ", 
        allowDefault=True
    ) #multi line writing as long as within parentheses
    amount = getAmount()
    category = getCategory()
    description = getDescription()
    CSV.addEntry(date, amount, category, description)

def plotTransactions(df):
    df.set_index('date', inplace=True) #set 'date' as index for easier manipulation; index by date

    incomeDF = df[df['category'] == 'Income'].resample('D').sum().reindex(df.index, fill_value=0) #resample('D') resamples the data to daily frequency; make sure there's a row for each day & aggregate values on same day
    expenseDF = df[df['category'] == 'Expense'].resample('D').sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5)) #set the size of the screen/figure
    plt.plot(incomeDF.index, incomeDF['amount'], label='Income', color="g") #X value is the index, Y value is the 'amount' column, label is for legend
    plt.plot(expenseDF.index, expenseDF['amount'], label='Expense', color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show() #shows the plot

def main():
    while True:
        print("\nChoose an option:")
        print("1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            startDate = getDate("Enter the start date (MM-DD-YYYY): ")
            endDate = getDate("Enter the end date (MM-DD-YYYY): ")
            df = CSV.getTransactions(startDate, endDate) #use df if want to plot on graph
            if input("Do you want to see a plot? (Y/N): ").upper() == "Y":
                plotTransactions(df)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
 
if __name__ == "__main__": #makes sure this script is ran directly, not imported as a module
    main()