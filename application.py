from Tkinter import *
import csv
import glob
import os

#Calculates most recent file
path = '../data'

list_of_files = glob.glob('../data/*.csv') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print latest_file

#fileName = '../data/Frangible_8_2019-02-13_14-30-48.csv' #The .csv file being used

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

cleanList = (removeBadData(toList(latest_file))) #This is the cleaned list that contains only the useful values

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

#print("First Hump:")
#print(count1)
#print("Largest Index: ",  largestIndex1)
#print("Largest Value: ", currentLargest1)

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

#print("Second Hump:")
#print(count2)
#print("Largest Index: ", largestIndex2)
#print("Largest Value: ", currentLargest2)

#The following finds the low point
betweenHumpList = cleanList[largestIndex1:largestIndex2]
lowPoint = min(betweenHumpList)
#print("Low point: ", lowPoint)

#Widgets
window = Tk()
titleLabel = Label(window, relief = 'flat', width = 20)
nameLabel = Label(window, relief = 'groove', width = 20)
peak1Label = Label(window, relief = 'groove', width = 20)
valleyLabel = Label(window, relief = 'groove', width = 20)
peak2Label = Label(window, relief = 'groove', width = 20)
peak1Check = Label(window, relief = 'groove', width = 2)
valleyCheck = Label(window, relief = 'groove', width = 2)
peak2Check = Label(window, relief = 'groove', width = 2)
calcButton = Button(window)
showLimits = Button(window)

#Geometry
titleLabel.grid(row = 1, column = 1, columnspan = 4)
nameLabel.grid(row = 3, column = 1, columnspan = 2)
peak1Label.grid(row = 4, column = 1, columnspan = 2)
valleyLabel.grid(row = 5, column = 1, columnspan = 2)
peak2Label.grid(row = 6, column = 1, columnspan = 2)
peak1Check.grid(row = 4, column = 3)
valleyCheck.grid(row = 5, column = 3)
peak2Check.grid(row = 6, column = 3)
calcButton.grid(row = 8, column = 1)
showLimits.grid(row = 8, column = 2)

#Static Properties
window.title("Frangible Results")
titleLabel.configure(text = "Frangible Results", font = ("Arial", 18))
nameLabel.configure(text = "File Name: ", anchor="w")
peak1Label.configure(text = "Peak 1: ", anchor="w")
valleyLabel.configure(text = "Valley: ", anchor="w")
peak2Label.configure(text = "Peak 2: ", anchor="w")
calcButton.configure(text = "Get Values")
showLimits.configure(text = "Show Limits")


peak1Limit = 1.0 #LIMIT FOR peak1
valleyLimit = .5 #LIMIT FOR valley
peak2Limit = 1.0 #LIMIT FOR peak2

#Function to add values to application labels and change colors of limit boxes
def getValues():
    nameLabel.configure(text = ("File Name: " + str(latest_file))) #latest_file is the name of the latest file
    peak1Label.configure(text = ("Peak 1: " + str(currentLargest1))) #currentLargest1 is the value of the first peak
    valleyLabel.configure(text = ("Valley: " + str(lowPoint))) #lowPoint is the value of the valley
    peak2Label.configure(text = ("Peak 2: " + str(currentLargest2))) #currentLargest2 is the value of the second peak
    if float(currentLargest1) > peak1Limit:
        peak1Check.configure(bg = "green")
    else:
        peak1Check.configure(bg = "red")
    if float(lowPoint) > valleyLimit:
        valleyCheck.configure(bg = "green")
    else:
        valleyCheck.configure(bg = "red")
    if float(currentLargest2) > peak2Limit:
        peak2Check.configure(bg = "green")
    else:
        peak2Check.configure(bg = "red")

#Function to create a popup message with limits
def limitPopup():
    popup = Tk()
    popup.wm_title("Limits")
    label = Label(popup, text=("Peak 1 Limit: " + str(peak1Limit) + "\nValley Limit: " + str(valleyLimit) + "\nPeak 2 Limit: " + str(peak2Limit)))
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Hide", command = popup.destroy)
    B1.pack()
    popup.mainloop()

calcButton.configure(command = getValues)
showLimits.configure(command = limitPopup)

#Sustain window
window.mainloop()