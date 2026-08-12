from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time


URL = "https://eservices.mas.gov.sg/statistics/dir/DomesticInterestRates.aspx"


def fetch_sora():

    today = datetime.today()

    end_year = today.year
    end_month = today.strftime("%b")

    start = today - relativedelta(months=11)

    start_year = start.year
    start_month = start.strftime("%b")

    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 30)

    data = []

    try:

        driver.get(URL)

        # ---------------------------------
        # Select SORA columns
        # ---------------------------------

        checkbox_ids = [
            "ContentPlaceHolder1_ColumnsCheckBoxList_13",  # SORA
            "ContentPlaceHolder1_ColumnsCheckBoxList_18",  # Aggregate Volume
            "ContentPlaceHolder1_ColumnsCheckBoxList_19",  # Highest Rate
            "ContentPlaceHolder1_ColumnsCheckBoxList_20",  # Lowest Rate
        ]

        for checkbox_id in checkbox_ids:

            checkbox = wait.until(EC.presence_of_element_located((By.ID, checkbox_id)))

            if not checkbox.is_selected():

                driver.execute_script("arguments[0].click();", checkbox)

        # ---------------------------------
        # Select date range
        # ---------------------------------

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_StartYearDropDownList")
        ).select_by_visible_text(str(start_year))

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_EndYearDropDownList")
        ).select_by_visible_text(str(end_year))

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_StartMonthDropDownList")
        ).select_by_visible_text(start_month)

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_EndMonthDropDownList")
        ).select_by_visible_text(end_month)

        # ---------------------------------
        # Display results
        # ---------------------------------

        driver.find_element(By.ID, "ContentPlaceHolder1_Button1").click()

        time.sleep(5)

        # ---------------------------------
        # Read table
        # ---------------------------------

        table = driver.find_element(By.TAG_NAME, "table")

        rows = table.find_elements(By.TAG_NAME, "tr")

        current_year = None
        current_month = None

        months = {
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        }

        for row in rows:

            text = row.text.strip()

            if not text:
                continue

            if "DATE" in text or "SORA" in text:
                continue

            parts = text.split()

            try:

                # ---------------------------------
                # Full row
                #
                # 2026 Aug 03 04 Aug 2026
                # 0.8830 2597 1.0500 0.4500
                # ---------------------------------

                if len(parts) >= 8 and parts[0].isdigit() and len(parts[0]) == 4:

                    current_year = parts[0]
                    current_month = parts[1]

                    day = parts[2]

                    publication = parts[3] + " " + parts[4] + " " + parts[5]

                    sora = parts[6]
                    aggregate_volume = parts[7]
                    highest_rate = parts[8]
                    lowest_rate = parts[9]

                # ---------------------------------
                # Month change row
                #
                # Aug 03 04 Aug 2026
                # 0.8830 2597 1.0500 0.4500
                # ---------------------------------

                elif parts[0] in months:

                    current_month = parts[0]

                    day = parts[1]

                    publication = parts[2] + " " + parts[3] + " " + parts[4]

                    sora = parts[5]
                    aggregate_volume = parts[6]
                    highest_rate = parts[7]
                    lowest_rate = parts[8]

                # ---------------------------------
                # Normal continuation
                #
                # 03 04 Aug 2026
                # 0.8830 2597 1.0500 0.4500
                # ---------------------------------

                else:

                    day = parts[0]

                    publication = parts[1] + " " + parts[2] + " " + parts[3]

                    sora = parts[4]
                    aggregate_volume = parts[5]
                    highest_rate = parts[6]
                    lowest_rate = parts[7]

                if current_year is None:
                    continue

                data.append(
                    {
                        "Year": current_year,
                        "Month": current_month,
                        "Day": day,
                        "Publication Date": publication,
                        "SORA": sora,
                        "Aggregate Volume": aggregate_volume,
                        "Highest Rate": highest_rate,
                        "Lowest Rate": lowest_rate,
                    }
                )

            except Exception:

                continue

    finally:

        driver.quit()

    print()
    print(f"Records extracted: {len(data)}")
    print()

    return data


if __name__ == "__main__":
    fetch_sora()
