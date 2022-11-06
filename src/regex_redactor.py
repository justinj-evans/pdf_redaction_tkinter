# imports
import fitz
import re

# https://regex101.com/
#text = "A machine learning project"
#search = re.search(r'\bmachine\b',text)
#print(search)

class Redactor:

    # constructor
    def __init__(self, path, lst_regex):
        self.path = path
        self.lst_regex = lst_regex

        print(lst_regex)

    # static methods work independent of class object
    @staticmethod
    def get_sensitive_data(lines, lst_regex):

        """ Function to get all the lines """

        # email regex
        EMAIL_REG = r"(\bmachine\b)"
        for line in lines:

            for regex in lst_regex:

            # matching the regex to each line
                if re.search(regex, line, re.IGNORECASE):
                    search = re.search(regex, line, re.IGNORECASE)

                    # yields creates a generator
                    # generator is used to return
                    # values in between function iterations
                    yield search.group(1)

    def redaction(self):

        """ main redactor code """

        # opening the pdf
        doc = fitz.open(self.path)

        # iterating through pages
        for page in doc:

            # _wrapContents is needed for fixing
            # alignment issues with rect boxes in some
            # cases where there is alignment issue
            #page._wrapContents()

            # getting the rect boxes which consists the matching email regex
            sensitive = self.get_sensitive_data(page.get_text("text")
                                                .split('\n'),
                                                self.lst_regex)


            for data in sensitive:
                areas = page.search_for(data)

                # drawing outline over sensitive datas
                [page.add_redact_annot(area, fill=(0, 0, 0)) for area in areas]

            # applying the redaction
            page.apply_redactions()

        # saving it to a new pdf
        #doc.save('pdf/redacted.pdf')
        doc.save(self.path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        print("Successfully redacted")


# driver code for testing
if __name__ == "__main__":
    # replace it with name of the pdf file
    path = '../pdf/sample2.pdf'
    redactor = Redactor(path,[r'(\bmachine\b)'])
    redactor.redaction()