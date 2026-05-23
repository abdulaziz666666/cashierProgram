from tkinter import Tk, Label, Entry, Button, Frame, Toplevel
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


class InvoiceWindow(Toplevel):
    def __init__(self, recordWindow):
        super().__init__(master=recordWindow)
        self.title('فاتورة جديدة')
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.totalPrice = 0

        self.invoiceDataFrame = Frame(self, bg=WINDOW_BG, width=300)
        self.invoiceDataFrame.grid(row=0, column=3, rowspan=9, columnspan=2, sticky='nsew')

        Label(self.invoiceDataFrame, text='رقم المنتج',
            bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=0, column=3, columnspan=2, pady=(20, 10))
        Label(self.invoiceDataFrame, text='اسم المنتج', 
            bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=2, column=3, columnspan=2, pady=10)
        Label(self.invoiceDataFrame, text='السعر', 
            bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=4, column=3, columnspan=2, pady=10)
        
        self.numberEntry = Entry(self.invoiceDataFrame, width=30)
        self.nameEntry = Entry(self.invoiceDataFrame, width=30)
        self.priceEntry = Entry(self.invoiceDataFrame, width=30)
        self.addBtn = Button(self.invoiceDataFrame, btnColorStyles['add'], text='إضافة', command=self.addProductToInvoice)
        self.deleteBtn = Button(self.invoiceDataFrame, btnColorStyles['delete'], text='حذف', command=self.deleteProductFromInvoice)
        self.editBtn = Button(self.invoiceDataFrame, btnColorStyles['process'], text='تعديل', command=self.editProductValues)
        self.saveInvoiceBtn = Button(self.invoiceDataFrame, btnColorStyles['save'], text='حفظ الفاتورة', command=self.saveInvoiceAtRecord)

        self.numberEntry.grid(row=1, column=3, columnspan=2, padx=40, sticky='we')
        self.nameEntry.grid(row=3, column=3, columnspan=2, padx=40, sticky='we')
        self.priceEntry.grid(row=5, column=3, columnspan=2, padx=40, sticky='we')
        self.addBtn.grid(btnGeometry, row=6, column=3, padx=(40, 3), pady=(20, 0), sticky='we')
        self.deleteBtn.grid(btnGeometry, row=6, column=4, padx=(3, 40), pady=(20, 0), sticky='we')
        self.editBtn.grid(btnGeometry, row=7, column=3, columnspan=2, padx=40, pady=5, sticky='we')
        self.saveInvoiceBtn.grid(btnGeometry, row=8, column=3, columnspan=2, padx=40, pady=(0, 20), sticky='we')


        self.totalPriceLabel = Label(self, text='0', bg='lightgrey', font=('', 16, 'bold'))
        self.totalPriceLabel.grid(row=8, column=0, columnspan=3, sticky='nsew')


    def createInvoiceTree(self, tree: Treeview):
        self.invoiceTree = tree
        self.invoiceTree.grid(row=0, column=0, rowspan=8, columnspan=3, sticky='nsew')

    def resetEntries(self, *entries):
        for e in entries:
            e.delete(0, 'end')

    def addProductToInvoice(self):
        try:
            self.totalPrice += float(self.priceEntry.get())

        except ValueError:
            showerror('خطأ', 'لم تقم بإدخال السعر')

        else:
            self.invoiceTree.insert(
                '',
                'end',
                text=datetime.datetime.strftime(todayDate, '%Y/%m/%d %H:%M'),
                values=(self.priceEntry.get(), self.nameEntry.get(), self.numberEntry.get())
            )

            self.resetEntries(self.priceEntry, self.nameEntry, self.numberEntry)

            self.totalPriceLabel.config(text=str(self.totalPrice))

    def deleteProductFromInvoice(self):
        try:
            selectedProduct = self.invoiceTree.selection()[0]
            
        except IndexError:
            pass

        else:
            selectionValues = self.invoiceTree.item(selectedProduct, 'values')
            self.invoiceTree.delete(self.invoiceTree.selection()[0])

            self.totalPrice -= float(selectionValues[0])
            self.totalPriceLabel.config(text=str(self.totalPrice))

    def saveChanges(self, master, selectedProduct, *entries):
        self.invoiceTree.item(selectedProduct, values=[e.get() for e in entries])

        try:
            newPrice = float(entries[0].get())

        except ValueError:
            showerror('خطأ', 'لم تقم بإدخال السعر')

        else:
            oldPrice = float(self.invoiceTree.item(selectedProduct, 'values')[0])
            self.totalPrice += newPrice - oldPrice
            self.totalPriceLabel.config(text=str(self.totalPrice))

            master.destroy()


    def editProductValues(self):
        try:
            selectedProduct = self.invoiceTree.selection()[0]
            
        except IndexError:
            pass

        else:

            editWindow = Toplevel(self)

            invoiceDataFrame = Frame(editWindow, bg=WINDOW_BG, width=300)
            invoiceDataFrame.grid(row=0, column=0, sticky='nsew')

            Label(invoiceDataFrame, text='رقم المنتج',
                bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=0, column=0, pady=(20, 10))
            Label(invoiceDataFrame, text='اسم المنتج', 
                bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=2, column=0, pady=10)
            Label(invoiceDataFrame, text='السعر', 
                bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=4, column=0, pady=10)
            
            numberEntry = Entry(invoiceDataFrame, width=30)
            nameEntry = Entry(invoiceDataFrame, width=30)
            priceEntry = Entry(invoiceDataFrame, width=30)
            saveChangesBtn = Button(invoiceDataFrame, btnColorStyles['process'], text='حفظ',
                            command=lambda: self.saveChanges(editWindow, selectedProduct, (priceEntry, nameEntry, numberEntry)))

            numberEntry.grid(row=1, column=0, padx=40, sticky='we')
            nameEntry.grid(row=3, column=0, padx=40, sticky='we')
            priceEntry.grid(row=5, column=0, padx=40, sticky='we')
            saveChangesBtn.grid(btnGeometry, row=6, column=0, padx=39, pady=20, sticky='we')

            selectionValues = self.invoiceTree.item(selectedProduct, 'values')
            for e, v in zip((priceEntry, nameEntry, numberEntry), selectionValues):
                e.insert(0, v)

            editWindow.mainloop()

    def saveData(self):
        self.data = [self.invoiceTree.item(item, 'values') for item in self.invoiceTree.get_children()]
    def returnData(self):
        return self.data
    def saveInvoiceAtRecord(self):
        self.saveData()
        self.resetEntries(self.priceEntry, self.nameEntry, self.numberEntry)
        self.invoiceTree.delete(*self.invoiceTree.get_children())
        self.totalPrice = 0
        self.totalPriceLabel.config(text=str(self.totalPrice))



class RecordWindow(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 2), weight=1)
        self.rowconfigure(1, weight=3)

        Label(self, text='سجل الفواتير اليوم ' + datetime.datetime.strftime(todayDate, '%Y/%m/%d'),
              font=('', 16, 'bold')).grid(row=0, column=0, pady=20, sticky='nsew')
        
        self.todayInvoicesTree = self.setupTree(self, ('الوقت', 'المبلغ', 'المبلغ بدون ضريبة', 'رقم الفاتورة'))
        self.todayInvoicesTree.grid(row=1, column=0, sticky='nsew')
        
        self.newInvoiceBtn = Button(self, btnColorStyles['add'], text='فاتورة جديدة', command=self.createNewInvoice)
        self.newInvoiceBtn.grid(row=2, column=0, sticky='nsew')

        self.invoiceWindow = None
        self.lastInvoiceData = tuple()

        self.mainloop()        

    def createNewInvoice(self):
        self.invoiceWindow = InvoiceWindow(self)
        self.invoiceWindow.createInvoiceTree(self.setupTree(self.invoiceWindow, ('التاريخ', 'السعر', 'اسم المنتج', 'رقم المنتج')))
        a = self.invoiceWindow.returnData()
        self.invoiceWindow.mainloop()

        currentTime = datetime.datetime.strftime(todayDate, '%H:%M:%S')
        self.todayInvoicesTree.insert('',
                                      'end',
                                      text=currentTime,
                                      values=())
        

    def setupTree(self, master, columns):
        columnsWithoutFirst = [c for c in columns if columns.index(c) != 0]

        tree = Treeview(master, columns=columnsWithoutFirst)
        tree.heading('#0', text=columns[0])
        tree.column('#0', anchor='center', width=120, stretch=False)

        for c in columnsWithoutFirst:
            tree.heading(c, text=c)
            tree.column(c, anchor='center', width=120, stretch=False)

        return tree
    
def main():
    recordWindow = RecordWindow('برنامج المحاسبة')

if __name__ == '__main__':
    main()