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

#label
colOne = Label(window, text="List of Downloadable items")
colOne.grid(column=0, row=0, ipadx=20)

#list
downloadableItems = Listbox(window)
downloadableItems.grid(column=0, row=1)

#setup the second column, which will allow the user to input an item to be requested

#label
colTwo = Label(window, text="Request an Item")
colTwo.grid(column=1, row=0, ipadx=20)



#textbox
entryBox = Entry(window, width=30)
entryBox.grid(column=1, row=1, ipadx=20)
entryBox.bind('<Return>', requested)

#type
typeBox = Combobox(window)
typeBox['values'] = ("URL","search","youtube","ipfs")
typeBox.current(1)
typeBox.grid(column=1, row=2, ipadx=20)

#button


requestButton = Button(window, text="Request")
requestButton.bind('<Button-1>', requested)
requestButton.grid(column=1, row=3, ipadx=20)



#setup the third column, which will have the list of the items requested shown

#label
colThree = Label(window, text="List of Requested items")
colThree.grid(column=2, row=0, ipadx=20)

#list
requestedItems = Listbox(window)
requestedItems.grid(column=2, row=1)
requestedItems.bind('<Delete>', removeRequest)


window.mainloop()
