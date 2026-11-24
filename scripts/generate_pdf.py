#!/usr/bin/env python3
"""
LEARNING_FLUTTER_NOTES.pdf Generator
------------------------------------
Compiles the master 12-Week Flutter & Full-Stack Reference Handbook.
Includes:
- Cover Page (Metadata, status indicator)
- Table of Contents & Curriculum Roadmap (Updated with Approved Week 1 status)
- Methodology & Progress Protocol
- Chapter 1: Dart Fundamentals & Core Syntax (2 high-density reference pages)
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
    Preformatted,
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
        self.drawString(54, 34, "WEEK 1 IN PROGRESS: DART FUNDAMENTALS & ASYNC PROGRAMMING")
        self.restoreState()


def create_notes_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=48,
        bottomMargin=48,
    )

    styles = getSampleStyleSheet()

    # Palette
    primary_blue = colors.HexColor("#02569B")    # Flutter Deep Navy
    secondary_blue = colors.HexColor("#0175C2")  # Flutter Mid Blue
    accent_blue = colors.HexColor("#0288D1")
    dark_text = colors.HexColor("#0F172A")
    muted_text = colors.HexColor("#64748B")
    card_bg = colors.HexColor("#F8FAFC")
    card_border = colors.HexColor("#CBD5E1")
    alert_bg = colors.HexColor("#EFF6FF")
    alert_border = colors.HexColor("#3B82F6")
    code_bg = colors.HexColor("#0F172A")
    success_bg = colors.HexColor("#ECFDF5")
    success_border = colors.HexColor("#10B981")

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
        fontSize=11,
        leading=15,
        textColor=secondary_blue,
        spaceBefore=8,
        spaceAfter=3,
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.2,
        textColor=dark_text,
    )

    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold',
    )

    badge_approved = ParagraphStyle(
        'BadgeApproved',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#047857"),
        alignment=1,
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

    code_inline = ParagraphStyle(
        'CodeInline',
        parent=body_style,
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#02569B"),
    )

    code_block_text = ParagraphStyle(
        'CodeBlockText',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#F8FAFC"),
    )

    story = []

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 25))
    
    tag_p = Paragraph(
        "<font color='#0288D1'><b>PROJECT: 12-WEEK FULL-STACK FLUTTER ROADMAP</b></font>",
        ParagraphStyle('TagStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12)
    )
    story.append(tag_p)
    story.append(Spacer(1, 8))

    story.append(Paragraph("12-Week Flutter &amp; Full-Stack<br/>Engineering Master Handbook", cover_title_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "A rigorous, production-grade syllabus covering Dart internals, advanced Flutter UI, BLoC state management, "
        "Supabase, PostgreSQL, Python, FastAPI, Clean Architecture, Docker, and CI/CD deployment.",
        cover_subtitle_style
    ))
    story.append(Spacer(1, 14))

    story.append(HRFlowable(width="100%", thickness=2.5, color=primary_blue, spaceBefore=0, spaceAfter=14))

    # Active Progress Notification Box
    notice_text = (
        "<b>CURRICULUM ACTIVE: WEEK 1 IN PROGRESS</b><br/>"
        "This master documentation manual is strictly synchronized with active learning progress. "
        "Chapter 1 (Part 1: Dart Fundamentals) has been reviewed, explicitly approved, and compiled. "
        "Further modules and weekly projects are added upon student verification."
    )
    notice_p = Paragraph(notice_text, ParagraphStyle('NoticeP', parent=body_style, fontSize=9, leading=13.5, textColor=colors.HexColor("#065F46")))
    
    notice_table = Table([[notice_p]], colWidths=[letter[0] - 100])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), success_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, success_border),
        ('PADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 16))

    meta_data = [
        [Paragraph("<b>Author / Learner:</b>", body_bold), Paragraph("Yash Raj Verma", body_style)],
        [Paragraph("<b>Target Stack:</b>", body_bold), Paragraph("Flutter, BLoC, Supabase, PostgreSQL, Python, FastAPI, Docker", body_style)],
        [Paragraph("<b>GitHub Repository:</b>", body_bold), Paragraph("https://github.com/yashrajverma555/learning-flutter", body_style)],
        [Paragraph("<b>Curriculum Length:</b>", body_bold), Paragraph("Strictly 12 Weeks (1 Mandatory Production Project per Week)", body_style)],
        [Paragraph("<b>Active Milestone:</b>", body_bold), Paragraph("Week 1: Dart Fundamentals &amp; Asynchronous Programming", body_style)],
        [Paragraph("<b>Documentation Rule:</b>", body_bold), Paragraph("Strict explicit learner review and sign-off before compiling updates", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[125, letter[0] - 100 - 125])
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
            Paragraph("<font color='#047857'>● Approved (P.4)</font>", badge_approved),
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

    toc_table = Table(toc_data, colWidths=[24, 235, 175, 78])
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
    protocol_table = Table(protocol_data, colWidths=[140, letter[0] - 100 - 140])
    protocol_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 5.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(protocol_table)

    story.append(Spacer(1, 14))

    # Week 1 Overview Box
    w1_box = [
        [Paragraph(
            "<b>Week 1 Status: Dart Fundamentals &amp; Asynchronous Programming</b><br/>"
            "• <b>Approved Modules:</b> Part 1 — Language Fundamentals, Variables, Types, Conversions, Operators &amp; Control Flow.<br/>"
            "• <b>Upcoming Focus:</b> Part 2 — OOP (Mixins, Factory Constructors, copyWith), Null-Safety Deep Dive, Streams &amp; Event Loop.<br/>"
            "• <b>Weekly Project:</b> API Data Fetching Application with robust error handling and model deserialization.",
            ParagraphStyle('W1Box', parent=body_style, fontSize=8.5, leading=13, textColor=colors.HexColor("#065F46"))
        )]
    ]
    w1_table = Table(w1_box, colWidths=[letter[0] - 100])
    w1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#10B981")),
        ('PADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(w1_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: CHAPTER 1 (PART 1) — DART SYNTAX, TYPES & IMMUTABILITY (APPROVED)
    # =========================================================================
    story.append(Paragraph("Chapter 1: Dart Fundamentals — Syntax, Types &amp; Immutability", h1_style))
    story.append(Paragraph(
        "<b>Status: Approved Reference</b> • Focus: Production syntax, memory behaviors, and type casting rules.",
        ParagraphStyle('SubH', parent=body_style, textColor=muted_text, fontSize=8)
    ))
    story.append(Spacer(1, 4))

    # Section 1: Entry Point & Variables
    story.append(Paragraph("1. Program Structure &amp; Variable Declarations", h2_style))
    
    var_table_data = [
        [
            Paragraph("<b>Keyword</b>", body_bold),
            Paragraph("<b>Type Inferred?</b>", body_bold),
            Paragraph("<b>Reassignable?</b>", body_bold),
            Paragraph("<b>Evaluation</b>", body_bold),
            Paragraph("<b>Production Memory &amp; Usage Rule</b>", body_bold),
        ],
        [
            Paragraph("<font color='#02569B'><b>var</b></font>", body_style),
            Paragraph("Yes (static)", body_style),
            Paragraph("Yes (same type)", body_style),
            Paragraph("Runtime", body_style),
            Paragraph("Standard stack/heap reference. Infer types locally.", body_style),
        ],
        [
            Paragraph("<font color='#DC2626'><b>dynamic</b></font>", body_style),
            Paragraph("No (any type)", body_style),
            Paragraph("Yes (any type)", body_style),
            Paragraph("Runtime", body_style),
            Paragraph("<b>Disables compile-time safety.</b> Avoid except for raw untyped JSON.", body_style),
        ],
        [
            Paragraph("<font color='#02569B'><b>final</b></font>", body_style),
            Paragraph("Optional", body_style),
            Paragraph("No (single assign)", body_style),
            Paragraph("Runtime", body_style),
            Paragraph("Set once at runtime (e.g. API responses, DateTime.now()).", body_style),
        ],
        [
            Paragraph("<font color='#047857'><b>const</b></font>", body_style),
            Paragraph("Optional", body_style),
            Paragraph("No (immutable)", body_style),
            Paragraph("Compile-time", body_style),
            Paragraph("<b>Canonicalized in memory.</b> Shared allocation. Essential for Flutter widgets.", body_style),
        ],
    ]
    var_table = Table(var_table_data, colWidths=[65, 80, 85, 80, 202])
    var_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 0.75, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(var_table)

    story.append(Spacer(1, 6))

    # Section 2: Built-in Types & Parsing
    story.append(Paragraph("2. Built-in Data Types, Parsing &amp; Safe Type Casting", h2_style))
    
    code_text_1 = (
        "// 1. Safe Parsing: Never use direct int.parse() on unvalidated inputs\n"
        "final int? count = int.tryParse(inputStr); // Returns null on invalid format\n"
        "final double price = double.tryParse(rawPrice) ?? 0.0; // Clean fallback idiom\n"
        "final String formattedPrice = price.toStringAsFixed(2); // '19.99' (crucial for currency)\n"
        "\n"
        "// 2. Type Checking (is) vs Unsafe Casting (as)\n"
        "final Object responseData = fetchUnknownData();\n"
        "if (responseData is Map<String, dynamic>) {\n"
        "  // Type Promotion: responseData is automatically treated as Map inside this scope\n"
        "  final String title = responseData['title'] as String? ?? 'Untitled';\n"
        "}\n"
        "// final int badCast = responseData as int; // DANGER: Throws TypeError if mismatch"
    )
    code_table_1 = Table([[Preformatted(code_text_1, code_block_text)]], colWidths=[letter[0] - 100])
    code_table_1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), code_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(code_table_1)

    story.append(Spacer(1, 6))

    # Section 3: Strings & Interpolation
    story.append(Paragraph("3. String Expressions, Multiline Strings &amp; Raw Strings", h2_style))
    
    code_text_2 = (
        "final String user = 'Alice';\n"
        "final String welcome = 'Hello, $user! Item count: ${user.length}'; // Use ${} for expressions\n"
        "\n"
        "// Multiline string: Preserves newlines and formatting (ideal for SQL/GraphQL queries)\n"
        "final String sqlQuery = '''\n"
        "  SELECT id, email, created_at \n"
        "  FROM users \n"
        "  WHERE is_active = true;\n"
        "''';\n"
        "\n"
        "// Raw string: Prefixed with 'r' to disable escape sequence interpretation (ideal for regex)\n"
        r"final RegExp emailRegex = RegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$');"
    )
    code_table_2 = Table([[Preformatted(code_text_2, code_block_text)]], colWidths=[letter[0] - 100])
    code_table_2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), code_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(code_table_2)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: CHAPTER 1 (PART 2) — OPERATORS, CONTROL FLOW & BEST PRACTICES (APPROVED)
    # =========================================================================
    story.append(Paragraph("Chapter 1: Operators, Modern Control Flow &amp; Pitfalls", h1_style))
    story.append(Paragraph(
        "<b>Status: Approved Reference</b> • Focus: Dart 3 pattern matching, null-aware operators, and memory hygiene.",
        ParagraphStyle('SubH2', parent=body_style, textColor=muted_text, fontSize=8)
    ))
    story.append(Spacer(1, 4))

    # Section 1: Null-Aware & Cascade Operators
    story.append(Paragraph("1. Essential Operators to Memorize", h2_style))
    
    op_table_data = [
        [
            Paragraph("<b>Operator</b>", body_bold),
            Paragraph("<b>Name &amp; Signature</b>", body_bold),
            Paragraph("<b>Production Code Example</b>", body_bold),
            Paragraph("<b>Behavioral Explanation</b>", body_bold),
        ],
        [
            Paragraph("<font color='#02569B'><b>??</b></font>", body_style),
            Paragraph("Null-Coalescing", body_style),
            Paragraph("<code>final name = user ?? 'Guest';</code>", body_style),
            Paragraph("Returns right operand if left operand is null.", body_style),
        ],
        [
            Paragraph("<font color='#02569B'><b>??=</b></font>", body_style),
            Paragraph("Null-Aware Assignment", body_style),
            Paragraph("<code>token ??= await fetchToken();</code>", body_style),
            Paragraph("Evaluates &amp; assigns right operand only if target is null.", body_style),
        ],
        [
            Paragraph("<font color='#02569B'><b>?.</b></font>", body_style),
            Paragraph("Conditional Member Access", body_style),
            Paragraph("<code>final len = profile?.bio?.length;</code>", body_style),
            Paragraph("Short-circuits to null if any link in chain is null.", body_style),
        ],
        [
            Paragraph("<font color='#02569B'><b>.. / ?..</b></font>", body_style),
            Paragraph("Cascade / Null-Safe Cascade", body_style),
            Paragraph("<code>paint..color = red..strokeWidth = 2.0;</code>", body_style),
            Paragraph("Performs sequence of operations on the same target.", body_style),
        ],
    ]
    op_table = Table(op_table_data, colWidths=[55, 110, 175, 172])
    op_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 0.75, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(op_table)

    story.append(Spacer(1, 6))

    # Section 2: Modern Control Flow (Dart 3 Pattern Matching Switch)
    story.append(Paragraph("2. Modern Control Flow: Dart 3 Switch Expressions", h2_style))
    
    code_text_3 = (
        "// Modern Dart 3 Switch Expression: Exhaustive, concise, returns value directly\n"
        "String mapStatusCode(int statusCode) => switch (statusCode) {\n"
        "  200 || 201 => 'Success: Request Processed',\n"
        "  400 => 'Bad Request: Check Parameters',\n"
        "  401 || 403 => 'Unauthorized: Invalid Credentials',\n"
        "  >= 500 && <= 599 => 'Server Error: Try Again Later',\n"
        "  _ => 'Unknown Error State', // Exhaustive default fallback\n"
        "};"
    )
    code_table_3 = Table([[Preformatted(code_text_3, code_block_text)]], colWidths=[letter[0] - 100])
    code_table_3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), code_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#334155")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(code_table_3)

    story.append(Spacer(1, 6))

    # Section 3: Loops & Best Practices
    story.append(Paragraph("3. Iteration, Documentation Comments &amp; Common Pitfalls", h2_style))
    
    pitfall_data = [
        [
            Paragraph("<b>Faulty / Fragile Pattern</b>", body_bold),
            Paragraph("<b>Production Recommended Pattern</b>", body_bold),
            Paragraph("<b>Why It Matters in Production</b>", body_bold),
        ],
        [
            Paragraph("<font color='#DC2626'><code>int.parse(untrustedInput)</code></font>", body_style),
            Paragraph("<font color='#047857'><code>int.tryParse(input) ?? 0</code></font>", body_style),
            Paragraph("Prevents unhandled <code>FormatException</code> runtime crashes on user input.", body_style),
        ],
        [
            Paragraph("<font color='#DC2626'><code>list.forEach((e) async { ... })</code></font>", body_style),
            Paragraph("<font color='#047857'><code>for (final e in list) { await ... }</code></font>", body_style),
            Paragraph("<code>forEach</code> does not await futures correctly; <code>for-in</code> preserves sequential execution.", body_style),
        ],
        [
            Paragraph("<font color='#DC2626'><code>/** C-Style doc comment */</code></font>", body_style),
            Paragraph("<font color='#047857'><code>/// Markdown doc comment</code></font>", body_style),
            Paragraph("Effective Dart standard: <code>///</code> formats tooltips in VS Code/IDE automatically.", body_style),
        ],
        [
            Paragraph("<font color='#DC2626'><code>var widget = Container(...)</code></font>", body_style),
            Paragraph("<font color='#047857'><code>const widget = Container(...)</code></font>", body_style),
            Paragraph("<code>const</code> widgets prevent redundant rebuild cycles and memory garbage collection churn.", body_style),
        ],
    ]
    pitfall_table = Table(pitfall_data, colWidths=[150, 165, 197])
    pitfall_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 0.75, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(pitfall_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated notes PDF at: {output_path}")


if __name__ == "__main__":
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notes", "LEARNING_FLUTTER_NOTES.pdf")
    create_notes_pdf(target_path)
