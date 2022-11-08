import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import fitz

"""
Source: # https://stackoverflow.com/questions/70302939/tkpdfviewer-open-several-pdf-in-grid-not-working-display-same-pdf-with-a-mix
"""
# alternative to:
# pdf_show = pdf.ShowPdf()
# pdf_load = pdf_show.pdf_view(master=frm_pdf,load="", width=50, height=100,
#                  pdf_location=pdf_location"
#                  )
# pdf_load.pack()

class PDFViewer(ScrolledText):
    def show(self, pdf_file):
        self.delete('1.0', 'end') # clear current content
        pdf = fitz.open(pdf_file) # open the PDF file
        self.images = []   # for storing the page images
        for page in pdf:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)

class Double_PDFViewer(ScrolledText):
    def show(self, pdf_file1, pdf_file2):
        self.delete('1.0', 'end') # clear current content
        pdf1 = fitz.open(pdf_file1) # open the PDF file
        pdf2 = fitz.open(pdf_file2) # open the PDF file

        self.images = []   # for storing the page images
        for page in pdf1:
            pix = page.get_pixmap()
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            photo = tk.PhotoImage(data=pix1.tobytes('ppm'))
            # insert into the text box
            self.image_create('end', image=photo)
            self.insert('end', '\n')
            # save the image to avoid garbage collected
            self.images.append(photo)

