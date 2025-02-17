import telebot
import cv2
import pandas as pd
import numpy as np
from pyzbar.pyzbar import decode
import os
import fitz  # PyMuPDF لاستخراج الصور من ملفات PDF

# ضع توكن البوت الخاص بك هنا
BOT_TOKEN = "your token"

# إنشاء كائن البوت
bot = telebot.TeleBot(BOT_TOKEN)

# اسم ملف Excel لحفظ الروابط
output_excel = "qr_links.xlsx"

# التأكد من وجود ملف Excel
if not os.path.exists(output_excel):
    df = pd.DataFrame(columns=["User", "QR Link"])
    df.to_excel(output_excel, index=False)

# دالة تحليل صورة QR

def extract_qr_link(image_bytes):
    """تحليل صورة QR واستخراج الرابط منها"""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    decoded_objects = decode(img)
    
    links = [obj.data.decode("utf-8") for obj in decoded_objects]
    return links if links else None

# دالة استخراج الصور من PDF وتحليلها

def extract_qr_from_pdf(pdf_path):
    """استخراج أكواد QR من ملف PDF"""
    extracted_links = []
    doc = fitz.open(pdf_path)
    
    for page in doc:
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            qr_links = extract_qr_link(image_bytes)
            if qr_links:
                extracted_links.extend(qr_links)
    
    return extracted_links

# استقبال ملفات PDF أو صور متعددة وتحليلها
@bot.message_handler(content_types=['document', 'photo'])
def handle_qr_files(message):
    """التعامل مع استقبال ملفات PDF أو صور متعددة واستخراج روابط QR منها"""
    user_id = message.from_user.username or message.from_user.id
    extracted_links = []
    
    if message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        file_extension = os.path.splitext(message.document.file_name)[1].lower()
        file_path = file_info.file_path
        file = bot.download_file(file_path)
        
        if file_extension == ".pdf":
            pdf_filename = "temp_qr.pdf"
            with open(pdf_filename, "wb") as pdf_file:
                pdf_file.write(file)
            extracted_links = extract_qr_from_pdf(pdf_filename)
            os.remove(pdf_filename)
        else:
            img_links = extract_qr_link(file)
            if img_links:
                extracted_links.extend(img_links)
    
    elif message.content_type == 'photo':
        for photo in message.photo:
            file_info = bot.get_file(photo.file_id)
            file = bot.download_file(file_info.file_path)
            img_links = extract_qr_link(file)
            if img_links:
                extracted_links.extend(img_links)
    
    if extracted_links:
        # تحديث ملف Excel
        df = pd.read_excel(output_excel)
        new_data = pd.DataFrame([{ "User": user_id, "QR Link": link } for link in extracted_links])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(output_excel, index=False)
        
        # إرسال الروابط المستخرجة للمستخدم
        bot.reply_to(message, "✅ الروابط المستخرجة:\n" + "\n".join(extracted_links))
        
        # إرسال ملف Excel للمستخدم
        with open(output_excel, "rb") as file:
            bot.send_document(message.chat.id, file, caption="📂 هذا هو ملف Excel المحدث بجميع الروابط.")
    else:
        bot.reply_to(message, "❌ لم أتمكن من استخراج أي أكواد QR من الملفات أو الصور المرسلة.")

# تشغيل البوت
bot.polling()
