"""
Thanks, Samyak, we will need to clean up this data a little. Can you please write a python code that does the following
to the individual files:

1. Create two new columns Coin1 Coin2 -- if the name of the file is BCH BTC Coin1 is BCH, Coin2 will be BTC

2. Rename the Volume Columns (H and I) -- For example, if the filename is  BCH BTC, volume columns right now are Volume
BCH and Volume BTC -- rename these to VolumeCoin1 VolumeCoin2

3. Create a new column exchange name that is equal to the name of the exchange (i.e., the folder name)

4. Do 1, 2, and 3 for all the files in all the folders

(also remove the first row in these Excel files that say *Timezones are UTC https://www.CryptoDataDownload.com*).

Append all the Excel files from all the folders to create just one final output file.

Regards,
Vasundhara
"""


# IMPORTS:

from os import listdir, chdir, startfile
from csv import reader, writer
from time import perf_counter


start = perf_counter()


# CONSTANTS:

DATA_DIR = '..\\Scraped Data'
CSV = 'Final Data.csv'
COLUMNS = ['Exchange Name', 'Coin1', 'Coin2', 'Unix Timestamp', 'Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume Coin1', 'Volume Coin2']
DEBUG = False  # default: False


# MAIN:

data = [COLUMNS]
print()  # spacing

csv_dirs = listdir(DATA_DIR)
chdir(DATA_DIR)
for exchange in csv_dirs:
    print(exchange, end=': ')

    csvs = listdir(exchange)
    print(len(csvs))
    chdir(exchange)
    for csv in csvs:
        if DEBUG:
            print(csv)

        # Reading the data from the CSVs:
        coin1, coin2 = csv.split('.')[0].split()
        with open(csv) as csvfile:
            for row in list(reader(csvfile))[2:]:  # [2:] -> skipping header columns
                for i in range(len(row)):  # converting strings to floats
                    try:
                        row[i] = float(row[i])
                    except ValueError:
                        pass
                # print(row)  # debugging
                data.append([exchange, coin1, coin2, *row])

        if DEBUG:
            break
    chdir('..')
    if DEBUG:
        break
chdir('..')

# Writing the data to the CSV:
total_rows = len(data)
print('\nTotal Rows:', total_rows)
with open(CSV, mode='w', newline='') as csvfile:
    writer(csvfile).writerows(data)

if DEBUG:
    startfile(CSV)

print(f'Time Taken: {perf_counter()-start}s')
