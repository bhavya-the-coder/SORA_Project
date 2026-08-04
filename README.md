# SORA Automation Project

An automated Python application that retrieves Singapore Overnight Rate Average (SORA) data, maintains historical records, generates Excel reports, and sends the report automatically by email.

The project runs daily using **GitHub Actions**, allowing the automation to operate without requiring a personal computer to be switched on.

---

# Features

* Automatically retrieves SORA data from the Monetary Authority of Singapore (MAS)
* Collects the latest SORA values using Selenium
* Maintains a historical SORA database in CSV format
* Generates Excel reports automatically
* Sends reports through Gmail SMTP
* Uses secure environment variables for email credentials
* Avoids unnecessary emails when there is no new SORA data
* Runs automatically every day using GitHub Actions

---

# Project Workflow

```
Daily at 9:00 AM Singapore Time

        |
        v

GitHub Actions starts workflow

        |
        v

Install Python environment

        |
        v

Install project dependencies

        |
        v

Run main.py

        |
        v

Fetch latest SORA data from MAS

        |
        v

Check for new SORA records

        |
        +----------------+
        |                |
        v                v

 New data found     No new data

        |                |
        v                v

Update CSV        Exit without email

        |
        v

Generate Excel report

        |
        v

Send email report

```

---

# Project Structure

```
SORA_Project/
│
├── main.py
│   Main automation controller
│
├── fetch_data.py
│   Retrieves SORA data from MAS using Selenium
│
├── process_data.py
│   Updates and maintains historical SORA records
│
├── create_report.py
│   Creates Excel reports using OpenPyXL
│
├── send_email.py
│   Sends reports through Gmail SMTP
│
├── requirements.txt
│   Python dependencies
│
├── .github/
│   └── workflows/
│       └── sora.yml
│           GitHub Actions automation schedule
│
├── data/
│   Generated CSV and Excel files (not stored in GitHub)
│
└── README.md
```

---

# Technologies Used

* Python 3.11
* Selenium
* OpenPyXL
* Python-dotenv
* Git
* GitHub Actions
* Gmail SMTP
* MAS SORA Data Source

---

# Installation (Local Setup)

## 1. Clone the repository

```powershell
git clone https://github.com/bhavya-the-coder/SORA_Project.git
```

Navigate into the project:

```powershell
cd SORA_Project
```

---

## 2. Create virtual environment

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# Email Configuration

The project uses environment variables to protect email credentials.

Create a file named:

```
.env
```

Add:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
RECEIVER_EMAIL=recipient_email@gmail.com
```

Do not upload this file to GitHub.

---

# Running Locally

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

Run:

```powershell
python main.py
```

The program will:

1. Fetch SORA data.
2. Check for new records.
3. Update the historical CSV.
4. Generate the Excel report.
5. Email the report if new data is available.

---

# GitHub Actions Automation

The project uses GitHub Actions to run automatically.

Workflow file:

```
.github/workflows/sora.yml
```

Schedule:

```
Every day at 9:00 AM Singapore Time
```

The workflow:

* Creates a temporary Python environment
* Installs dependencies
* Installs Chrome for Selenium
* Runs the automation
* Sends the generated report by email

---

# GitHub Secrets

Email credentials are stored securely using GitHub Actions Secrets.

Required secrets:

```
EMAIL_ADDRESS
EMAIL_APP_PASSWORD
RECEIVER_EMAIL
```

These values are never stored in the repository.

---

# Data Storage

Generated files:

```
data/
│
├── historical_sora.csv
└── SORA_Report.xlsx
```

are created during execution but are not committed to GitHub.

The GitHub Actions runner is temporary, so generated files are used only for report creation and email delivery.

---

# Error Handling

The automation includes checks for:

* Missing report files
* Failed email delivery
* Missing SORA data
* No new SORA records

The workflow output logs can be viewed from:

```
GitHub Repository
        |
        v
Actions
        |
        v
SORA Daily Automation
```

---

# Future Improvements

Possible future enhancements:

* Add detailed execution logs
* Store reports in cloud storage
* Add notifications for failed runs
* Create a dashboard for SORA trends
* Deploy as a web application

---

# Author

Bhavya

---

# License

This project is for personal automation and learning purposes.
