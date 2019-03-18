import tkinter as tk
from tkinter import ttk
from difflib import SequenceMatcher
import random, time, os, csv, datetime

# global vars

# Helper functions 

# Get a list of CSV in DIR then return a list of the ones that are search reports

def getSearchTermReports():
    csvInDir = [item for item in os.listdir() if '.csv' in item]
    searchTermInDir = []
    for csvFile in csvInDir:
        with open(csvFile) as csvFileCheck:
            csvReader = csv.reader(csvFileCheck)
            if 'search term' in next(csvReader)[0].lower():
                searchTermInDir.append(csvFile)

    return tuple(searchTermInDir)

# Get a current datetime string to append to created CSV file name for uniqueness 

def getDateTimeNow():
    dateTimeNow = datetime.datetime.now()
    return f'{dateTimeNow.strftime("%y")}{dateTimeNow.strftime("%d")}{dateTimeNow.strftime("%y")}{dateTimeNow.strftime("%H")}{dateTimeNow.strftime("%M")}{dateTimeNow.strftime("%f")}'

# Get SequenceMatcher between two strings
def getRatio(a,b):
    return SequenceMatcher(None, stringPrep(a), stringPrep(b)).ratio()

# prep strings for comparison
def stringPrep(stringToPrep):
    return stringToPrep.lower().replace(" ","")

# Get Search Term Report CSV reader and advance to header, prep header, and prep for scoring
def prepSearchTermReader(searchTermReader):

    return True

# audit main to kick off scoring
def auditMain():
    totalRows = 0
    with open(cboxGetSearchTermReport.get(), errors="ignore") as csvReader:
        reader = csv.reader(csvReader)
        headerSearchRow = next(reader)

        while 'Account name' not in headerSearchRow:
            if headerSearchRow:
                if 'Rows' in headerSearchRow[0]:
                    rowCountsplit = headerSearchRow[0].split(" ")
                    totalRows = int(rowCountsplit[1]) + 11

            headerSearchRow = next(reader)
        
        
        with open(f'TEST{getDateTimeNow()}.csv', 'w', newline='') as csvwriter:
            searchTermReportWriter = csv.writer(csvwriter)
            headerSearchRow.append('Difference Ratio')
            searchTermReportWriter.writerow(headerSearchRow)
            for row in reader:
                var.set(f'{reader.line_num} rows scored out of {totalRows}')
                window.update()        
                
                if row:
                    if row[headerSearchRow.index('Keyword')].replace(" ",""):                       
                        ratio = getRatio(row[headerSearchRow.index('Search term')], row[headerSearchRow.index('Keyword')])
                                    
                        if ratio < float(cboxGetDiffRatioThresh.get()):
                            row.append(ratio)
                            searchTermReportWriter.writerow(row)             
                else:
                    break

# Global variables
tupleOfSearchTermInDir = getSearchTermReports()

# main thread to kick off script

# GUI Setup

# GUI | Base window

window = tk.Tk()
window.title('Tech Solutions | Search Term Report - Exact Match Variance Audit')
window.geometry('550x200')

# GUI | Label for choosing Search Term Report to Audit
chooseSearchTermReport = tk.Label(text='Search Term Report:', font=36)
chooseSearchTermReport.grid(column=0,row=0, sticky="W", pady=10) 

cboxGetSearchTermReport = ttk.Combobox(values=tupleOfSearchTermInDir, state="readonly", font=12)
cboxGetSearchTermReport.set(tupleOfSearchTermInDir[0])
cboxGetSearchTermReport.grid(column=1,row=0)

# GUI | Label for Diff Ratio Threshhold
title = tk.Label(text='Difference Ratio Threshhold:', font=36)
title.grid(column=0,row=1, sticky="W", pady=10) 

# GUI | Combox Box for Diff Ratio Threshhold
cboxGetDiffRatioThresh = ttk.Combobox(values=(0.25,0.50,0.75,1.00), state="readonly", font=12)
cboxGetDiffRatioThresh.set(0.25)
cboxGetDiffRatioThresh.grid(column=1,row=1)
# BUTTON
auditButton = tk.Button(text="Audit", command=auditMain, font=36, width=10)
auditButton.grid(column=1,row=3, padx=10, pady=10)

# progressbar = ttk.Progressbar(maximum=100)
# progressbar.grid(column=0,row=2)

var = tk.StringVar()
var.set('')
proglabel = tk.Label(textvariable=var)
proglabel.grid(column=0,row=3)

# GUI | Label for help contact fooder

# GUI | LAUNCH WINDOW
window.mainloop()

# Run main def

