# SORA Automation Project

## Overview

This project automates the collection, processing, and reporting of SORA (Singapore Overnight Rate Average) values.

The automation workflow:

1. Fetches SORA data
2. Processes and cleans the data
3. Generates reports in Excel format
4. Saves historical SORA values for analysis

## Project Structure

```
SORA_Project/
│
├── main.py              # Runs the complete automation workflow
├── fetch_data.py        # Retrieves SORA values
├── process_data.py      # Cleans and processes data
├── create_report.py     # Generates Excel reports
│
├── requirements.txt     # Required Python packages
├── README.md            # Project documentation
└── data/                # Generated data files (not tracked by Git)
```

## Installation

Clone the repository:

```
git clone https://github.com/bhavya-the-coder/SORA_Project.git
```

Create a virtual environment:

```
python -m venv venv
```

Activate it:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Running the Automation

Run:

```
python main.py
```

The program will:

* Retrieve SORA values
* Process the data
* Generate the latest report

## Future Improvements

* Automatic daily execution
* Email report delivery
* Cloud-based scheduling
* Dashboard visualization
* Long-term SORA trend analysis
