from tkinter import *
from tkinter.ttk import Treeview
import datetime
from tkinter.messagebox import showerror

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
WINDOW_BG = '#7A8DAB'
todayDate = datetime.datetime.today()

btnColorStyles = {
    'add': {'bg': "#36D79A"},
    'delete': {'bg': "#E05851"},
    'process': {'bg': "#26B0DE"},
}
btnGeometry = {'ipadx': 10, 'ipady': 3}

def setupTree(master: Toplevel, columns):
    columnsWithoutFirst = [c for c in columns if columns.index(c) != 0]

    tree = Treeview(master, columns=columnsWithoutFirst)
    tree.heading('#0', text=columns[0])
    tree.column('#0', anchor='center', width=120, stretch=False)

    for c in columnsWithoutFirst:
        tree.heading(c, text=c)
        tree.column(c, anchor='center', width=120, stretch=False)

    return tree


def addProductToInvoice(numberEntry, nameEntry, priceEntry):
    global totalPrice

    try:
        totalPrice += float(priceEntry.get())

    except ValueError:
        showerror('خطأ', 'لم تقم بإضافة السعر')

    else:
        invoiceTree.insert(
            '',
            'end',
            text=datetime.datetime.strftime(todayDate, '%Y/%m/%d %H:%M'),
            values=(priceEntry.get(), nameEntry.get(), numberEntry.get())
        )

        for e in (numberEntry, nameEntry, priceEntry):
            e.delete(0, END)

        totalPriceLabel.config(text=str(totalPrice))

def deleteProductFromInvoice():
    global invoiceTree, totalPrice

    try:
        selectedProduct = invoiceTree.selection()[0]
        selectionValues = invoiceTree.item(selectedProduct, 'values')
        invoiceTree.delete(invoiceTree.selection()[0])

        totalPrice -= float(selectionValues[0])
        totalPriceLabel.config(text=str(totalPrice))
        
    except IndexError:
        pass

def saveChanges(selectedProduct, entries):
    invoiceTree.item(selectedProduct, values=[e.get() for e in entries])

def editProductValues():
    global totalPrice

    try:
        selectedProduct = invoiceTree.selection()[0]
        
    except IndexError:
        pass

    else:
        selectionValues = invoiceTree.item(selectedProduct, 'values')

        editWindow = Toplevel(invoiceWindow)

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
        saveBtn = Button(invoiceDataFrame, btnColorStyles['process'], text='حفظ',
                         command=lambda: saveChanges(selectedProduct, [priceEntry, nameEntry, numberEntry]))
        
        '''
        السعر الاجمالي يتغير حسب السعر الجديد
        التحقق من ان السعر المدخل عدد
        تدمير النافذة عند الحفظ
        '''


        numberEntry.grid(row=1, column=0, padx=40, sticky='we')
        nameEntry.grid(row=3, column=0, padx=40, sticky='we')
        priceEntry.grid(row=5, column=0, padx=40, sticky='we')
        saveBtn.grid(btnGeometry, row=6, column=0, padx=39, pady=20, sticky='we')

        for e, v in zip((priceEntry, nameEntry, numberEntry), selectionValues):
            e.insert(0, v)

        editWindow.mainloop()

        

def openInvoicesRecord():
    global invoicesRecordWindow

    invoicesRecordWindow = Toplevel(window)
    invoicesRecordWindow.title('قائمة الفواتير')
    invoicesRecordWindow.rowconfigure((0, 1, 2), weight=1)

    Label(invoicesRecordWindow, text='سجل الفواتير اليوم ' + datetime.datetime.strftime(todayDate, '%Y/%m/%d'),
          font=('', 16, 'bold')).grid(row=0, column=0, ipady=30, sticky='nsew')

    todayInvoicesTree = setupTree(invoicesRecordWindow, ('الوقت', 'المبلغ', 'المبلغ بدون ضريبة', 'رقم الفاتورة'))
    todayInvoicesTree.grid(row=1, column=0, sticky='nsew')

    Button(invoicesRecordWindow, btnColorStyles['process'], text='عودة',
           command=invoicesRecordWindow.destroy).grid(row=2, column=0, sticky='nsew', ipady=10)

    invoicesRecordWindow.mainloop()

def createNewInvoice():
    global invoiceWindow, invoiceTree, totalPriceLabel, totalPrice
    totalPrice = 0

    invoiceWindow = Toplevel(window)
    invoiceWindow.title('فاتورة جديدة')
    invoiceWindow.columnconfigure((0, 1, 2, 3, 4), weight=1)
    invoiceWindow.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

    invoiceDataFrame = Frame(invoiceWindow, bg=WINDOW_BG, width=300)
    invoiceDataFrame.grid(row=0, column=3, rowspan=8, sticky='nsew')

    Label(invoiceDataFrame, text='رقم المنتج',
          bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=0, column=3, columnspan=2, pady=(20, 10))
    Label(invoiceDataFrame, text='اسم المنتج', 
          bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=2, column=3, columnspan=2, pady=10)
    Label(invoiceDataFrame, text='السعر', 
          bg=WINDOW_BG, fg='white', font=('', 12, 'bold')).grid(row=4, column=3, columnspan=2, pady=10)
    
    numberEntry = Entry(invoiceDataFrame, width=30)
    nameEntry = Entry(invoiceDataFrame, width=30)
    priceEntry = Entry(invoiceDataFrame, width=30)
    addBtn = Button(invoiceDataFrame, btnColorStyles['add'], text='إضافة', command=lambda: addProductToInvoice(numberEntry, nameEntry, priceEntry))
    editBtn = Button(invoiceDataFrame, btnColorStyles['process'], text='تعديل', command=editProductValues)
    deleteBtn = Button(invoiceDataFrame, btnColorStyles['delete'], text='حذف', command=deleteProductFromInvoice)

    numberEntry.grid(row=1, column=3, columnspan=2, padx=40, sticky='we')
    nameEntry.grid(row=3, column=3, columnspan=2, padx=40, sticky='we')
    priceEntry.grid(row=5, column=3, columnspan=2, padx=40, sticky='we')
    addBtn.grid(btnGeometry, row=6, column=3, padx=(40, 5), pady=(20, 5), sticky='we')
    deleteBtn.grid(btnGeometry, row=6, column=4, padx=(5, 40), pady=(20, 5), sticky='we')
    editBtn.grid(btnGeometry, row=7, column=3, columnspan=2, padx=40, pady=(0, 20), sticky='we')

    invoiceTree = setupTree(invoiceWindow, ('التاريخ', 'السعر', 'اسم المنتج', 'رقم المنتج'))
    invoiceTree.grid(row=0, column=0, rowspan=7, columnspan=3, sticky='nsew')

    totalPriceFrame = Frame(invoiceWindow, bg='lightgrey')
    totalPriceFrame.columnconfigure(0, weight=1)
    totalPriceFrame.rowconfigure(0, weight=1)
    totalPriceFrame.grid(row=7, column=0, columnspan=3, sticky='nsew')

    totalPriceLabel = Label(totalPriceFrame, text='0', font=('', 16, 'bold'))
    totalPriceLabel.grid(row=0, column=0, sticky='nsew')

    invoiceWindow.mainloop()

window = Tk()
window.title('برنامج المحاسبة')
window.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
window.columnconfigure((0, 1, 2, 3), weight=1)
window.rowconfigure((0, 1, 2), weight=1)
window.config(bg=WINDOW_BG)

Label(window, text='مرحبًا بك في برنامج المحاسبة', font=('', 18, 'bold'), bg=WINDOW_BG).grid(row=0, column=1, columnspan=2, ipadx=10)

newInvoiceBtn = Button(window, btnColorStyles['add'], text='فاتورة جديدة', command=createNewInvoice)
newInvoiceBtn.grid(btnGeometry, row=1, column=2, columnspan=2, padx=30, ipady=5, sticky='ew')

invoicesRecordBtn = Button(window, btnColorStyles['process'], text='قائمة الفواتير', command=openInvoicesRecord)
invoicesRecordBtn.grid(btnGeometry, row=1, column=0, columnspan=2, padx=30, ipady=5, sticky='ew')


window.mainloop()