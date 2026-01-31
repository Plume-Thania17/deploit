from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def generer_pdf_recu(inscription):
    """Génère un PDF de reçu d'inscription"""
    buffer = BytesIO()
    
    # Créer le document PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#64B5F6'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Style pour les sous-titres
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # En-tête
    story.append(Paragraph("ÉCOLE SUPÉRIEURE AFRICAINE DES", title_style))
    story.append(Paragraph("TECHNOLOGIES DE L'INFORMATION ET DE LA COMMUNICATION", title_style))
    story.append(Paragraph("(ESATIC)", title_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Titre du document
    recu_style = ParagraphStyle(
        'RecuTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph("REÇU D'INSCRIPTION AU CONCOURS", recu_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Numéro d'inscription
    numero_data = [
        ["Numéro d'inscription:", inscription.numero_inscription]
    ]
    numero_table = Table(numero_data, colWidths=[8*cm, 8*cm])
    numero_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#E3F2FD')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#BBDEFB')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#64B5F6'))
    ]))
    story.append(numero_table)
    story.append(Spacer(1, 0.8*cm))
    
    # Informations du candidat
    story.append(Paragraph("INFORMATIONS DU CANDIDAT", subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    
    candidat_data = [
        ['Nom:', inscription.nom],
        ['Prénom:', inscription.prenom],
        ['Email:', inscription.email],
        ["Niveau d'études:", inscription.niveauEtude],
        ["Établissement d'origine:", inscription.etablissementOrigine],
        ['Concours souhaité:', inscription.get_concoursSouhaiter_display()],
        ["Date d'inscription:", inscription.date_inscription.strftime('%d/%m/%Y à %H:%M')]
    ]
    
    candidat_table = Table(candidat_data, colWidths=[7*cm, 9*cm])
    candidat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BBDEFB'))
    ]))
    story.append(candidat_table)
    story.append(Spacer(1, 1*cm))
    
    # Documents fournis
    story.append(Paragraph("DOCUMENTS FOURNIS", subtitle_style))
    story.append(Spacer(1, 0.3*cm))
    
    documents_data = [
        ['✓', "Photo d'identité"],
        ['✓', 'Extrait de naissance'],
        ['✓', 'Certificat de nationalité'],
        ['✓', 'Diplôme'],
        ['✓', 'Lettre de motivation']
    ]
    
    documents_table = Table(documents_data, colWidths=[1.5*cm, 14.5*cm])
    documents_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#27AE60')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(documents_table)
    story.append(Spacer(1, 1*cm))
    
    # Note importante
    note_text = """
    <b>NOTE IMPORTANTE:</b><br/>
    Ce reçu confirme votre inscription au concours d'entrée à l'ESATIC. 
    Conservez-le précieusement. Vous recevrez votre convocation par email 
    quelques jours avant la date des épreuves.
    """
    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#E74C3C'),
        leftIndent=1*cm,
        rightIndent=1*cm,
        spaceAfter=12
    )
    story.append(Paragraph(note_text, note_style))
    
    # Pied de page
    story.append(Spacer(1, 1*cm))
    footer_text = f"""
    <i>Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</i><br/>
    ESATIC - Route de Bingerville, Abidjan, Côte d'Ivoire<br/>
    Tél: +225 27 22 48 38 00 | Email: concours@esatic.ci
    """
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(footer_text, footer_style))
    
    # Construire le PDF
    doc.build(story)
    
    # Récupérer le contenu du buffer
    buffer.seek(0)
    return buffer


def generer_pdf_convocation(inscription):
    """Génère un PDF de convocation pour le concours"""
    buffer = BytesIO()
    
    # Créer le document PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#64B5F6'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # En-tête officiel
    story.append(Paragraph("RÉPUBLIQUE DE CÔTE D'IVOIRE", title_style))
    story.append(Paragraph("Union - Discipline - Travail", title_style))
    story.append(Spacer(1, 0.5*cm))
    
    story.append(Paragraph("ÉCOLE SUPÉRIEURE AFRICAINE DES TECHNOLOGIES", title_style))
    story.append(Paragraph("DE L'INFORMATION ET DE LA COMMUNICATION", title_style))
    story.append(Paragraph("(ESATIC)", title_style))
    story.append(Spacer(1, 1*cm))
    
    # Titre de la convocation
    convocation_style = ParagraphStyle(
        'ConvocationTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#E74C3C'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    story.append(Paragraph("CONVOCATION AU CONCOURS D'ENTRÉE", convocation_style))
    story.append(Paragraph("Session 2025", subtitle_style))
    story.append(Spacer(1, 0.8*cm))
    
    # Numéro de convocation
    numero_text = f"<b>N° de convocation:</b> {inscription.numero_inscription}"
    story.append(Paragraph(numero_text, subtitle_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Informations du candidat
    story.append(Paragraph("CANDIDAT", subtitle_style))
    candidat_data = [
        ['Nom et Prénom:', f"{inscription.nom} {inscription.prenom}"],
        ['Date de naissance:', '[À compléter]'],
        ['Concours:', inscription.get_concoursSouhaiter_display()]
    ]
    
    candidat_table = Table(candidat_data, colWidths=[6*cm, 10*cm])
    candidat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#64B5F6'))
    ]))
    story.append(candidat_table)
    story.append(Spacer(1, 0.8*cm))
    
    # Informations sur les épreuves
    story.append(Paragraph("INFORMATIONS SUR LES ÉPREUVES", subtitle_style))
    epreuves_data = [
        ['Date:', '15 août 2025'],
        ['Heure de convocation:', '07h30'],
        ['Début des épreuves:', '08h00'],
        ['Lieu:', 'ESATIC - Route de Bingerville, Abidjan'],
        ['Salle:', '[Sera affichée le jour J]']
    ]
    
    epreuves_table = Table(epreuves_data, colWidths=[6*cm, 10*cm])
    epreuves_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#64B5F6'))
    ]))
    story.append(epreuves_table)
    story.append(Spacer(1, 0.8*cm))
    
    # Documents à apporter
    story.append(Paragraph("DOCUMENTS À APPORTER OBLIGATOIREMENT", subtitle_style))
    documents_text = """
    • Cette convocation<br/>
    • Une pièce d'identité valide (CNI, Passeport, Attestation)<br/>
    • Deux (2) stylos à bille bleus ou noirs<br/>
    • Une règle, un rapporteur et une équerre<br/>
    • Une calculatrice scientifique non programmable
    """
    doc_style = ParagraphStyle(
        'DocList',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=1*cm,
        spaceAfter=6
    )
    story.append(Paragraph(documents_text, doc_style))
    story.append(Spacer(1, 0.8*cm))
    
    # Instructions importantes
    story.append(Paragraph("INSTRUCTIONS IMPORTANTES", subtitle_style))
    instructions_text = """
    <b>1.</b> Présentez-vous 30 minutes avant le début des épreuves.<br/>
    <b>2.</b> Aucun retard ne sera toléré après le début des épreuves.<br/>
    <b>3.</b> Les téléphones portables et tous appareils électroniques sont strictement interdits dans la salle d'examen.<br/>
    <b>4.</b> Toute fraude ou tentative de fraude entraînera l'exclusion immédiate du candidat.<br/>
    <b>5.</b> Les résultats seront publiés le 30 août 2025 sur le site web de l'ESATIC.
    """
    instructions_style = ParagraphStyle(
        'Instructions',
        parent=styles['Normal'],
        fontSize=10,
        leftIndent=0.5*cm,
        spaceAfter=6
    )
    story.append(Paragraph(instructions_text, instructions_style))
    story.append(Spacer(1, 1*cm))
    
    # Note de bonne chance - CORRECTION ICI: Utiliser Helvetica au lieu de Helvetica-Bold-Oblique
    bonne_chance_text = "Nous vous souhaitons bonne chance pour vos épreuves!"
    bonne_chance_style = ParagraphStyle(
        'BonneChance',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#27AE60'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'  # CHANGÉ de Helvetica-Bold-Oblique à Helvetica-Bold
    )
    story.append(Paragraph(bonne_chance_text, bonne_chance_style))
    story.append(Spacer(1, 0.8*cm))
    
    # Signature
    signature_data = [
        ['', 'Fait à Abidjan, le ' + datetime.now().strftime('%d/%m/%Y')],
        ['', ''],
        ['', 'Le Directeur Général'],
        ['', '[Signature et Cachet]']
    ]
    signature_table = Table(signature_data, colWidths=[8*cm, 8*cm])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (1, -1), 10)
    ]))
    story.append(signature_table)
    
    # Construire le PDF
    doc.build(story)
    
    # Récupérer le contenu du buffer
    buffer.seek(0)
    return buffer