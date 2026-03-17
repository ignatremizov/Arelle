'''
See COPYRIGHT.md for copyright information.
'''
from tkinter import Toplevel, PhotoImage, Text, N, S, E, W, EW, NW
from tkinter import font as tkFont
try:
    from tkinter.ttk import Label, Button, Frame, Scrollbar
except ImportError:
    from ttk import Label, Button, Frame, Scrollbar
from regex import match as re_match
from arelle.TtkUtil import compute_dialog_width
'''
caller checks accepted, if True, caller retrieves url
'''
def about(parent, title, imageFile, body):
    dialog = DialogAbout(parent, title, imageFile, body)
    return None


class DialogAbout(Toplevel):
    DEFAULT_DIALOG_WIDTH = 760
    MIN_DIALOG_WIDTH = 560
    DEFAULT_DIALOG_HEIGHT = 560
    MIN_DIALOG_HEIGHT = 420

    def __init__(self, parent, title, imageFile, body):
        super(DialogAbout, self).__init__(parent)
        self.parent = parent
        parentGeometry = re_match(r"(\d+)x(\d+)[+]?([-]?\d+)[+]?([-]?\d+)", parent.geometry())
        dialogX = int(parentGeometry.group(3))
        dialogY = int(parentGeometry.group(4))
        screenWidth = self.winfo_screenwidth()
        self.transient(self.parent)
        self.title(title)

        frame = Frame(self)
        self.image = PhotoImage(file=imageFile)
        aboutImage = Label(frame, image=self.image)
        bodyFrame = Frame(frame)
        bodyScrollbar = Scrollbar(bodyFrame, orient="vertical")
        bodyFont = tkFont.nametofont("TkDefaultFont")
        aboutBody = Text(
            bodyFrame,
            wrap="word",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            font=bodyFont,
        )
        aboutBody.insert("1.0", body)
        includesLine = aboutBody.search("Includes:", "1.0", stopindex="end")
        if includesLine:
            includesItemsStart = aboutBody.index(f"{includesLine} +1 lines linestart")
            aboutBody.tag_configure("includes", lmargin1=24, lmargin2=48)
            aboutBody.tag_add("includes", includesItemsStart, "end")
        aboutBody.configure(state="disabled")
        aboutBody["yscrollcommand"] = bodyScrollbar.set
        bodyScrollbar["command"] = aboutBody.yview
        okButton = Button(frame, text=_("OK"), command=self.ok)
        okButton.focus_set()
        aboutImage.grid(row=0, column=0, sticky=NW, pady=20, padx=16)
        bodyFrame.grid(row=0, column=1, columnspan=2, sticky=(N, S, E, W), pady=12, padx=(0, 12))
        aboutBody.grid(row=0, column=0, sticky=(N, S, E, W))
        bodyScrollbar.grid(row=0, column=1, sticky=(N, S))
        okButton.grid(row=1, column=2, sticky=EW, pady=3)

        frame.grid(row=0, column=0, sticky=(N,S,E,W))
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        bodyFrame.rowconfigure(0, weight=1)
        bodyFrame.columnconfigure(0, weight=1)
        window = self.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        window.rowconfigure(0, weight=1)
        dialogWidth = compute_dialog_width(screenWidth, self.DEFAULT_DIALOG_WIDTH, self.MIN_DIALOG_WIDTH)
        self.minsize(self.MIN_DIALOG_WIDTH, self.MIN_DIALOG_HEIGHT)
        self.geometry("{0}x{1}+{2}+{3}".format(dialogWidth, self.DEFAULT_DIALOG_HEIGHT, dialogX+200, dialogY+140))

        self.bind("<Alt-u>", lambda *ignore: okButton.focus_set())
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.close)

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.grab_set()
        self.wait_window(self)

    def ok(self, event=None):
        self.close()

    def close(self, event=None):
        self.parent.focus_set()
        self.destroy()
