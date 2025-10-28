import argparse
import os
import pandas as pd
from pdf2image import convert_from_path
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def pdf_to_text(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path)
        for img in images:
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
    return text

def process_pdf(pdf_path):
    if not os.path.isfile(pdf_path):
        print(f"File not found: {pdf_path}")
        return
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_path = f"{base_name}.txt"
    print(f"Processing: {pdf_path}")
    text = pdf_to_text(pdf_path)
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"Saved OCR text to {txt_path}")

def process_excel(file_path):
    df = pd.read_excel(file_path)
    if 'path' not in df.columns:
        print(f"No 'path' column found in {file_path}")
        return
    for pdf_path in df['path'].dropna():
        process_pdf(str(pdf_path))

def process_txt_list(txt_file):
    with open(txt_file, 'r') as f:
        paths = [line.strip() for line in f if line.strip()]
    for pdf_path in paths:
        process_pdf(pdf_path)

def main():
    parser = argparse.ArgumentParser(description="Extract OCR text from local PDFs.")
    parser.add_argument("--xlsx", help="Path to a single .xlsx file with a 'path' column")
    parser.add_argument("--path", help="Direct path to a single PDF file")
    parser.add_argument("--txtlist", help="Path to a .txt file with newline-separated PDF paths")
    args = parser.parse_args()

    if args.xlsx:
        process_excel(args.xlsx)
    elif args.path:
        process_pdf(args.path)
    elif args.txtlist:
        process_txt_list(args.txtlist)
    else:
        print("Please provide one of --xlsx, --path, or --txtlist")

if __name__ == "__main__":
    main()
