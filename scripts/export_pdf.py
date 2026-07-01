import os
import sys
from markdown_pdf import MarkdownPdf, Section

def convert_md_to_pdf():
    # Read Markdown content
    md_path = "D:/6th Sem/tata innovent/Proposed Solution.md"
    pdf_path = "D:/6th Sem/tata innovent/Proposed Solution.pdf"
    
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        sys.exit(1)
        
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Pre-process image paths so markdown-pdf can find them locally
    # Replacing relative paths "src/flask_app/static/images/" with absolute paths
    base_dir = "D:/6th Sem/tata innovent"
    md_content = md_content.replace(
        "src/flask_app/static/images/",
        f"{base_dir}/src/flask_app/static/images/"
    )

    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(md_content))
    
    # Write to PDF
    pdf.save(pdf_path)
    print(f"Success: Converted Markdown to PDF at {pdf_path}")

if __name__ == "__main__":
    convert_md_to_pdf()
