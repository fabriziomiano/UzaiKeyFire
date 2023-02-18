from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class PdfHandler(object):
    """
    Class to convert the content of a PDF into a string.

    Attributes:
        stream_in (bytes): byte-like content of PDF

    """

    def __init__(self, stream_in):
        self.stream_in = stream_in

    def get_corpus(self):
        """
        Return a string made of the content of the PDF

        """
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(
            rsrcmgr, retstr, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        maxpages = 0
        caching = True
        pagenos = set()
        pages = PDFPage.get_pages(
            self.stream_in,
            pagenos,
            maxpages=maxpages,
            password="",
            caching=caching,
            check_extractable=True
        )
        for page in pages:
            interpreter.process_page(page)
        device.close()
        text = retstr.getvalue()
        retstr.close()
        return text

    def save_to_txt(self):
        """
        Save a .txt file with the content of the PDF
        """
        content = self.get_corpus()
        txt_pdf = open('text_pdf.txt', 'wb')
        txt_pdf.write(content.encode('utf-8'))
        txt_pdf.close()
