#USE latestFile2.py

import os

path = '/Users/sammyconrad-rooney/Documents/Projects/frangible-analyzer/'
files = sorted(os.listdir(path), key=os.path.getctime)

newest = files[-1]
print(newest)