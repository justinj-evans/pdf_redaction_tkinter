from tkinter import *
import tkinter as tk
from ttkthemes import ThemedTk

from custom_pdf_view import PDFViewer
from regex_redactor import Redactor
import fitz

class App():
    def __init__(self):
        super().__init__()
        self.window = Tk()

        # GUI Format
        self.window.title('PDF Text Redaction')

        # PDF Setup
        pdf_location = r"C:\Users\Justin Evans\Documents\Python\pdf-blinding\pdf"
        pdf = r"\sample.pdf"
        self.pdf = pdf_location+pdf
        print(self.pdf)
        self.pdf_temp = pdf_location+r"\temp.pdf"
        doc = fitz.open(self.pdf)
        doc.save(self.pdf_temp, encryption=fitz.PDF_ENCRYPT_KEEP)

        # Setup Grid of Window
        self.window.columnconfigure([0, 1, 2], minsize=100)
        self.window.rowconfigure([0, 1, 2], minsize=25)

        # PDF Frame
        self.frm_pdf = tk.Frame(self.window)
        self.frm_pdf.grid(row=0, column=0, rowspan=2)

        lbl_pdf = tk.Label(master=self.frm_pdf, text="PDF Space")
        lbl_pdf.pack(side=tk.TOP)

        pdf1 = PDFViewer(master=self.frm_pdf, width=60, height=25, spacing3=5, bg='black')
        pdf1.pack(side=tk.LEFT)
        pdf1.show(self.pdf)

        pdf2 = PDFViewer(master=self.frm_pdf, width=60, height=25, spacing3=5, bg='black')
        pdf2.pack(side=tk.RIGHT)
        pdf2.show(self.pdf)

        # Frame: Add Item
        self.frm_options = tk.Frame()
        self.frm_options.grid(row=0, column=1, padx=15)

        # Add Item - Instructions
        lbl_add_item = tk.Label(self.frm_options,text="Add word(s) to be redacted")
        lbl_add_item.pack(side=tk.TOP)

        frm_add_item = tk.Frame(self.frm_options)
        frm_add_item.pack()

        # Add Item - Submit & Enter
        add_item = Button(frm_add_item, text="Insert", command=self.insert)
        add_item.pack(side=tk.LEFT)

        self.entry_txt = tk.StringVar()
        entry = tk.Entry(frm_add_item, textvariable=self.entry_txt)
        entry.pack(side=tk.RIGHT)

        # Delete item from listbox
        global my_label
        my_label = Label(self.window, text=" ")
        my_label.grid(row=2, column=2)

        # Frame: ListBox
        self.frm_listbox = tk.Frame()
        self.frm_listbox.grid(row=1, column=1, padx=15)

        self.my_listbox = Listbox(self.frm_options)
        self.my_listbox.pack(side=tk.TOP, fill=tk.X)

        # Add default values to listbox
        self.my_list = ["Example Text"]
        for item in self.my_list:
            self.my_listbox.insert(END, item)

        my_button = Button(self.frm_options, text="Remove", command=self.delete)
        my_button.pack()

        # Frame: Redaction
        my_button = Button(self.frm_options, text="Redact PDF", command=lambda: self.redactor_button(self))
        my_button.pack(side=tk.BOTTOM, pady=10, fill=tk.X)
        #my_button.grid(row=, column=1)

        self.window.mainloop()

    def insert(self):
        self.my_listbox.insert(END, self.entry_txt.get())
        self.my_list.append(self.entry_txt.get())

    def delete(self):
        self.my_listbox.delete(ANCHOR)
        my_label.config(text=" ")

    def redactor_button(self):
        lst_regex = []
        for item in self.my_list:
            lst_regex.append(r"(\b{0}\b)".format(item))

        redactor = Redactor(self.pdf_temp, lst_regex)
        redactor.redaction()

        self.frm_pdf.destroy()
        frm_pdf = tk.Frame(self.window)
        frm_pdf.grid(row=0, column=0, rowspan=2)

        pdf1 = PDFViewer(master=frm_pdf, width=50, height=20, spacing3=5, bg='black')
        pdf1.pack(side=tk.LEFT)
        pdf1.show(self.pdf)

        pdf2 = PDFViewer(master=frm_pdf, width=50, height=20, spacing3=5, bg='black')
        pdf2.pack(side=tk.RIGHT)
        pdf2.show(self.pdf_temp)

if __name__ == "__main__":
    app = App()
    app.mainloop()