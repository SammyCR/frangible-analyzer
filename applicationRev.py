#Last modified on 8/13/19 by Sammy Conrad-Rooney
#Designed to work with 1000 samples per second at 1 inch per minute

from tkinter import *
import csv
import glob
import os

def calculateResults():
    #Calculates most recent file
    #path = '../../../data' #use for exe application (not actually needed)
    #path = '../data' #use for .py application (not actually needed)

    list_of_files = glob.glob('../../CSX/*.csv') # * means all if need specific format then *.csv USE FOR EXE APPLICATION 
    #list_of_files = glob.glob('../data/*.csv') #USE FOR .py APPLICATION 
    latest_file = max(list_of_files, key=os.path.getmtime) # Finds the most recent file **USE FOR EXE APPLICATION**
    print(latest_file)

    #latest_file = '../data/Kestra-Testing-Data/Frangible_385_2019-07-29_11-06-53.csv' #The .csv file being used (previously fileName)

    #the following converts the csv file into a list
    def toList(name):
        with open(name, 'r') as f:
            reader = csv.reader(f)
            completeList = list(reader)

        #listLen = len(completeList)
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

    while numDecreasing1 < 5000: #While the values haven't been decreasing for over 5000 entries (used to be 2000)
        if float(cleanList[count1]) > float(currentLargest1): #Set the largest value to the current value if the current value is larger than the previous largest value
            currentLargest1 = cleanList[count1]
            largestIndex1 = count1
            numDecreasing1 = 0
        elif cleanList[count1] < currentLargest1: #If the current value is less than the current largest value, add 1 to the decreasing counter
            numDecreasing1 += 1
        count1 += 1 #Increase the counter by 1 to go through the entire data set

    currentLowest = largestIndex1
    smallestIndex = 0 # Calculated lowest point
    numIncreasing = 0
    count3 = largestIndex1

    while numIncreasing < 2000: #While the values haven't been increasing for over 2000
        if float(cleanList[count3]) < float(currentLowest): #Set the smallest value to the current value if the current value is smaller than the previous largest value
            currentLowest = cleanList[count3]
            smallestIndex = count3
            numIncreasing = 0
        elif cleanList[count3] > currentLowest: #If the current value is less than the current largest value, add 1 to the decreasing counter
            numIncreasing += 1
        count3 += 1 #Increase the counter by 1 to go through the entire data set


    #print("First Hump:")
    #print(count1)
    #print("Largest Index: ",  largestIndex1)
    #print("Largest Value: ", currentLargest1)

    #The following finds the second hump
    currentLargest2 = 0
    largestIndex2 = 0
    numDecreasing2 = 0
    count2 = smallestIndex   # largestIndex1 + 4000 #Start at 4000 entries past the first hump to get past the decrease after the first hump

    while numDecreasing2 < 2000: #While the values haven't been decreasing for over 2000 entries
        if float(cleanList[count2]) > float(currentLargest2):
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
    return [latest_file, currentLargest1, lowPoint, currentLargest2]

#Widgets
window = Tk()
titleLabel = Label(window, relief = 'flat', width = 20)
nameLabel = Label(window, relief = 'groove', width = 28)
peak1Label = Label(window, relief = 'groove', width = 28)
valleyLabel = Label(window, relief = 'groove', width = 28)
peak2Label = Label(window, relief = 'groove', width = 28)
#peak1Check = Label(window, relief = 'groove', width = 2) # Box for displaying color for limit check for peak1
#valleyCheck = Label(window, relief = 'groove', width = 2) # Box for displaying color for limit check for the valley
#peak2Check = Label(window, relief = 'groove', width = 2) # Box for displaying color for limit check for peak2
spaceLabel = Label(window, relief = 'flat', width = 37)
calcButton = Button(window)
darkButton = Button(window)
#showLimits = Button(window) # A button for displaying the limit popup

#Geometry
titleLabel.grid(row = 1, column = 1, columnspan = 4)
nameLabel.grid(row = 3, column = 1, columnspan = 2)
peak1Label.grid(row = 4, column = 1, columnspan = 2)
valleyLabel.grid(row = 5, column = 1, columnspan = 2)
peak2Label.grid(row = 6, column = 1, columnspan = 2)
#peak1Check.grid(row = 4, column = 3) # Define location of the peak1 limit check color box
#valleyCheck.grid(row = 5, column = 3) # Define location of the valley limit check color box
#peak2Check.grid(row = 6, column = 3) # Define location of the peak2 limit check color box
spaceLabel.grid(row = 8, column = 1)
calcButton.grid(row = 9, column = 1)
#showLimits.grid(row = 9, column = 2) # Define location of the limit popup button
darkButton.grid(row=10, column=1, pady=(10, 5))

darkVar = False # A variable to store the boolean value of whether dark mode is selected or not

def configProp(): # A function to configure element properties (used for setting dark or light theme)
    if darkVar == True:
        bkgrnd = "#000000"
        textColor = "#ffffff"
        darkText = "Light Mode"
    else:
        bkgrnd = "#ffffff"
        textColor = "#000000"
        darkText = "Dark Mode"

    window.title("Frangible Results")
    titleLabel.configure(text = "Frangible Results", font = ("Arial", 14), bg = bkgrnd, fg = textColor)
    nameLabel.configure(text = "File Name", font = ("Arial", 12), bg = bkgrnd, fg = textColor, anchor="w")
    peak1Label.configure(text = "Peak-1: ", font = ("Arial", 12), bg = bkgrnd, fg = textColor, anchor="w")
    valleyLabel.configure(text = "Lowest: ", font = ("Arial", 12), bg = bkgrnd, fg = textColor, anchor="w")
    peak2Label.configure(text = "Peak-2: ", font = ("Arial", 12), bg = bkgrnd, fg = textColor, anchor="w")
    spaceLabel.configure(bg = bkgrnd, fg = textColor)
    calcButton.configure(text = "\n   Get Values   \n", font = ("Arial", 12), bg = "#d1d800")
    #showLimits.configure(text = "\nShow Limits\n", font = ("Arial", 12)) # Text properties of the limit popup button
    darkButton.configure(text = darkText, font=("Arial", 9), bg = textColor, fg = bkgrnd)
    window.configure(bg = bkgrnd)

configProp() # Call the configure properties function after definition to configure the default properties

def darkConfig(): # A function to toggle dark mode
    global darkVar
    if darkVar == False:
        darkVar = True
    elif darkVar == True:
        darkVar = False
    configProp()


#peakLowLimit = 0.75 #LOW LIMIT FOR PEAKS
#peakHighLimit = 1.75 #HIGH LIMIT FOR PEAKS
#valleyLowLimit = 0.12 #LOW LIMIT FOR valley
#valleyHighLimit = 0.50 #HIGH LIMIT FOR valley

#Function to add values to application labels and change colors of limit boxes
def getValues():
	resultList = calculateResults()
	nameLabel.configure(text = (str(resultList[0])[20:])) # latest_file is the name of the latest file
	peak1Label.configure(text = ("Peak 1: " + str(resultList[1]))) # currentLargest1 is the value of the first peak
	valleyLabel.configure(text = ("Lowest: " + str(resultList[2]))) # lowPoint is the value of the valley
	peak2Label.configure(text = ("Peak 2: " + str(resultList[3]))) # currentLargest2 is the value of the second peak
    
    # Conditional statements to adjust check colors

    #if (float(resultList[1]) >= peakLowLimit and float(resultList[1]) <= peakHighLimit):
		#peak1Check.configure(bg = "green")
	#else:
		#peak1Check.configure(bg = "red")
	#if (float(resultList[2]) >= valleyLowLimit and float(resultList[2]) <= valleyHighLimit):
		#valleyCheck.configure(bg = "green")
	#else:
		#valleyCheck.configure(bg = "red")
	#if (float(resultList[3]) >= peakLowLimit and float(resultList[3]) <= peakHighLimit):
		#peak2Check.configure(bg = "green")
	#else:
		#peak2Check.configure(bg = "red")


#Function to create a popup message with limits
'''
def limitPopup():
    popup = Tk()
    popup.wm_title("Limits")
    label = Label(popup, text=("Peak Low Limit: " + str(peakLowLimit) + "\nPeak High Limit: " + str(peakHighLimit) +"\n\nValley Low Limit: " + str(valleyLowLimit) + "\nValley High Limit: " + str(valleyHighLimit)), font = ("Arial", 12))
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Hide", command = popup.destroy, font = ("Arial", 12))
    B1.pack()
    popup.mainloop()
'''

calcButton.configure(command = getValues)
#showLimits.configure(command = limitPopup) # Attaches limitPopup function to showLimits button
darkButton.configure(command = darkConfig)

#Sustain window
window.mainloop()
