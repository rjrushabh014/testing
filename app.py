from flask import Flask, render_template, request, redirect, url_for, session
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  

genai.configure(api_key="AIzaSyBFcVdWmupoYN_u6yH4lykcdx6qymaiXLY")  

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "You are a healthcare chatbot.",
                "Start by asking the user for their name, age, and gender.",
                "Then, inquire about their symptoms by asking up to five relevant questions, one at a time. Whatever they say, ask a related question to it.",
                "Based on the symptoms provided, generate a list of three potential diseases (number them as 1., 2., 3.), each on a new line with descriptions.",
                "Do not just acknowledge symptoms. Instead, ask follow-up questions or give potential causes.",
                "Every response must include a disclaimer: 'This is not a medical diagnosis. Please consult a doctor.'"
            ],
        },
        {
            "role": "model",
            "parts": [
                "Hello! I'm here to help. To begin, can you please share your name, age, and gender?",
            ],
        },
    ]
)

chat_history = []

@app.route("/", methods=["GET", "POST"])
def homepage():
    """
    Renders the homepage where the user completes the initial assessment form.
    """
    if request.method == "POST":
        age = request.form.get("age")
        sex = request.form.get("sex")
        try:
            age = int(age)
        except (ValueError, TypeError):
            return render_template("index.html", error="Please enter a valid age.")
        if age < 1 or age > 130:
            return render_template("index.html", error="Age must be between 1 and 130.")
        if not sex:
            return render_template("index.html", error="Please select your sex.")
        session["age"] = age
        session["sex"] = sex
        return redirect(url_for("chat"))
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    """
    Handles chat interactions. When the chatbot response includes three disease outputs,
    stores the result and redirects to the assessment complete page.
    """
    global chat_history
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            chat_history.append({"role": "user", "content": user_input})
            greeting_keywords = ["hi", "hello", "hey", "hola", "greetings"]
            if any(greeting in user_input.lower() for greeting in greeting_keywords):
                chatbot_response = ("Hello! How can I assist you today? Please describe your symptoms. "
                                    "This is not a medical diagnosis. Please consult a doctor.")
                chat_history.append({"role": "model", "content": chatbot_response})
            else:
                response = chat_session.send_message(user_input)
                chatbot_response = ""
                if hasattr(response, "_result") and response._result.candidates:
                    candidate = response._result.candidates[0]
                    parts = candidate.content.parts if hasattr(candidate.content, "parts") else []
                    if parts:
                        chatbot_response = parts[0].text if hasattr(parts[0], "text") else "No valid response found"
                chat_history.append({"role": "model", "content": chatbot_response})
                if "1." in chatbot_response and "2." in chatbot_response and "3." in chatbot_response:
                    session['assessment_result'] = chatbot_response
                    return redirect(url_for("assessment_complete"))
    return render_template("homepage.html", chat_history=chat_history)

@app.route("/assessment_complete", methods=["GET"])
def assessment_complete():
    """
    Renders the assessment complete page.
    """
    result = session.get('assessment_result', '')
    return render_template("Assesment_complete.html", result=result)

@app.route("/possible_disease", methods=["GET"])
def possible_disease():
    """
    Parses the assessment result and renders the possible disease page.
    """
    result = session.get('assessment_result', '')
    diseases = []
    if result:
        lines = result.splitlines()
        for line in lines:
            for num in ["1.", "2.", "3."]:
                if line.strip().startswith(num):
                    line = line.strip()[len(num):].strip()
            if ":" in line:
                title, description = line.split(":", 1)
            else:
                title, description = line, ""
            diseases.append({
                "title": title.strip(),
                "description": description.strip()
            })
    return render_template("possible_disease.html", diseases=diseases)

@app.route("/assessment_report", methods=["GET"])
def assessment_report():
    """
    Renders the assessment report page with patient details from the homepage.
    """
    age = session.get("age", "N/A")
    sex = session.get("sex", "N/A")
    completed_on = datetime.now().strftime("%d/%m/%Y, %H:%M")
    return render_template("Assesment_report.html", age=age, sex=sex, completed_on=completed_on)

if __name__ == "__main__":
    app.run(debug=True)
