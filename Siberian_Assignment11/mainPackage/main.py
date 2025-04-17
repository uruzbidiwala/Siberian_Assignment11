# File Name: #main.py 
# Names: Nogaye Gueye, Uruz Bidiwala
# email:  gueyene@mail.uc.edu  bidiwaur@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:  04/17/2025
# Course #/Section:   IS4010
# Semester/Year:   Spring 2025
# Brief Description of the assignment: Created classes and methods with code to clean data sets and create csv files. 
# Brief Description of what this module does: Contains entry point and prints extra credit statements.  
# Citations: openai.com 
# Anything else that's relevant: N/A

from cleanedDataPackage.cleanedData import DataCleaner


def main():
    cleaner = DataCleaner("Data/fuelPurchaseData.csv")
    cleaner.clean_and_save()
    #("Data/cleanedData.csv")
   

if __name__ == "__main__":
    main()

print ("For extra credit")
print ("Issue #1: Addresses are not in the same format, making it harder to pull zip codes")
print ("Issue #2: Site ID has random words other than numbers")

