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

# دوال عامة
def setupTree(master, columns):
    columnsWithoutFirst = [c for c in columns if columns.index(c) != 0]

    tree = Treeview(master, columns=columnsWithoutFirst)
    tree.heading('#0', text=columns[0])
    tree.column('#0', anchor='center', width=120, stretch=False)

    for c in columnsWithoutFirst:
        tree.heading(c, text=c)
        tree.column(c, anchor='center', width=120, stretch=False)

    return tree


class RecordWindow(Tk):
    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0, 2), weight=1)
        self.rowconfigure(1, weight=3)

        self.totalPrice = 0

        Label(self, text='سجل الفواتير اليوم ' + datetime.datetime.strftime(todayDate, '%Y/%m/%d'),
              font=('', 16, 'bold')).grid(row=0, column=0, pady=20, sticky='nsew')
        
        self.todayInvoicesTree = setupTree(self, ('الوقت', 'المبلغ', 'المبلغ بدون ضريبة', 'رقم الفاتورة'))
        self.todayInvoicesTree.grid(row=1, column=0, sticky='nsew')

        self.newInvoiceBtn = Button(self, btnColorStyles['add'], text='فاتورة جديدة', command=self.createNewInvoice)
        self.newInvoiceBtn.grid(row=2, column=0, sticky='nsew')

        self.mainloop()

    
    def resetEntries(self, *entries: Entry):
        for e in entries:
            e.delete(0, 'end')

    def addProductToInvoice(self, numberEntry, nameEntry, priceEntry):
        try:
            self.totalPrice += float(priceEntry.get())

        except ValueError:
            showerror('خطأ', 'لم تقم بإدخال السعر')

        else:
            self.invoiceTree.insert(
                '',
                'end',
                text=datetime.datetime.strftime(todayDate, '%Y/%m/%d %H:%M'),
                values=(priceEntry.get(), nameEntry.get(), numberEntry.get())
            )

            self.resetEntries(priceEntry, nameEntry, numberEntry)

            self.totalPriceLabel.config(text=str(self.totalPrice))

    def deleteProductFromInvoice(self):
        try:
            selectedProduct = self.invoiceTree.selection()[0]
            selectionValues = self.invoiceTree.item(selectedProduct, 'values')
            self.invoiceTree.delete(self.invoiceTree.selection()[0])

            self.totalPrice -= float(selectionValues[0])
            self.totalPriceLabel.config(text=str(self.totalPrice))
            
        except IndexError:
            pass

    def saveChanges(self, editWindow, selectedProduct, entries):
        selectedProductPrice = self.invoiceTree.item(selectedProduct, 'values')[0]
        self.invoiceTree.item(selectedProduct, values=[e.get() for e in entries])

        try:
            newPrice = float(entries[0].get())

        except ValueError:
            showerror('خطأ', 'لم تقم بإدخال السعر')

        else:
            oldPrice = float(selectedProductPrice)
            self.totalPrice += newPrice - oldPrice
            self.totalPriceLabel.config(text=str(self.totalPrice))

            editWindow.destroy()

    def editProductValues(self):
        try:
            selectedProduct = self.invoiceTree.selection()[0]
            
        except IndexError:
            pass

        else:
            selectionValues = self.invoiceTree.item(selectedProduct, 'values')

            editWindow = Toplevel(self.invoiceWindow)

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
                            command=lambda: self.saveChanges(editWindow, selectedProduct, [priceEntry, nameEntry, numberEntry]))

            numberEntry.grid(row=1, column=0, padx=40, sticky='we')
            nameEntry.grid(row=3, column=0, padx=40, sticky='we')
            priceEntry.grid(row=5, column=0, padx=40, sticky='we')
            saveChangesBtn.grid(btnGeometry, row=6, column=0, padx=39, pady=20, sticky='we')

            for e, v in zip((priceEntry, nameEntry, numberEntry), selectionValues):
                e.insert(0, v)

            editWindow.mainloop()

    def saveInvoiceAtRecord(self, *entries: Entry):
        invoiceItemsValues = [self.invoiceTree.item(item, 'values') for item in self.invoiceTree.get_children()]

        for itemValues in invoiceItemsValues:
            self.todayInvoicesTree.insert('',
                                    'end',
                                    text=datetime.datetime.strftime(todayDate, '%H:%M:%S'),
                                    values=tuple(itemValues))
        
        self.resetEntries(*entries)
        self.invoiceTree.delete(*self.invoiceTree.get_children())
        self.totalPrice = 0
        self.totalPriceLabel.config(text=str(self.totalPrice))

    def createNewInvoice(self):
        self.invoiceWindow = Toplevel(self)
        self.invoiceWindow.title('فاتورة جديدة')
        self.invoiceWindow.columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.invoiceWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        invoiceDataFrame = Frame(self.invoiceWindow, bg=WINDOW_BG, width=300)
        invoiceDataFrame.grid(row=0, column=3, rowspan=9, columnspan=2, sticky='nsew')

        Label(invoiceDataFrame, text='رقم المنتج',
            bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=0, column=3, columnspan=2, pady=(20, 10))
        Label(invoiceDataFrame, text='اسم المنتج', 
            bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=2, column=3, columnspan=2, pady=10)
        Label(invoiceDataFrame, text='السعر', 
            bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=4, column=3, columnspan=2, pady=10)
        
        numberEntry = Entry(invoiceDataFrame, width=30)
        nameEntry = Entry(invoiceDataFrame, width=30)
        priceEntry = Entry(invoiceDataFrame, width=30)
        addBtn = Button(invoiceDataFrame, btnColorStyles['add'], text='إضافة', command=lambda: self.addProductToInvoice(numberEntry, nameEntry, priceEntry))
        deleteBtn = Button(invoiceDataFrame, btnColorStyles['delete'], text='حذف', command=self.deleteProductFromInvoice)
        editBtn = Button(invoiceDataFrame, btnColorStyles['process'], text='تعديل', command=self.editProductValues)
        saveInvoiceBtn = Button(invoiceDataFrame, btnColorStyles['save'], text='حفظ الفاتورة', command=self.saveInvoiceAtRecord)

        numberEntry.grid(row=1, column=3, columnspan=2, padx=40, sticky='we')
        nameEntry.grid(row=3, column=3, columnspan=2, padx=40, sticky='we')
        priceEntry.grid(row=5, column=3, columnspan=2, padx=40, sticky='we')
        addBtn.grid(btnGeometry, row=6, column=3, padx=(40, 3), pady=(20, 0), sticky='we')
        deleteBtn.grid(btnGeometry, row=6, column=4, padx=(3, 40), pady=(20, 0), sticky='we')
        editBtn.grid(btnGeometry, row=7, column=3, columnspan=2, padx=40, pady=5, sticky='we')
        saveInvoiceBtn.grid(btnGeometry, row=8, column=3, columnspan=2, padx=40, pady=(0, 20), sticky='we')

        self.invoiceTree = setupTree(self.invoiceWindow, ('التاريخ', 'السعر', 'اسم المنتج', 'رقم المنتج'))
        self.invoiceTree.grid(row=0, column=0, rowspan=8, columnspan=3, sticky='nsew')

        totalPriceFrame = Frame(self.invoiceWindow, bg='lightgrey')
        totalPriceFrame.columnconfigure(0, weight=1)
        totalPriceFrame.rowconfigure(0, weight=1)
        totalPriceFrame.grid(row=8, column=0, columnspan=3, sticky='nsew')

        self.totalPriceLabel = Label(totalPriceFrame, text='0', font=('', 16, 'bold'))
        self.totalPriceLabel.grid(row=0, column=0, sticky='nsew')

        self.invoiceWindow.mainloop()


def main():
    recordWindow = RecordWindow('برنامج المحاسبة')

if __name__ == '__main__':
    main()