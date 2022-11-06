from tkinter import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path
from custom_pdf_view import PDFViewer
from regex_redactor import Redactor
from fitz import *


class App:
    def __init__(self):
        super().__init__()
        # Class attributes
        self.pdf = ""
        self.pdf2 = None
        self.pdf_name = None
        self.pdf1 = None
        self.pdf_redacted = None

        self.window = Tk()

        # GUI Format
        self.window.title('PDF Redaction')

        # Setup Grid of Window
        self.window.columnconfigure([0, 1, 2], minsize=100)
        self.window.rowconfigure([0, 1, 2], minsize=25)

        # Frame - PDF Menu
        self.frm_pdf_menu = tk.Frame(self.window)
        self.frm_pdf_menu.grid(row=0, column=0)

        # PDF - Selection & Close
        btn_open_pdf = tk.Button(self.frm_pdf_menu, text='Open a PDF File', command=self.select_filename)
        btn_open_pdf.pack(side=tk.LEFT, padx=15)

        btn_close_pdf = tk.Button(self.frm_pdf_menu, text='Close the PDF File', command=self.close_pdf)
        btn_close_pdf.pack(side=tk.RIGHT)

        # Frame: Add Item
        self.frm_options = tk.Frame()
        self.frm_options.grid(row=1, column=1, padx=15)

        # Add Item - Instructions
        lbl_add_item = tk.Label(self.frm_options, text="Add text string to be redacted")
        lbl_add_item.pack(side=tk.TOP)

        frm_add_item = tk.Frame(self.frm_options)
        frm_add_item.pack()

        # Add Item - Submit & Enter
        bt_add_button = Button(frm_add_item, text="Insert", command=self.insert)
        bt_add_button.pack(side=tk.LEFT)

        self.entry_txt = tk.StringVar()
        entry = tk.Entry(frm_add_item, textvariable=self.entry_txt)
        entry.pack(side=tk.RIGHT)

        # Delete item from listbox
        self.lbl_box = Label(self.frm_options, text=" ")
        self.lbl_box.pack()

        # Frame: ListBox
        self.frm_listbox = tk.Frame()
        self.frm_listbox.grid(row=2, column=1, padx=15)

        self.my_listbox = Listbox(self.frm_options)
        self.my_listbox.pack(side=tk.TOP, fill=tk.X)

        # Add default values to listbox
        self.my_list = ["Example Text"]
        for item in self.my_list:
            self.my_listbox.insert(END, item)

        btn_remove = Button(self.frm_options, text="Remove entered text string", command=self.delete)
        btn_remove.pack(fill=tk.X)

        # Frame: PDF Redaction
        self.frm_pdf = tk.Frame(self.window)
        self.frm_pdf.grid(row=1, column=0)

        # PDF icon
        self.pdf_icon()
        self.lbl_pdf_icon = Label(self.frm_pdf, image=self.photo)
        self.lbl_pdf_icon.pack()

        btn_redact = Button(self.frm_options, text="Redact PDF", command=lambda: self.redactor_button())
        btn_redact.pack(side=tk.BOTTOM, pady=10, fill=tk.X, anchor=SE)

        self.window.mainloop()

    def pdf_icon(self):
        dir = Path.cwd()
        image_path = str(dir)+r'\src\icons\redaction.jpg'
        img = Image.open(image_path)
        img.thumbnail((200,200), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)

    def select_filename(self):
        filetypes = [('PDF File', '*.pdf')]

        filename = tk.filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        self.pdf = filename
        self.pdf_name = os.path.splitext(self.pdf)[0]
        self.pdf_redacted = str(self.pdf_name + "_redacted.pdf")

        # open pdf and a pdf_redacted for redaction
        self.open_pdf()

    def open_pdf(self):
        self.frm_pdf.destroy()
        self.frm_pdf = tk.Frame(self.window)
        self.frm_pdf.grid(row=1, column=0)

        doc = fitz.open(self.pdf)
        doc.save(self.pdf_redacted, encryption=fitz.PDF_ENCRYPT_KEEP)

        self.pdf1 = PDFViewer(master=self.frm_pdf, width=50, height=20, spacing3=5, bg='black')
        self.pdf1.pack(side=tk.LEFT)
        self.pdf1.show(self.pdf)

        self.pdf2 = PDFViewer(master=self.frm_pdf, width=50, height=20, spacing3=5, bg='black')
        self.pdf2.pack(side=tk.RIGHT)
        self.pdf2.show(self.pdf)

    # close windows and open pdf icon
    def close_pdf(self):
        self.frm_pdf.destroy()
        self.frm_pdf = tk.Frame(self.window)
        self.frm_pdf.grid(row=1, column=0)

        self.pdf_icon()
        self.lbl_image = Label(self.frm_pdf, image=self.photo)
        self.lbl_image.pack()

    def insert(self):
        self.my_listbox.insert(END, self.entry_txt.get())
        self.my_list.append(self.entry_txt.get())

    def delete(self):
        self.my_listbox.delete(ANCHOR)
        self.lbl_box.config(text=" ")

    def redactor_button(self):
        lst_regex = []
        for item in self.my_list:
            lst_regex.append(r"(\b{0}\b)".format(item))

        redactor = Redactor(self.pdf_redacted, lst_regex)
        redactor.redaction()

        self.frm_pdf.destroy()
        frm_pdf = tk.Frame(self.window)
        frm_pdf.grid(row=1, column=0, rowspan=2)

        pdf1 = PDFViewer(master=frm_pdf, width=50, height=20, spacing3=5, bg='black')
        pdf1.pack(side=tk.LEFT)
        pdf1.show(self.pdf)

        pdf2 = PDFViewer(master=frm_pdf, width=50, height=20, spacing3=5, bg='black')
        pdf2.pack(side=tk.RIGHT)
        pdf2.show(self.pdf_redacted)


if __name__ == "__main__":
    app = App()
    app.mainloop()
