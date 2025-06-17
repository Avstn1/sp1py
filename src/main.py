import tkinter as tk
from tkinter import ttk, messagebox
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING
from openai import OpenAI
import os

# For docx -> pdf conversion
try:
    from docx2pdf import convert
except ImportError:
    convert = None

# Read your API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    messagebox.showerror("API Key Error", "Please set your OPENAI_API_KEY environment variable.")
    exit()

client = OpenAI(api_key=api_key)

def get_skills_prompt(job_description):
    return f"""
You're writing a SKILLS section for a resume.

Format the output as exactly 5 skills, each on its own line, with no blank lines in between.

Each skill should be labeled (e.g., "Customer Service:") followed by a concise description on the same line.

DO NOT add any extra blank lines or paragraph breaks between skills.

Use simple plain text, no markdown, no bolding.

Example:

Customer Service: Ability to provide excellent sales service and ensure high levels of customer satisfaction by being knowledgeable on all products offered.
Sales Skills: Delivering sales, outstanding customer experience, and achieving personal productivity goals.
Communication: Connecting with every customer by asking open-ended questions to assess needs and adapting communication styles to different types of customers.
Product Knowledge: Maintaining awareness of all product knowledge, current trends, and upcoming products to fit customer needs.
Teamwork: Working as part of a team to create a positive and inclusive work environment, while also improving individual skills on the sales floor.

Now write the SKILLS section tailored to this job:

{job_description}
"""

def get_experience_prompt(job_description, role_name, example_bullets):
    return f"""
You're writing bullet points for a resume's EXPERIENCE section. Each bullet must:
- Start with an action verb
- Stay authentic to the original experience
- Be concise
- Use • (the bullet symbol) at the beginning of each line
- Be limited to 3 bullet points UNLESS the job description clearly calls for a specific skill shown in the original experience. In that case, write 4.

Job Title: {role_name}

Original Experience:
{example_bullets}

Job Posting:
{job_description}

Now rewrite concise and relevant bullet points for this role.
"""

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        messagebox.showerror("OpenAI Error", str(e))
        return ""

def replace_skills_placeholder(doc, placeholder, skills_text):
    skills_lines = [line.strip() for line in skills_text.splitlines() if line.strip()]

    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            parent = paragraph._element.getparent()
            p_idx = parent.index(paragraph._element)

            original_style = paragraph.style
            parent.remove(paragraph._element)

            for i, skill_line in enumerate(skills_lines):
                new_p = doc.add_paragraph(skill_line)
                new_p.style = original_style

                for run in new_p.runs:
                    run.font.size = Pt(10)

                p_format = new_p.paragraph_format
                p_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                p_format.space_before = Pt(0)
                p_format.space_after = Pt(0)

                new_p_element = new_p._element
                parent.remove(new_p_element)
                parent.insert(p_idx + i, new_p_element)
            break

def replace_placeholders(doc_path, output_path, replacements):
    doc = Document(doc_path)

    for key, value in replacements.items():
        if key == "SKILLS":
            replace_skills_placeholder(doc, f"{{{{{key}}}}}", value)
        else:
            for paragraph in doc.paragraphs:
                if f"{{{{{key}}}}}" in paragraph.text:
                    for run in paragraph.runs:
                        if f"{{{{{key}}}}}" in run.text:
                            run.text = run.text.replace(f"{{{{{key}}}}}", value or "")

            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        for paragraph in cell.paragraphs:
                            if f"{{{{{key}}}}}" in paragraph.text:
                                for run in paragraph.runs:
                                    if f"{{{{{key}}}}}" in run.text:
                                        run.text = run.text.replace(f"{{{{{key}}}}}", value or "")

    doc.save(output_path)

def convert_docx_to_pdf(docx_path, pdf_path):
    if convert is None:
        messagebox.showwarning("Conversion Warning", "docx2pdf not installed. PDF conversion skipped.")
        return False

    try:
        convert(docx_path, pdf_path)
        return True
    except Exception as e:
        messagebox.showerror("PDF Conversion Error", f"Failed to convert DOCX to PDF:\n{str(e)}")
        return False

def generate():
    job_desc = job_text.get("1.0", tk.END).strip()

    if not job_desc:
        messagebox.showerror("Missing Info", "Please enter the job description.")
        return

    generate_button.config(state=tk.DISABLED)
    root.update()

    skills_text = ask_openai(get_skills_prompt(job_desc))

    jdrf_example = "• Engaged customers in natural, friendly conversations to assess needs and provide exceptional sales service\n• Maintained personal and productivity goals to contribute to a positive work environment\n• Demonstrated expertise in products and trends to fit customer needs\n• Collaborated with team members to ensure high levels of customer satisfaction"

    doordash_example = "• Engaged customers in friendly and knowledgeable conversations to assess their needs\n• Exceeded personal and productivity goals to contribute to a positive sales environment\n• Maintained up-to-date product knowledge and trends to provide tailored recommendations\n• Collaborated with team members to ensure outstanding customer service and satisfaction"

    rev_example = "• Engaged with customers to deliver exceptional sales service and ensure high levels of satisfaction\n• Achieved personal and productivity goals while maintaining knowledge of all products offered\n• Adapted to different customer needs by asking open-ended questions and sharing expertise on products and trends\n• Contributed to a positive work environment by collaborating with team members and initiating tasks independently"

    camp_example = "• Engaged with customers to deliver an elevated shopping experience\n• Achieved personal and productivity goals while maintaining product knowledge\n• Collaborated with team members to provide excellent sales service\n• Adapted to different customer needs and resolved issues with a smile"

    exp_jdrf = ask_openai(get_experience_prompt(job_desc, "Software Engineer Co-op", jdrf_example))
    exp_door = ask_openai(get_experience_prompt(job_desc, "DoorDash Delivery Driver", doordash_example))
    exp_rev = ask_openai(get_experience_prompt(job_desc, "Rev Captionist", rev_example))
    exp_camp = ask_openai(get_experience_prompt(job_desc, "Church Children’s Camp Volunteer", camp_example))

    replacements = {
        "SKILLS": skills_text,
        "JDRF": exp_jdrf,
        "DOORDASH": exp_door,
        "REV": exp_rev,
        "CAMP": exp_camp
    }

    try:
        replace_placeholders("resume_template.docx", "output_resume.docx", replacements)
        
        # Convert to PDF
        pdf_success = convert_docx_to_pdf("output_resume.docx", "Austin Bartolome - Resume.pdf")

        msg = "Resume generated as 'output_resume.docx'."
        if pdf_success:
            msg += "\nAlso saved as 'output_resume.pdf'."
        else:
            msg += "\nPDF conversion was skipped or failed."

        messagebox.showinfo("Success", msg)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate resume: {str(e)}")
    finally:
        generate_button.config(state=tk.NORMAL)

# UI Setup
root = tk.Tk()
root.title("Resume Generator")

# Set window size to 900x450 (slightly bigger)
root.geometry("900x450")

tk.Label(root, text="Job Description:").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
job_text = tk.Text(root, width=80, height=15)
job_text.grid(row=0, column=1, padx=5, pady=5)

generate_button = tk.Button(root, text="Generate Resume", command=generate)
generate_button.grid(row=1, column=1, sticky="e", padx=5, pady=10)

root.mainloop()
