from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import DataManagement

window = Tk()
window.title("ORE-PACKAGERS")
window.geometry('700x600')


RequestListLength = 0;
DownloadableListLength = 0;


#downloadable function to be called by command and control
def downloadable(item):
    global DownloadableListLength
    downloadableItems.insert(DownloadableListLength, item)
    DownloadableListLength += 1

#gets the lists of items for the user to see from the database
def getListsFromDatabase(RequestList, DownloadableList):
    global DownloadableListLength
    global RequestListLength

    #fills the requested items list
    for item in RequestList:
        requestedItems.insert(RequestListLength, item)
        RequestListLength+=1

    #fills the downloadable items list
    for item in DownloadableList:
        downloadableItems.insert(DownloadableListLength, item)
        DownloadableListLength += 1

#requested Function
def requested(event):
    global RequestListLength
    requestedItems.insert(RequestListLength, entryBox.get())
    RequestListLength+=1

    #user is currently None because the object hasn't been created yet
    DataManagement.add_request(typeBox.current(), entryBox.get(), None)
    
    messagebox.showinfo("", "request for \n" + entryBox.get() + " \nhas been sent.")
    entryBox.delete(0,END)

#removes the selected request from the list
def removeRequest(event):
    global RequestListLength

    requestedItems.delete(requestedItems.curselection()[0])
    RequestListLength -= 1

#removes a given item from the downloadable list
#this should probably not be able to be called by the user, but by an admin or somthing
def removeDownloadableContent(item):
    global DownloadableListLength

    downloadableItems.delete(item)
    DownloadableListLength -= 1


#setup the first column, which will show the items that the
#system already has, that can be downloaded

mainFrame = Frame(window)
mainFrame.pack(expand=True, fill= BOTH)

#label
leftFrame = Frame(mainFrame)
leftFrame.pack(side=LEFT, padx = 20, fill = Y)
colOne = Label(leftFrame, text="List of Downloadable items")
colOne.pack(side=TOP)

#list
downloadableItems = Listbox(leftFrame)
downloadableItems.pack(fill = Y, expand = True, pady = 10)

#setup the second column, which will allow the user to input an item to be requested
middleFrame = Frame(mainFrame)
middleFrame.pack(side=LEFT, padx = 20, fill = Y, expand = True)
#label
colTwo = Label(middleFrame, text="Request an Item")
colTwo.pack(pady = 20)



#textbox
entryBox = Entry(middleFrame, width=30)
entryBox.pack(pady=5)
entryBox.bind('<Return>', requested)

#type
typeBox = Combobox(middleFrame)
typeBox['values'] = ("URL","search","youtube","ipfs")
typeBox.current(1)
typeBox.pack()

#button


requestButton = Button(middleFrame, text="Request")
requestButton.bind('<Button-1>', requested)
requestButton.pack(pady=5)



#setup the third column, which will have the list of the items requested shown
rightFrame = Frame(mainFrame)
rightFrame.pack(side=RIGHT, padx = 20, fill = Y)
#label
colThree = Label(rightFrame, text="List of Requested items")
colThree.pack()

#list
requestedItems = Listbox(rightFrame)
requestedItems.pack(fill = Y, expand = True, pady = 10)
requestedItems.bind('<Delete>', removeRequest)


window.mainloop()
