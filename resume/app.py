from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text_from_pdf
from ai_analyzer import analyze_resume_with_ai
import json
import re
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return {"status": "Backend Running"}


@app.route("/analyze", methods=["POST"])
def analyze():
    print("🔥 Request received")

    # ✅ Check file
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["resume"]
    job_desc = request.form.get("job_description", "")

    # ✅ Allow job role (short input allowed)
    if not job_desc or len(job_desc.strip()) < 2:
        return jsonify({"error": "Enter a job role or description"}), 400

    # ✅ Validate PDF (case insensitive)
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    file_path = "temp_resume.pdf"
    file.save(file_path)

    try:
        # ✅ Extract resume text
        text = extract_text_from_pdf(file_path)

        if not text or len(text.strip()) < 100:
            return jsonify({"error": "Resume has no readable content"}), 400

        # ✅ Basic resume validation
        resume_keywords = [
            "education", "skills", "experience",
            "project", "internship", "contact", "summary"
        ]

        text_lower = text.lower()
        match_count = sum(1 for word in resume_keywords if word in text_lower)

        if match_count < 2:
            return jsonify({"error": "Invalid resume content"}), 400

        # 🔥 AI ANALYSIS
        ai_output = analyze_resume_with_ai(text, job_desc)
        print("🤖 RAW AI OUTPUT:", ai_output)

        # ✅ Clean AI response
        clean_output = ai_output.replace("```json", "").replace("```", "").strip()
        match = re.search(r"\{.*\}", clean_output, re.DOTALL)

        if not match:
            return jsonify({
                "score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "suggestions": ["AI response format issue"]
            })

        parsed = json.loads(match.group())

        # 🔥 SMART ERROR HANDLING (IMPORTANT)
        if parsed.get("ats_score", 0) == 0 and not parsed.get("matched_skills"):
            if parsed.get("suggestions"):
                return jsonify({
                    "error": parsed["suggestions"][0]
                }), 400

        # ✅ Normal response
        return jsonify({
            "score": parsed.get("ats_score", 0),
            "matched_skills": parsed.get("matched_skills", []),
            "missing_skills": parsed.get("missing_skills", []),
            "suggestions": parsed.get("suggestions", [])
        })

    except Exception as e:
        import traceback
        traceback.print_exc()

        return jsonify({
            "error": str(e),
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": []
        }), 500

    finally:
        # ✅ Clean temp file
        if os.path.exists(file_path):
            os.remove(file_path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)