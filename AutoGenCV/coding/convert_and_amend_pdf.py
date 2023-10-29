# filename: convert_and_amend_pdf.py
import subprocess

# Convert Word file to PDF using pandoc
file_path = r'C:\Users\irene\!AI-LLM\AutoGenCV\coding\2023-10 - CV Eric TOMASZEWSKI.doc'
pdf_file_path = 'Amended.pdf'

subprocess.run(['pandoc', file_path, '-o', pdf_file_path])

print(f"The Word file has been converted and saved as '{pdf_file_path}' in PDF format.")