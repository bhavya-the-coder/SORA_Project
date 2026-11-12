from fetch_data import fetch_sora
from process_data import save_to_csv, save_domestic_to_csv
from create_report import create_excel_report, create_domestic_interest_rates_report
from send_email import send_email


def main():

    print()
    print("==============================")
    print(" SORA UPDATE STARTED")
    print("==============================")
    print()

    print("Fetching SORA data from MAS...")
    print()

    result = fetch_sora()

    data = result["sora"]
    domestic_data = result["domestic"]

    if len(data) == 0:

        print("No SORA data found.")

        return

    print(f"Retrieved {len(data)} SORA records.")
    print(f"Retrieved {len(domestic_data)} Domestic Interest Rates records.")

    print()

    print("Updating SORA CSV database...")

    updated = save_to_csv(data)

    print()

    print("Updating Domestic Interest Rates CSV database...")

    save_domestic_to_csv(domestic_data)

    if not updated:

        print()
        print("No report generated.")
        print("No email sent.")
        print()
        print("SORA update completed.")
        print()

        return

    print()

    print("Generating SORA Excel report...")

    create_excel_report()

    print()

    print("Generating Domestic Interest Rates Excel report...")

    create_domestic_interest_rates_report()

    print()

    print("Sending email...")

    send_email()

    print()

    print("==============================")
    print(" SORA UPDATE COMPLETED")
    print("==============================")
    print()


if __name__ == "__main__":

    main()
