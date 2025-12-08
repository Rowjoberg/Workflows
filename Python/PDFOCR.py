import argparse
import csv
import re
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path

# Configure tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)


def pdf_to_text(pdf_path):
    """Convert a PDF to text using OCR."""
    text = ""
    try:
        images = convert_from_path(str(pdf_path))
        for img in images:
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"Error converting {pdf_path}: {e}")
    return text


def load_match_strings(match_arg):
    """Load match strings from a file or single string."""
    match_path = Path(match_arg)
    if match_path.is_file():
        with match_path.open("r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return [match_arg]


def extract_actions_taken(text, verbose=False):
    """
    Extract descriptive text between AMP and ALL TESTS, removing AMP lines.
    Handles case-insensitivity and ignores AMP followed by uppercase letters.
    """
    # Pattern explanation:
    # (?i) → case-insensitive
    # \\sAMP[^A-Z] → AMP followed by something that is NOT an uppercase letter
    pattern = r"(?i)(\sAMP[^A-Z][\s\S]*?)ALL TESTS ARE PERFORMED"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        if verbose:
            print("Summary not found")
        return ""

    raw_section = match.group(1)
    # Handle hyphen or space after AMP (case-insensitive)
    amp_start = re.search(r"(?i) AMP[- ]?", raw_section)
    if amp_start:
        raw_section = raw_section[amp_start.start() :]

    cleaned_lines = []
    for line in raw_section.splitlines():
        # Remove lines containing AMP (case-insensitive)
        if not re.search(r"(?i)\bAMP\b", line):
            if line.strip():
                cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines)


def extract_fields(text, verbose=False):
    date_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{8})"
    repair_date_match = re.search(rf"Repair / Overhaul Date:\s*{date_pattern}", text)
    serial_number_match = re.search(r"20\d{8}", text)
    manufacture_date_match = re.search(rf"Date of Manufacture:\s*{date_pattern}", text)
    job_no_match = re.search(r"Job No:\s*(\d{7})", text)

    return {
        "Repair/Overhaul Date": repair_date_match.group(1) if repair_date_match else "",
        "Serial Number": serial_number_match.group(0) if serial_number_match else "",
        "Date of Manufacture": (
            manufacture_date_match.group(1) if manufacture_date_match else ""
        ),
        "Job No": job_no_match.group(1) if job_no_match else "",
        "Actions Taken": extract_actions_taken(text, verbose),
    }


def check_matches(text, match_strings, case_sensitive=False):
    if case_sensitive:
        return [m for m in match_strings if m in text]
    else:
        text_lower = text.lower()
        return [m for m in match_strings if m.lower() in text_lower]


def process_pdf(
    pdf_path,
    export_txt,
    csv_writer,
    match_strings,
    verbose,
    csv_path_for_export,
    summary,
    match_case,
):
    try:
        summary["processed"] += 1
        if not pdf_path.is_file():
            if verbose:
                print(f"File not found: {pdf_path}")
            summary["errors"] += 1
            return

        if verbose:
            print(f"Processing: {pdf_path}")
        text = pdf_to_text(pdf_path)

        matched_strings = check_matches(text, match_strings, case_sensitive=match_case)
        if not matched_strings:
            if verbose:
                print(f"No matches found in {pdf_path}")
            return

        summary["matches"] += 1
        fields = extract_fields(text, verbose)

        if export_txt:
            export_txt_path = Path(export_txt)
            export_txt_path.mkdir(parents=True, exist_ok=True)
            txt_path = export_txt_path / f"{pdf_path.stem}.txt"
            with txt_path.open("w", encoding="utf-8") as f:
                f.write(text)
            if verbose:
                print(f"Saved OCR text to {txt_path}")

        if csv_writer:
            hyperlink = f'=HYPERLINK("{pdf_path}")'
            csv_writer.writerow(
                [
                    hyperlink,
                    ", ".join(matched_strings),
                    fields["Repair/Overhaul Date"],
                    fields["Serial Number"],
                    fields["Date of Manufacture"],
                    fields["Job No"],
                    f'"{fields["Actions Taken"]}"',
                ]
            )
    except Exception as e:
        if verbose:
            print(f"Error processing {pdf_path}: {e}")
        summary["errors"] += 1


def parse_pdf_paths_from_txt(txt_path):
    paths = []
    with txt_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.endswith(".pdf"):
                p = Path(line)
                csv_path = f'=HYPERLINK("{line}")'
                paths.append((p, csv_path))
    return paths


def process_path(
    path_arg,
    export_txt,
    csv_writer,
    match_strings,
    verbose,
    summary,
    match_case,
    limit=None,
):
    path_obj = Path(path_arg)
    if path_obj.is_dir():
        for pdf_file in path_obj.rglob("*.pdf"):
            process_pdf(
                pdf_file,
                export_txt,
                csv_writer,
                match_strings,
                verbose,
                f'=HYPERLINK("{pdf_file}")',
                summary,
                match_case,
            )
            # Stop if we hit the limit
            if limit is not None and summary["matches"] >= limit:
                if verbose:
                    print(f"Match limit ({limit}) reached. Stopping.")
                break

    elif path_obj.is_file():
        if path_obj.suffix.lower() == ".pdf":
            process_pdf(
                path_obj,
                export_txt,
                csv_writer,
                match_strings,
                verbose,
                f'=HYPERLINK("{path_obj}")',
                summary,
                match_case,
            )
        elif path_obj.suffix.lower() == ".txt":
            pdf_paths = parse_pdf_paths_from_txt(path_obj)
            for actual_path, csv_path in pdf_paths:
                process_pdf(
                    actual_path,
                    export_txt,
                    csv_writer,
                    match_strings,
                    verbose,
                    csv_path,
                    summary,
                    match_case,
                )
                # Stop if we hit the limit
                if limit is not None and summary["matches"] >= limit:
                    if verbose:
                        print(f"Match limit ({limit}) reached. Stopping.")
                    break
        else:
            print(
                f"Invalid file type: {path_obj}. Must be a PDF, TXT, or directory containing PDFs."
            )
    else:
        print(
            f"Invalid path: {path_obj}. Must be a PDF file, TXT file, or directory containing PDFs."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Extract OCR text from PDFs and check for matches."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Path to a PDF file, directory, or TXT file with PDF paths",
    )
    parser.add_argument(
        "--match",
        required=True,
        help="Single string or path to a text file with match strings",
    )

    parser.add_argument(
        "--match-case",
        action="store_true",
        help="Enable case-sensitive matching for match strings",
    )
    parser.add_argument(
        "--export-txt", help="Directory to save extracted text files for matched PDFs"
    )
    parser.add_argument(
        "--export-csv", help="Path or directory to save CSV summary of matched PDFs"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    parser.add_argument(
        "--limit",
        type=int,
        help="Stop processing after this many files are found to have matches",
    )

    args = parser.parse_args()

    match_strings = load_match_strings(args.match)
    match_case = args.match_case

    csv_writer = None
    csv_file = None
    if args.export_csv:
        export_csv_path = Path(args.export_csv)
        if export_csv_path.is_dir():
            export_csv_path = export_csv_path / "summary.csv"
        export_csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_file = export_csv_path.open("w", newline="", encoding="utf-8")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            [
                "Path",
                "Equipment Type",
                "Repair/Overhaul Date",
                "Serial Number",
                "Date of Manufacture",
                "Job No",
                "Actions Taken",
            ]
        )

    summary = {"processed": 0, "matches": 0, "errors": 0}

    process_path(
        args.path,
        args.export_txt,
        csv_writer,
        match_strings,
        args.verbose,
        summary,
        match_case,
        limit=args.limit,
    )

    if csv_file:
        csv_file.close()

    print("\nSummary Report:")
    print(f"Total PDFs processed: {summary['processed']}")
    print(f"Total matches found: {summary['matches']}")
    print(f"Total errors: {summary['errors']}")


if __name__ == "__main__":
    main()
