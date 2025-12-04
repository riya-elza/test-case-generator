import os
import json
import io
from openai import OpenAI
from flask import Flask, request, jsonify, send_file, render_template
from openpyxl import Workbook
from dotenv import load_dotenv
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------
# Frontend route
# -----------------------
@app.route("/", methods=["GET"])
def home_page():
    """
    Serves the HTML frontend for the QA Test Case Generator
    """
    return render_template("index.html")


# -----------------------
# Export test cases to Excel
# -----------------------
@app.route("/export/excel", methods=["POST"])
def export_excel():
    """
    Accepts JSON test cases and returns them as an Excel (.xlsx) file.
    """
    data = request.get_json()
    test_cases = data.get("test_cases", [])

    if not test_cases:
        return jsonify({"error": "No test cases provided"}), 400

    # Create Excel workbook in memory
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    # Add header row
    ws.append(["ID", "Title", "Preconditions", "Steps", "Expected Result"])

    # Fill data rows
    for tc in test_cases:
        ws.append([
            tc.get("id", ""),
            tc.get("title", ""),
            tc.get("preconditions", ""),
            "\n".join(tc.get("steps", [])),
            tc.get("expected_result", "")
        ])

    # Save workbook to memory
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    # Send Excel file as response
    return send_file(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="test_cases.xlsx"
    )


# -----------------------
# Combined route: generate + export
# -----------------------
@app.route("/generate-and-export", methods=["POST"])
def generate_and_export():
    """
    Combines test case generation and Excel export in a single request.
    Returns the Excel file immediately after generating test cases.
    """
    data = request.get_json()
    requirements = data.get("requirements", "")

    if not requirements:
        return jsonify({"error": "Requirements text is required"}), 400

    # Prompt to generate test cases in JSON format
    prompt = f"""
    You are an expert QA test designer.

    Generate 5 detailed test cases in valid JSON format ONLY for the below requirement:

    {requirements}

    The output MUST be a JSON array of objects.

    Each test case must contain:
    - id
    - title
    - preconditions
    - steps (as an array)
    - expected_result
    """

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response.choices[0].message.content.strip()
    ai_output = ai_output.replace("```json", "").replace("```", "").strip()

    # Convert AI output to JSON
    try:
        test_cases = json.loads(ai_output)
    except json.JSONDecodeError:
        return jsonify({"error": "Model returned invalid JSON", "raw_output": ai_output}), 500

    # Create Excel workbook in memory
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"
    ws.append(["ID", "Title", "Preconditions", "Steps", "Expected Result"])

    for tc in test_cases:
        ws.append([
            tc.get("id", ""),
            tc.get("title", ""),
            tc.get("preconditions", ""),
            "\n".join(tc.get("steps", [])),
            tc.get("expected_result", "")
        ])

    # Save workbook to memory
    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    # Send Excel file as response
    return send_file(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="test_cases.xlsx"
    )


# -----------------------
# Run Flask app
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
