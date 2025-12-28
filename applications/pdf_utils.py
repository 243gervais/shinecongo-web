from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse


class NumberedCanvas(canvas.Canvas):
    """Custom canvas for page numbers"""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.grey)
        self.drawRightString(7*inch, 0.5*inch, f"Page {self._pageNumber} / {page_count}")
        self.restoreState()


def generate_cv_pdf(application):
    """Generate a modern PDF CV from manual application data - optimized for one page"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                           rightMargin=1*cm, leftMargin=1*cm,
                           topMargin=1*cm, bottomMargin=1*cm)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Modern color scheme
    navy = colors.HexColor('#003B5C')
    cyan = colors.HexColor('#2A9D8F')
    light_cyan = colors.HexColor('#E8F4F3')
    dark_grey = colors.HexColor('#333333')
    medium_grey = colors.HexColor('#666666')
    light_grey = colors.HexColor('#E5E5E5')
    
    # Header style - Compact but prominent name
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=navy,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold',
        leading=26
    )
    
    # Contact info style - Compact
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontSize=8.5,
        textColor=medium_grey,
        spaceAfter=2,
        alignment=TA_LEFT,
        leading=11
    )
    
    # Section heading style - Compact
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=11,
        textColor=navy,
        spaceAfter=4,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        leading=14
    )
    
    # Content style - Compact
    content_style = ParagraphStyle(
        'ContentStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        textColor=dark_grey,
        spaceAfter=4,
        leading=13,
        alignment=TA_LEFT
    )
    
    # Label style for personal info - Compact
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        textColor=navy,
        fontName='Helvetica-Bold',
        leading=13,
        leftIndent=0
    )
    
    # Value style - Compact
    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        textColor=dark_grey,
        leading=13,
        leftIndent=0
    )
    
    # ========== HEADER SECTION ==========
    # Name
    if application.nom and application.prenom:
        full_name = f"{application.prenom} {application.nom}"
        if application.post_nom:
            full_name += f" {application.post_nom}"
    elif application.full_name:
        full_name = application.full_name
    else:
        full_name = "Candidat"
    
    # Create header with colored sidebar
    header_content = []
    header_content.append(Paragraph(full_name.upper(), header_style))
    
    # Contact information - each on separate line
    contact_lines = []
    if application.phone:
        contact_lines.append(Paragraph(f"<b>Téléphone:</b> {application.phone}", contact_style))
    if application.physical_address:
        contact_lines.append(Paragraph(f"<b>Adresse:</b> {application.physical_address}", contact_style))
    if application.city:
        contact_lines.append(Paragraph(f"<b>Ville:</b> {application.city}", contact_style))
    
    # Header table with colored sidebar
    header_rows = [[header_content[0], '']]
    for contact_line in contact_lines:
        header_rows.append([contact_line, ''])
    
    header_table = Table(header_rows, colWidths=[6.3*inch, 0.2*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (1, -1), cyan),  # Colored sidebar
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 0),
        ('TOPPADDING', (0, 0), (0, -1), 2),
        ('BOTTOMPADDING', (0, 0), (0, -1), 2),
        ('TOPPADDING', (0, 0), (0, 0), 0),  # No top padding for name
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.25*inch))
    
    # ========== PERSONAL INFORMATION SECTION ==========
    personal_info_rows = []
    
    if application.date_of_birth:
        dob_str = application.date_of_birth.strftime('%d/%m/%Y')
        personal_info_rows.append([
            Paragraph('<b>Date de naissance:</b>', label_style),
            Paragraph(dob_str, value_style)
        ])
    
    if application.lieu_de_naissance:
        personal_info_rows.append([
            Paragraph('<b>Lieu de naissance:</b>', label_style),
            Paragraph(application.lieu_de_naissance, value_style)
        ])
    
    if application.sexe:
        sexe_display = dict(application.GENDER_CHOICES).get(application.sexe, application.sexe)
        personal_info_rows.append([
            Paragraph('<b>Sexe:</b>', label_style),
            Paragraph(sexe_display, value_style)
        ])
    
    if application.nationalite:
        personal_info_rows.append([
            Paragraph('<b>Nationalité:</b>', label_style),
            Paragraph(application.nationalite, value_style)
        ])
    
    if personal_info_rows:
        # Section divider
        divider = Table([['']], colWidths=[6.5*inch])
        divider.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 2, cyan),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0), 6),
        ]))
        elements.append(Paragraph("INFORMATIONS PERSONNELLES".upper(), section_style))
        elements.append(divider)
        
        # Personal info table - single column, compact layout
        personal_table = Table(personal_info_rows, colWidths=[2*inch, 4.5*inch])
        personal_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (1, 0), (1, -1), 0),
        ]))
        elements.append(personal_table)
        elements.append(Spacer(1, 0.15*inch))
    
    # ========== EDUCATION SECTION ==========
    if application.education:
        divider = Table([['']], colWidths=[6.5*inch])
        divider.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 2, cyan),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0), 6),
        ]))
        elements.append(Paragraph("FORMATION".upper(), section_style))
        elements.append(divider)
        
        # Format education - preserve line breaks but compact
        education_text = application.education.replace('\n', '<br/>')
        education_para = Paragraph(education_text, content_style)
        elements.append(education_para)
        elements.append(Spacer(1, 0.12*inch))
    
    # ========== SKILLS SECTION ==========
    if application.skills:
        divider = Table([['']], colWidths=[6.5*inch])
        divider.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 2, cyan),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0), 6),
        ]))
        elements.append(Paragraph("COMPÉTENCES".upper(), section_style))
        elements.append(divider)
        
        # Format skills - add bullet points
        skills_text = application.skills
        # Convert line breaks to bullet points
        if '\n' in skills_text:
            lines = [line.strip() for line in skills_text.split('\n') if line.strip()]
            skills_text = '<br/>'.join([f"• {line}" for line in lines])
        elif ', ' in skills_text and '•' not in skills_text:
            # Convert comma-separated to bullet points
            items = [item.strip() for item in skills_text.split(',') if item.strip()]
            skills_text = '<br/>'.join([f"• {item}" for item in items])
        elif '•' not in skills_text:
            skills_text = f"• {skills_text}"
        
        skills_para = Paragraph(skills_text, content_style)
        elements.append(skills_para)
        elements.append(Spacer(1, 0.12*inch))
    
    # ========== LANGUAGES SECTION ==========
    if application.languages:
        divider = Table([['']], colWidths=[6.5*inch])
        divider.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 2, cyan),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0), 6),
        ]))
        elements.append(Paragraph("LANGUES PARLÉES".upper(), section_style))
        elements.append(divider)
        
        languages_para = Paragraph(application.languages, content_style)
        elements.append(languages_para)
        elements.append(Spacer(1, 0.12*inch))
    
    # ========== REFERENCE SECTION ==========
    if application.how_heard_about:
        divider = Table([['']], colWidths=[6.5*inch])
        divider.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 2, cyan),
            ('TOPPADDING', (0, 0), (0, 0), 0),
            ('BOTTOMPADDING', (0, 0), (0, 0), 6),
        ]))
        elements.append(Paragraph("RÉFÉRENCE".upper(), section_style))
        elements.append(divider)
        
        how_heard_display = dict(application.HOW_HEARD_CHOICES).get(application.how_heard_about, application.how_heard_about)
        reference_text = f"<b>{how_heard_display}</b>"
        if application.how_heard_details:
            reference_text += f"<br/>{application.how_heard_details}"
        
        reference_para = Paragraph(reference_text, content_style)
        elements.append(reference_para)
        elements.append(Spacer(1, 0.12*inch))
    
    # ========== FOOTER ==========
    elements.append(Spacer(1, 0.15*inch))
    footer_line = Table([['']], colWidths=[6.5*inch])
    footer_line.setStyle(TableStyle([
        ('LINEBELOW', (0, 0), (0, 0), 1, light_grey),
        ('TOPPADDING', (0, 0), (0, 0), 0),
        ('BOTTOMPADDING', (0, 0), (0, 0), 4),
    ]))
    elements.append(footer_line)
    
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=7.5,
        textColor=medium_grey,
        alignment=TA_CENTER,
        spaceBefore=4
    )
    if application.applied_at:
        applied_date = application.applied_at.strftime('%d/%m/%Y à %H:%M')
        elements.append(Paragraph(f"Candidature soumise le {applied_date}", footer_style))
    
    # Build PDF (no page numbers needed for single page)
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    
    return pdf
