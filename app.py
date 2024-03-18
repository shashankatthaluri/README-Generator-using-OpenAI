from flask import Flask, render_template, request, send_filae
import time
import openai
import PyPDF2
import pdfplumber

app = Flask(__name__)
openai.api_key = "REPLACE YOUR OWN OPENAI API KEY HERE"  # Replace with your actual OpenAI API key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "user_input" in request.form:
            user_input = request.form["user_input"]
            readme_content = generate_readme(user_input)
        elif "pdf_file" in request.files:
            pdf_file = request.files["pdf_file"]
            pdf_text = extract_text_from_pdf(pdf_file)
            readme_content = generate_readme(pdf_text)
        else:
            readme_content = "No input provided."
        return render_template("result.html", readme_content=readme_content)
    return render_template("index.html")

@app.route("/download_readme")
def download_readme():
    readme_content = request.args.get("readme_content")
    if readme_content:
        # Save README content to a file
        with open("README.md", "w") as f:
            f.write(readme_content)
        # Return the file as a response
        return send_file("README.md", as_attachment=True)
    else:
        return "No README content provided."

def generate_readme(content):
    prompt = f"Analyze the following text and generate a well-structured README.md file for the project:\n\n{content}"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )
    readme_content = response.choices[0].text.strip()
    return readme_content

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        with pdfplumber.open(page) as pdf:
            text += pdf.extract_text()
    return text

if __name__ == "__main__":
    app.run(debug=True, port=5008)
