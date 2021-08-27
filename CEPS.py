import os, os.path, argparse
from datetime import date, datetime
import pandas as pd
import calendar

name = str(date.today()).split()[0]
excelDir = '' #ENTER WHERE YOU WANT THE EXCEL OUTPUT FILE TO GO

assignedTo = ["Jin Moon", "Sara Bauman", "Adel Ferjani", "Claudette Pion"]
columnsToRemove = ["Permit Number", "Pending", "Purpose", "Trade Type", "Permit Usage", "Date In", "Created in CEPS Date", "Assigned Date", "Entering Date", "Date Out", "Days Pending", "Days from Received to Created",
                   "Days from Created to Assigned", "Days from Received to Entering", "Days with MA", "Days with SA", "Days from Received to Issued", "Days Prcessing minus Pending Days", 
                   "Application Weight Factor", "Permit Weight Factor", "Created By", "Issued By", "Last Updated By", "Last Updated"]

d2 = date.today()
d1 = date(2021, 5, 4)

# Parser for the input file
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True)
args = parser.parse_args()

# CSV Input File
csvFile = args.file

df = pd.read_csv(csvFile)

df = df.drop(df[df["Assigned To"].isin(["Jin Moon", "Sara Bauman", "Adel Ferjani", "Claudette Pion"]) == False].index)

df = df.drop(df[df.Pending == "Yes"].index)

df = df.drop(df[df.Status == "MA Approved"].index)

df['Days Pending'] = df['Days Pending'].fillna(0)

df['Date In'] = df['Date In'].astype('datetime64[ns]').dt.date

df['Age'] = ((date.today() - df['Date In']).dt.days) - df['Days Pending']

df.drop(columnsToRemove, inplace=True, axis=1)

output = {}

df = df.sort_values(['Assigned To', 'Status', 'Age'])
 

df.to_excel(excelDir + name + '_CEPS.xlsx', index=False)