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

        label = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "label[for='ContentPlaceHolder1_ColumnsCheckBoxList_13']",
                )
            )
        )

        driver.execute_script("arguments[0].click();", label)

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

        driver.find_element(By.ID, "ContentPlaceHolder1_Button1").click()

        time.sleep(5)

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

                # Full row:
                # 2025 Sep 01 02 Sep 2025 0.7261

                if len(parts) >= 7 and parts[0].isdigit() and len(parts[0]) == 4:

                    current_year = parts[0]
                    current_month = parts[1]

                    day = parts[2]

                    publication = parts[3] + " " + parts[4] + " " + parts[5]

                    sora = parts[6]

                # Month change row:
                # Oct 01 02 Oct 2025 1.0402

                elif parts[0] in months:

                    current_month = parts[0]

                    day = parts[1]

                    publication = parts[2] + " " + parts[3] + " " + parts[4]

                    sora = parts[5]

                # Normal continuation:
                # 02 03 Sep 2025 0.9315

                else:

                    day = parts[0]

                    publication = parts[1] + " " + parts[2] + " " + parts[3]

                    sora = parts[4]

                if current_year is None:
                    continue

                data.append(
                    {
                        "Year": current_year,
                        "Month": current_month,
                        "Day": day,
                        "Publication Date": publication,
                        "SORA": sora,
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
