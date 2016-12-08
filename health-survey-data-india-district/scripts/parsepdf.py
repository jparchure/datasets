import csv
import pandas as pd
from tabula import read_pdf_table
import os

def file_extractor(directory, state, filename):
    files = [f for f in os.listdir(directory) if os.path.isfile(f)]
    #header = ["State","District","DistrictType", "Indicators","Urban","Rural", "Total"]
    #myfile = open(filename, 'wb')
    #wr = csv.writer(myfile)
    #wr.writerow(header)
    for f in files:
        if f.endswith(".pdf"):
            df=read_pdf_table(f,pages="3-5")
            parse_file(df,f[:-4],state,filename)


def parse_file(df,district,state,writefile):
    newdata = pd.DataFrame(df[29:])
    newdata = newdata.dropna(axis=0)
    newdata.columns=["Indicators", "Type Total"]
    district_type=""

    if "Urban Total" in list(newdata.iloc[:,1]):
        district_type="Urban"
        newdata["Rural"] = newdata["Type Total"].dropna(axis=0).apply(lambda x: "NA")
        newdata["Urban"] = newdata["Type Total"].str.split(" ").dropna(axis=0).apply(lambda x: x[0])
    elif "Rural Total" in list(newdata.iloc[:,1]):
        district_type="Rural"
        newdata["Urban"] = newdata["Type Total"].dropna(axis=0).apply(lambda x: "NA")
        newdata["Rural"] = newdata["Type Total"].str.split(" ").dropna(axis=0).apply(lambda x: x[0])
    elif "Urban Rural Total" in list(newdata.iloc[:,1]):
        district_type="Urban Rural"
        newdata["Urban"] = newdata["Type Total"].str.split(" ").dropna(axis=0).apply(lambda x: x[0])
        newdata["Rural"] = newdata["Type Total"].str.split(" ").dropna(axis=0).apply(lambda x: x[1])
    else:
        return("Error")

    newdata["Total"] = newdata["Type Total"].str.split(" ").dropna(axis=0).apply(lambda x: x[-1])

    #Exclude the rows with the Indicator banner which denotes a new page
    newdata = newdata[newdata['Indicators']!='Indicators']
    newdata=  newdata[newdata['Type Total']!=district_type + " Total"]

    #Hard coded values to parse indicators that span multiple lines
    truncated_value_indices = [33,34,35,38,46,59,60]
    truncated_values=[
    "34. Registered pregnancies for which the mother received Mother and Child Protection(MCP) card (%)",
    "35. Mothers who received postnatal care from a doctor/nurse/LHV/ANM/midwife/other health personnel within 2 days of delivery (%)",
    "36. Mothers who received financial assistance under Janani Suraksha Yojana (JSY) for births delivered in an institution (%)",
    "39. Children who received a health check after birth from a doctor/nurse/LHV/ANM/ midwife/other health personnel within 2 days of birth (%)",
    "47. Children age 12-23 months fully immunized (BCG, measles, and 3 doses each of polio and DPT) (%)",
    "60. Prevalence of symptoms of acute respiratory infection (ARI) in the last 2 weeks preceding the survey (%)",
    "61. Children with fever or symptoms of ARI in the last 2 weeks preceding the survey taken to a health facility (%)"
    ]

    newdata["Indicators"].iloc[truncated_value_indices] = truncated_values

    #Get rid of parentheses
    newdata["Urban"] = newdata["Urban"].str.strip("()")
    newdata["Rural"] = newdata["Rural"].str.strip("()")
    newdata["Total"] = newdata["Total"].str.strip("()")

    #Remove numbering
    newdata['Indicators'] = newdata['Indicators'].str.split(" ",1).apply(lambda x: x[1])

    newdata.drop(["Type Total"],axis=1, inplace=True)

    #Add geographical data
    newdata["District"] = district
    newdata["State"] = state
    newdata["DistrictType"] = district_type

    #Reorder columns
    newdata=newdata[["State","District","DistrictType", "Indicators","Urban","Rural", "Total"]]

    with open(writefile, 'a') as f:
        newdata.to_csv(f, header=False,index=False)

file_extractor(".", "Madhya Pradesh", "healthdata.csv")
