
# AI-Powered Test Case Generator

## Overview
The **AI-Powered Test Case Generator** is a lightweight web application that helps QA engineers automatically generate structured test cases from natural language requirements. It saves time, reduces human error, and allows exporting test cases directly into Excel format for further use in QA workflows.

---

## Features
- Convert natural language requirements into structured test cases.
- Generate multiple test cases per requirement.
- Export generated test cases to Excel (`.xlsx` format) with proper formatting.
- Built with Python, Flask, OpenAI API, and OpenPyXL.
- Simple web interface for quick testing.

---

## Tech Stack
- **Backend:** Python, Flask  
- **AI Integration:** OpenAI API  
- **Excel Export:** OpenPyXL  
- **Frontend:** HTML/CSS  

---

## Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/test-case-generator.git
cd test-case-generator
````

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set your OpenAI API key**

* **Option 1 (local development):** Create a `.env` file in the root folder:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

* **Option 2 (deployment like PythonAnywhere):** Set it in the WSGI file or environment variables.

---

## Usage

1. **Run the app locally**

```bash
python app.py
```

2. Open your browser and navigate to:

```
http://127.0.0.1:5000
```

3. Enter your requirements and click **Generate**.
4. Download the generated test cases as an Excel file.

---

## Project Structure

```
test-case-generator/
│
├── app.py                  # Main Flask application
├── templates/
│   └── index.html          # Frontend HTML page
├── requirements.txt        # Python dependencies
├── README.md
└── .env                    # Local environment variables (not committed)
```

---

## Demo

* Input a sample requirement:
  `"User should be able to log in using valid credentials."`
* Generated test cases:

  * Login with valid email/password
  * Login with invalid password
  * Login with unregistered email, etc.
* Exported as Excel for QA tracking.

---

## Notes

* Keep your **OpenAI API key private**. Do not commit `.env` to GitHub.
* The tool uses OpenAI’s GPT model for test case generation, so ensure you have sufficient API quota.

---

## Author

Riya – QA Engineer & AI Enthusiast

```


Do you want me to do that next?
```

