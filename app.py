import streamlit as st
import datetime
from fpdf import FPDF
import io
import textwrap

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
def sanitize_text(text):
    """Replace unsupported characters with safe alternatives."""
    replacements = {
        '\u2013': '-',  # En-dash
        '\u2014': '-',  # Em-dash
        '\u2026': '...',  # Ellipsis
        '\u2018': "'",  # Left single quote
        '\u2019': "'",  # Right single quote
        '\u201c': '"',  # Left double quote
        '\u201d': '"',  # Right double quote
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def create_download_pdf(name, email, phone, linkedin, summary, projects, experiences, education, skills, certifications):
    pdf = PDF()
    pdf.add_page()
    
    # Set font
    pdf.set_font('Arial', 'B', 16)
    
    # Name
    pdf.cell(0, 10, sanitize_text(name), ln=True, align='L')
    
    # Contact Info
    pdf.set_font('Arial', '', 10)
    contact_info = f"{sanitize_text(email)} | {sanitize_text(phone)} | {sanitize_text(linkedin)}"
    pdf.cell(0, 10, sanitize_text(contact_info), ln=True, align='L')
    
    # Professional Summary
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'PROFESSIONAL SUMMARY', ln=True)
    pdf.set_font('Arial', '', 10)
    
    # Handle multi-line summary with text wrapping
    wrapped_summary = textwrap.fill(sanitize_text(summary), width=95)
    for line in wrapped_summary.split('\n'):
        pdf.cell(0, 5, line, ln=True)
    pdf.ln(5)
    
    # Repeat the `sanitize_text` function for other text inputs in the function.
    # Example:
    # projects, experiences, education, skills, certifications
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')


def main():
    st.title("ATS-Friendly Resume Generator")
    st.write("Fill in your details to generate a professional resume")

    # Personal Information
    st.header("Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        email = st.text_input("Email")
    with col2:
        phone = st.text_input("Phone Number")
        linkedin = st.text_input("LinkedIn URL")

    # Professional Summary
    st.header("Professional Summary")
    summary = st.text_area("Enter your professional summary")

    # Projects
    st.header("Projects")
    num_projects = st.number_input("Number of Projects", min_value=0, max_value=10, value=1)
    projects = []
    
    for i in range(num_projects):
        st.subheader(f"Project {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            project_name = st.text_input(f"Project Name", key=f"proj_name_{i}")
            project_duration = st.text_input(f"Duration (e.g., Jun 2021 – July 2021)", key=f"proj_dur_{i}")
        
        project_points = st.text_area(f"Project Details (One point per line)", key=f"proj_points_{i}")
        
        projects.append({
            "name": project_name,
            "duration": project_duration,
            "points": project_points.split('\n') if project_points else []
        })

    # Experience
    st.header("Work Experience")
    num_experiences = st.number_input("Number of Work Experiences", min_value=0, max_value=10, value=1)
    experiences = []
    
    for i in range(num_experiences):
        st.subheader(f"Experience {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input(f"Company Name", key=f"comp_name_{i}")
            duration = st.text_input(f"Duration (e.g., Nov 2023 – Mar 2024)", key=f"exp_dur_{i}")
        
        experience_points = st.text_area(f"Experience Details (One point per line)", key=f"exp_points_{i}")
        
        experiences.append({
            "company": company_name,
            "duration": duration,
            "points": experience_points.split('\n') if experience_points else []
        })

    # Education
    st.header("Education")
    num_education = st.number_input("Number of Educational Qualifications", min_value=0, max_value=5, value=1)
    education = []
    
    for i in range(num_education):
        st.subheader(f"Education {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            institution = st.text_input(f"Institution Name", key=f"edu_name_{i}")
            degree = st.text_input(f"Degree/Certificate", key=f"edu_deg_{i}")
        with col2:
            duration = st.text_input(f"Duration", key=f"edu_dur_{i}")
            grade = st.text_input(f"Grade/Percentage", key=f"edu_grade_{i}")
        
        education.append({
            "institution": institution,
            "degree": degree,
            "duration": duration,
            "grade": grade
        })

    # Skills
    st.header("Skills")
    skills = st.text_area("Enter your skills (comma-separated)")

    # Certifications
    st.header("Certifications")
    certifications = st.text_area("Enter your certifications (One per line)")

    # Generate Resume
    if st.button("Generate Resume"):
        # Preview the resume
        generate_resume(
            name, email, phone, linkedin, summary,
            projects, experiences, education,
            skills.split(',') if skills else [],
            certifications.split('\n') if certifications else []
        )
        
        # Create download button for PDF
        pdf_bytes = create_download_pdf(
            name, email, phone, linkedin, summary,
            projects, experiences, education,
            skills.split(',') if skills else [],
            certifications.split('\n') if certifications else []
        )
        
        st.download_button(
            label="Download Resume as PDF",
            data=pdf_bytes,
            file_name=f"{name.lower().replace(' ', '_')}_resume.pdf",
            mime="application/pdf"
        )

def generate_resume(name, email, phone, linkedin, summary, projects, experiences, education, skills, certifications):
    st.markdown("---")
    st.header("Generated Resume")
    
    # Personal Information
    st.markdown(f"# {name}")
    st.markdown(f"{email} | {phone} | {linkedin}")
    
    # Professional Summary
    st.markdown("## PROFESSIONAL SUMMARY")
    st.write(summary)
    
    # Projects
    if projects:
        st.markdown("## PROJECTS")
        for project in projects:
            st.markdown(f"**{project['name']}** ({project['duration']})")
            for point in project['points']:
                if point.strip():
                    st.markdown(f"• {point.strip()}")
    
    # Experience
    if experiences:
        st.markdown("## EXPERIENCE")
        for exp in experiences:
            st.markdown(f"**{exp['company']}** ({exp['duration']})")
            for point in exp['points']:
                if point.strip():
                    st.markdown(f"• {point.strip()}")
    
    # Education
    if education:
        st.markdown("## EDUCATION")
        for edu in education:
            st.markdown(f"**{edu['institution']}** ({edu['duration']})")
            st.markdown(f"{edu['degree']} - {edu['grade']}")
    
    # Skills
    if skills:
        st.markdown("## SKILLS")
        st.markdown(", ".join(skill.strip() for skill in skills if skill.strip()))
    
    # Certifications
    if certifications:
        st.markdown("## CERTIFICATION")
        for cert in certifications:
            if cert.strip():
                st.markdown(f"• {cert.strip()}")

if __name__ == "__main__":
    main()
