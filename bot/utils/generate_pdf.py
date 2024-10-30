import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from bot.data.config import CHANNEL_ID
from bot.loader import dp
from PIL import Image as PilImage

async def create_pdf_with_tables(filename, data, image_stream=None):
    buffer = io.BytesIO()  # In-memory buffer
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Title in a single-row centered table
    title_data = [["Sizning ma'lumotlaringiz"]]
    title_table = Table(title_data, colWidths=[400])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(title_table)
    elements.append(Spacer(1, 12))

    # Adjusted table function with more space for the left column and wrapped text
    def create_table(data, col_widths):
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('WORDWRAP', (0, 0), (-1, -1), 'LTR'),
        ]))
        return table

    # Add image with aspect ratio preserved and increased size
    if image_stream:
        try:
            image_stream.seek(0)
            pil_image = PilImage.open(image_stream)
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            # Set image size while maintaining aspect ratio
            img = Image(img_buffer, width=1.5 * inch, height=1.5 * inch)
            img.hAlign = 'LEFT'
            elements.append(img)
            elements.append(Spacer(1, 8))
        except Exception as e:
            elements.append(Paragraph(f"Error displaying image: {e}", styles["Normal"]))

    # Basic Information section with increased left column width
    basic_info_data = [
        ["Ism, Familyasi", data.get('full_name')],
        ["Tug'ilgan yili", data.get('birth_year')],
        ["Telefon raqami", data.get('phone_number')],
        ["Soha bo'yicha yo'nalishi", data.get('position')],
        ["Viloyati", data.get('region')],
        ["Millati", data.get('nationality')],
        ["Ma'lumoti", data.get('education')],
        ["Oilaviy axvoli", data.get('marriage')],
    ]
    elements.append(create_table(basic_info_data, [250, 300]))  # Adjusted column widths
    elements.append(Spacer(1, 10))

    # Work Experience with adjusted column widths and wrapped text
    work_experience_data = [
        ["Mebel sohasida ishlagansizmi", data.get('worked_furniture')],
        ["Qaysi korxona yoki lavozimlarda ishlagansiz", data.get('first_answer')],
        ["Bizda qancha maoshga ishlamoqchisiz", data.get('salary')],
        ["Bizning korxonada qancha muddat ishlamoqchisiz", data.get('second_answer')],
        ["Sudlanganmisiz", data.get('convince')],
    ]
    elements.append(create_table(work_experience_data, [250, 300]))
    elements.append(Spacer(1, 10))

    # Skills and Language Information with adjusted column widths and wrapped text
    skills_data = [
        ["Xaydovchilik guvoxnomangiz bormi", data.get('driver_license')],
        ["O'zingizning shaxsiy avtomobilingiz bormi", data.get('has_car')],
        ["Ingliz tilini bilish darajangiz", data.get('english_level')],
        ["Rus tilini bilish darajangiz", data.get('russian_level')],
        ["Boshqa tillar", data.get('other_language')],
        ["Word dasturini bilish darajangiz", data.get('third_answer')],
        ["Excel dasturini bilish darajangiz", data.get('fourth_answer')],
        ["1C dasturini bilish darajangiz", data.get('c1_program_level')],
        ["Boshqa dasturlarni bilish darajangiz", data.get('fifth_answer')],
    ]
    elements.append(create_table(skills_data, [250, 300]))

    # Generate the PDF
    pdf.build(elements)
    buffer.seek(0)
    
    # Save the PDF to file
    with open(filename, 'wb') as pdf_file:
        pdf_file.write(buffer.getvalue())
    
    buffer.seek(0)  # Reset the buffer for further use
    return buffer  # Return buffer for uploading



async def upload_to_channel(pdf_buffer, image_file_id, caption_text):
    # Upload PDF
    pdf_message = await dp.bot.send_document(chat_id=CHANNEL_ID, document=("data.pdf", pdf_buffer), caption=caption_text)
    pdf_file_id = pdf_message.document.file_id

    # Upload Image if available
    image_file_id_uploaded = None
    if image_file_id:
        image_message = await dp.bot.send_photo(chat_id=CHANNEL_ID, photo=image_file_id)
        image_file_id_uploaded = image_message.photo[-1].file_id

    return pdf_file_id, image_file_id_uploaded