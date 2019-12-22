#Import libraries responsible for functionality
import sys
import json
import requests
import time
import numpy
import re
import os
import tkinter
import _tkinter
from tkinter import ttk

def fullCircleFunction():
    firstFilmCastList = []       #Dynamic list used to hold cast members of entered film
    comparedFilmCastList = []    #Dynamic list used to hold cast members of film compared with cast of firstFilmCastList
    finalActorList = []          #Final list to hold all actors/actresses that fit the requirements
    comparedFilmTitle = ""       #Placeholder variable for the read-in film's title
    comparedFilmYear = ""        #Placeholder variable for the read-in film's year
    iterator = 0                 #Incremental variable for while loop below
    firstCharacter = ""          #First stored character role from the list intersection
    secondCharacter = ""         #Second stored character role from the list intersection
    addToFile = False            #Variable to determine whether the film input by the user should be added to the test file
    fileTitle = ""

    firstFilmTitle = e1.get()
    firstFilmYear = e2.get()
    fileResponse = radioAddValue.get()

    #If the title/year are being saved, change the boolean value to True
    if fileResponse == 1:
        addToFile = True

    #The first film title without excess space and non-alphanumeric characters
    reducedFilmTitle = re.sub('[^A-Za-z0-9]+', '', firstFilmTitle)

    #Provided API Key that allows me to call TMDb
    apikey = "ef9bd486181321a8c5dbd8d87432ecaf"

    #First generated URL that allows us to grab the id of the movie provided by user input
    firstFilmID_URL = "https://api.themoviedb.org/3/search/movie?api_key=" + apikey + "&query=" + firstFilmTitle + "&year=" + firstFilmYear

    #Takes the provided JSON and stores it into a new variable
    userResponse = requests.get(firstFilmID_URL)
    IDGrab = userResponse.json()

    #Grabs the film ID of the film requested by the user
    for x in IDGrab['results']:
        if str(x['release_date'][0:4]) == firstFilmYear and str(x['title']) == firstFilmTitle:
            firstFilmID = str(x['id'])

    #API call that grabs the cast of the movie provided by user input, the call is accomplished with the film ID
    firstFilmCastURL = "https://api.themoviedb.org/3/movie/" + firstFilmID + "/credits?api_key=" + apikey

    #Take the JSON-ed cast and convert it into something easily readable for Python code
    castResponse = requests.get(firstFilmCastURL)
    firstFilmCastGrab = castResponse.json()

    #Store each cast member of the user's film into the dynamic list
    for x in firstFilmCastGrab['cast']:
        firstFilmCastList.append(x['name'])

    #Open up and read in the text file with all of the films covered by the They Remade It podcast
    filmListIn = open("theyRemadeItList.txt", "r")
    filmCompareList = filmListIn.read().splitlines()

    #So, while the incremented variable is less than the length of the text file, this while loop will run through and make an API call for each
    #film in the text file, grab it's ID, make a call with the ID to grab the cast list of the film, compare the cast with that of the movie provided
    #through user input, and store any actors/actresses that show up in both into a new dynamic list
    while iterator < len(filmCompareList):
        comparedFilmTitle = filmCompareList[iterator][0:len(filmCompareList[iterator])-4]
        comparedFilmYear = filmCompareList[iterator][len(filmCompareList[iterator])-4:len(filmCompareList[iterator])]

        #The URL for the film being compared to the original entry
        filmCompareURL = "https://api.themoviedb.org/3/search/movie?api_key=" + apikey + "&query=" + comparedFilmTitle + "&year=" + comparedFilmYear

        #Convert the JSON from the call into a usable film ID
        compareResponse = requests.get(filmCompareURL)
        compareGrab = compareResponse.json()

        #Used to grab the film ID listed in the pull request
        for x in compareGrab['results']:
            if str(x['release_date'][0:4]) == comparedFilmYear:
                filmCompareID = str(x['id'])

        #API call using the ID to obtain the cast list from film listed in the text file
        castCompareURL = "https://api.themoviedb.org/3/movie/" + filmCompareID + "/credits?api_key=" + apikey

        #Converts JSON in Python readable format
        compareCastResponse = requests.get(castCompareURL)
        compareCastGrab = compareCastResponse.json()

        #Places entire cast list of film from text file into a dynamic list
        for x in compareCastGrab['cast']:
            comparedFilmCastList.append(x['name'])

        #Goes through and grabs the name of the role that the actor/actress portrayed in the film. Only lists one if they have multiple in the same movie
        #It then makes a line for the new text file and puts it into a string array
        for x in set(firstFilmCastList).intersection(comparedFilmCastList):
            actorURL = "http://api.tmdb.org/3/search/person?api_key=" + apikey + "&query=" + x

            actorResponse = requests.get(actorURL)
            actorGrab = actorResponse.json()

            for y in actorGrab['results']:
                actorID = str(y['id'])
                break

            characterURL = "https://api.themoviedb.org/3/person/" + actorID + "/movie_credits?api_key=" + apikey

            characterResponse = requests.get(characterURL)
            characterGrab = characterResponse.json()

            for y in characterGrab['cast']:
                if re.sub('[^A-Za-z0-9]+', '', y['title']) == reducedFilmTitle and str(y['release_date'][0:4]) == firstFilmYear:
                    firstCharacter = y['character']
                if re.sub('[^A-Za-z0-9]+', '', y['title']) == re.sub('[^A-Za-z0-9]+', '', comparedFilmTitle) and str(y['release_date'][0:4]) == comparedFilmYear:
                    secondCharacter = y['character']

            if firstCharacter == "":
                firstCharacter = "**UNABLE TO PULL CHARACTER DATA**"
            if secondCharacter == "":
                secondCharacter = "**UNABLE TO PULL CHARACTER DATA**"
            
            finalActorList.append(x + " plays " + firstCharacter + " in " + firstFilmTitle + " (" + firstFilmYear + ") and plays " + secondCharacter + " in " + comparedFilmTitle + "(" + comparedFilmYear + ")")

            firstCharacter = ""
            secondCharacter = ""

        #Clears out the compare array for the next go around
        comparedFilmCastList.clear()

        #Prevents the while loop from stepping past the length of the file and crashing/ending prematurely
        if iterator + 1 > len(filmCompareList):
            break
        else:
            iterator = iterator + 1

        #Used to reduce the amount of API calls the program makes (otherwise the program might crash)
        time.sleep(0.125)

    #Sort the list of actors//actresses alphabetically
    finalActorList.sort()

    #For every value between 0 and the length of the list, this section of code will compare the first sections (with actor name and user's film)
    #of different sections of the list and will condense those attributed to the same actor in order to make things more readable
    for y in range(0, len(finalActorList)):
        if finalActorList[y] != "":
            for z in range (y + 1, len(finalActorList)):
                if finalActorList[y][0:finalActorList[y].index("and plays")] == finalActorList[z][0:finalActorList[z].index("and plays")]:
                    finalActorList[y] = finalActorList[y] + " " + finalActorList[z][finalActorList[z].index("and plays"):len(finalActorList[z])]
                    finalActorList[z] = ""

    fileTitle = reducedFilmTitle + firstFilmYear + '.txt'

    #Writes every line from the string array into the new text file
    with open(fileTitle, 'w') as finalOut:
        for y in finalActorList:
            if y != "":
                finalOut.write(y)
                finalOut.write("\n")
    if addToFile == True:
        with open("theyRemadeItList.txt", 'a') as addToFile:
            addToFile.write("\n")
            addToFile.write(firstFilmTitle + " " + firstFilmYear)
            addToFile.close()

    #Close the theyRemadeIt text file to prevent memory leak
    filmListIn.close()
    finalOut.close()

    os.startfile(fileTitle)

master = tkinter.Tk()
radioAddValue = tkinter.IntVar()
master.title("Full Circle")
master.geometry("500x280")

tabControl = ttk.Notebook(master)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Full Circle')
tabControl.add(tab2, text='Cast List')
tabControl.pack(expand=1, fill="both")

tkinter.Label(tab1, text="Film Title").grid(row=0)
tkinter.Label(tab1, text="Film Year").grid(row=1)
tkinter.Radiobutton(tab1, text="Add to List (YES)", variable=radioAddValue, value=1).grid(row=2, column=0)
tkinter.Radiobutton(tab1, text="Add to List (NO)", variable=radioAddValue, value=2).grid(row=2, column=1)

e1 = tkinter.Entry(tab1)
e2 = tkinter.Entry(tab1)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

tkinter.Button(tab1, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tkinter.W, pady=4)
tkinter.Button(tab1, text='Show', command=fullCircleFunction).grid(row=3, column=1, sticky=tkinter.W, pady=4)

master.mainloop()