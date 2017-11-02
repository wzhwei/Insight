import numpy as np
import pandas as pd

data = pd.read_csv('./input/itcont.txt', sep='|', header=None, dtype=np.object)
f1 = open('./output/medianvals_by_zip.txt','w')
f2 = open('./output/medianvals_by_date.txt','w')
#print(data.info())
#print(data.head())

zdic={}
ddic={}

for i in range(data.shape[0]):
    temp = data.iloc[i]
    if temp.isnull()[15]:
        id = temp[0]
        zip = temp[10]
        date = temp[13]
        amount = float(temp[14])
        
        if (not len(id)) or (not amount):
            break

        if len(zip) >= 5:
            zip = temp[10][:5]
            zdic[zip] = zdic.get(zip,[]) + [amount]
            a = str(id) + '|' + str(zip) + '|' + str(int(np.round(np.median(zdic[zip])))) + '|' + str(len(zdic[zip])) + '|' + str(int(np.sum(zdic[zip]))) + '\n'
            f1.write(a)

        if len(date) == 8:
            ddic[(id, date)] = ddic.get((id, date), []) + [amount]
            
for key in sorted(ddic):
    a = str(key[0]) + '|' + str(key[1]) + '|' + str(int(np.round(np.median(ddic[key])))) + '|' + str(len(ddic[key])) + '|' + str(int(np.sum(ddic[key]))) + '\n'
    f2.write(a)

f1.close()
f2.close()
