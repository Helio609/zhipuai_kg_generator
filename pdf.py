import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_text(path, password="", maxpages=0, caching=True):
    rsrcmgr = PDFResourceManager()
    with io.StringIO() as retstr:
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        with open(path, "rb") as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            pagenos = set()

            for page in PDFPage.get_pages(
                fp,
                pagenos,
                maxpages=maxpages,
                password=password,
                caching=caching,
                check_extractable=True,
            ):
                interpreter.process_page(page)

            text = retstr.getvalue()
            device.close()
            return text


import unittest


class TestPdf(unittest.TestCase):

    def test_convert_pdf_to_text(self):
        self.assertNotEqual(convert_pdf_to_text("test.pdf"), "")

if __name__ == '__main__':
    unittest.main()