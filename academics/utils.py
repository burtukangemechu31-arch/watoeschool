# academics/utils.py
import io
from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import StudentProfile, MarkAssessment

def calculate_and_rank_section(section, semester, academic_year):
    """
    Computes total marks, semester average, and sorts students to assign class rank.
    """
    students = StudentProfile.objects.filter(section=section)
    report_data = []

    for student in students:
        assessments = MarkAssessment.objects.filter(
            student=student, semester=semester, academic_year=academic_year
        )
        total_marks = sum(a.total_mark for a in assessments)
        subject_count = assessments.count()
        average_mark = (total_marks / subject_count) if subject_count > 0 else Decimal('0.00')

        report_data.append({
            'student': student,
            'assessments': assessments,
            'total_marks': total_marks,
            'average_mark': average_mark,
        })

    # Sort descending by total marks to determine class rank
    report_data = sorted(report_data, key=lambda x: x['total_marks'], reverse=True)

    for rank, data in enumerate(report_data, start=1):
        data['rank'] = rank

    return report_data

def generate_report_card_pdf(student, semester, academic_year):
    """
    Generates an official Wato Secondary School student report card PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1, # Center
        textColor=colors.HexColor('#1B5E20')
    )
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=1,
        textColor=colors.HexColor('#424242')
    )

    # School Header
    elements.append(Paragraph("WATO SECONDARY SCHOOL", title_style))
    elements.append(Paragraph(f"Official Student Report Card — Semester {semester} ({academic_year.name})", subtitle_style))
    elements.append(Spacer(1, 15))

    # Student Details Table
    user_full_name = f"{student.user.first_name} {student.user.last_name}".strip() or student.user.username
    student_info = [
        [Paragraph(f"<b>Student Name:</b> {user_full_name}", styles['Normal']),
         Paragraph(f"<b>Student ID:</b> {student.student_id}", styles['Normal'])],
        [Paragraph(f"<b>Section:</b> {student.section.name if student.section else 'N/A'}", styles['Normal']),
         Paragraph(f"<b>Program:</b> {student.program.get_name_display()}", styles['Normal'])],
    ]
    info_table = Table(student_info, colWidths=[250, 250])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F8E9')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#C8E6C9')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 15))

    # Marks Assessment Table
    assessments = MarkAssessment.objects.filter(student=student, semester=semester, academic_year=academic_year)
    total_marks = sum(a.total_mark for a in assessments)
    subject_count = assessments.count()
    average_mark = (total_marks / subject_count) if subject_count > 0 else Decimal('0.00')

    table_data = [["Subject", "Total Mark (100%)", "Remark"]]
    for a in assessments:
        remark = "Pass" if a.total_mark >= 50 else "Needs Improvement"
        table_data.append([a.subject.name, f"{a.total_mark:.2f}", remark])

    table_data.append(["<b>Aggregate Summary</b>", f"<b>Total: {total_marks:.2f}</b>", f"<b>Average: {average_mark:.2f}%</b>"])

    marks_table = Table(table_data, colWidths=[220, 140, 140])
    marks_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E7D32')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#E8F5E9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#2E7D32')),
    ]))
    elements.append(marks_table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer