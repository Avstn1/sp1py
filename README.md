# Personal Resume Tailor Automation

Welcome to **Personal Resume Tailor Automation**, a powerful Python tool designed to effortlessly customize your resume for any job application — so you can present the most relevant skills and experience with precision and confidence.

---

## 🚀 What It Does

This project automates the entire process of **tailoring your personal resume** based on a job description you provide. Using a combination of:

- **Python**  
- **OpenAI’s GPT-3.5 Turbo API** for smart content generation  
- **tkinter** for a simple user interface  
- **python-docx** for Word document manipulation  
- **docx2pdf** (optional) for seamless conversion to PDF  

it generates a professionally tailored resume highlighting the exact skills and experience that match the role, saving you countless hours and boosting your chances of standing out.

---

## 💡 Key Features

- **Intelligent Skills Extraction**: Automatically crafts a concise, 5-skill summary tailored to the job description.
- **Experience Personalization**: Transforms your past roles’ bullet points to directly align with the job requirements — emphasizing the most relevant achievements.
- **Dynamic Placeholder Replacement**: Replaces predefined placeholders in your existing resume template with AI-generated content, maintaining your formatting and style.
- **One-Click PDF Export**: Converts your newly tailored Word resume into a polished PDF (requires `docx2pdf`).
- **User-Friendly GUI**: A clean, simple tkinter interface to input your job description and generate your resume with ease.

---

## 🎯 Why Use This?

Hiring managers spend mere seconds scanning each resume. This automation ensures that every word you present is **purpose-built for the job**, highlighting what matters most to recruiters. Instead of generic resumes, you’ll have a laser-focused document that speaks directly to the role — making you the obvious candidate.

---

## 🛠 How It Works (Behind the Scenes)

1. You paste a job description into the application’s input box.
2. The app sends targeted prompts to OpenAI’s API to generate:
   - A tailored **SKILLS** section with exactly five relevant skills.
   - Customized **experience bullet points** for multiple roles based on your original achievements.
3. These generated texts replace placeholders in your Word resume template (`resume_template.docx`).
4. The updated resume is saved as a new Word document.
5. Optionally, it converts the Word document to PDF, ready to send to employers.

---

## 📦 Requirements

- Python 3.7+
- Libraries:
  - `openai` (or compatible OpenAI client)
  - `tkinter` (usually pre-installed with Python)
  - `python-docx`
  - `docx2pdf` (optional, for PDF conversion)
- An **OpenAI API key** set as an environment variable:  
  `OPENAI_API_KEY`

---
## ⚡ Quick Start

1. Clone the repository.  
2. Ensure your environment has the necessary packages installed:  
   
       pip install openai python-docx docx2pdf
   
3. Set your OpenAI API key in your environment:  
   - On Windows (PowerShell):  
     
         setx OPENAI_API_KEY "your_api_key_here"
     
   - On Linux/macOS (bash):  
     
         export OPENAI_API_KEY="your_api_key_here"
     
4. Prepare your resume template with placeholders like `{SKILLS}`, `{JDRF}`, `{DOORDASH}`, etc.  
5. Run the script:  
   
       python your_resume_tailor_script.py
   
6. Paste the job description into the UI, click **Generate Resume**, and get your tailored resume ready.

