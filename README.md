# SORA Automation Project

An automated Python application that retrieves Singapore Overnight Rate Average (SORA) data, maintains historical records, generates Excel reports, and sends the report automatically by email.

The project is scheduled using **cron-job.org** and executed through **GitHub Actions**, allowing the automation to run daily without requiring a personal computer to be switched on.

---

# Features

* Automatically retrieves SORA data from the Monetary Authority of Singapore (MAS)
* Collects the latest SORA values using Selenium
* Maintains a historical SORA database in CSV format
* Generates Excel reports automatically
* Sends reports through Gmail SMTP
* Supports multiple email recipients and CC recipients
* Uses secure environment variables and GitHub Secrets for email credentials
* Avoids unnecessary emails when there is no new SORA data
* Uses cron-job.org for daily scheduling
* Uses GitHub Actions as the cloud execution environment
* Runs completely automatically without requiring a local computer

---

# Project Workflow

```text
Daily at 9:00 AM Singapore Time

        |
        v

cron-job.org scheduler starts

        |
        v

Send API request to GitHub Actions

        |
        v

GitHub Actions workflow starts

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

```text
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
│           GitHub Actions workflow (triggered via workflow_dispatch)
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
* cron-job.org
* Gmail SMTP
* GitHub REST API
* MAS SORA Data Source

---

# Installation (Local Setup)

## 1. Clone the repository

```bash
git clone https://github.com/bhavya-the-coder/SORA_Project.git
```

Navigate into the project:

```bash
cd SORA_Project
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Email Configuration

The project uses environment variables to protect email credentials.

Create a file named:

```text
.env
```

Add the following:

```text
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password
RECEIVER_EMAILS=recipient@gmail.com,another_recipient@gmail.com
CC_EMAILS=cc_email@gmail.com,another_cc@gmail.com
```

Multiple email addresses can be separated using commas.

Do **not** upload this file to GitHub.

---

# Running Locally

Activate the virtual environment:

```bash
venv\Scripts\activate
```

Run:

```bash
python main.py
```

The program will:

1. Fetch the latest SORA data.
2. Check for new records.
3. Update the historical CSV.
4. Generate an Excel report.
5. Email the report if new data is available.

---

# Automation Setup

The project uses **cron-job.org** as the scheduler and **GitHub Actions** as the execution environment.

The workflow is triggered using GitHub's **workflow_dispatch** API instead of GitHub's built-in scheduler.

Workflow file:

```text
.github/workflows/sora.yml
```

Daily automation flow:

```text
cron-job.org
      |
      v
GitHub REST API
      |
      v
workflow_dispatch
      |
      v
GitHub Actions
      |
      v
Run Python automation
      |
      v
Generate report
      |
      v
Send email
```

The GitHub Actions workflow:

* Creates a temporary Ubuntu environment
* Installs Python and project dependencies
* Installs Google Chrome for Selenium
* Runs the automation
* Sends the generated report by email

Since the workflow runs on GitHub-hosted runners, your computer does not need to be switched on.

---

# cron-job.org Configuration

The project uses **cron-job.org** to trigger the GitHub Actions workflow every day.

Configuration:

```text
Method:
POST

Schedule:
Daily at 9:00 AM Singapore Time

Branch:
main
```

Request body:

```json
{
  "ref": "main"
}
```

The request is authenticated using a GitHub Personal Access Token stored securely within cron-job.org.

---

# GitHub Secrets

Email credentials are stored securely using GitHub Actions Secrets.

Required secrets:

```text
EMAIL_ADDRESS
EMAIL_APP_PASSWORD
RECEIVER_EMAILS
CC_EMAILS
```

These values are never stored in the repository.

---

# Data Storage

Generated files:

```text
data/
│
├── historical_sora.csv
└── SORA_Report.xlsx
```

are created during execution but are not committed to GitHub.

The GitHub Actions runner is temporary, so generated files exist only for the duration of the workflow and are used to create and email the report.

---

# Error Handling

The automation includes checks for:

* Missing report files
* Failed email delivery
* Missing SORA data
* No new SORA records
* Selenium execution failures

Workflow logs can be viewed from:

```text
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

Possible future enhancements include:

* Store historical reports in cloud storage
* Add automatic notifications for failed workflows
* Build a dashboard to visualize SORA trends
* Containerize the application using Docker
* Add unit and integration tests
* Package the project as a reusable Python application

---

# Author

**Bhavya**

---

# License

This project is intended for personal automation, educational purposes, and learning GitHub Actions, Selenium, and Python automation.