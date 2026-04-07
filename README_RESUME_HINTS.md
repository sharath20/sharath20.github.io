# Resume parsing and population hints

What this repo now contains:
- A lightweight HTML/CSS dark portfolio starter at index.html
- A Python-based resume parser at scripts/parse_resume.py
- A small dependency file requirements.txt for parsing

How to use:
- Put your resume PDF at the repo root (e.g., VENKAT_MUDHIGONDA_Resume.pdf)
- Run: python3 scripts/parse_resume.py VENKAT_MUDHIGONDA_Resume.pdf -o resume.md
- The output resume.md will be placed at the path you specify (default resume.md)

Notes:
- PDF text extraction quality depends on the source; simple layouts extract best.
- You can adapt the generated resume.md into your site content or import sections into your portfolio.
