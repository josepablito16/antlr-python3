from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
# show an "Open" dialog box and return the path to the selected file
filename = askopenfilename()
print(filename)
