"""
Professional PDF Report Generator for Campus Impact Ministry
Uses ReportLab for high-quality output
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.platypus import PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from datetime import date, datetime

# Brand colors (primary is deep teal; NAVY name kept for backwards compat).
NAVY = HexColor('#0d5e64')
DARK_BLUE = HexColor('#0f6a70')
GOLD = HexColor('#c49a1a')
WHITE = HexColor('#ffffff')
LIGHT_GRAY = HexColor('#e8eaf6')
MID_GRAY = HexColor('#8b92a5')
DARK_GRAY = HexColor('#0a4a4f')

CAT_COLORS = {
    'gospel': HexColor('#c49a1a'),
    'political': HexColor('#8b1a1a'),
    'worship': HexColor('#2d6e2d'),
    'business': HexColor('#1a3a8f'),
    'career': HexColor('#6b2d8b'),
}


def generate_pdf_report(output):
    """Generate the full ministry PDF report"""
    from .models import Student, Category, Event, Attendance, University

    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Campus Impact Ministry Report",
        author="TAG SCT Changanyikeni",
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Custom styles ──────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        'CITitle', parent=styles['Title'],
        fontName='Helvetica-Bold', fontSize=28,
        textColor=NAVY, spaceAfter=4, leading=32,
    )
    subtitle_style = ParagraphStyle(
        'CISubtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=13,
        textColor=GOLD, spaceAfter=2,
    )
    heading_style = ParagraphStyle(
        'CIHeading', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=14,
        textColor=NAVY, spaceBefore=14, spaceAfter=6,
        borderPad=4,
    )
    body_style = ParagraphStyle(
        'CIBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=10,
        textColor=HexColor('#333333'), spaceAfter=6, leading=14,
    )
    small_style = ParagraphStyle(
        'CISmall', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8,
        textColor=MID_GRAY,
    )
    white_style = ParagraphStyle(
        'CIWhite', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11,
        textColor=WHITE,
    )

    # ── COVER HEADER ──────────────────────────────────────────────────────
    # Navy header bar via table
    header_data = [[
        Paragraph('CAMPUS IMPACT', ParagraphStyle('H', fontName='Helvetica-Bold',
                   fontSize=30, textColor=WHITE, leading=34)),
    ]]
    header_table = Table(header_data, colWidths=[doc.width])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)

    # Gold accent bar
    gold_bar_data = [[
        Paragraph('3,000 UNIVERSITY STUDENTS IMPACT IN 2 YEARS  ·  TAG SCT CHANGANYIKENI',
                  ParagraphStyle('G', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY)),
    ]]
    gold_bar = Table(gold_bar_data, colWidths=[doc.width])
    gold_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GOLD),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
    ]))
    story.append(gold_bar)
    story.append(Spacer(1, 0.4 * cm))

    # Report meta
    meta_data = [[
        Paragraph(f'Generated: {datetime.now().strftime("%d %B %Y, %I:%M %p")}', small_style),
        Paragraph('Career  ·  Faith  ·  Teaching  ·  Purpose', small_style),
    ]]
    meta_table = Table(meta_data, colWidths=[doc.width / 2, doc.width / 2])
    meta_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(meta_table)
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    story.append(Spacer(1, 0.5 * cm))

    # ── KEY METRICS ───────────────────────────────────────────────────────
    total_students = Student.objects.filter(is_active=True).count()
    total_goal = 3000
    progress_pct = min(round(total_students / total_goal * 100, 1), 100)
    total_events = Event.objects.count()
    universities_reached = University.objects.filter(is_reached=True).count()
    total_att = Attendance.objects.filter(attended=True).count()
    total_possible = Attendance.objects.count()
    att_rate = round(total_att / total_possible * 100) if total_possible else 0

    story.append(Paragraph('Executive Summary', heading_style))

    metrics = [
        ('Students Reached', str(total_students), f'Goal: {total_goal:,}'),
        ('Overall Progress', f'{progress_pct}%', 'of 2-year goal'),
        ('Events Held', str(total_events), f'{Event.objects.filter(is_completed=True).count()} completed'),
        ('Universities Reached', str(universities_reached), f'of {University.objects.count()} in DSM'),
        ('Avg. Attendance Rate', f'{att_rate}%', 'across all events'),
    ]

    metrics_data = [[
        _make_metric_cell(label, value, sub)
        for label, value, sub in metrics
    ]]
    col_w = doc.width / 5
    metrics_table = Table(metrics_data, colWidths=[col_w] * 5, rowHeights=[2.5 * cm])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), NAVY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#0a4a4f')),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── PROGRESS BAR (visual) ─────────────────────────────────────────────
    story.append(Paragraph('Overall Goal Progress', heading_style))
    story.append(_make_progress_bar(progress_pct, total_students, total_goal, doc.width))
    story.append(Spacer(1, 0.4 * cm))

    # ── CATEGORY BREAKDOWN ────────────────────────────────────────────────
    story.append(Paragraph('Category Breakdown — Vivid Outcomes', heading_style))
    categories = Category.objects.all()

    cat_header = [
        Paragraph('Category', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE)),
        Paragraph('Target', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE)),
        Paragraph('Reached', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE)),
        Paragraph('Progress', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE)),
        Paragraph('%', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=10, textColor=WHITE)),
    ]
    cat_rows = [cat_header]
    for cat in categories:
        cat_rows.append([
            Paragraph(cat.name, body_style),
            Paragraph(str(cat.target_count), body_style),
            Paragraph(str(cat.current_count), body_style),
            _make_inline_progress(cat.progress_percent, CAT_COLORS.get(cat.slug, MID_GRAY)),
            Paragraph(f'{cat.progress_percent}%', body_style),
        ])

    cat_table = Table(cat_rows, colWidths=[
        doc.width * 0.38, doc.width * 0.1,
        doc.width * 0.1, doc.width * 0.32, doc.width * 0.1
    ])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.3, MID_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 0.5 * cm))

    # ── STUDENT LIST ──────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('Registered Students', heading_style))

    students = Student.objects.filter(is_active=True).select_related(
        'university'
    ).prefetch_related('categories').order_by('last_name')

    s_header = [
        Paragraph('#', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Name', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('University', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Category', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Year', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Joined', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
    ]
    s_rows = [s_header]
    for i, s in enumerate(students, 1):
        student_cats = list(s.categories.all())
        primary = student_cats[0] if student_cats else None
        cat_color = CAT_COLORS.get(primary.slug if primary else '', MID_GRAY)
        cat_label = ', '.join(c.name for c in student_cats) if student_cats else '-'
        row = [
            Paragraph(str(i), small_style),
            Paragraph(s.full_name, body_style),
            Paragraph(str(s.university) if s.university else '-', small_style),
            Paragraph(cat_label,
                      ParagraphStyle('cc', fontName='Helvetica', fontSize=8,
                                     textColor=cat_color)),
            Paragraph(s.get_year_of_study_display(), small_style),
            Paragraph(s.date_joined.strftime('%d %b %Y'), small_style),
        ]
        s_rows.append(row)

    if len(s_rows) > 1:
        s_table = Table(s_rows, colWidths=[
            doc.width * 0.05, doc.width * 0.22, doc.width * 0.22,
            doc.width * 0.25, doc.width * 0.1, doc.width * 0.16
        ], repeatRows=1)
        s_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ('GRID', (0, 0), (-1, -1), 0.3, MID_GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        story.append(s_table)
    else:
        story.append(Paragraph('No students registered yet.', body_style))

    story.append(Spacer(1, 0.5 * cm))

    # ── EVENTS SUMMARY ────────────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph('Events Summary', heading_style))

    events = Event.objects.all().order_by('-event_date')
    ev_header = [
        Paragraph('Event', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Type', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Date', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Location', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Attended', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
        Paragraph('Rate', ParagraphStyle('H', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE)),
    ]
    ev_rows = [ev_header]
    for ev in events:
        ev_rows.append([
            Paragraph(ev.title, body_style),
            Paragraph(ev.get_event_type_display(), small_style),
            Paragraph(ev.event_date.strftime('%d %b %Y'), small_style),
            Paragraph(ev.location[:30] + '...' if len(ev.location) > 30 else ev.location, small_style),
            Paragraph(str(ev.actual_attendance), body_style),
            Paragraph(f'{ev.attendance_rate}%', small_style),
        ])

    if len(ev_rows) > 1:
        ev_table = Table(ev_rows, colWidths=[
            doc.width * 0.28, doc.width * 0.15, doc.width * 0.13,
            doc.width * 0.22, doc.width * 0.1, doc.width * 0.12
        ], repeatRows=1)
        ev_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), NAVY),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ('GRID', (0, 0), (-1, -1), 0.3, MID_GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(ev_table)

    # ── FOOTER ────────────────────────────────────────────────────────────
    story.append(Spacer(1, 1 * cm))
    story.append(HRFlowable(width="100%", thickness=1, color=GOLD))
    story.append(Spacer(1, 0.2 * cm))
    footer_data = [[
        Paragraph('Campus Impact · TAG SCT Changanyikeni', small_style),
        Paragraph(f'Report Date: {date.today().strftime("%d %B %Y")}', small_style),
        Paragraph('Career · Faith · Teaching · Purpose', small_style),
    ]]
    footer_table = Table(footer_data, colWidths=[doc.width / 3] * 3)
    footer_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(footer_table)

    doc.build(story)


def _make_metric_cell(label, value, sub):
    """Create a styled metric cell paragraph"""
    return Paragraph(
        f'<font color="#8b92a5" size="8">{label}</font><br/>'
        f'<font color="#c49a1a" size="20"><b>{value}</b></font><br/>'
        f'<font color="#8b92a5" size="7">{sub}</font>',
        ParagraphStyle('M', fontName='Helvetica', fontSize=10,
                       textColor=WHITE, alignment=1, leading=16)
    )


def _make_progress_bar(pct, current, total, width):
    """Create a visual progress bar drawing"""
    bar_height = 28
    d = Drawing(width, bar_height + 30)

    # Background
    d.add(Rect(0, 10, width, bar_height, fillColor=HexColor('#0a4a4f'), strokeColor=None))

    # Fill
    fill_width = max(2, width * pct / 100)
    d.add(Rect(0, 10, fill_width, bar_height, fillColor=GOLD, strokeColor=None))

    # Labels
    d.add(String(2, bar_height + 15, f'{current:,} students reached', fontSize=9,
                  fillColor=HexColor('#8b92a5')))
    d.add(String(width - 2, bar_height + 15, f'Goal: {total:,}', fontSize=9,
                  fillColor=HexColor('#8b92a5'), textAnchor='end'))
    d.add(String(min(fill_width - 4, width - 40), 20, f'{pct}%', fontSize=11,
                  fillColor=NAVY, fontName='Helvetica-Bold'))
    return d


def _make_inline_progress(pct, color):
    """Small inline progress bar for table"""
    w, h = 120, 12
    d = Drawing(w, h)
    d.add(Rect(0, 2, w, h - 4, fillColor=HexColor('#e0e0e0'), strokeColor=None))
    fill_w = max(1, w * pct / 100)
    d.add(Rect(0, 2, fill_w, h - 4, fillColor=color, strokeColor=None))
    return d
