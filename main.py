from fetch_data import fetch_sora
from process_data import save_to_csv
from create_report import create_excel_report
from send_email import send_email


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

    updated = save_to_csv(data)

    if not updated:

        print()
        print("No report generated.")
        print("No email sent.")
        print()
        print("SORA update completed.")
        print()

        return

    print()

    print("Generating Excel report...")

    create_excel_report()

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
