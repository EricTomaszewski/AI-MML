# filename: read_and_amend_word_file.py
from docx import Document
from docx.shared import Pt

# Read the Word file
file_path = r'C:\Users\irene\!AI-LLM\AutoGenCV\coding\2023-10 - CV Eric TOMASZEWSKI.doc'
doc = Document(file_path)

# Change the font to Arial
for paragraph in doc.paragraphs:
    for run in paragraph.runs:
        run.font.name = 'Arial'
        run.font.size = Pt(12)  # Change the font size if needed

# Save the amended file
save_path = 'Amended.doc'
doc.save(save_path)

print(f"The Word file has been amended and saved as '{save_path}'.")