from tkinter import Tk, Label, Button, Frame, Toplevel
from tkinter.ttk import Treeview
from tkinter.messagebox import showerror
import datetime

# ثوابت البرنامج

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
WINDOW_BG = '#7A8DAB'
todayDate = datetime.datetime.today()

btnColorStyles = {
    'add': {'bg': '#36D79A'},
    'delete': {'bg': '#E05851'},
    'process': {'bg': '#26B0DE'},
    'save': {'bg': '#CCC65C'}
}
btnGeometry = {'ipadx': 10, 'ipady': 3}

class RecordWindow(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 2), weight=1)
        self.rowconfigure(1, weight=3)

        Label(self, text='سجل الفواتير اليوم ' + datetime.datetime.strftime(todayDate, '%Y/%m/%d'),
              font=('', 16, 'bold')).grid(row=0, column=0, pady=20, sticky='nsew')
        
        self.todayInvoicesTree = self.setupTree(('الوقت', 'المبلغ', 'المبلغ بدون ضريبة', 'رقم الفاتورة'))
        self.todayInvoicesTree.grid(row=1, column=0, sticky='nsew')
        
        # self.newInvoiceBtn = Button(self, btnColorStyles['add'], text='فاتورة جديدة', command=createNewInvoice)
        # self.newInvoiceBtn.grid(row=2, column=0, sticky='nsew')

        self.mainloop()

    def setupTree(self, columns):
        columnsWithoutFirst = [c for c in columns if columns.index(c) != 0]

        tree = Treeview(self, columns=columnsWithoutFirst)
        tree.heading('#0', text=columns[0])
        tree.column('#0', anchor='center', width=120, stretch=False)

        for c in columnsWithoutFirst:
            tree.heading(c, text=c)
            tree.column(c, anchor='center', width=120, stretch=False)

        return tree


class InvoiceWindow(Toplevel):
    def __init__(self):
        super().__init__()
        
    def createNewInvoice(self):
        pass


def main():
    recordWindow = RecordWindow('برنامج المحاسبة')


if __name__ == '__main__':
    main()