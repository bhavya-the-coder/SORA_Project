from pathlib import Path
import csv
from datetime import datetime

# ---------------------------------
# Project paths
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_FOLDER = BASE_DIR / "data"

FILE_PATH = DATA_FOLDER / "historical_sora.csv"


def save_to_csv(data):

    DATA_FOLDER.mkdir(exist_ok=True)

    existing_records = {}

    new_data_found = False

    # ---------------------------------
    # Read existing CSV
    # ---------------------------------

    if FILE_PATH.exists():

        with open(FILE_PATH, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                existing_records[row["Date"]] = row

    # ---------------------------------
    # Current retrieval time
    # ---------------------------------

    retrieved_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    # ---------------------------------
    # Add only NEW records
    # ---------------------------------

    for item in data:

        date = datetime.strptime(
            f"{item['Year']} {item['Month']} {item['Day']}",
            "%Y %b %d",
        ).strftime("%Y-%b-%d")

        publication = datetime.strptime(
            item["Publication Date"],
            "%d %b %Y",
        ).strftime("%d-%b-%Y")

        if date not in existing_records:

            existing_records[date] = {
                "Date": date,
                "Publication Date": publication,
                "SORA": item["SORA"],
                "Retrieved At": retrieved_time,
            }

            new_data_found = True

    if not new_data_found:

        print("No new SORA data found.")

        return False

    # ---------------------------------
    # Sort oldest to newest
    # ---------------------------------

    sorted_records = sorted(
        existing_records.values(),
        key=lambda x: datetime.strptime(x["Date"], "%Y-%b-%d"),
    )

    # ---------------------------------
    # Save CSV
    # ---------------------------------

    with open(FILE_PATH, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "Date",
                "Publication Date",
                "SORA",
                "Retrieved At",
            ],
        )

        writer.writeheader()

        writer.writerows(sorted_records)

    print("New SORA data added successfully.")

    return True
