#!/usr/bin/env python3
"""Simple Markdown-to-PDF converter (resume.md -> resume.pdf).
Uses ReportLab to render a naive resume layout.
"""
from pathlib import Path
import sys

try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas
except Exception:
    print("ERROR: reportlab is not installed. Install with: pip install reportlab")
    sys.exit(3)

def draw_text(c, text, x, y, max_width=None):
    # naive word-wrap: split by spaces and wrap within max_width roughly using characters
    lines = [text]
    if max_width:
        # approximate wrap by 90 chars per line as a simple heuristic
        wrap_at = max_width
        words = text.split()
        current = []
        lines = []
        current_len = 0
        for w in words:
            if current_len + len(w) + 1 > wrap_at:
                lines.append(" ".join(current))
                current = [w]
                current_len = len(w) + 1
            else:
                current.append(w)
                current_len += len(w) + 1
        if current:
            lines.append(" ".join(current))
    for ln in lines:
        c.drawString(x, y, ln)
        y -= 14
        if y < 50:
            c.showPage()
            y = 750
    return y

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert resume.md to resume.pdf (simple layout).")
    parser.add_argument("md_path", help="Path to resume.md")
    parser.add_argument("-o", "--output", default="resume.pdf", help="Output PDF path")
    args = parser.parse_args()
    md_path = Path(args.md_path)
    if not md_path.exists():
        print(f"ERROR: {md_path} not found.")
        sys.exit(2)
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    c = canvas.Canvas(str(args.output), pagesize=LETTER)
    width, height = LETTER
    y = height - 40
    c.setFont("Helvetica-Bold", 16)
    # Title
    if lines:
        c.drawString(40, y, lines[0].strip())
        y -= 28
    c.setFont("Helvetica", 12)
    for line in lines[1:]:
        line = line.rstrip()
        if not line:
            y -= 8
            continue
        if line.startswith("# "):
            c.setFont("Helvetica-Bold", 14)
            draw_text(c, line[2:], 40, y, max_width=90)
            y -= 20
            c.setFont("Helvetica", 12)
        else:
            draw_text(c, line, 40, y, max_width=90)
            y -= 14
        if y < 60:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 12)
    c.save()
    print(f"Wrote: {args.output}")

if __name__ == "__main__":
    main()
