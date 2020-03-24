#Library imports
import tkinter
import requests
import time
import re
import os
import _tkinter
from docx import Document
from docx.shared import Inches
from tkinter import ttk

listOfWatchedFilms = []    #Value will be used for storing films for the watched list
listCastList = []          #Value will be used for storing the cast list of a given film
listFullCircle = []        #Value will be used for storing the list used for Full Circle

#Function for enabling the Opening Line field
def enableOpeningLineEntryFunc():
    openingLineEntry.configure(state="normal")    #Sets the entry field to normal, or enabled
    openingLineEntry.update()                     #Update the status of the entry field

#Function for disabling the Opening Line field
def disableOpeningLineEntryFunc():
    openingLineEntry.configure(state="disabled")    #Sets the entry field to disabled
    openingLineEntry.update()                       #Update the status of the entry field

#Function for enabling the Plot fields
def enablePlotEntryFunc():
    firstFilmPlotEntry.configure(state="normal")     #Sets the entry field to normal, or enabled
    firstFilmPlotEntry.update()                      #Update the status of the entry field
    secondFilmPlotEntry.configure(state="normal")    #Sets the entry field to normal, or enabled
    secondFilmPlotEntry.update()                     #Update the status of the entry field

#Function for disabling the Plot fields
def disablePlotEntryFunc():
    firstFilmPlotEntry.configure(state="disabled")     #Sets the entry field to disabled
    firstFilmPlotEntry.update()                        #Update the status of the entry field
    secondFilmPlotEntry.configure(state="disabled")    #Sets the entry field to disabled
    secondFilmPlotEntry.update()                       #Update the status of the entry field

#Function for adding in films to the watch list
def addToWatchListFunc():
    filmToAdd = filmWatchedEntry.get()      #Grab the film placed into the filmWatchedEntry field
    listOfWatchedFilms.append(filmToAdd)    #Append this film to the list of watched films
    filmWatchedEntry.delete(0, 'end')       #Empty out the filmWatchedEntry field

#Function for obtaining a films cast list and formatting it
def castListFunc(filmTitle, filmYear):
    filmCastList = []         #Dynamic list used to hold cast members of entered film
    finalFilmCastList = []    #Dynamic list used to hold cast members with added format for output
    filmCharacter = ""        #Variable for storing the character that a given actor played

    #The film title without excess space and non-alphanumeric characters
    reducedFilmTitle = re.sub('[^A-Za-z0-9]+', '', filmTitle)

    #Provided API Key that allows me to call TMDb
    apikey = "ef9bd486181321a8c5dbd8d87432ecaf"

    #Generated URL that allows us to grab the id of the movie provided by user input
    filmID_URL = "https://api.themoviedb.org/3/search/movie?api_key=" + apikey + "&query=" + filmTitle + "&year=" + filmYear

    #Takes the provided JSON and stores it into a new variable
    userResponse = requests.get(filmID_URL)
    IDGrab = userResponse.json()

    #Grabs the film ID of the film requested by the user
    for x in IDGrab['results']:
        if str(x['release_date'][0:4]) == filmYear and str(x['title']) == filmTitle:
            filmID = str(x['id'])

    #API call that grabs the cast of the movie provided by user input, the call is accomplished with the film ID
    filmCastURL = "https://api.themoviedb.org/3/movie/" + filmID + "/credits?api_key=" + apikey

    #Take the JSON-ed cast and convert it into something easily readable for Python code
    castResponse = requests.get(filmCastURL)
    filmCastGrab = castResponse.json()

    #Store each cast member of the user's film into the dynamic list
    for x in filmCastGrab['cast']:
        filmCastList.append(x['name'])

    #Goes through every actor/actress in the film and pulls the character they played
    for x in set(filmCastList):
        actorURL = "http://api.tmdb.org/3/search/person?api_key=" + apikey + "&query=" + x

        #Take the JSON-ed actors and convert it into something easily readable for Python code
        actorResponse = requests.get(actorURL)
        actorGrab = actorResponse.json()

        #Hokey, don't replicate. This pulls the first ID present and then exits the loop
        for y in actorGrab['results']:
            actorID = str(y['id'])
            break

        #Obtain the URL for the characters played by the given actor/actress
        characterURL = "https://api.themoviedb.org/3/person/" + actorID + "/movie_credits?api_key=" + apikey

        #Take the JSON-ed characters and convert it into something easily readable for Python code
        characterResponse = requests.get(characterURL)
        characterGrab = characterResponse.json()

        #For every cast tag in the character list, find the one that matches the film title/release date passed in
        for y in characterGrab['cast']:
            if re.sub('[^A-Za-z0-9]+', '', y['title']) == reducedFilmTitle and str(y['release_date'][0:4]) == filmYear:
                filmCharacter = y['character']

        #If empty string, replace with error message. To be properly handled/fixed in the future
        if filmCharacter == "":
            filmCharacter = "**UNABLE TO PULL CHARACTER DATA**"
        
        #Add a formatted cast message to the cast list that will be returned at the end of the function
        finalFilmCastList.append(x + " plays " + filmCharacter + " in " + filmTitle + " (" + filmYear + ")")

        filmCharacter = ""    #Set the film character string back to empty

    return(finalFilmCastList)    #Return the cast list of the film that was passed in

#Function for obtaining Full Circle instances between the passed in film and previously covered films on the show
def fullCircleFunc(firstFilmTitle, firstFilmYear):
    firstFilmCastList = []       #Dynamic list used to hold cast members of entered film
    comparedFilmCastList = []    #Dynamic list used to hold cast members of film compared with cast of firstFilmCastList
    finalActorList = []          #Final list to hold all actors/actresses that fit the requirements
    comparedFilmTitle = ""       #Placeholder variable for the read-in film's title
    comparedFilmYear = ""        #Placeholder variable for the read-in film's year
    iterator = 0                 #Incremental variable for while loop below
    firstCharacter = ""          #First stored character role from the list intersection
    secondCharacter = ""         #Second stored character role from the list intersection

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
    filmListIn = open("../textFiles/theyRemadeItList.txt", "r")
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

            #Convert the JSON from the call into a usable actor/actress
            actorResponse = requests.get(actorURL)
            actorGrab = actorResponse.json()

            #Grab the first actor/actress ID and then break
            for y in actorGrab['results']:
                actorID = str(y['id'])
                break

            #API call to grab character data based on the actor/actress
            characterURL = "https://api.themoviedb.org/3/person/" + actorID + "/movie_credits?api_key=" + apikey

            #Convert the JSON from the call into a usable character
            characterResponse = requests.get(characterURL)
            characterGrab = characterResponse.json()

            #For every actor in the list, grab both the characters that the actor played that warrant inclusion in Full Circle
            for y in characterGrab['cast']:
                if re.sub('[^A-Za-z0-9]+', '', y['title']) == reducedFilmTitle and str(y['release_date'][0:4]) == firstFilmYear:
                    firstCharacter = y['character']
                if re.sub('[^A-Za-z0-9]+', '', y['title']) == re.sub('[^A-Za-z0-9]+', '', comparedFilmTitle) and str(y['release_date'][0:4]) == comparedFilmYear:
                    secondCharacter = y['character']

            #Hokey, don't replicate. Will be fixed later. For both characters, if the string is empty add this error message
            if firstCharacter == "":
                firstCharacter = "**UNABLE TO PULL CHARACTER DATA**"
            if secondCharacter == "":
                secondCharacter = "**UNABLE TO PULL CHARACTER DATA**"
            
            #Formatting message for the Full Circle final output
            finalActorList.append(x + " plays " + firstCharacter + " in " + firstFilmTitle + " (" + firstFilmYear + ") and plays " + secondCharacter + " in " + comparedFilmTitle + "(" + comparedFilmYear + ")")

            firstCharacter = ""     #Set the first film character string back to empty
            secondCharacter = ""    #Set the second film character string back to empty

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

    return(finalActorList)    #Return the list of Full Circle cases

#Function for creating the show notes document
def theyRemadeItFunc():
    document = Document()    #Initialize the document

    #If the OpenLineRadio button is set to enabled, add in the Opening Line section of the notes
    if openLineRadio.get() == 0:
        document.add_heading('Opening Line:', 1)
        document.add_paragraph(openingLineEntry.get())
    
    #Add in the header for the What I've Been Watching section of the notes
    document.add_heading('What I\'ve Been Watching:', 1)

    #For every item in the watched films list, add the item to the document under the What I've Been Watching section of the notes
    for y in listOfWatchedFilms:
        if y != "":
            document.add_paragraph(y)

    #Add in the header for the first Cast List section of the notes
    document.add_heading(firstFilmTitleEntry.get() + ' (' + firstFilmYearEntry.get() + ')' + ' Cast List:', 1)
    listCastList = castListFunc(firstFilmTitleEntry.get(), firstFilmYearEntry.get())    #Set the returned list to the listCastList list
    
    #For every item in the cast list, add the item under the first Cast List section of the notes
    for y in listCastList:
        if y != "":
            document.add_paragraph(y)
    
    #Add in the header for the second Cast List section of the notes
    document.add_heading(secondFilmTitleEntry.get() + ' (' + secondFilmYearEntry.get() + ')' + ' Cast List:', 1)
    listCastList = castListFunc(secondFilmTitleEntry.get(), secondFilmYearEntry.get())    #Set the returned list to the listCastList list
    
    #For every item in the cast list, add the item under the second Cast List section of the notes
    for y in listCastList:
        if y != "":
            document.add_paragraph(y)

    #Add in the header for the Full Circle section of the notes
    document.add_heading('Full Circle:', 1)
    listFullCircle = fullCircleFunc(firstFilmTitleEntry.get(), firstFilmYearEntry.get())    #Run the Full Circle function for the first film

    #For every item in the full circle list, add the item under the Full Circle section of the notes
    for y in listFullCircle:
        if y != "":
            document.add_paragraph(y)

    listFullCircle = fullCircleFunc(secondFilmTitleEntry.get(), secondFilmYearEntry.get())    #Run the Full Circle function for the second film

    #For every item in the full circle list, add the item under the Full Circle section of the notes
    for y in listFullCircle:
        if y != "":
            document.add_paragraph(y)

    #If the plotRadio button is enabled, then add in sections for the plots of both films
    if plotRadio.get() == 0:
        document.add_heading(firstFilmTitleEntry.get() + ' (' + firstFilmYearEntry.get() + ')' + ' Plot:', 1)
        document.add_paragraph(firstFilmPlotEntry.get())
        document.add_page_break()    #Add in a page break between plots (as they can get rather large)
        document.add_heading(secondFilmTitleEntry.get() + ' (' + secondFilmYearEntry.get() + ')' + ' Plot:', 1)
        document.add_paragraph(secondFilmPlotEntry.get())

    #Store proposed file title into string var
    titleOfFile = firstFilmTitleEntry.get() + ' ' + firstFilmYearEntry.get() + '.docx'

    #Save off the document under the freshly created title
    document.save(titleOfFile)

    #Print out the file that you just created
    #os.startfile(titleOfFile, "print")

#Application Window
master = tkinter.Tk()               #Initialization of the application
openLineRadio = tkinter.IntVar()    #Initialization of the Opening Line enable radio button
plotRadio = tkinter.IntVar()        #Initialization of the Plot enable radio button
master.title("They Remade It")      #Application title
master.geometry("1080x720")         #Application size

masterStyle = ttk.Style()                               #Intitialize a Style variable for the application's layout control
masterStyle.configure('TNotebook', tabposition='ne')    #'ne' positions tabs to the NorthEast of the application

tabControl = ttk.Notebook(master)    #Initialize the tabs

tab1 = ttk.Frame(tabControl)                           #Frame for tab 1
tab2 = ttk.Frame(tabControl)                           #Frame for tab 2
tab3 = ttk.Frame(tabControl)                           #Frame for tab 3
tab4 = ttk.Frame(tabControl)                           #Frame for tab 4
tab5 = ttk.Frame(tabControl)                           #Frame for tab 5
tabControl.add(tab1, text='Movies Being Discussed')    #Addition of Movies Being Discussed tab
tabControl.add(tab2, text='Opening Line')              #Addition of Opening Line tab
tabControl.add(tab3, text='Movies Watched')            #Addition of Movies Watched tab
tabControl.add(tab4, text='Movie Plots')               #Addition of Movie Plots tab
tabControl.add(tab5, text='Finish Up')                 #Addition of Finish Up tab
tabControl.pack(expand=1, fill="both")                 #The "pack" makes the tabs visible in the application

tkinter.Label(tab1, text="First Film Title").grid(row=0, column=0)     #Label for the First Film Title text entry field
tkinter.Label(tab1, text="First Film Year").grid(row=1, column=0)      #Label for the First Film Year text entry field
tkinter.Label(tab1, text="Second Film Title").grid(row=2, column=0)    #Label for the Second Film Title text entry field
tkinter.Label(tab1, text="Second Film Year").grid(row=3, column=0)     #Label for the Second Film Year text entry field
tkinter.Label(tab2, text="Opening Title").grid(row=0)                  #Label for the Opening Title text entry field
tkinter.Label(tab3, text="Film Watched").grid(row=0, column=0)         #Label for the Film Watched text entry field
tkinter.Label(tab4, text="First Film Plot").grid(row=0, column=0)      #Label for the First Film Plot text entry field
tkinter.Label(tab4, text="Second Film Plot").grid(row=1, column=0)     #Label for the Second Film Plot text entry field

firstFilmTitleEntry = tkinter.Entry(tab1)     #Text entry field for the First Film Title
firstFilmYearEntry = tkinter.Entry(tab1)      #Text entry field for the First Film Year
secondFilmTitleEntry = tkinter.Entry(tab1)    #Text entry field for the Second Film Title
secondFilmYearEntry = tkinter.Entry(tab1)     #Text entry field for the Second Film Year
openingLineEntry = tkinter.Entry(tab2)        #Text entry field for the Opening Title
filmWatchedEntry = tkinter.Entry(tab3)        #Text entry field for Film Watched
firstFilmPlotEntry = tkinter.Entry(tab4)      #Text entry field for the First Film Plot
secondFilmPlotEntry = tkinter.Entry(tab4)     #Text entry field for the Second Film Plot

openingLineEntry.grid(row=0, column=1)        #Placement for the Opening Title text entry field
filmWatchedEntry.grid(row=0, column=1)        #Placement for the Film Watched text entry field
firstFilmTitleEntry.grid(row=0, column=1)     #Placement for the First Film Title text entry field
firstFilmYearEntry.grid(row=1, column=1)      #Placement for the First Film Year text entry field
secondFilmTitleEntry.grid(row=2, column=1)    #Placement for the Second Film Title text entry field
secondFilmYearEntry.grid(row=3, column=1)     #Placement for the Second Film Year text entry field
firstFilmPlotEntry.grid(row=0, column=1)      #Placement for the First Film Plot text entry field
secondFilmPlotEntry.grid(row=1, column=1)     #Placement for the Second Film Plot text entry field

#Setting up the enable button for the Opening Line Widget
enableOpeningLineEntry = tkinter.Radiobutton(tab2, text="Enable", variable=openLineRadio, value="0", command=enableOpeningLineEntryFunc)
enableOpeningLineEntry.grid(row=2, column=0)    #Placement for the Opening Line enable button

#Setting up the disable button for the Opening Line Widget
disableOpeningLineEntry = tkinter.Radiobutton(tab2, text="Disable", variable=openLineRadio, value="1", command=disableOpeningLineEntryFunc)
disableOpeningLineEntry.grid(row=2, column=1)    #Placement for the Opening Line disable button

#Setting up the enable button for the Plot Widget
enablePlotEntry = tkinter.Radiobutton(tab4, text="Enable", variable=plotRadio, value="0", command=enablePlotEntryFunc)
enablePlotEntry.grid(row=2, column=0)    #Placement for the Plot enable button

#Setting up the disable button for the Plot Widget
disablePlotEntry = tkinter.Radiobutton(tab4, text="Disable", variable=plotRadio, value="1", command=disablePlotEntryFunc)
disablePlotEntry.grid(row=2, column=1)    #Placement for the Plot disable button

#Setting up the Add Film button, for putting films into the Watched list
tkinter.Button(tab3, text='Add Film', command=addToWatchListFunc).grid(row=2, column=0, sticky=tkinter.W, pady=4)

#Setting up the Submit button for creating the show notes doc
tkinter.Button(tab5, text='Submit', command=theyRemadeItFunc).grid(row=2, column=0, sticky=tkinter.W, pady=4)

master.mainloop()    #Keeps the Application open until the user closes it