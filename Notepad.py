# -*- coding: utf-8 -*-
"""

@author: KAJAL KAKADE
"""

'''
Notepad: 
    1. create new file
    2. save new file, save as
    3. Edit existing file- Cut, Copy, Paste, Find, Replace, Undo, Select All, Go to, Time/Date 
    4. open existing file
    5. Change Format- Word Wrap
    6. Close notepad
    7. Help - View help, About Notepad
    8. Find and replace feature
    
'''
# libraries
import tkinter 
import os     
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import tkinter.simpledialog as simpledialog
import datetime
import webbrowser
import tkinter.messagebox as messagebox
import textwrap
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import linecache


 
#--------------------------------------------------------------------------
#defining class notepad
class Notepad:
    
    #defining object of class TK().This creates a toplevel widget of Tk which usually is the main window of an application
    root = Tk()
    
    #initalizing default height and width of notepad
    Width = 800
    Height = 400
    
    #initializing default Text, Menu bar
    Text = Text(root, undo=True) 
    MenuBar = Menu(root) 
    FileMenu = Menu(MenuBar, tearoff=0) 
    EditMenu = Menu(MenuBar, tearoff=0)
    FormatMenu = Menu(MenuBar, tearoff=0)
    ViewMenu = Menu(MenuBar, tearoff=0)
    HelpMenu = Menu(MenuBar, tearoff=0) 

    #Creating  scrollbar object
    ScrollBar = Scrollbar(Text)
    file=None
    
    #Constructor
    def __init__(self,*args):
        
        
        #initialize notepad icon
        self.root.wm_iconbitmap('Notepad.ico')
              
        
        #Set window title. default is untitled
        self.root.title('Untitled')
        self.root.geometry('600x400')
        
        # To make the textarea auto resizable 
        self.root.grid_rowconfigure(0, weight=1) 
        self.root.grid_columnconfigure(0, weight=1) 
        
        #Add widgets- N,S,E,W use to align text in the grid
        self.Text.grid(sticky = N + E + S + W)
        
        #Create new file
        self.FileMenu.add_command(label='New     ctrl+N', command=self.newFile)
        
        #Open existing File
        self.FileMenu.add_command(label='Open    Ctrl+O', command=self.openFile)
        
        #Save file
        self.FileMenu.add_command(label='Save   Ctrl+S', command=self.saveFile)
        self.root.bind("<KeyPress>", self.event)
        
        #save as file
        self.FileMenu.add_command(label='Save as', command=self.saveAsFile)
        
        #Exit file
        self.FileMenu.add_command(label='Exit', command=self.exitFile)
        
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)
        
        #adding fetures in Edit tab
        
        #Create Undo file
        self.EditMenu.add_command(label='Undo     ctrl+Z', command=self.undoFile)
        
        #Cut File
        self.EditMenu.add_command(label='Cut    Ctrl+X', command=self.cutFile)
        
        #Copy file
        self.EditMenu.add_command(label='Copy   Ctrl+C', command=self.copyFile)
        
        #Paste file
        self.EditMenu.add_command(label='Paste  Ctrl+V', command=self.pasteFile)
        
        #Delete file
        self.EditMenu.add_command(label='Delete', command=self.deleteFile)
        
        #Find 
        self.EditMenu.add_command(label='Find     Ctrl+F', command=self.findFile)
        
        
        #Replace words
        self.EditMenu.add_command(label='Replace   Ctrl+H', command=self.replaceFile)
        
        #Go to word
        self.EditMenu.add_command(label='Go to  Ctrl+G', command=self.goToFile)
        
        #Select all
        self.EditMenu.add_command(label='Select All   Ctrl+A', command=self.selectAllFile)
        
        #time/Date
        self.EditMenu.add_command(label='Time/Date', command=self.timeDate)
        
        self.MenuBar.add_cascade(label="Edit", menu=self.EditMenu)
        
        
        # adding features in format tab
        
        self.FormatMenu.add_command(label='Word Wrap', command=self.wordWrapFile)
        
        
        self.MenuBar.add_cascade(label='Format', menu=self.FormatMenu)
        

        #adding features in help tab
        
        self.HelpMenu.add_command(label='View Help', command=self.helpFile)
        self.HelpMenu.add_command(label='About Notepad', command=self.aboutNotepad)
        self.MenuBar.add_cascade(label='Help', menu=self.HelpMenu)
        
        #add configurationof menu bar
        self.root.config(menu=self.MenuBar)
        
        #add scrollBar
#        1. pack- It is a geometry management instruction.The manager handles all widgets that are packed inside the same master widget
#                   you call pack to let Tkinter now that the widget is ready to be used
#        2. config- used to access an object's attributes after its initialisation
#        3. set method - When the widget view is modified, the widget notifies the scrollbar by calling the set method.
#        4. yview and xview - when the user manipulates the scrollbar, the widget’s yview or xview method is called with the appropriate arguments.
        
        #Creating  scrollbar object
#        self.ScrollBar = Scrollbar(self.Text)
        self.ScrollBar.config(command=Text.yview)
        self.Text.config(yscrollcommand=self.ScrollBar.set)
        self.ScrollBar.pack(side=RIGHT, fill=Y)
        
        
     
#    Functions:
        
#    Function for shortcut keys
    def event(self,e):
#        print(e)
        if e.state==12: 
            if e.keysym=='s':
                self.saveFile()
            if e.keysym=='n':
                self.newFile()
            if e.keysym=='o':
                self.openFile()
            if e.keysym=='c':
                self.copyFile()
            if e.keysym=='x':
                self.cutFile()
            if e.keysym=='v':
                self.pasteFile()
            if e.keysym=='a':
                self.selectAllFile()
            if e.keysym=='f':
                self.findFile()
            if e.keysym=='z':
                self.undoFile()
            if e.keysym=='g':
                self.goToFile()
            
                
 # function to create new file       
    def newFile(self):
        self.root.title("Untitled") 
        self.file = None
        self.Text.delete(1.0,END) # clear entire text
 
#FUNCTION TO OPEN A FILE       
    def openFile(self):
        self.file=askopenfilename(defaultextension=".txt", 
                                        filetypes=[("All Files","*.*"), 
                                            ("Text Documents","*.txt")])
        self.root.title(os.path.basename(self.file))
        file=open(self.file,'r')
        self.Text.insert(1.0,file.read())
        file.close()
        pass
 
#Function to save file
    def saveFile(self):
        #Saving as a new file
        if self.file==None:
            self.file=self.saveAsFile()
        else:
            file=open(self.file,'w')
            file.write(self.Text.get(1.0,END))
            file.close()
        
#Function to save as file    
    def saveAsFile(self):
        self.file=asksaveasfile(mode='w', initialfile='Untitled.txt', 
                                        defaultextension=".txt", 
                                        filetypes=[("All Files","*.*"), 
                                            ("Text Documents","*.txt")])
        
       
        self.file.write(self.Text.get(1.0,END))
        name = self.file.name.split("/")
        name1 = name[len(name)-1].split(".")
        self.root.title(os.path.basename(name1[0])) # adding heading to notepad after saving
        

#Function to exit File    
    def exitFile(self):
        textData =self.Text.get(0.0,END)
        if len(textData) != 0:
           result = messagebox.askyesno("alert","Do you want to save?")
           if result == True: 
               self.saveFile()
           else:
               self.root.destroy()
        self.root.destroy()
        
#Function to undo Text       
    def undoFile(self):
        self.Text.edit_undo()
        pass

# Function to Cut  Text      
    def cutFile(self):
        self.Text.event_generate("<<Cut>>")
    
#Function to copy Text    
    def copyFile(self):
        self.Text.event_generate("<<Copy>>")

#Function to paste Text        
    def pasteFile(self):
        self.Text.event_generate("<<Paste>>")
        
    def deleteFile(self):
        pass
        
 #Funtion to find text       
    def findFile(self):
        findString = simpledialog.askstring("Find...", "Enter text")
        textData = self.Text.get(0.0, END)
        print(findString)
        print(textData)
        if findString in textData:
#            The "1.0" here represents where to insert the text, and can be read as "line 1, character 0".
            tag_start = self.Text.search(findString, 1.0, stopindex=END, regexp=True)
            print(tag_start)
            tag_end = '%s+%dc' % (tag_start, len(findString))
            print(tag_end)
            self.Text.tag_add("SEL",tag_start,tag_end)
            self.Text.tag_config("SEL",background="blue", foreground="black")
  
        else:
            messagebox.showerror("Error","Unable to find word")
            print("Unable to find word")
        pass

#function to find        
    def findNextFile(self):
        pass

#function to replace text            
    def replaceFile(self):
        findString = simpledialog.askstring("Find...", "Enter text")
        replaceString = simpledialog.askstring("Replace...", "Enter text")
        textData = self.Text.get(0.0, END)
        if findString in textData:
            tag_start = self.Text.search(findString, 1.0, stopindex=END, regexp=True)
            print(tag_start)
            tag_end = '%s+%dc' % (tag_start, len(findString))
            print(tag_end)
            self.Text.replace(tag_start,tag_end,replaceString)
        else:
            messagebox.showerror("Error","Unable to find word")

#Go to Specific line            
    def goToFile(self):
        name = int(askstring('GoTo', 'Enter Line number?'))
        print(name)
        line = linecache.getline(self.file, name)
        
            
    def selectAllFile(self):
        self.Text.tag_add('SEL',1.0,END)
        pass
            
    def timeDate(self):
        date_time= datetime.datetime.now().replace(microsecond=0)
        self.Text.insert(END,date_time)
        pass
            
    def wordWrapFile(self):
        wrapper = textwrap.TextWrapper(width=(self.Width)+10)
        finalwordwrap = wrapper.fill(text=self.Text.get(0.0, END))
        self.Text.replace(0.0,END,finalwordwrap)
        pass
            
            
    def helpFile(self):
        link="https://www.bing.com/search?q=get+help+with+notepad+in+windows+10&filters=guid:%224466414-en-dia%22%20lang:%22en%22&form=T00032&ocid=HelpPane-BingIA"
        webbrowser.open_new(link)
        pass
            
    def aboutNotepad(self):
        messagebox.showinfo("About Notepad", "Windows 10" )
        pass
        
    
    
    def run(self):
        self.root.mainloop()
    #mainloop() is an infinite loop used to run the application, wait for an event to occur and process the event till the window is not closed. 
      
    
if __name__ == '__main__':
    N1= Notepad(600,400)
    N1.run()

