import os
from datetime import date
from datetime import datetime
import csv
import sys
import pandas as pd
import matplotlib.pyplot as plt



#Functionality
class Transaction:
    def __init__(self):
        self.trans_file_path = "transaction.csv"



    #function for Add
    def Add_trans(self):

        for count in range(5):
            date_in = input("Enter date (YYYY-MM-DD), or Enter for today: ").strip()
            if not date_in:
                self.date_obj = date.today()
                break
            try:
                self.date_obj = datetime.strptime(date_in, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid format — please try again. ")
            if count == 4:
                print("Sorry range is over try again from home page")
                return


        for count in range(5):
            self.amount = input("Enter amount (in dollars) ")
            try:
                self.amount = float(self.amount)
                break
            except ValueError:
                print("Invalid amount please try again. ")

            if count == 4:
                print("Sorry range is over try again from home page")
                return


        self.category = input("Enter category(i for income or enter e for expense): ").lower()
        if self.category == "i":
            self.category = "Income"

        else:
            self.category = "Expense"



        self.description = input("Enter description(Optional): ").strip()
        if not self.description:
            self.description = f"Some {self.category}."



        #Writing details
        if os.path.exists(self.trans_file_path):
            with open(self.trans_file_path, "a", newline="") as trans_file:
                writer = csv.writer(trans_file)
                writer.writerow([self.date_obj, self.amount, self.category, self.description])

        else:
            print("Transection file does not exist")
            with open(self.trans_file_path, "w", newline="") as trans_file:
                writer = csv.writer(trans_file)
                writer.writerow([self.date_obj, self.amount, self.category, self.description])



        return





    #Function for View
    def view_all_trans(self):

        df = pd.read_csv(self.trans_file_path)
        print(df.to_markdown(index=False, tablefmt="psql", floatfmt=".2f"))

        print(" ")

        summery = input("Want to know summery (y/n): ").lower()
        print(" ")
        if summery == "y":
            df = pd.read_csv(self.trans_file_path, parse_dates=['Date'])

            self.totel_incomes = df.loc[df['Category'] == 'Income', 'Amount'].sum()
            self.totel_expenses = df.loc[df['Category'] == 'Expense', 'Amount'].sum()
            self.totel_savings = self.totel_incomes - self.totel_expenses

            print(f"Total Income: ${self.totel_incomes}")
            print(f"Total Expense: ${self.totel_expenses}")
            print(f"Total Savings: ${self.totel_savings}")

        chart = input("Want to see chart (y/n): ").lower()
        if chart == "y":
            df = pd.read_csv(self.trans_file_path, parse_dates=['Date'])
            daily = (df.groupby([df['Date'].dt.date, 'Category'])
                     ['Amount'].sum()
                     .unstack(fill_value=0))

            chart_choice = input("Bar chart or Pie chart or Both(b/p/both): ").lower()
            if chart_choice == "b":
                # For the Bar chart
                daily.plot(kind='bar', figsize=(10, 6))
                plt.title('Income and Expense by Date')
                plt.xlabel('Date')
                plt.ylabel('Amount')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

            elif chart_choice == "p":
                # For the Pie chart
                totals = df.groupby('Category')['Amount'].sum()
                totals.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], figsize=(6, 6))
                plt.title('Income vs Expense Share')
                plt.ylabel('')
                plt.show()


            else:
                # For the Bar chart
                daily.plot(kind='bar', figsize=(10, 6))
                plt.title('Income and Expense by Date')
                plt.xlabel('Date')
                plt.ylabel('Amount')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()

                # For the Pie chart
                totals = df.groupby('Category')['Amount'].sum()
                totals.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], figsize=(6, 6))
                plt.title('Income vs Expense Share')
                plt.ylabel('')
                plt.show()

        return






    def view_trans(self):
        for count in range(5):
            start_date_in = input("Enter start date (YYYY-MM-DD): ")

            try:
                self.start_date = datetime.strptime(start_date_in, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid format — please try again. ")
            if count == 4:
                print("Sorry range is over try again from home page")
                return


        for count in range(5):
            end_date_in = input("Enter date (YYYY-MM-DD): ")

            try:
                self.end_date = datetime.strptime(end_date_in, "%Y-%m-%d").date()
                break

            except ValueError:
                print("Invalid format — please try again. ")

            if count == 4:
                print("Sorry range is over try again from home page")
                return

        print(" ")

        df = pd.read_csv(self.trans_file_path, parse_dates=['Date'])

        mask = (df['Date'].dt.date >= self.start_date) & (df['Date'].dt.date <= self.end_date)
        subset = df.loc[mask]

        if len(subset) != 0:
               print(subset.to_markdown(index=False, tablefmt="psql", floatfmt=".2f"))

               print(" ")

               incomes_dr = subset.loc[subset['Category'] == 'Income', 'Amount'].sum()
               expenses_dr = subset.loc[subset['Category'] == 'Expense', 'Amount'].sum()
               savings_dr = incomes_dr - expenses_dr

               print(f"Total Income from {self.start_date} to {self.end_date}: ${incomes_dr}")
               print(f"Total Expense from {self.start_date} to {self.end_date}: ${expenses_dr}")
               print(f"Total Savings from {self.start_date} to {self.end_date}: ${savings_dr}")

               chart = input("Want to see chart (y/n): ").lower()
               if chart == "y":
                   chart_choice = input("Pie chart or Bar chart or Both (p/b/both): ").lower()
                   if chart_choice == "p":
                       #for pie chart

                       totals = subset.groupby('Category')['Amount'].sum()
                       totals.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], figsize=(6, 6))
                       plt.title('Income vs Expense Share')
                       plt.ylabel('')
                       plt.show()


                   elif chart_choice == "b":
                       #for bar chart
                       daily = (subset.groupby([df['Date'].dt.date, 'Category'])
                                ['Amount'].sum()
                                .unstack(fill_value=0))

                       daily.plot(kind='bar', figsize=(10, 6))
                       plt.title('Income and Expense by Date')
                       plt.xlabel('Date')
                       plt.ylabel('Amount')
                       plt.xticks(rotation=45)
                       plt.tight_layout()
                       plt.show()

                   else:
                       #For Pie chart
                       totals = subset.groupby('Category')['Amount'].sum()
                       totals.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'], figsize=(6, 6))
                       plt.title('Income vs Expense Share')
                       plt.ylabel('')
                       plt.show()

                       #For Bar chart
                       daily = (subset.groupby([df['Date'].dt.date, 'Category'])
                                ['Amount'].sum()
                                .unstack(fill_value=0))

                       daily.plot(kind='bar', figsize=(10, 6))
                       plt.title('Income and Expense by Date')
                       plt.xlabel('Date')
                       plt.ylabel('Amount')
                       plt.xticks(rotation=45)
                       plt.tight_layout()
                       plt.show()

        else:
            print(f"No transactions found from {self.start_date} to {self.end_date}!")

        return





#Interface
print("Welcome")
trans = Transaction()
while True:

         print("____________________________")
         print("|--1.Add new transaction---|")
         print("|--2.View all transaction--|")
         print("|--3.View trans daterange--|")
         print("|--4.Exit------------------|")
         print("|__________________________|")


         choice = input("Enter your choice: ")


         #For select the page(function)
         match choice:
             case '1':
                 print("Create page load")
                 trans.Add_trans()

             case '2':
                 print("View page load")
                 trans.view_all_trans()

             case '3':
                 print("Trans within date range page loading")
                 trans.view_trans()

             case '4':
                 print("Thank you!")
                 sys.exit(0)

