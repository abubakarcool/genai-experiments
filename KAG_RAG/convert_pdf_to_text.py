# convert_pdf_to_text.py
from PyPDF2 import PdfReader

reader = PdfReader("Old formula, new failures.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

with open("ipl_article.txt", "w", encoding="utf-8") as f:
    f.write(text)
