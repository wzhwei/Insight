"""
This is my solution to the data challenge of finding political donors. 
The details of the challenge can be found in:
https://github.com/InsightDataScience/find-political-donors
"""

import numpy as np
import pandas as pd

data = pd.read_csv('./input/itcont.txt', sep='|', header=None, dtype=np.object)
fzip = open('./output/medianvals_by_zip.txt','w')
fdate = open('./output/medianvals_by_date.txt','w')
#print(data.info())
#print(data.head())

zdic={} # To collect the data for medianvals_by_zip
ddic={} # To collect the data for medianvals_by_date

for i in range(data.shape[0]):
    current_row = data.iloc[i]
    if current_row.isnull()[15]: # we only want records that have the field, OTHER_ID (current_row[15]), set to empty
        id = current_row[0]
        zip_code_raw = current_row[10]
        date = current_row[13]
        amount = float(current_row[14])
        
        # Ignore any lines with empty cells in the CMTE_ID (id) or TRANSACTION_AMT(amount) fields
        if (not len(id)) or (not amount): 
            break

        if len(zip_code_raw) >= 5: # we only want the first five digits/characters of zip code
            zip_code = zip_code_raw[:5]
            
            zdic[(id,zip_code)] = zdic.get((id,zip_code),[]) + [amount]
            
            # calculate the running median of contributions, 
            # total number of transactions and 
            # total amount of contributions streaming in so far for that recipient and zip code
            a = str(id) + '|' + str(zip_code) + '|' \
                + str(int(np.round(np.median(zdic[(id,zip_code)])))) + '|' \
                + str(len(zdic[(id,zip_code)])) + '|' \
                + str(int(np.sum(zdic[(id,zip_code)]))) + '\n'
            fzip.write(a)

        if len(date) == 8: # Ignore when TRANSACTION_DT (date) is an invalid date
            ddic[(id, date)] = ddic.get((id, date), []) + [amount]
            
for key in sorted(ddic): # this  output file should have lines sorted alphabetical by recipient and then chronologically by date
    # Each line should list every unique combination of date and recipient from the input file 
    # and then the calculated median contributions 
    # and total contribution for that combination of date and recipient.
    a = str(key[0]) + '|' + str(key[1]) + '|' \
        + str(int(np.round(np.median(ddic[key])))) + '|' \
        + str(len(ddic[key])) + '|' \
        + str(int(np.sum(ddic[key]))) + '\n'
    fdate.write(a)

fzip.close()
fdate.close()
