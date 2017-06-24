'''
Created on Jan 30, 2016

@author: Ziv
'''
import sys
import tkinter as tk
import tkinter.constants
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
from srtFix.processFile import processFile
from getArgs import fixParams
from srtFix.processFile import calculateOffset
from srtFix.processFile import translateFile
from srtFix.translate import Translator

class TkFileDialogExample(tk.Frame):

  def __init__(self, root):

    tk.Frame.__init__(self, root)

#     # input field example
#     self.pack()
# 
#     self.entrythingy = tk.Entry(self)
#     self.entrythingy.pack()
#     # here is the application variable
#     self.contents = tk.StringVar()
#     # set it to some value
#     self.contents.set("this is a variable")
#     # tell the entry widget to watch this variable
#     self.entrythingy["textvariable"] = self.contents
# 
#     # and here we get a callback when the user hits return.
#     # we will have the program print out the value of the
#     # application variable when the user hits return
#     self.entrythingy.bind('<Key-Return>',
#            self.print_contents)
    #Test widget
    self.log=ScrolledText(self,width=70)
    '''init filename to empty string'''
    self.filename=''
    # options for buttons
    button_opt = {'fill': tk.constants.BOTH, 'padx': 5, 'pady': 5}

    #direction
    self.dirVal='movie-after'
    self.dirButton = tk.Button(self, text=self.dirVal,
                                     command=self.dirToggle)
    # define buttons
    tk.Label(self, text='Start Diff',anchor=tk.E).grid(row=0,column=0,sticky=tk.E+tk.W)
    self.startDiff=tk.StringVar()
    self.startDiff.set('')
    tk.Entry(self, textvariable=self.startDiff).grid(row=0,column=1,sticky=tk.W+tk.E)
    tk.Label(self, text='End Diff',anchor=tk.E).grid(row=1,column=0,sticky=tk.E+tk.W)
    self.endDiff=tk.StringVar()
    self.endDiff.set('')
    tk.Entry(self, textvariable=self.endDiff).grid(row=1,column=1,sticky=tk.W+tk.E)
    self.dirButton.grid(row=0,column=2,sticky=tk.W+tk.E)
    tk.Button(self, text='Choose file', command=self.askfilename).grid(row=1,column=2,sticky=tk.W+tk.E)
    # Translate
    tk.Button(self, text='Translate',command=self.translate).grid(row=2,column=0,sticky=tk.E+tk.W)

    tk.Button(self, text='Go', command=self.go).grid(row=0,column=3, rowspan=2,sticky=tk.W+tk.S+tk.E+tk.N)
    self.log.grid(row=3,column=0,columnspan=4)

#     tk.Button(self, text='askopenfile', command=self.askopenfile).pack(**button_opt)
#     tk.Button(self, text='asksaveasfile', command=self.asksaveasfile).pack(**button_opt)
#     tk.Button(self, text='asksaveasfilename', command=self.asksaveasfilename).pack(**button_opt)
#     tk.Button(self, text='askdirectory', command=self.askdirectory).pack(**button_opt)

    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.srt'
    options['filetypes'] = [('srt files', '.srt'),('all files', '.*')]
    options['initialdir'] = 'C:\\Data\\--Movies'
    #options['initialfile'] = 'myfile.txt'
    options['parent'] = root
    options['title'] = 'srtFix - Choose file'

    # This is only available on the Macintosh, and only when Navigation Services are installed.
    # options['message'] = 'message'

    # if you use the multiple file version of the module functions this option is set automatically.
    # options['multiple'] = 1

    # defining options for opening a directory
    self.dir_opt = options = {}
    options['parent'] = root
    options['title'] = 'This is a title'
    options['mustexist'] = True
    options['initialdir'] = 'C:\\'

  def dirToggle(self):
    self.dirVal = 'movie-before' if self.dirVal == 'movie-after' else 'movie-after'
    self.dirButton['text']=self.dirVal
  
  def translate(self):
    params=fixParams(f=self.filename)
    translateFile(params)
#     r=Translator()
#     res=r.TraslateNodeAPI(self.startDiff.get())
    self.toScreenLog('translated:{}'.format(params.outfname))
  
  def toScreenLog(self, s):
    self.log.insert(tk.END, '\n'+s)
  def print_contents(self, event):
      print("hi. contents of entry is now ---->",
            self.contents.get())
      print("startDiff:", self.startDiff.get())

  def go(self):
    try:
      print ("startDiff:{0},endDiff:{1},dir:{2},file:{3}".format(self.startDiff.get(),self.endDiff.get(),self.dirVal,self.filename))
      #pack paramaters and process file
      sd=float(self.startDiff.get())
      #r=parse('{n:d}',self.endDiff.get())
      ed= None if None == self.endDiff.get() or '' == self.endDiff.get() else float(self.endDiff.get()) 
      params=fixParams(f=self.filename,s=sd,e=ed, d=self.dirVal)
      self.toScreenLog("startDiff:{0},endDiff:{1},dir:{2},file:{3}".format(params.startDiff,params.endDiff,params.direction,params.fname))
      calculateOffset(params)
      #self.toScreenLog("movie len:{0},out file name:{1}".format(params.movieLen,params.outfname))
      processFile(params)
      self.toScreenLog("Done. Output file:%s" % params.outfname)
    except ValueError as e:
      print("Exception in go:{1}\n",str(e))
      self.toScreenLog('Enter a number in the Diff fields')
    except IOError:
      e=sys.exc_info()[0]
      self.toScreenLog(e)      
      print('Try again')
    except:
      e=sys.exc_info()[0]
      print("Unexpected error:", e)
      raise

 
  def askopenfile(self):

    """Returns an opened file in read mode."""

    return tk.filedialog.askopenfile(mode='r', **self.file_opt)

  def askfilename(self):

    """Returns an opened file in read mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """

    # get filename
    self.filename = tk.filedialog.askopenfilename(**self.file_opt)
    self.toScreenLog(self.filename)

  def asksaveasfile(self):

    """Returns an opened file in write mode."""

    return tk.filedialog.asksaveasfile(mode='w', **self.file_opt)

  def asksaveasfilename(self):

    """Returns an opened file in write mode.
    This time the dialog just returns a filename and the file is opened by your own code.
    """

    # get filename
    filename = tk.filedialog.asksaveasfilename(**self.file_opt)

    # open file on your own
    if filename:
      return open(filename, 'w')

  def askdirectory(self):

    """Returns a selected directoryname."""

    return tk.filedialog.askdirectory(**self.dir_opt)

if __name__ == '__main__':
  root = tk.Tk()
  TkFileDialogExample(root).grid()
  root.mainloop()
