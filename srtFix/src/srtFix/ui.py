'''
Created on Jan 29, 2016

@author: Ziv
'''
import tkinter as tk


class UIMain(tk.Tk):
    '''
    classdocs
    '''
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        
    def initialize(self):
        self.grid()
        
        self.entryVatiable=tk.StringVar()
        self.entry=tk.Entry(self,textvariable=self.entryVatiable)
        self.entry.grid(column=0, row=0, sticky='EW')
        self.entry.bind("<Return>",self.OnPressEnter)
        self.entryVatiable.set(u"Enter text here")
        
        button = tk.Button(self,text=u"Click me",command=self.OnButtonClick)
        button.grid(column=1,row=0)
        
        self.lavelVariable=tk.StringVar()
        label = tk.Label(self,textvariable=self.lavelVariable,anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.lavelVariable.set(u"Hello") 
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0,tk.END)
        
    def OnButtonClick(self):
        self.lavelVariable.set(self.entryVatiable.get())
        
    def OnPressEnter(self,event):
        self.lavelVariable.set(self.entryVatiable.get())

if __name__ == "__main__":
    app = UIMain(None)
    app.title('strFix')
    app.mainloop()