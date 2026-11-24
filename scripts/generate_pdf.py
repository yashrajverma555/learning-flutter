#!/usr/bin/env python3
"""
LEARNING_FLUTTER_NOTES.pdf Generator
------------------------------------
Generates a beautifully styled, professional PDF handbook for Flutter & Dart learning.
Includes custom running headers, footers with 'Page X of Y', styled callout boxes,
table of contents, and modular support for approved chapters.
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
    """
    Two-pass canvas to dynamically compute and print total page count 'Page X of Y'
    and add consistent running headers and footers.
    """
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
        # Don't draw header/footer on cover page (page 1)
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#02569B"))

        # Running Header
        self.drawString(54, letter[1] - 34, "FLUTTER & DART ENGINEERING MASTER REFERENCE")
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(letter[0] - 54, letter[1] - 34, "Yash Raj Verma | Learning Handbook")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, letter[1] - 40, letter[0] - 54, letter[1] - 40)

        # Running Footer
        self.line(54, 46, letter[0] - 54, 46)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(letter[0] - 54, 34, page_str)
        self.drawString(54, 34, "STATUS: INITIALIZED — AWAITING FIRST APPROVED TOPIC")
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
    primary_blue = colors.HexColor("#02569B")    # Flutter Primary Navy
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
        fontSize=27,
        leading=33,
        textColor=primary_blue,
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=17,
        textColor=secondary_blue,
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=primary_blue,
        spaceBefore=0,
        spaceAfter=6,
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=secondary_blue,
        spaceBefore=14,
        spaceAfter=6,
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
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
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#B45309"),
        alignment=1,
    )

    story = []

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 35))
    
    # Tag
    tag_p = Paragraph(
        "<font color='#0288D1'><b>PROJECT: LEARNING FLUTTER • MASTER ARCHIVE</b></font>",
        ParagraphStyle('TagStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=12)
    )
    story.append(tag_p)
    story.append(Spacer(1, 10))

    # Main Title
    story.append(Paragraph("Flutter &amp; Dart Engineering<br/>Personal Reference Handbook", cover_title_style))
    story.append(Spacer(1, 10))

    # Subtitle
    story.append(Paragraph(
        "A structured, production-grade learning manual covering syntax, widget lifecycle, architecture patterns, state management, and real-world implementations.",
        cover_subtitle_style
    ))
    story.append(Spacer(1, 18))

    story.append(HRFlowable(width="100%", thickness=2.5, color=primary_blue, spaceBefore=0, spaceAfter=18))

    # Prominent Status Notice Box
    notice_text = (
        "<b>DOCUMENT STATUS: INITIALIZED — AWAITING FIRST APPROVED TOPIC</b><br/>"
        "This master reference manual is strictly synchronized with active learning progress. "
        "Per our teaching methodology, chapters, syntax cheat-sheets, and verified code patterns are "
        "compiled into this document <b>only after explicit review and approval</b>.<br/><br/>"
        "<i>Currently, no learning chapters have been approved yet. The manual is primed and ready to "
        "receive Topic 1.</i>"
    )
    notice_p = Paragraph(notice_text, ParagraphStyle('NoticeP', parent=body_style, fontSize=9.5, leading=14.5, textColor=colors.HexColor("#1E3A8A")))
    
    notice_table = Table([[notice_p]], colWidths=[letter[0] - 108])
    notice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), alert_bg),
        ('BOX', (0, 0), (-1, -1), 1.5, alert_border),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 25))

    # Metadata Card
    meta_data = [
        [Paragraph("<b>Target Audience:</b>", body_bold), Paragraph("Intermediate Developer transitioning to Production-Ready Flutter", body_style)],
        [Paragraph("<b>Author / Learner:</b>", body_bold), Paragraph("Yash Raj Verma", body_style)],
        [Paragraph("<b>GitHub Repository:</b>", body_bold), Paragraph("https://github.com/yashrajverma555/learning-flutter", body_style)],
        [Paragraph("<b>Ultimate Objective:</b>", body_bold), Paragraph("Independently architect and ship production-ready Flutter applications", body_style)],
        [Paragraph("<b>Version:</b>", body_bold), Paragraph("1.0.0 (Initial Framework)", body_style)],
        [Paragraph("<b>Review Policy:</b>", body_bold), Paragraph("Strict explicit learner approval required before any additions", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[130, letter[0] - 108 - 130])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 7.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 35))
    story.append(Paragraph("<i>Compiled dynamically via automated PDF pipeline • notes/LEARNING_FLUTTER_NOTES.pdf</i>", ParagraphStyle('FootMeta', parent=body_style, textColor=muted_text, fontSize=8, alignment=1)))

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: TABLE OF CONTENTS & ROADMAP
    # ==========================================
    story.append(Paragraph("Table of Contents &amp; Curriculum Roadmap", h1_style))
    story.append(Paragraph(
        "The curriculum is arranged logically from modern Dart language features to full production architecture. Each chapter will contain dedicated sections for syntax to memorize, common gotchas, and enterprise code examples.",
        body_style
    ))
    story.append(Spacer(1, 10))

    toc_data = [
        [
            Paragraph("<b>Chapter / Module</b>", body_bold),
            Paragraph("<b>Core Focus Area &amp; Key Deliverables</b>", body_bold),
            Paragraph("<b>Status</b>", body_bold),
        ],
        [
            Paragraph("<b>Ch 1. Modern Dart &amp; OOP</b>", body_style),
            Paragraph("Null safety idioms, mixins, factory constructors, copyWith pattern, sealed classes", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 2. Widget Internals &amp; Lifecycle</b>", body_style),
            Paragraph("Stateless vs Stateful, Element &amp; RenderObject trees, BuildContext, GlobalKey", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 3. Responsive Layouts &amp; Slivers</b>", body_style),
            Paragraph("BoxConstraints, Flex rules, CustomScrollView, Slivers, LayoutBuilder", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 4. Navigation &amp; Routing</b>", body_style),
            Paragraph("Navigator 2.0, GoRouter, deep links, route guards, shell routes", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 5. Form Handling &amp; Validation</b>", body_style),
            Paragraph("TextEditingController lifecycle, FormField, FocusNode, custom formatters", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 6. Modern State Management</b>", body_style),
            Paragraph("Riverpod / Bloc patterns, immutability, selectors, side-effect isolation", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 7. Networking &amp; API Integration</b>", body_style),
            Paragraph("Dio/HTTP clients, interceptors, error mapping, JSON serialization with Freezed", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 8. Local Persistence &amp; Firebase</b>", body_style),
            Paragraph("Secure storage, Hive / Isar, Firebase Auth, Firestore, Cloud Messaging", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Ch 9. Architecture &amp; Performance</b>", body_style),
            Paragraph("Clean architecture, repository pattern, DevTools profiling, leak prevention", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
        [
            Paragraph("<b>Appendix: Quick Syntax Reference</b>", body_style),
            Paragraph("High-frequency widget properties, constructor parameters, common error fixes", body_style),
            Paragraph("<font color='#D97706'>⏳ Pending</font>", badge_pending),
        ],
    ]

    toc_table = Table(toc_data, colWidths=[150, 260, 94])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 6.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(toc_table)

    story.append(Spacer(1, 14))

    # Notes on updates
    update_note = Paragraph(
        "<i>Note: As topics are covered and explicitly approved, the pending badges above will transition "
        "to 'Approved' with exact page hyperlinks, and the corresponding detailed chapters will expand below.</i>",
        ParagraphStyle('UpdateNote', parent=body_style, fontSize=8, textColor=muted_text)
    )
    story.append(update_note)

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: METHODOLOGY & HOW TO USE
    # ==========================================
    story.append(Paragraph("Pedagogical Methodology &amp; Documentation Rules", h1_style))
    story.append(Paragraph(
        "This reference manual adheres to a strict 6-step engineering methodology designed for intermediate developers. "
        "The goal is not rote memorization of concepts you already know, but rapid retrieval of exact syntax, patterns, and production techniques.",
        body_style
    ))
    story.append(Spacer(1, 10))

    method_data = [
        [Paragraph("<b>Step 1: Understand the Topic</b>", body_bold), Paragraph("Briefly establish what we are learning and why it is critical in production Flutter apps.", body_style)],
        [Paragraph("<b>Step 2: Teach the Concept</b>", body_bold), Paragraph("Deconstruct internal workings, constructor properties, parameter types, and differences from similar widgets/APIs.", body_style)],
        [Paragraph("<b>Step 3: Practical Code Examples</b>", body_bold), Paragraph("Provide clean, idiomatic code snippets. Highlight must-memorize syntax and common errors with their fixes.", body_style)],
        [Paragraph("<b>Step 4: Real-World Use Cases</b>", body_bold), Paragraph("Ground every concept in practical scenarios (e-commerce, authentication, real-time dashboards, payment flows).", body_style)],
        [Paragraph("<b>Step 5: Test Understanding</b>", body_bold), Paragraph("Targeted coding questions and debugging exercises without revealing solutions upfront.", body_style)],
        [Paragraph("<b>Step 6: Explicit Approval</b>", body_bold), Paragraph("Present a structured summary for approval. Only upon explicit confirmation is content compiled into this PDF and pushed to GitHub.", body_style)],
    ]
    method_table = Table(method_data, colWidths=[140, letter[0] - 108 - 140])
    method_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, card_border),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(method_table)

    story.append(Spacer(1, 14))

    story.append(Paragraph("Documentation Standards for Approved Chapters", h2_style))
    story.append(Paragraph(
        "Every approved chapter included in this PDF must satisfy the following criteria:<br/>"
        "• <b>Concise yet complete:</b> No filler theory; straight to mechanics and implementation.<br/>"
        "• <b>Syntax Callouts:</b> Distinct formatting for properties that are easily forgotten.<br/>"
        "• <b>Common Pitfalls Table:</b> Side-by-side contrast of faulty patterns vs recommended patterns.<br/>"
        "• <b>Modern Standards:</b> Strictly uses the latest Flutter 3.x and Dart 3.x null-safe idioms.",
        body_style
    ))

    story.append(Spacer(1, 18))

    # Action Callout Box
    c1_box = [
        [Paragraph(
            "<b>Ready for Your First Topic!</b><br/>"
            "To begin Chapter 1, provide any of the following:<br/>"
            "1. A Flutter / Dart concept you want to master or refresh (e.g., BuildContext, GoRouter, Riverpod).<br/>"
            "2. A YouTube tutorial link or video topic.<br/>"
            "3. A specific coding problem, bug, or implementation pattern.<br/>"
            "4. A code snippet you would like to thoroughly understand.<br/><br/>"
            "We will deconstruct it step-by-step, verify your mastery, and compile your first official chapter!",
            ParagraphStyle('C1Box', parent=body_style, fontSize=9, leading=13.5, textColor=colors.HexColor("#065F46"))
        )]
    ]
    c1_table = Table(c1_box, colWidths=[letter[0] - 108])
    c1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#10B981")),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(c1_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated initial PDF at: {output_path}")


if __name__ == "__main__":
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "notes", "LEARNING_FLUTTER_NOTES.pdf")
    create_initial_pdf(target_path)
