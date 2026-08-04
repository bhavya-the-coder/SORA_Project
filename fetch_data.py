from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
from dateutil.relativedelta import relativedelta


URL = "https://eservices.mas.gov.sg/statistics/dir/DomesticInterestRates.aspx"


def fetch_sora():

    today = datetime.today()

    end_year = today.year
    end_month = today.strftime("%b")

    start = today - relativedelta(months=11)

    start_year = start.year
    start_month = start.strftime("%b")

    # ------------------------
    # Chrome options
    # ------------------------

    options = webdriver.ChromeOptions()

    # Run Chrome without opening a window
    options.add_argument("--headless")

    # Required for cloud environments
    options.add_argument("--no-sandbox")

    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 20)

    data = []

    try:

        driver.get(URL)

        # ------------------------
        # Select SORA
        # ------------------------

        label = wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "label[for='ContentPlaceHolder1_ColumnsCheckBoxList_13']",
                )
            )
        )

        driver.execute_script("arguments[0].click();", label)

        # ------------------------
        # Select Start Year
        # ------------------------

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_StartYearDropDownList")
        ).select_by_visible_text(str(start_year))

        # ------------------------
        # Select End Year
        # ------------------------

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_EndYearDropDownList")
        ).select_by_visible_text(str(end_year))

        # ------------------------
        # Select Start Month
        # ------------------------

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_StartMonthDropDownList")
        ).select_by_visible_text(start_month)

        # ------------------------
        # Select End Month
        # ------------------------

        Select(
            driver.find_element(By.ID, "ContentPlaceHolder1_EndMonthDropDownList")
        ).select_by_visible_text(end_month)

        # ------------------------
        # Click Display
        # ------------------------

        driver.find_element(By.ID, "ContentPlaceHolder1_Button1").click()

        # Wait for table

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

        tables = driver.find_elements(By.TAG_NAME, "table")

        print()

        print(f"Tables found: {len(tables)}")

        # ------------------------
        # Extract SORA table
        # ------------------------

        for table in tables:

            rows = table.find_elements(By.TAG_NAME, "tr")

            for row in rows:

                cells = row.find_elements(By.TAG_NAME, "td")

                if len(cells) != 5:

                    continue

                year = cells[0].text.strip()

                if not year.isdigit():

                    continue

                data.append(
                    {
                        "Year": year,
                        "Month": cells[1].text.strip(),
                        "Day": cells[2].text.strip(),
                        "Publication Date": cells[3].text.strip(),
                        "SORA": cells[4].text.strip(),
                    }
                )

    finally:

        driver.quit()

    return data
