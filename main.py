from fetch_data import fetch_sora
from process_data import save_to_csv
from create_report import create_excel_report


def main():

    print()
    print("==============================")
    print(" SORA UPDATE STARTED")
    print("==============================")
    print()

    print("Fetching SORA data from MAS...")
    print()

    data = fetch_sora()

    if len(data) == 0:

        print("No SORA data found.")

        return

    print(f"Retrieved {len(data)} records.")

    print()

    print("Updating CSV database...")

    save_to_csv(data)

    print()

    print("Generating Excel report...")

    create_excel_report()

    print()

    print("SORA update completed successfully.")

    print()


if __name__ == "__main__":

    main()
