import os
import json
import io
import re
from flask import Flask, request, jsonify, send_file, render_template
from openpyxl import Workbook
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-8b-instant")
# Initialize Flask app
app = Flask(__name__)

# -----------------------
# Groq Config
# -----------------------
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -----------------------
# Frontend route
# -----------------------
@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")

# -----------------------
# Export test cases to Excel
# -----------------------
@app.route("/export/excel", methods=["POST"])
def export_excel():
    data = request.get_json()
    test_cases = data.get("test_cases", [])

    if not test_cases:
        return jsonify({"error": "No test cases provided"}), 400

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

    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)

    return send_file(
        file_stream,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name="test_cases.xlsx"
    )

# -----------------------
# Generate + Export
# -----------------------
@app.route("/generate-and-export", methods=["POST"])
def generate_and_export():
    try:
        print("STEP 1: Request received")

        data = request.get_json()
        requirements = data.get("requirements", "")
        print("STEP 2:", requirements)

        if not requirements:
            return jsonify({"error": "Requirements text is required"}), 400

        # Prompt
        prompt = f"""
You are an expert QA test designer.

Generate exactly 5 test cases in STRICT JSON format.

Return ONLY a JSON array.

[
  {{
    "id": "TC1",
    "title": "...",
    "preconditions": "...",
    "steps": ["step1", "step2"],
    "expected_result": "..."
  }}
]

Requirement:
{requirements}
"""

        print("STEP 3: Calling Groq")
        print(client.models.list())
        # -----------------------
        # Groq API Call
        # -----------------------
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # or mixtral
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        ai_output = response.choices[0].message.content.strip()

        # Clean markdown if present
        ai_output = ai_output.replace("```json", "").replace("```", "").strip()

        # Extract JSON
        match = re.search(r'\[.*\]', ai_output, re.DOTALL)
        if match:
            ai_output = match.group(0)

        try:
            test_cases = json.loads(ai_output)
        except json.JSONDecodeError:
            print("INVALID JSON:", ai_output)
            return jsonify({
                "error": "Invalid JSON from model",
                "raw_output": ai_output
            }), 500

        print("STEP 4: Creating Excel")

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

        file_stream = io.BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        print("STEP 5: Sending file")

        return send_file(
            file_stream,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name="test_cases.xlsx"
        )

    except Exception as e:
        import traceback
        print("ERROR:")
        traceback.print_exc()
        return str(e), 500

# -----------------------
# Run app
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)