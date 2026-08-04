from pathlib import Path
import csv

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# ---------------------------------
# Project paths
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDER = BASE_DIR / "data"


CSV_FILE = DATA_FOLDER / "historical_sora.csv"

EXCEL_FILE = DATA_FOLDER / "SORA_Report.xlsx"


def is_file_open(filename):

    if not filename.exists():

        return False

    try:

        with open(filename, "a"):

            pass

        return False

    except PermissionError:

        return True


def create_excel_report():

    if not CSV_FILE.exists():

        print("CSV file not found.")

        return

    if is_file_open(EXCEL_FILE):

        print()

        print("SORA_Report.xlsx is open.")

        print("Please close Excel and run again.")

        return

    records = []

    # ---------------------------------
    # Read CSV
    # ---------------------------------

    with open(CSV_FILE, "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            records.append(row)

    if len(records) == 0:

        print("No data available.")

        return

    # ---------------------------------
    # Latest first
    # ---------------------------------

    records.reverse()

    # ---------------------------------
    # Create workbook
    # ---------------------------------

    wb = Workbook()

    ws = wb.active

    ws.title = "Historical SORA"

    headers = ["Date", "Publication Date", "SORA"]

    ws.append(headers)

    # ---------------------------------
    # Header formatting
    # ---------------------------------

    for cell in ws[1]:

        cell.font = Font(bold=True)

        cell.fill = PatternFill("solid", fgColor="DDDDDD")

        cell.alignment = Alignment(horizontal="center", vertical="center")

    # ---------------------------------
    # Add data
    # ---------------------------------

    for row in records:

        ws.append([row["Date"], row["Publication Date"], float(row["SORA"])])

    # ---------------------------------
    # Center all cells
    # ---------------------------------

    for row in ws.iter_rows():

        for cell in row:

            cell.alignment = Alignment(horizontal="center", vertical="center")

    # ---------------------------------
    # SORA number format
    # ---------------------------------

    for cell in ws["C"][1:]:

        cell.number_format = "0.0000"

    # ---------------------------------
    # AutoFit columns
    # ---------------------------------

    for column_cells in ws.columns:

        max_length = 0

        column_letter = get_column_letter(column_cells[0].column)

        for cell in column_cells:

            if cell.value is not None:

                max_length = max(max_length, len(str(cell.value)))

        ws.column_dimensions[column_letter].width = max_length + 3

    # Freeze header

    ws.freeze_panes = "A2"

    # Save Excel

    wb.save(EXCEL_FILE)

    print("Excel report created successfully.")
