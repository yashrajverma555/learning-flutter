#!/usr/bin/env python3
"""
LEARNING_FLUTTER_NOTES.pdf Generator
------------------------------------
Compiles the master 12-Week Flutter & Full-Stack Reference Handbook.
Includes cover page, 12-week comprehensive roadmap table of contents with status badges,
pedagogical engineering framework, and dynamically appended approved chapters.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    HRFlowable,
)
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page count and consistent headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Omit header and footer on cover page
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#02569B"))

        # Running Header
        self.drawString(54, letter[1] - 34, "12-WEEK FLUTTER FULL-STACK ENGINEERING HANDBOOK")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(letter[0] - 54, letter[1] - 34, "Yash Raj Verma | Learning Master Notes")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)

        # Running Footer
        self.line(54, 46, letter[0] - 54, 46)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.drawString(54, 34, "STATUS: 12-WEEK BLUEPRINT INITIALIZED — AWAITING WEEK 1 APPROVAL")
        self.restoreState()


def create_initial_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    # Custom palette
    primary_blue = colors.HexColor("#02569B")    # Flutter Deep Navy
    secondary_blue = colors.HexColor("#0175C2")  # Flutter Mid Blue
    accent_blue = colors.HexColor("#0288D1")
    dark_text = colors.HexColor("#0F172A")
    muted_text = colors.HexColor("#64748B")
    card_bg = colors.HexColor("#F8FAFC")
    card_border = colors.HexColor("#CBD5E1")
    alert_bg = colors.HexColor("#EFF6FF")
    alert_border = colors.HexColor("#3B82F6")

    # Typography styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=primary_blue,
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11.5,
        leading=16.5,
        textColor=secondary_blue,
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_blue,
        spaceBefore=0,
        spaceAfter=5,
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_blue,
        spaceBefore=10,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=dark_text,
    )

    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold',
    )

    badge_pending = ParagraphStyle(
        'BadgePending',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#B45309"),
        alignment=1,
    )

    story = []

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 25))
    
    # Tag
    tag_p = Paragraph(
        "<font color='#0288D1'><b>PROJECT: 12-WEEK FULL-STACK FLUTTER ROADMAP</b></font>",
        ParagraphStyle('TagStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12)
    )
    story.append(tag_p)
    story.append(Spacer(1, 8))

    # Title
    story.append(Paragraph("12-Week Flutter &amp; Full-Stack<br/>Engineering Master Handbook", cover_title_style))
    story.append(Spacer(1, 8))

    # Subtitle
    story.append(Paragraph(
        "A rigorous, production-grade syllabus covering Dart internals, advanced Flutter UI, BLoC state management, "
        "Supabase, PostgreSQL, Python, FastAPI, Clean Architecture, Docker, and CI/CD deployment.",
        cover_subtitle_style
    ))
    story.append(Spacer(1, 14))

    story.append(HRFlowable(width="100%", thickness=2.5, color=primary_blue, spaceBefore=0, spaceAfter=14))

    # Status Notice Box
    notice_text = (
        "<b>ROADMAP BLUEPRINT INITIALIZED — AWAITING WEEK 1 APPROVAL</b><br/>"
        "This master documentation manual is strictly updated following our 12-week structured curriculum. "
        "Each week concludes with an assessment, practical project delivery, and <b>explicit student approval</b> "
        "before content and code patterns are compiled into this permanent document.<br/><br/>"
        "<i>Currently, no learning chapters have been approved yet. The manual is primed for Week 1: "
        "Dart Fundamentals &amp; Asynchronous Programming.</i>"
    )
    notice_p = Paragraph(notice_text, ParagraphStyle('NoticeP', parent=body_style, fontSize=9, leading=13.5, textColor=colors.HexColor("#1E3A8A")))
    
    notice_table = Table([[notice_p]], colWidths=[letter[0] - 108])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), alert_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, alert_border),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 16))

    # Metadata Card
    meta_data = [
        [Paragraph("<b>Author / Learner:</b>", body_bold), Paragraph("Yash Raj Verma", body_style)],
        [Paragraph("<b>Target Stack:</b>", body_bold), Paragraph("Flutter, BLoC, Supabase, PostgreSQL, Python, FastAPI, Docker", body_style)],
        [Paragraph("<b>GitHub Repository:</b>", body_bold), Paragraph("https://github.com/yashrajverma555/learning-flutter", body_style)],
        [Paragraph("<b>Curriculum Length:</b>", body_bold), Paragraph("Strictly 12 Weeks (1 Mandatory Production Project per Week)", body_style)],
        [Paragraph("<b>Terminal Objective:</b>", body_bold), Paragraph("Independently architect, secure, test, containerize, and deploy full-stack apps", body_style)],
        [Paragraph("<b>Documentation Rule:</b>", body_bold), Paragraph("Strict explicit learner review and sign-off before compiling updates", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[125, letter[0] - 108 - 125])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 24))
    story.append(Paragraph("<i>Automated Master Notes Builder • notes/LEARNING_FLUTTER_NOTES.pdf</i>", ParagraphStyle('FootMeta', parent=body_style, textColor=muted_text, fontSize=8, alignment=1)))

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: 12-WEEK TABLE OF CONTENTS & ROADMAP
    # ==========================================
    story.append(Paragraph("12-Week Full-Stack Curriculum &amp; Project Roadmap", h1_style))
    story.append(Paragraph(
        "Each week represents an intensive engineering module with concrete deliverables and a mandatory project. "
        "Upon explicit approval, the pending status will transition to 'Approved' and the detailed chapter will be compiled below.",
        body_style
    ))
    story.append(Spacer(1, 8))

    toc_data = [
        [
            Paragraph("<b>Wk</b>", body_bold),
            Paragraph("<b>Module &amp; Core Concepts</b>", body_bold),
            Paragraph("<b>Mandatory Weekly Project</b>", body_bold),
            Paragraph("<b>Status</b>", body_bold),
        ],
        [
            Paragraph("<b>01</b>", body_style),
            Paragraph("<b>Dart &amp; Async:</b> Types, OOP, streams, event loop, JSON serialization", body_style),
            Paragraph("API Data Fetching Application", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>02</b>", body_style),
            Paragraph("<b>Flutter UI &amp; Slivers:</b> Tree internals, lifecycle, responsive layouts, slivers", body_style),
            Paragraph("Responsive E-commerce Frontend", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>03</b>", body_style),
            Paragraph("<b>Navigation &amp; Routing:</b> Navigator 1.0, GoRouter, deep links, route guards", body_style),
            Paragraph("Multi-Screen Shopping Application", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>04</b>", body_style),
            Paragraph("<b>BLoC State Management:</b> Events, states, Cubit, BlocConsumer, Equatable", body_style),
            Paragraph("Shopping Cart Application Using BLoC", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>05</b>", body_style),
            Paragraph("<b>Supabase &amp; DB Security:</b> PostgreSQL modeling, Supabase Auth, Storage, RLS", body_style),
            Paragraph("Auth &amp; User Notes App (with RLS)", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>06</b>", body_style),
            Paragraph("<b>Python &amp; FastAPI:</b> Pydantic v2, async endpoints, SQLAlchemy 2.0, Alembic", body_style),
            Paragraph("Task Management REST API", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>07</b>", body_style),
            Paragraph("<b>Full-Stack Integration:</b> Dio interceptors, Supabase JWT verification in FastAPI", body_style),
            Paragraph("Full-Stack Task Management App", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>08</b>", body_style),
            Paragraph("<b>Clean Architecture:</b> SOLID, Domain/Data/Presentation layers, Use Cases", body_style),
            Paragraph("Clean Architecture Flutter App", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>09</b>", body_style),
            Paragraph("<b>Advanced Backend &amp; DB:</b> Query optimization, Redis caching, WebSockets", body_style),
            Paragraph("Order Management &amp; Events Backend", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>10</b>", body_style),
            Paragraph("<b>Testing &amp; Security:</b> Pytest, BLoC tests, Golden tests, OWASP API Top 10", body_style),
            Paragraph("Security-Audited &amp; Tested REST API", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>11</b>", body_style),
            Paragraph("<b>DevOps &amp; Cloud:</b> Docker Compose, GitHub Actions CI/CD, Nginx SSL reverse proxy", body_style),
            Paragraph("Dockerized Full-Stack Deployment", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>12</b>", body_style),
            Paragraph("<b>Capstone:</b> Complete Full-Stack E-commerce with UPI, Admin, Real-time &amp; Docker", body_style),
            Paragraph("Production Full-Stack E-commerce Platform", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
    ]

    toc_table = Table(toc_data, colWidths=[24, 235, 175, 70])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4.2),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(toc_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: METHODOLOGY & PROGRESS PROTOCOL
    # ==========================================
    story.append(Paragraph("Weekly Learning &amp; Verification Protocol", h1_style))
    story.append(Paragraph(
        "To guarantee independent, production-level engineering capability, every single week strictly follows this 8-point cycle:",
        body_style
    ))
    story.append(Spacer(1, 8))

    protocol_data = [
        [Paragraph("<b>1. Overview &amp; Assessment:</b>", body_bold), Paragraph("Define core deliverables and evaluate prior experience to skip trivial basics.", body_style)],
        [Paragraph("<b>2. Deep-Dive Sessions:</b>", body_bold), Paragraph("Break topics into bite-sized concepts. Dissect syntax, internal architecture, and gotchas.", body_style)],
        [Paragraph("<b>3. Practical Exercises:</b>", body_bold), Paragraph("Targeted coding drills to anchor muscle memory and critical signatures.", body_style)],
        [Paragraph("<b>4. Mandatory Project:</b>", body_bold), Paragraph("Guided end-of-week production project with explicit folder structure and checklist.", body_style)],
        [Paragraph("<b>5. Code Review:</b>", body_bold), Paragraph("Rigorous evaluation of code quality, architecture, error handling, and performance.", body_style)],
        [Paragraph("<b>6. Revision &amp; Assessment:</b>", body_bold), Paragraph("Concept verification questions before concluding the week's syllabus.", body_style)],
        [Paragraph("<b>7. Explicit Approval:</b>", body_bold), Paragraph("Structured summary presented to learner. Added to PDF strictly upon confirmation.", body_style)],
        [Paragraph("<b>8. GitHub Progress Sync:</b>", body_bold), Paragraph("Push clean, tested implementations and updated PDF with meaningful commits.", body_style)],
    ]
    protocol_table = Table(protocol_data, colWidths=[140, letter[0] - 108 - 140])
    protocol_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 5.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(protocol_table)

    story.append(Spacer(1, 14))

    # Week 1 Callout Box
    w1_box = [
        [Paragraph(
            "<b>Ready for Week 1: Dart Fundamentals &amp; Asynchronous Programming</b><br/>"
            "• <b>Objective:</b> Master modern Dart types, null-safety idioms, OOP patterns, and async mechanics (Event Loop, Futures, Streams).<br/>"
            "• <b>Weekly Project:</b> API Data Fetching Application with robust error handling and model deserialization.<br/><br/>"
            "<i>Upon your explicit approval of this 12-week roadmap, we will initiate Week 1!</i>",
            ParagraphStyle('W1Box', parent=body_style, fontSize=8.5, leading=13, textColor=colors.HexColor("#065F46"))
        )]
    ]
    w1_table = Table(w1_box, colWidths=[letter[0] - 108])
    w1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#10B981")),
        ('PADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(w1_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated initial PDF at: {output_path}")


if __name__ == "__main__":
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notes", "LEARNING_FLUTTER_NOTES.pdf")
    create_initial_pdf(target_path)
