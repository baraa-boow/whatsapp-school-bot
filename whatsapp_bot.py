from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import mysql.connector
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this if needed
    password="Baraa0909@",  # Change this if you have a MySQL password
    database="school_chatbot"
)
cursor = db.cursor()

# Predefined school chatbot responses (English & Arabic)
responses = {
    "admission": {
        "en": "To register, visit [our website](https://www.akaisschool.com). Call us at +971-6-565-9870.",
        "ar": "للتسجيل، قم بزيارة [موقعنا](https://www.akaisschool.com). اتصل بنا على +971-6-565-9870."
    },
    "curriculum": {
        "en": "We follow the American curriculum from KG to Grade 12. Classes are co-ed until Grade 5, then separated for boys and girls.",
        "ar": "نتبع المنهج الأمريكي من الروضة إلى الصف 12. الفصول مختلطة حتى الصف الخامس، ثم يتم الفصل بين الأولاد والبنات."
    },
    "fees": {
        "en": "For tuition fees, contact info@akaisschool.com or call +971-6-565-9870.",
        "ar": "لرسوم التعليم، يرجى الاتصال info@akaisschool.com أو الاتصال على +971-6-565-9870."
    },
    "facilities": {
        "en": "Our school offers a library, science labs, a mosque, sports facilities, and a medical clinic.",
        "ar": "تقدم مدرستنا مكتبة، مختبرات علمية، مسجد، مرافق رياضية وعيادة طبية."
    },
    "sports": {
        "en": "We offer football, karate, basketball, and more extracurricular activities.",
        "ar": "نحن نقدم كرة القدم، الكاراتيه، كرة السلة، وغيرها من الأنشطة اللامنهجية."
    },
    "contact": {
        "en": "You can contact us at info@akaisschool.com or call +971-6-565-9870.",
        "ar": "يمكنك الاتصال بنا على info@akaisschool.com أو الاتصال على +971-6-565-9870."
    },
    "default": {
        "en": "Hello! Ask about admissions, curriculum, fees, facilities, or contact details.",
        "ar": "مرحبًا! اسأل عن القبول، المناهج، الرسوم، المرافق، أو تفاصيل الاتصال."
    }
}

@app.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").lower()
    user_number = request.values.get("From", "")

    # Detect language (English or Arabic)
    lang = "ar" if any(char in "ءآأؤإئبةتثجحخدذرزسشصضطظعغفقكلمنهوي" for char in incoming_msg) else "en"

    # Check if message matches any predefined response
    response_text = responses["default"][lang]
    for key, values in responses.items():
        if key in incoming_msg:
            response_text = values[lang]
            break

    # Store inquiry in the database
    cursor.execute("INSERT INTO inquiries (user_number, message, response) VALUES (%s, %s, %s)",
                   (user_number, incoming_msg, response_text))
    db.commit()

    # Respond to the user
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(response_text)
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)