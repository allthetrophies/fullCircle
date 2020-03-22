#Library imports
import tkinter
import _tkinter
from docx import Document
from docx.shared import Inches
from tkinter import ttk

listOfWatchedFilms = []                                               #Value will be used for storing films for the watched list

#Function for enabling the Opening Line field
def enableOpeningLineEntryFunc():
    openingLineEntry.configure(state="normal")                        #Sets the entry field to normal, or enabled
    openingLineEntry.update()                                         #Update the status of the entry field

#Function for disabling the Opening Line field
def disableOpeningLineEntryFunc():
    openingLineEntry.configure(state="disabled")                      #Sets the entry field to disabled
    openingLineEntry.update()                                         #Update the status of the entry field

#Function for enabling the Plot fields
def enablePlotEntryFunc():
    firstFilmPlotEntry.configure(state="normal")                      #Sets the entry field to normal, or enabled
    firstFilmPlotEntry.update()                                       #Update the status of the entry field
    secondFilmPlotEntry.configure(state="normal")                     #Sets the entry field to normal, or enabled
    secondFilmPlotEntry.update()                                      #Update the status of the entry field

#Function for disabling the Plot fields
def disablePlotEntryFunc():
    firstFilmPlotEntry.configure(state="disabled")                    #Sets the entry field to disabled
    firstFilmPlotEntry.update()                                       #Update the status of the entry field
    secondFilmPlotEntry.configure(state="disabled")                   #Sets the entry field to disabled
    secondFilmPlotEntry.update()                                      #Update the status of the entry field

def addToWatchListFunc():
    filmToAdd = filmWatchedEntry.get()
    listOfWatchedFilms.append(filmToAdd)
    filmWatchedEntry.delete(0, 'end')

def theyRemadeItFunc():
    document = Document()

    if openLineRadio.get() == 0:
        document.add_heading('Opening Line:', 1)
        document.add_paragraph(openingLineEntry.get())
    
    document.add_heading('What I\'ve Been Watching:', 1)
    document.add_paragraph(listOfWatchedFilms)

    document.add_heading(firstFilmTitleEntry.get() + ' (' + firstFilmYearEntry.get() + ')' + ' Cast List:', 1)
    document.add_heading(secondFilmTitleEntry.get() + ' (' + secondFilmYearEntry.get() + ')' + ' Cast List:', 1)

    document.add_heading('Full Circle:', 1)

    if plotRadio.get() == 0:
        document.add_heading(firstFilmTitleEntry.get() + ' (' + firstFilmYearEntry.get() + ')' + ' Plot:', 1)
        document.add_paragraph(firstFilmPlotEntry.get())
        document.add_page_break()
        document.add_heading(secondFilmTitleEntry.get() + ' (' + secondFilmYearEntry.get() + ')' + ' Plot:', 1)
        document.add_paragraph(secondFilmPlotEntry.get())

    document.save(firstFilmTitleEntry.get() + ' ' + firstFilmYearEntry.get() + '.docx')

#Application Window
master = tkinter.Tk()                                                 #Initialization of the application
openLineRadio = tkinter.IntVar()                                      #Initialization of the Opening Line enable radio button
plotRadio = tkinter.IntVar()                                          #Initialization of the Plot enable radio button
master.title("They Remade It")                                        #Application title
master.geometry("1080x720")                                           #Application size

masterStyle = ttk.Style()                                             #Intitialize a Style variable for the application's layout control
masterStyle.configure('TNotebook', tabposition='ne')                  #'ne' positions tabs to the NorthEast of the application

tabControl = ttk.Notebook(master)                                     #Initialize the tabs

tab1 = ttk.Frame(tabControl)                                          #Frame for tab 1
tab2 = ttk.Frame(tabControl)                                          #Frame for tab 2
tab3 = ttk.Frame(tabControl)                                          #Frame for tab 3
tab4 = ttk.Frame(tabControl)                                          #Frame for tab 4
tab5 = ttk.Frame(tabControl)                                          #Frame for tab 5
tabControl.add(tab1, text='Opening Line')                             #Addition of Opening Line tab
tabControl.add(tab2, text='Movies Watched')                           #Addition of Movies Watched tab
tabControl.add(tab3, text='Movies Being Discussed')                   #Addition of Movies Being Discussed tab
tabControl.add(tab4, text='Movie Plots')                              #Addition of Movie Plots tab
tabControl.add(tab5, text='Finish Up')                                #Addition of Finish Up tab
tabControl.pack(expand=1, fill="both")                                #The "pack" makes the tabs visible in the application

tkinter.Label(tab1, text="Opening Title").grid(row=0)                 #Label for the Opening Title text entry field
tkinter.Label(tab2, text="Film Watched").grid(row=0, column=0)        #Label for the Film Watched text entry field
tkinter.Label(tab3, text="First Film Title").grid(row=0, column=0)    #Label for the First Film Title text entry field
tkinter.Label(tab3, text="First Film Year").grid(row=1, column=0)     #Label for the First Film Year text entry field
tkinter.Label(tab3, text="Second Film Title").grid(row=2, column=0)   #Label for the Second Film Title text entry field
tkinter.Label(tab3, text="Second Film Year").grid(row=3, column=0)    #Label for the Second Film Year text entry field
tkinter.Label(tab4, text="First Film Plot").grid(row=0, column=0)     #Label for the First Film Plot text entry field
tkinter.Label(tab4, text="Second Film Plot").grid(row=1, column=0)    #Label for the Second Film Plot text entry field

openingLineEntry = tkinter.Entry(tab1)                                #Text entry field for the Opening Title
filmWatchedEntry = tkinter.Entry(tab2)                                #Text entry field for Film Watched
firstFilmTitleEntry = tkinter.Entry(tab3)                             #Text entry field for the First Film Title
firstFilmYearEntry = tkinter.Entry(tab3)                              #Text entry field for the First Film Year
secondFilmTitleEntry = tkinter.Entry(tab3)                            #Text entry field for the Second Film Title
secondFilmYearEntry = tkinter.Entry(tab3)                             #Text entry field for the Second Film Year
firstFilmPlotEntry = tkinter.Entry(tab4)                              #Text entry field for the First Film Plot
secondFilmPlotEntry = tkinter.Entry(tab4)                             #Text entry field for the Second Film Plot

openingLineEntry.grid(row=0, column=1)                                #Placement for the Opening Title text entry field
filmWatchedEntry.grid(row=0, column=1)                                #Placement for the Film Watched text entry field
firstFilmTitleEntry.grid(row=0, column=1)                             #Placement for the First Film Title text entry field
firstFilmYearEntry.grid(row=1, column=1)                              #Placement for the First Film Year text entry field
secondFilmTitleEntry.grid(row=2, column=1)                            #Placement for the Second Film Title text entry field
secondFilmYearEntry.grid(row=3, column=1)                             #Placement for the Second Film Year text entry field
firstFilmPlotEntry.grid(row=0, column=1)                              #Placement for the First Film Plot text entry field
secondFilmPlotEntry.grid(row=1, column=1)                             #Placement for the Second Film Plot text entry field

#Setting up the enable button for the Opening Line Widget
enableOpeningLineEntry = tkinter.Radiobutton(tab1, text="Enable", variable=openLineRadio, value="0", command=enableOpeningLineEntryFunc)
enableOpeningLineEntry.grid(row=2, column=0)                          #Placement for the Opening Line enable button
#Setting up the disable button for the Opening Line Widget
disableOpeningLineEntry = tkinter.Radiobutton(tab1, text="Disable", variable=openLineRadio, value="1", command=disableOpeningLineEntryFunc)
disableOpeningLineEntry.grid(row=2, column=1)                         #Placement for the Opening Line disable button
#Setting up the enable button for the Plot Widget
enablePlotEntry = tkinter.Radiobutton(tab4, text="Enable", variable=plotRadio, value="0", command=enablePlotEntryFunc)
enablePlotEntry.grid(row=2, column=0)                                 #Placement for the Plot enable button
#Setting up the disable button for the Plot Widget
disablePlotEntry = tkinter.Radiobutton(tab4, text="Disable", variable=plotRadio, value="1", command=disablePlotEntryFunc)
disablePlotEntry.grid(row=2, column=1)                                #Placement for the Plot disable button

tkinter.Button(tab2, text='Add Film', command=addToWatchListFunc).grid(row=2, column=0, sticky=tkinter.W, pady=4)

tkinter.Button(tab5, text='Submit', command=theyRemadeItFunc).grid(row=2, column=0, sticky=tkinter.W, pady=4)

master.mainloop()                                                     #Keeps the Application open until the user closes it