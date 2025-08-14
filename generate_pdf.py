from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from pathlib import Path
import re

INPUT_MD = "/workspace/ai_guide_rewrite.md"
OUTPUT_PDF = "/workspace/ai_guide_refreshed.pdf"


def build_styles():
	styles = getSampleStyleSheet()
	# Base body
	styles.add(ParagraphStyle(
		name="Body",
		parent=styles["BodyText"],
		fontName="Helvetica",
		fontSize=11,
		leading=15,
		spaceAfter=8,
	))
	# Headings with subtle color
	styles.add(ParagraphStyle(
		name="H1",
		parent=styles["Heading1"],
		fontName="Helvetica-Bold",
		fontSize=22,
		leading=26,
		textColor=colors.HexColor("#0B5FFF"),
		spaceBefore=6,
		spaceAfter=14,
	))
	styles.add(ParagraphStyle(
		name="H2",
		parent=styles["Heading2"],
		fontName="Helvetica-Bold",
		fontSize=16,
		leading=20,
		textColor=colors.HexColor("#0B5FFF"),
		spaceBefore=16,
		spaceAfter=10,
	))
	styles.add(ParagraphStyle(
		name="H3",
		parent=styles["Heading3"],
		fontName="Helvetica-Bold",
		fontSize=13,
		leading=17,
		textColor=colors.HexColor("#0B5FFF"),
		spaceBefore=12,
		spaceAfter=8,
	))
	return styles


def parse_markdown(lines, styles):
	story = []
	para_buf = []
	list_buf = []
	list_type = None  # 'bullet' or 'number'

	def flush_paragraph():
		if para_buf:
			text = " ".join(para_buf).strip()
			if text:
				story.append(Paragraph(text, styles["Body"]))
				story.append(Spacer(1, 6))
			para_buf.clear()

	def flush_list():
		if list_buf:
			bulletType = 'bullet' if list_type == 'bullet' else '1'
			items = [ListItem(Paragraph(item, styles["Body"])) for item in list_buf]
			story.append(ListFlowable(items, bulletType=bulletType, start='1', leftIndent=18, spaceBefore=2, spaceAfter=8))
			list_buf.clear()
			return True
		return False

	for raw in lines:
		line = raw.rstrip()
		if not line.strip():
			# blank line
			flushed = flush_list()
			flush_paragraph()
			if not flushed:
				story.append(Spacer(1, 4))
			continue

		# Headings
		if line.startswith('# '):
			flush_list(); flush_paragraph()
			story.append(Paragraph(line[2:].strip(), styles["H1"]))
			story.append(Spacer(1, 8))
			continue
		if line.startswith('## '):
			flush_list(); flush_paragraph()
			story.append(Paragraph(line[3:].strip(), styles["H2"]))
			continue
		if line.startswith('### '):
			flush_list(); flush_paragraph()
			story.append(Paragraph(line[4:].strip(), styles["H3"]))
			continue

		# Lists
		if re.match(r"^[-\u2022]\s+", line):
			flush_paragraph()
			content = re.sub(r"^[-\u2022]\s+", "", line).strip()
			if list_type not in (None, 'bullet'):
				flush_list()
			list_type = 'bullet'
			list_buf.append(content)
			continue
		m = re.match(r"^(\d+)\.\s+", line)
		if m:
			flush_paragraph()
			content = line[m.end():].strip()
			if list_type not in (None, 'number'):
				flush_list()
			list_type = 'number'
			list_buf.append(content)
			continue

		# Default: paragraph text
		para_buf.append(line)

	# flush any remaining
	flush_list(); flush_paragraph()
	return story


def add_page_number(canvas, doc):
	page_num_text = f"{canvas.getPageNumber()}"
	canvas.setFont("Helvetica", 9)
	canvas.setFillColor(colors.HexColor("#666666"))
	canvas.drawRightString(doc.pagesize[0] - 54, 24, page_num_text)


def main():
	styles = build_styles()
	text = Path(INPUT_MD).read_text(encoding="utf-8")
	lines = text.splitlines()
	story = []

	# Title is first heading
	# Let parser handle the rest
	story.extend(parse_markdown(lines, styles))

	doc = SimpleDocTemplate(
		OUTPUT_PDF,
		pagesize=LETTER,
		leftMargin=0.9*inch,
		rightMargin=0.9*inch,
		topMargin=0.9*inch,
		bottomMargin=0.9*inch,
	)
	doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
	print(f"Wrote {OUTPUT_PDF}")


if __name__ == "__main__":
	main()