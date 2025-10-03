import telebot
from telebot import types
import os

# إعداد التوكن وتشغيل البوت
TOKEN = "8239915227:AAFSi9Cx4u7SpCoyVwRPnzbgUrc3fhwJxLI"
bot = telebot.TeleBot(TOKEN)

# الأقسام الرئيسية والفرعية
SECTIONS = {
    "📅 البرنامج السنوي": ["سنة أولى", "سنة ثانية", "سنة ثالثة"],
    "🕒 استعمال الزمن": ["سنة أولى", "سنة ثانية", "سنة ثالثة"],
    "🧑‍⚕️ سنة أولى طب": {
        "اناتومي": ["cour", "qcm", "resumer", "video"],
        "فيزيولوجي": ["cour", "qcm", "resumer", "video"],
        "امبريولوجي": ["cour", "qcm", "resumer", "video"],
        "شيمي": ["cour", "qcm", "resumer", "video"],
        "بيوشيمي": ["cour", "qcm", "resumer", "video"],
        "هيستولوجي": ["cour", "qcm", "resumer", "video"],
        "بيوستات": ["cour", "qcm", "resumer", "video"],
        "SSH": ["cour", "qcm", "resumer", "video"],
        "سيتولوجي": ["cour", "qcm", "resumer", "video"],
        "بيوفيزيك": ["cour", "qcm", "resumer", "video"]
    },
    "🧑‍⚕️ سنة ثانية طب": {
    "Cardio-respiratoire": ["cour", "qcm", "resumer", "video"],
    "Degestif": ["cour", "qcm", "resumer", "video"],
    "Urinaire": ["cour", "qcm", "resumer", "video"],
    "Le systeme endocrinien": ["cour", "qcm", "resumer", "video"],
    "le systeme nerveux": ["cour", "qcm", "resumer", "video"],
    "Immunologie": ["cour", "qcm", "resumer", "video"],
    "Genitique": ["cour", "qcm", "resumer", "video"]
},
"🧑‍⚕️ سنة ثالثة طب": {
    "Appareil digestif et organes hématopoïétiques": ["cour", "qcm", "resumer", "video"],
    "Appareil endocrinien, appareil de reproduction & Appareil urinaire": ["cour", "qcm", "resumer", "video"],
    "Appareil Neurologique, Locomoteur & Cutanée": ["cour", "qcm", "resumer", "video"],
    "Appareil Cardio-Vasculaire et Respiratoire": ["cour", "qcm", "resumer", "video"],
    "Immunologie": ["cour", "qcm", "resumer", "video"],
    "Parasitologie mycologie": ["cour", "qcm", "resumer", "video"],
    "Microbiologie medicale": ["cour", "qcm", "resumer", "video"],
    "Parmacologie clinique": ["cour", "qcm", "resumer", "video"],
    "Anatomie et cytologie pathologique": ["cour", "qcm", "resumer", "video"]
}

    },
    "📢 قنوات تلجرام": ["قنوات تعليمية", "قنوات طبية", "قنوات عامة"],
    "🌐 مواقع وتطبيقات مفيدة": ["مواقع", "تطبيقات", "تطبيقات باشتراكات مجانية"],
    "🕊️ أدعية": ["أدعية الصباح والمساء", "أدعية الامتحان", "أدعية متنوعة"],
    "👥 حسابات النادي والأعضاء الرىيسيين": ["رئيس النادي", "نائب الرئيس", "أعضاء الفريق"],
    "💻 حسابات المطور": ["insagram", "Telegram", "facebook"],
    "🚀 قسم تطوير المهارات": ["مهارات الدراسة", "مهارات تقنية"],
    "📚 كتب طبية": ["كتب سنة أولى", "كتب سنة ثانية", "كتب سنة ثالثة"],
    "📂 درايفات جميع الملحقات والكليات": ["كلية الطب وهران", " باقي الكليات الملحقات"],
    "🤖 بوتات مفيدة": ["بوتات مكتبة", "اخرى"]
}

user_state = {}

# زر الرجوع والصفحة الرئيسية
def add_navigation_buttons(markup):
    markup.add("🔙 رجوع")
    markup.add("🏠 الصفحة الرئيسية")
    return markup

# بدء البوت
@bot.message_handler(commands=['start', 'upload'])
def start_upload(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = list(SECTIONS.keys())
    for i in range(0, len(buttons), 2):
        markup.add(*buttons[i:i+2])
    add_navigation_buttons(markup)
    user_state[message.chat.id] = {"step": "section"}
    bot.send_message(message.chat.id, "📂 اختر القسم الرئيسي لعرض الملفات:", reply_markup=markup)

# الصفحة الرئيسية
@bot.message_handler(func=lambda msg: msg.text == "🏠 الصفحة الرئيسية")
def go_home(message):
    start_upload(message)

# الرجوع خطوة للخلف
@bot.message_handler(func=lambda msg: msg.text == "🔙 رجوع")
def go_back_step(message):
    state = user_state.get(message.chat.id)
    if not state:
        start_upload(message)
        return

    step = state.get("step")
    if step == "subsection":
        start_upload(message)
    elif step == "subject":
        choose_subsection(message)
    elif step == "file_type":
        choose_subject(message)
    elif step == "semester":
        choose_file_type(message)
    elif step == "section":
        bot.send_message(message.chat.id, "🔙 أنت في الصفحة الرئيسية بالفعل.")
    else:
        start_upload(message)

# اختيار القسم الفرعي أو المادة
@bot.message_handler(func=lambda msg: user_state.get(msg.chat.id, {}).get("step") == "section")
def choose_subsection(message):
    section = message.text.strip()
    if section not in SECTIONS:
        bot.send_message(message.chat.id, "❗️الاختيار غير صحيح، يرجى اختيار من القائمة.")
        return

    user_state[message.chat.id]["section"] = section
    subsections = SECTIONS[section]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if isinstance(subsections, list):
        for item in subsections:
            markup.add(item)
        add_navigation_buttons(markup)
        user_state[message.chat.id]["step"] = "subsection"
        bot.send_message(message.chat.id, "📁 اختر القسم الفرعي لعرض الملفات:", reply_markup=markup)
    elif isinstance(subsections, dict):
        for item in subsections:
            markup.add(item)
        add_navigation_buttons(markup)
        user_state[message.chat.id]["step"] = "subject"
        bot.send_message(message.chat.id, "📘 اختر المادة لعرض الملفات:", reply_markup=markup)

# عرض ملفات القسم الفرعي
@bot.message_handler(func=lambda msg: user_state.get(msg.chat.id, {}).get("step") == "subsection")
def browse_show_subsection(message):
    subsection = message.text.strip()
    section = user_state[message.chat.id]["section"]
    if subsection not in SECTIONS.get(section, []):
        bot.send_message(message.chat.id, "❗️الاختيار غير صحيح، يرجى اختيار من القائمة.")
        return
    path = os.path.join("uploads", section, subsection)
    send_files_from_path(message.chat.id, path)

# اختيار نوع الملف حسب المادة
@bot.message_handler(func=lambda msg: user_state.get(msg.chat.id, {}).get("step") == "subject")
def choose_subject(message):
    subject = message.text.strip()
    section = user_state[message.chat.id]["section"]
    if subject not in SECTIONS.get(section, {}):
        bot.send_message(message.chat.id, "❗️الاختيار غير صحيح، يرجى اختيار من القائمة.")
        return
    user_state[message.chat.id]["subject"] = subject
    file_types = SECTIONS[section][subject]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in file_types:
        markup.add(item)
    add_navigation_buttons(markup)
    user_state[message.chat.id]["step"] = "file_type"
    bot.send_message(message.chat.id, "📂 اختر نوع الملف لعرضه:", reply_markup=markup)

# اختيار الفصل الدراسي
@bot.message_handler(func=lambda msg: user_state.get(msg.chat.id, {}).get("step") == "file_type")
def choose_file_type(message):
    file_type = message.text.strip()
    section = user_state[message.chat.id]["section"]
    subject = user_state[message.chat.id]["subject"]
    if file_type not in SECTIONS.get(section, {}).get(subject, []):
        bot.send_message(message.chat.id, "❗️الاختيار غير صحيح، يرجى اختيار من القائمة.")
        return
    user_state[message.chat.id]["file_type"] = file_type
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("الفصل الأول", "الفصل الثاني")
    add_navigation_buttons(markup)
    user_state[message.chat.id]["step"] = "semester"
    bot.send_message(message.chat.id, "📅 اختر الفصل لعرض الملفات:", reply_markup=markup)

# عرض الملفات النهائية
@bot.message_handler(func=lambda msg: user_state.get(msg.chat.id, {}).get("step") == "semester")
def browse_show_files(message):
    semester = message.text.strip()
    if semester not in ["الفصل الأول", "الفصل الثاني"]:
        bot.send_message(message.chat.id, "❗️الاختيار غير صحيح، يرجى اختيار من القائمة.")
        return
    section = user_state[message.chat.id]["section"]
    subject = user_state[message.chat.id]["subject"]
    file_type = user_state[message.chat.id]["file_type"]
    path = os.path.join("uploads", section, subject, file_type, semester)
    send_files_from_path(message.chat.id, path)

def send_files_from_path(chat_id, path):
    if not os.path.exists(path):
        bot.send_message(chat_id, "❌ لا توجد ملفات في هذا القسم.")
        return

    files_sent = False
    for root, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            with open(full_path, 'rb') as f:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    bot.send_photo(chat_id, f)
                    files_sent = True
                elif file.lower().endswith(('.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt')):
                    bot.send_document(chat_id, f)
                    files_sent = True
                else:
                    bot.send_message(chat_id, f"📎 ملف غير مدعوم: {file}")
                    files_sent = True

    if not files_sent:
        bot.send_message(chat_id, "📂 تم العثور على ملفات، لكن لا يمكن عرضها مباشرة عبر البوت.")

print("✅ البوت جاهز ويعمل الآن...")
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"❌ حدث خطأ أثناء تشغيل البوت: {e}")