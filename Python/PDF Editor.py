import sys
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
import fnmatch


def rotate_pages(file, degrees):
    if (degrees % 90 != 0) | (degrees == 0):
        raise ValueError(
            "The degrees must be a multiple of 90, rotate_pages(file, degrees)"
        )
    if not file is None:
        raise ValueError("The file must be a PDF file, rotate_pages(file, degrees)")
    pdf_path = Path(file)
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()
    print("Number of pages is", len(reader.pages))

    for n in range(len(reader.pages)):
        page = writer.add_page(reader.pages[n])
        writer.pages[n].rotate(180)  # Degrees of Rotation
    return writer


def merger(file1, file2):
    if (file1 is None) | (file2 is None):
        raise ValueError("Both files must be PDF files")
    pdf_path1 = Path(file1)
    pdf_path2 = Path(file2)
    reader1 = PdfReader(str(pdf_path1))
    reader2 = PdfReader(str(pdf_path2))
    writer = PdfWriter()
    for n in range(len(reader1.pages)):
        writer.add_page(reader1.pages[n])
    for n in range(len(reader2.pages)):
        writer.add_page(reader2.pages[n])
    return writer


if __name__ == "__main__":

    PdfPattern = "fnmatch_*.pdf"

    PdfFunction = str(sys.argv[1])
    if PdfFunction is None:
        raise ValueError(
            "PdfFunction is required, PDF Editor.py <RotatePages/Merge> <PathOutput>"
        )

    PathOutput = sys.argv[2]
    if fnmatch.fnmatch(PathOutput, PdfPattern):
        raise ValueError(
            "Output Path is required, PDF Editor.py <RotatePages or Merge> <PathOutput.pdf>"
        )

    match PdfFunction:

        case "RotatePages":
            file = Path(sys.argv[3])
            if file is None:
                raise ValueError(
                    "File path is required, RotatePages <PathOutput> <PathInput> <Degrees>"
                )

            degrees = int(sys.argv[4])
            if degrees is None:
                raise ValueError(
                    "Degrees is required, RotatePages <PathOutput> <PathInput> <Degrees>"
                )
            writer = rotate_pages(file, degrees)

        case "Merge":
            file1 = Path(sys.argv[3])
            if file1 is None:
                raise ValueError(
                    "File1 path is required, Merge <PathOutput> <PathInput1> <PathInput2>"
                )
            file2 = Path(sys.argv[4])
            if file2 is None:
                raise ValueError(
                    "File2 path is required, Merge <PathOutput> <PathInput1> <PathInput2>"
                )
            writer = merger(file1, file2)

    output = open(PathOutput, "wb")
    writer.write(output)
