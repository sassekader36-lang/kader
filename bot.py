import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ✅ التوكن
TOKEN = "8277901276:AAHlBTkn3FgWuDrcwrHRIS1DEJRllKr1Hfg"

# ✅ خادم ويب وهمي لمنع توقف Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), SimpleHandler)
    print(f"🌐 Web server running on port {port}")
    server.serve_forever()

threading.Thread(target=run_web_server).start()

# 🧠 الأقسام الفرعية
section_map = {
    "📄 QCM": "qcm",
    "📄Cour": "cour",
    "📄 Resumer": "resumer",
    "Video": "video"
}

# 🧠 السنة الأولى
first_year_subjects = [
    "📘 Anatomie", "🧪 Chimie", "🧬 Biochimie", "🔬 Cytologie",
    "⚛️ Biophysique", "💓 Physiologie", "👶 Embryologie", "📖 SSH",
    "🧫 Histologie", "📊 Biostatistique"
]

# 🧠 السنة الثانية
second_year_subjects = [
    "Cardio", "Digestif", "Urinaire", "Endocrinien",
    "Neurologie", "Immunologie", "Génétique"
]

# 🧠 السنة الثالثة
third_year_subjects = [
    "Biochimie", "Immunologie", "Pharmacologie", "Physiopathologie",
    "Radiologie", "Sémiologie"
]

# 🧠 الأقسام العامة
static_sections = {
    "📚 كتب طبية": "files/livres",
    "🌐 مواقع مفيدة": "files/sites",
    "🤲 أدعية": "files/ad3ya",
    "📎 درايف جميع الكليات والملحقات": "files/drive",
    "👨‍💻 حسابات المطور": "files/developer"
}

# 🏁 البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📚 السنة أولى طب", "📘 السنة ثانية طب"],
        ["📕 السنة ثالثة طب", "📚 كتب طبية"],
        ["🌐 مواقع مفيدة", "🤲 أدعية"],
        ["📎 درايف جميع الكليات والملحقات"],
        ["🌐 وساىل التواصل الاجتماعي الخاصة بالنادي والاعضاء المؤسسين"],
        ["👨‍💻 حسابات المطور"],
        ["🔙 رجوع"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.user_data["last_state"] = "start"
    await update.message.reply_text(
        "👋 أهلاً بك!\nبوت جينيورا مخصص لطلبة الطب.\nاختر القسم المطلوب:",
        reply_markup=reply_markup
    )

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def first_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subjects = [
        ["📘 Anatomie", "🧪 Chimie"],
        ["🧬 Biochimie", "🔬 Cytologie"],
        ["⚛️ Biophysique", "💓 Physiologie"],
        ["👶 Embryologie", "📖 SSH"],
        ["🧫 Histologie", "📊 Biostatistique"],
        ["🔙 رجوع"]
    ]
    reply_markup = ReplyKeyboardMarkup(subjects, resize_keyboard=True)
    context.user_data["last_state"] = "first_year"
    await update.message.reply_text("📚 السنة أولى طب:\nاختر المادة:", reply_markup=reply_markup)

async def second_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subjects = [
        ["Cardio", "Digestif"],
        ["Urinaire", "Endocrinien"],
        ["Neurologie", "Immunologie"],
        ["Génétique"],
        ["🔙 رجوع"]
    ]
    reply_markup = ReplyKeyboardMarkup(subjects, resize_keyboard=True)
    context.user_data["last_state"] = "second_year"
    await update.message.reply_text("📘 السنة ثانية طب:\nاختر المادة:", reply_markup=reply_markup)

async def third_year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subjects = [
        ["Biochimie", "Immunologie"],
        ["Pharmacologie", "Physiopathologie"],
        ["Radiologie", "Sémiologie"],
        ["🔙 رجوع"]
    ]
    reply_markup = ReplyKeyboardMarkup(subjects, resize_keyboard=True)
    context.user_data["last_state"] = "third_year"
    await update.message.reply_text("📕 السنة ثالثة طب:\nاختر المادة:", reply_markup=reply_markup)

async def show_subsections(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subject = update.message.text
    context.user_data["current_subject"] = subject
    context.user_data["last_state"] = "subsections"
    keyboard = [["📄 QCM", "📄Cour", "📄 Resumer", "Video"], ["🔙 رجوع"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(f"{subject}:\nاختر الفصل:", reply_markup=reply_markup)

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subject = context.user_data.get("current_subject")
    section = update.message.text
    folder_name = section_map.get(section)

    if not folder_name:
        await update.message.reply_text("⚠️ القسم غير معروف.")
        return

    if subject in first_year_subjects:
        year_folder = "annee1"
    elif subject in second_year_subjects:
        year_folder = "annee2"
    elif subject in third_year_subjects:
        year_folder = "annee3"
    else:
        await update.message.reply_text("⚠️ المادة غير معروفة.")
        return

    clean_subject = subject.split(" ", 1)[-1].lower()
    target_folder = f"files/{year_folder}/{clean_subject}/{folder_name}"

    if not os.path.exists(target_folder):
        await update.message.reply_text("📁 لا توجد ملفات متاحة لهذا القسم حالياً.")
        return

    files = os.listdir(target_folder)
    if not files:
        await update.message.reply_text("📁 لا توجد ملفات في هذا القسم.")
        return

    for file_name in files:
        file_path = os.path.join(target_folder, file_name)
        try:
            if file_name.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    await update.message.reply_text(f"📄 محتوى الملف ({file_name}):\n{content}")
            else:
                await update.message.reply_document(document=open(file_path, "rb"))
        except Exception:
            await update.message.reply_text(f"⚠️ تعذر تحميل الملف: {file_name}")

async def static_section(update: Update, context: ContextTypes.DEFAULT_TYPE):
    section = update.message.text
    folder_path = static_sections.get(section)

    if not folder_path or not os.path.exists(folder_path):
        await update.message.reply_text("📁 لا توجد ملفات متاحة حالياً في هذا القسم.")
        return

    files = os.listdir(folder_path)
    if not files:
        await update.message.reply_text("📁 لا توجد ملفات في هذا القسم.")
        return

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            if file_name.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    await update.message.reply_text(f"📄 محتوى الملف ({file_name}):\n{content}")
            else:
                await update.message.reply_document(document=open(file_path, "rb"))
        except Exception:
            await update.message.reply_text(f"⚠️ تعذر إرسال الملف: {file_name}")

async def show_social_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    folder_path = "files/social"

    if not os.path.exists(folder_path):
        await update.message.reply_text("📁 لا توجد روابط حالياً.")
        return

    files = os.listdir(folder_path)
    if not files:
        await update.message.reply_text("📁 لا توجد ملفات في هذا القسم.")
        return

    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            if file_name.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:

                    content = f.read()
                    await update.message.reply_text(f"🌐 روابط التواصل ({file_name}):\n{content}")
            else:
                await update.message.reply_document(document=open(file_path, "rb"))
        except Exception:
            await update.message.reply_text(f"⚠️ تعذر إرسال الملف: {file_name}")

# 🚀 تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

# أوامر البداية والتنقل
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📚 السنة أولى طب$"), first_year))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📘 السنة ثانية طب$"), second_year))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^📕 السنة ثالثة طب$"), third_year))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^🔙 رجوع$"), go_back))

# المواد الدراسية
for subject in first_year_subjects + second_year_subjects + third_year_subjects:
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f"^{subject}$"), show_subsections))

# الأقسام الفرعية داخل المواد
for section in section_map.keys():
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f"^{section}$"), send_file))

# الأقسام العامة مثل الكتب والمواقع والأدعية والدرايف والمطور
for static in static_sections.keys():
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(f"^{static}$"), static_section))

# قسم روابط التواصل الاجتماعي للنادي والأعضاء المؤسسين
app.add_handler(MessageHandler(
    filters.TEXT & filters.Regex("^🌐 وساىل التواصل الاجتماعي الخاصة بالنادي والاعضاء المؤسسين$"),
    show_social_links
))

print("✅ البوت يعمل الآن وينتظر الرسائل...")
app.run_polling()
