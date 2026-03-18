'''
See COPYRIGHT.md for copyright information.
'''
from tkinter import Toplevel, StringVar, N, S, E, W, EW
try:
    from tkinter.ttk import Frame, Button, Label, Entry
except ImportError:
    from ttk import Frame, Button, Label, Entry
from arelle.CntlrWinTooltip import ToolTip
from arelle.TtkUtil import compute_dialog_width
import regex as re

'''
caller checks accepted, if True, caller retrieves url
'''
def askURL(parent, url=None, buttonSEC=False, buttonRSS=False):
    dialog = DialogURL(parent, url, buttonSEC, buttonRSS)
    if dialog.accepted:
        return dialog.url
    return None


class DialogURL(Toplevel):
    DEFAULT_DIALOG_WIDTH = 700
    MIN_DIALOG_WIDTH = 700

    def __init__(self, parent, url=None, buttonSEC=False, buttonRSS=False):
        super(DialogURL, self).__init__(parent)
        self.parent = parent
        parentGeometry = re.match(r"(\d+)x(\d+)[+]?([-]?\d+)[+]?([-]?\d+)", parent.geometry())
        dialogX = int(parentGeometry.group(3))
        dialogY = int(parentGeometry.group(4))
        screenWidth = self.winfo_screenwidth()
        self.accepted = False
        self.url = None
        self.transient(self.parent)
        self.title("Enter URL")
        self.urlVar = StringVar()
        self.urlVar.set(url if url is not None else "")

        frame = Frame(self)
        buttonRow = Frame(frame)
        leftButtons = Frame(buttonRow)
        rightButtons = Frame(buttonRow)
        urlLabel = Label(frame, text=_("URL:"), underline=0)
        urlEntry = Entry(frame, textvariable=self.urlVar, width=60)
        urlEntry.focus_set()
        okButton = Button(rightButtons, text=_("OK"), command=self.ok)
        cancelButton = Button(rightButtons, text=_("Cancel"), command=self.close)
        if buttonSEC:
            usSecButton = Button(leftButtons, text=_("SEC search"), command=self.usSec)
            usSecButton.grid(row=0, column=0, sticky=W, pady=3, padx=(3, 4))
            ToolTip(usSecButton, text=_("Opens US SEC Edgar Company Search (in web browser)\n\n"
                                     "(1) Find the company in web browser,\n"
                                     "(2) Click 'documents' button for desired filing,\n"
                                     "(3) Find 'data files' panel, instance document row, 'document' column,\n"
                                     "(4) On instance document file name, right-click browser menu: 'copy shortcut',\n"
                                     "(5) Come back to this dialog window,\n"
                                     "(6) Ctrl-v (paste) shortcut into above URL text box,\n"
                                     "(7) Click ok button to load instance document"),
                                     wraplength=480)
        if buttonRSS:
            rssButton = Button(leftButtons, text=_("SEC RSS"), command=self.rssFeed)
            rssButton.grid(row=0, column=1, sticky=W, pady=3, padx=(0, 4))
            ToolTip(rssButton, text=_("Opens current US SEC Edgar RSS feed"),
                                     wraplength=480)
        urlLabel.grid(row=0, column=0, sticky=W, pady=3, padx=3)
        urlEntry.grid(row=0, column=1, columnspan=4, sticky=EW, pady=3, padx=(3, 12))
        buttonRow.grid(row=1, column=1, columnspan=4, sticky=EW, pady=3, padx=(0, 12))
        buttonRow.columnconfigure(0, weight=1)
        buttonRow.columnconfigure(1, weight=1)
        leftButtons.grid(row=0, column=0, sticky=W)
        rightButtons.grid(row=0, column=1, sticky=E)
        okButton.grid(row=0, column=0, sticky=E, padx=(0, 4))
        ToolTip(okButton, text=_("Opens above URL from web cache, downloading to cache if necessary"), wraplength=240)
        cancelButton.grid(row=0, column=1, sticky=E, padx=3)
        ToolTip(cancelButton, text=_("Cancel operation"))

        frame.grid(row=0, column=0, sticky=(N,S,E,W))
        frame.columnconfigure(1, weight=1)
        window = self.winfo_toplevel()
        window.columnconfigure(0, weight=1)
        dialogWidth = compute_dialog_width(screenWidth, self.DEFAULT_DIALOG_WIDTH, self.MIN_DIALOG_WIDTH)
        self.minsize(self.MIN_DIALOG_WIDTH, 140)
        self.geometry("{0}x140+{1}+{2}".format(dialogWidth, dialogX+50, dialogY+100))

        self.bind("<Alt-u>", lambda *ignore: urlEntry.focus_set())
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.close)

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.grab_set()
        self.wait_window(self)

    def ok(self, event=None):
        self.url = self.urlVar.get().strip()
        if self.url and self.url[0] == '"' and self.url[-1] == '"':
            self.url = self.url[1:-1] # strip double quotes (from cut and paste from database etc
        self.accepted = True
        self.close()

    def close(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def usSec(self, event=None):
        import webbrowser
        webbrowser.open("http://www.sec.gov/edgar/searchedgar/companysearch.html")

    def rssFeed(self, event=None):
        self.url = "http://www.sec.gov/Archives/edgar/usgaap.rss.xml"
        self.accepted = True
        self.close()
