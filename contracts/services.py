import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
import os

def generate_contract_pdf(contract):
    """
    Generates an official, legally structured PDF document for the Contract Farming Agreement.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ContractTitle",
        parent=styles["Heading1"],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f5132"),
        alignment=1, # Center
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        "ContractSubTitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#495057"),
        alignment=1,
        spaceAfter=15
    )
    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0f5132"),
        spaceBefore=10,
        spaceAfter=4,
        fontName="Helvetica-Bold"
    )
    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#212529")
    )
    meta_style = ParagraphStyle(
        "MetaText",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#6c757d")
    )

    # Header with Logo
    logo_path = os.path.join(settings.BASE_DIR, "static", "images", "agrisure_logo.png")
    if os.path.exists(logo_path):
        try:
            logo = RLImage(logo_path, width=1.5*inch, height=1.5*inch)
            story.append(logo)
        except Exception:
            pass

    story.append(Paragraph("AGRISURE DIGITAL FARMING AGREEMENT", title_style))
    story.append(Paragraph(f"Legally Binding Contract #{contract.contract_number} | Formulated under State Model APMC & Contract Farming Framework", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#198754"), spaceAfter=12))

    # Parties Information Table
    farmer = contract.farmer
    buyer = contract.buyer
    farmer_profile = getattr(farmer, "farmer_profile", None)
    buyer_profile = getattr(buyer, "buyer_profile", None)

    party_data = [
        [
            Paragraph("<b>PRODUCER / FARMER (PARTY A)</b>", section_heading),
            Paragraph("<b>PURCHASER / BUYER (PARTY B)</b>", section_heading)
        ],
        [
            Paragraph(f"<b>Name:</b> {farmer.get_full_name() or farmer.username}<br/>"
                      f"<b>Farm:</b> {farmer_profile.farm_name if farmer_profile else 'Registered Farm'}<br/>"
                      f"<b>Location:</b> {farmer_profile.village if farmer_profile else ''}, {farmer_profile.district if farmer_profile else ''}, {farmer_profile.state if farmer_profile else ''}<br/>"
                      f"<b>Contact:</b> {farmer.phone or 'Verified on Platform'}", body_style),
            Paragraph(f"<b>Entity:</b> {buyer_profile.business_name if buyer_profile else buyer.username}<br/>"
                      f"<b>Type:</b> {buyer_profile.get_business_type_display() if buyer_profile else 'Agricultural Buyer'}<br/>"
                      f"<b>Address:</b> {buyer_profile.address if buyer_profile else ''}, {buyer_profile.district if buyer_profile else ''}, {buyer_profile.state if buyer_profile else ''}<br/>"
                      f"<b>Reg/GST No:</b> {buyer_profile.registration_number if buyer_profile else 'Pending Submission'}", body_style),
        ]
    ]

    t_parties = Table(party_data, colWidths=[260, 260])
    t_parties.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8f9fa")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#dee2e6")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_parties)
    story.append(Spacer(1, 10))

    # Commercial Terms Table
    story.append(Paragraph("1. COMMERCIAL TERMS & VALUATION", section_heading))
    commercial_data = [
        ["Parameter", "Agreed Specification / Value"],
        ["Commodity / Crop", f"{contract.crop_name} ({contract.variety or 'Standard Variety'})"],
        ["Contracted Quantity", f"{contract.quantity_kg:,.2f} Kilograms ({contract.quantity_kg/1000:,.2f} Metric Tonnes)"],
        ["Guaranteed Assured Price", f"₹ {contract.agreed_price_per_kg:,.2f} per Kilogram"],
        ["Total Contract Valuation", f"₹ {contract.total_value:,.2f} (Indian Rupees)"],
        ["Designated Delivery Point", f"{contract.delivery_location}"],
        ["Contract Execution Status", f"{contract.get_status_display()}"],
    ]
    t_comm = Table(commercial_data, colWidths=[180, 340])
    t_comm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f5132")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#ced4da")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_comm)
    story.append(Spacer(1, 10))

    # Contract Clauses
    story.append(Paragraph("2. QUALITY ASSURANCE & INSPECTION PROTOCOL", section_heading))
    story.append(Paragraph(contract.quality_specifications, body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. DELIVERY & LOGISTICS SCHEDULE", section_heading))
    story.append(Paragraph(contract.delivery_schedule, body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. PAYMENT TERMS & SETTLEMENT ESCROW", section_heading))
    story.append(Paragraph(contract.payment_terms, body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. DISPUTE CONCILIATION & RESOLUTION", section_heading))
    story.append(Paragraph(contract.dispute_procedure, body_style))
    story.append(Spacer(1, 12))

    # Digital Signature & Acceptance Block
    story.append(Paragraph("6. BILATERAL ELECTRONIC ACCEPTANCE RECORDS", section_heading))

    farmer_sig = "SIGNED & VERIFIED" if contract.farmer_accepted else "PENDING ACCEPTANCE"
    buyer_sig = "SIGNED & VERIFIED" if contract.buyer_accepted else "PENDING ACCEPTANCE"

    farmer_time = contract.farmer_accepted_at.strftime('%d-%b-%Y %H:%M:%S UTC') if contract.farmer_accepted_at else "Awaiting Authentication"
    buyer_time = contract.buyer_accepted_at.strftime('%d-%b-%Y %H:%M:%S UTC') if contract.buyer_accepted_at else "Awaiting Authentication"

    sig_data = [
        [
            Paragraph(f"<b>Farmer Signature:</b><br/>"
                      f"<font color='{'#198754' if contract.farmer_accepted else '#dc3545'}'><b>{farmer_sig}</b></font><br/>"
                      f"<b>Timestamp:</b> {farmer_time}<br/>"
                      f"<b>Hash:</b> {contract.farmer_digital_signature or 'N/A'}", meta_style),
            Paragraph(f"<b>Buyer Signature:</b><br/>"
                      f"<font color='{'#198754' if contract.buyer_accepted else '#dc3545'}'><b>{buyer_sig}</b></font><br/>"
                      f"<b>Timestamp:</b> {buyer_time}<br/>"
                      f"<b>Hash:</b> {contract.buyer_digital_signature or 'N/A'}", meta_style)
        ]
    ]

    t_sig = Table(sig_data, colWidths=[260, 260])
    t_sig.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0f5132")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e8f5e9")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sig)

    story.append(Spacer(1, 15))
    story.append(Paragraph("This document is generated by the AgriSure Platform under Section 65B of the Indian Evidence Act for electronic records.", meta_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
