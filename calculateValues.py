import csv

fileName = '../data/Frangible_1_2019-02-13_11-45-56.csv' #The .csv file being used

#the following converts the csv file into a list
def toList(name):
    with open(name, 'r') as f:
        reader = csv.reader(f)
        completeList = list(reader)

    listLen = len(completeList)
    firstItemList = []

    for item in completeList: #Extracts only the second column from the .csv file
        firstItemList.append(item[1])
    return firstItemList

#print(toList(fileName))

#Removes the first entries that are empty or are the column title
def removeBadData(badList):
    count = 0
    while (badList[count] == 'Load (lbf)' or badList[count] == ''):
        count += 1
    return badList[count:]

cleanList = (removeBadData(toList(fileName))) #This is the cleaned list that contains only the useful values

#The following finds the first hump
currentLargest1 = 0
largestIndex1 = 0
numDecreasing1 = 0
count1 = 1000 #Start looking at entry 1000 to prevent incorrect hump values because of fluctuations

while numDecreasing1 < 500: #While the values haven't been decreasing for over 500 entries
    if cleanList[count1] > currentLargest1: #Set the largest value to the current value if the current value is larger than the previous largest value
        currentLargest1 = cleanList[count1]
        largestIndex1 = count1
        numDecreasing1 = 0
    elif cleanList[count1] < currentLargest1: #If the current value is less than the current largest value, add 1 to the decreasing counter
        numDecreasing1 += 1
    count1 += 1 #Increase the counter by 1 to go through the entire data set

print("First Hump:")
print(count1)
print("Largest Index: ",  largestIndex1)
print("Largest Value: ", currentLargest1)

#The following finds the second hump
currentLargest2 = 0
largestIndex2 = 0
numDecreasing2 = 0
count2 = largestIndex1 + 2000 #Start at 2000 entries past the first hump to get past the decrease after the first hump

while numDecreasing2 < 500: #While the values haven't been decreasing for over 500 entries
    if cleanList[count2] > currentLargest2:
        currentLargest2 = cleanList[count2]
        largestIndex2 = count2
        numDecreasing2 = 0
    elif cleanList[count2] < currentLargest2:
        numDecreasing2 += 1
    count2 += 1

print("Second Hump:")
print(count2)
print("Largest Index: ", largestIndex2)
print("Largest Value: ", currentLargest2)

#The following finds the low point
betweenHumpList = cleanList[largestIndex1:largestIndex2]
lowPoint = min(betweenHumpList)
print("Low point: ", lowPoint)