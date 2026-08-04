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
    # Add / update MAS records
    # ---------------------------------

    for item in data:

        date = datetime.strptime(
            f"{item['Year']} {item['Month']} {item['Day']}", "%Y %b %d"
        ).strftime("%Y-%b-%d")

        publication = datetime.strptime(item["Publication Date"], "%d %b %Y").strftime(
            "%d-%b-%Y"
        )

        # Existing date

        if date in existing_records:

            existing_records[date]["Publication Date"] = publication

            existing_records[date]["SORA"] = item["SORA"]

        # New date

        else:

            existing_records[date] = {
                "Date": date,
                "Publication Date": publication,
                "SORA": item["SORA"],
                "Retrieved At": retrieved_time,
            }

    # ---------------------------------
    # Sort records oldest to newest
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
            file, fieldnames=["Date", "Publication Date", "SORA", "Retrieved At"]
        )

        writer.writeheader()

        writer.writerows(sorted_records)

    print(f"{len(data)} records processed successfully.")
