#!/usr/bin/env python3
"""Resume parser: extract sections from a PDF resume and emit a Git-friendly Markdown.

Usage:
  python3 scripts/parse_resume.py path/to/resume.pdf [-o resume.md]
"""
from pathlib import Path
import sys

def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        print("ERROR: PyPDF2 is not installed. Install with: pip install PyPDF2")
        sys.exit(3)
    reader = PdfReader(str(pdf_path))
    parts = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            parts.append(t)
    return "\n".join(parts)

def split_into_sections(text: str) -> dict:
    lines = text.splitlines()
    sections = {}
    current = "Summary"
    sections[current] = []
    headings = {
        "summary","objective","experience","work experience","education",
        "projects","skills","certifications","languages","awards","achievements"
    }
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        low = line.lower()
        if low in headings:
            current = line.title()
            sections.setdefault(current, [])
            continue
        # a light heuristic: treat lines starting with known headings as headings too
        for h in ["Education","Experience","Projects","Skills","Certifications","Languages","Awards","Achievements"]:
            if low == h.lower():
                current = h
                sections.setdefault(current, [])
                break
        else:
            sections[current].append(line)
    # cleanup: join collected lines
    for k in list(sections.keys()):
        sections[k] = "\n".join([l for l in sections[k] if l.strip() != ""])
    return sections

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Parse a resume PDF into Markdown sections.")
    parser.add_argument("pdf_path", help="Path to resume PDF")
    parser.add_argument("-o", "--output", default="resume.md", help="Output markdown file path")
    args = parser.parse_args()
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"ERROR: Cannot read \"{pdf_path.name}\" (file does not exist).")
        sys.exit(2)
    text = extract_text_from_pdf(pdf_path)
    sections = split_into_sections(text)

    md_lines = [f"# Resume: {pdf_path.stem}", ""]
    # If a Summary section exists, include it first
    if "Summary" in sections and sections["Summary"]:
        md_lines.append("## Summary")
        md_lines.append(sections["Summary"])
        md_lines.append("")

    order = ["Experience", "Education", "Projects", "Skills", "Certifications", "Languages", "Awards", "Achievements"]
    for sec in order:
        if sec in sections and sections[sec]:
            md_lines.append(f"### {sec}")
            md_lines.append(sections[sec])
            md_lines.append("")

    # any other sections
    known = set(order + ["Summary"])
    for sec, content in sections.items():
        if sec not in known and content:
            md_lines.append(f"### {sec}")
            md_lines.append(content)
            md_lines.append("")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"Wrote: {out.resolve()}")

if __name__ == "__main__":
    main()
