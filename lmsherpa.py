from llmsherpa.readers import LayoutPDFReader
import os, sys
from IPython.core.display import HTML


llmsherpa_api_url = "http://localhost:5001/api/parseDocument?renderFormat=all"
pdf_url = "/Users/pmarek/work/github.com/scriptingShrimp/rag-sandbox/books/Sidecarless-Istio-Explained_Solo.pdf" # also allowed is a file path e.g. /home/downloads/xyz.pdf
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)
# print(doc)

# HTML(doc.to_html())
print(doc.to_html())