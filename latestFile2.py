import glob
import os

path = '/Users/sammyconrad-rooney/Documents/Projects/frangible-project/data'

list_of_files = glob.glob('/Users/sammyconrad-rooney/Documents/Projects/frangible-project/data/*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print latest_file