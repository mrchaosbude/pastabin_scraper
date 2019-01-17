from tkinter import *
from tkinter.filedialog import askopenfilename
import sqlite3
import os

class viewer(object):
    def __init__(self):
        self.db_root = None
        self.root = Tk()
        self.root.title('DB Viewer')
               
        Grid.rowconfigure(self.root, 0, weight=2)
        Grid.columnconfigure(self.root, 0, weight=1)
        #Grid.rowconfigure(self.root, 1, weight=1)
        Grid.columnconfigure(self.root, 1, weight=10)
        if os.path.isfile('pastabin.db'):
            self.db_root = 'pastabin.db'

        #self.menue_button()
        self.listBox_filler(db=self.db_root, dont_show_seen=False)
        self.text_widget()
        self.menue()
        # makes the window to sthe top
        self.root.lift()
        self.root.attributes('-topmost',True)
        self.root.after_idle(self.root.attributes,'-topmost',False)
        # end
        self.root.mainloop()

    def menue(self):    # deactivatet    
        self.menubar = Menu(self.root)
        filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.opener)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.mexit)

        optionMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Option", menu=optionMenu)
        self.show_notall = IntVar()
        optionMenu.add_checkbutton(label="Show Only Unssen", variable=self.show_notall, command=self.showAll_option)
        self.root.config(menu=self.menubar)
    
    def showAll_option(self, event=None):
        if self.show_notall.get() == 1:
            self.listBox_filler(db=self.db_root , dont_show_seen=True)
        else:
            self.listBox_filler(db=self.db_root)


    def listBox_filler(self, db=None, dont_show_seen=False):
        listFrame = Frame(self.root) #seperad frame for the listbox
        listFrame.grid(row=0, column=0, sticky=NSEW,)
        
        scrollBar = Scrollbar(listFrame)
        scrollBar.pack(side=RIGHT, fill=Y)
        self.listBox = Listbox(listFrame,)
        self.listBox.pack(side=LEFT, fill=BOTH, expand=1)
        scrollBar.config(command=self.listBox.yview)
        self.listBox.config(yscrollcommand=scrollBar.set)
        self.listBox.focus_set()
        if db != None:
            try:
                connection = sqlite3.connect(db)
            except:
                print('cant open or find db')
            cursor = connection.cursor()
            cursor.execute("SELECT Id, key, unseen FROM pastabin_meta ") # gets id and kay from db
            self.data = cursor.fetchall()
            num = 0
            for item in self.data: # puts it in the listbox
                if dont_show_seen == True:
                    if item[2] == 1:
                        self.listBox.insert(END, item[:2])
                        if item[2] == 1:
                            self.listBox.itemconfig(num, bg='#D6D6D6')
                        num += 1
                else:
                    self.listBox.insert(END, item[:2])
                    if item[2] == 1:
                        self.listBox.itemconfig(num, bg='#D6D6D6')
                    num += 1            
        
            self.listBox.select_set(0) # pre select the firt item
            self.listBox.bind('<<ListboxSelect>>', self.onselect) #select handler
    
    def onselect(self, evt):
        self.textb.delete(1.0,END)
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        #print ('You selected item {}: "{}"'.format(index, value[0], ))
        connection = sqlite3.connect(self.db_root)
        cursor = connection.cursor()
        cursor.execute("SELECT content FROM pastabin_meta WHERE Id = ?", (value[0],)) # gets id and kay from db
        self.data = cursor.fetchone()
        self.textb.insert(END, self.data)
        cursor.execute("UPDATE pastabin_meta SET unseen = 0 WHERE Id = ?", (value[0],))
        connection.commit()
        self.listBox.itemconfig(index, bg='#FFFFFF')

    
    def text_widget(self):
        txtFrame = Frame(self.root) #seperad frame for the listbox
        txtFrame.grid(row=0, column=1, sticky=NSEW, )
        self.textb = Text(txtFrame, undo=True,)
        self.textb.insert(END, 'select an entry')
        self.textb.pack(side=LEFT, fill=BOTH, expand=1)
        scrollb = Scrollbar(txtFrame, command=self.textb.yview)
        scrollb.pack(side=RIGHT, fill=Y)
        self.textb.config(yscrollcommand=scrollb.set)
    
    def mexit(self):
        quit()
    
    def opener(self):
        filename = askopenfilename(title = "Select file",filetypes = (("SQLite3 DB","*.db"),("all files","*.*")))
        self.db_root = filename
        if self.show_notall.get() == 1:
            self.listBox_filler(db=filename , dont_show_seen=True)
        else:
            self.listBox_filler(db=filename)

if __name__ == "__main__":
    c = viewer()