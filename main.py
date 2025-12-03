import time
import threading
import telebot
from telebot import types

# ================= إعداد البوت =================

BOT_TOKEN = "6819257727:AAHnRyaBSJZEMoyJcWjFHotvfuZFBbKrhYo"   # ضع التوكن هنا
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

user_lang = {}          # {chat_id: "ar" / "en" / "fr" / "ru"}
DEFAULT_LANG = "ar"

# ضع هنا روابط قنوات الفيديو
FRENCH_VIDEO_LINK  = "https://t.me/YourFrenchChannel"   # فيديو النسخة الفرنسية
ENGLISH_VIDEO_LINK = "https://t.me/YourEnglishChannel"  # فيديو النسخة الإنجليزية
ARABIC_VIDEO_LINK  = "https://t.me/YourArabicChannel"   # فيديو النسخة العربية

TEXTS = {
    "btn_open": {
        "ar": "فتح المتنبئ",
        "en": "Open predictor",
        "fr": "Ouvrir le prédicteur",
        "ru": "Открыть предсказатель"
    },
    "btn_change_lang": {
        "ar": "تغيير اللغة",
        "en": "Change language",
        "fr": "Changer de langue",
        "ru": "Сменить язык"
    },
    "fake_window": {
        "ar": "يتم الآن فتح المتنبئ، يرجى الانتظار...",
        "en": "Opening predictor, please wait...",
        "fr": "Ouverture du prédicteur, veuillez patienter...",
        "ru": "Открывается модуль предсказаний, подождите..."
    },
    "lang_changed": {
        "ar": "تم تغيير اللغة بنجاح.",
        "en": "Language changed successfully.",
        "fr": "Langue changée avec succès.",
        "ru": "Язык успешно изменен."
    },
    "unknown": {
        "ar": "لم أفهم رسالتك. استخدم الأزرار الموجودة تحت الرسالة.",
        "en": "I did not understand. Please use the buttons under the message.",
        "fr": "Je n'ai pas compris. Utilisez les boutons sous le message.",
        "ru": "Я не понял. Используйте кнопки под сообщением."
    }
}

LANG_SELECT_TEXT = (
    "🇫🇷 Veuillez choisir votre langue préférée en cliquant sur le bouton...\n\n"
    "🇺🇸 Please choose your preferred language by clicking on the button...\n\n"
    "🇷🇺 Пожалуйста, выберите предпочитаемый язык, нажав на кнопку...\n\n"
    "🇸🇦 من فضلك، اختر اللغة المفضلة لديك بالضغط على الزر..."
)


# ================= دوال مساعدة =================

def get_lang(chat_id: int) -> str:
    return user_lang.get(chat_id, DEFAULT_LANG)


def set_lang(chat_id: int, lang: str):
    user_lang[chat_id] = lang


def get_text(key: str, lang: str) -> str:
    data = TEXTS.get(key, {})
    return data.get(lang, data.get("en", ""))


def main_message(lang: str) -> str:
    """رسالة ستارت؛ نسخة العربية مطابقة تقريبًا للصورة مع الاقتباسات."""
    if lang == "ar":
        return (
            "<b>اقرأ بشكل إلزامي 🔴</b>\n\n"
            "<blockquote>عزيزي المستخدم،\n"
            "للحصول على موثوقية تصل إلى 99٪ يرجى اتباع هذه الخطوات دون استثناء:</blockquote>\n\n"
            "PREDICTOR SIGNO-BOX\n\n"
            "١️⃣ استخدم الرمز الترويجي:\n"
            "<code>PRED BOX 2 ROBOT</code>\n\n"
            "٢️⃣ فعِّل مكافأة CASINO+GAMME عند التسجيل\n\n"
            "٣️⃣ سجِّل فقط عبر هذا الرابط 👇\n"
            "https://mlbt.cc 👉 <b>/PREDBOX2ROBOT (MELBET)</b>\n\n"
            f"<blockquote>🇫🇷 <a href=\"{FRENCH_VIDEO_LINK}\">فيديو النسخة الفرنسية</a></blockquote>\n"
            f"<blockquote>🇬🇧 <a href=\"{ENGLISH_VIDEO_LINK}\">فيديو النسخة الإنجليزية</a></blockquote>\n\n"
            "٤️⃣ سجِّل فقط عبر هذا الرابط 👇\n"
            "http://bit.ly/48PtwTk 👉 <b>(1XCASINO)</b>\n\n"
            f"<blockquote>🇫🇷 <a href=\"{FRENCH_VIDEO_LINK}\">فيديو النسخة الفرنسية</a></blockquote>\n"
            f"<blockquote>🇸🇦 <a href=\"{ARABIC_VIDEO_LINK}\">فيديو النسخة العربية</a></blockquote>\n\n"
            "<blockquote>هذه الإجراءات تسمح بالمزامنة الصحيحة مع خوارزمياتنا، "
            "بدون ذلك ستكون النتائج جزئية ولا يمكن ضمان الدقة.</blockquote>\n\n"
            "<blockquote>▶️ اتّبع التعليمات = تحصل على أفضل التوقعات.</blockquote>"
        )

    # باقي اللغات تنسيق أبسط؛ تعدّلها لو حابب
    if lang == "en":
        return (
            "<b>Read this carefully 🔴</b>\n\n"
            "Dear user,\n"
            "To reach up to 99% accuracy, follow all steps exactly.\n\n"
            "1) Use promo code: <code>PREDBOX2ROBOT</code>\n"
            "2) Activate CASINO+GAMME bonus during registration\n"
            "3) Register only via our official links\n\n"
            f"🇫🇷 <a href=\"{FRENCH_VIDEO_LINK}\">French version video</a>\n"
            f"🇬🇧 <a href=\"{ENGLISH_VIDEO_LINK}\">English version video</a>\n"
            f"🇸🇦 <a href=\"{ARABIC_VIDEO_LINK}\">Arabic version video</a>\n"
        )

    if lang == "fr":
        return (
            "<b>Lisez ceci attentivement 🔴</b>\n\n"
            "1) Code promo : <code>PREDBOX2ROBOT</code>\n"
            "2) Activez le bonus CASINO+GAMME\n"
            f"🇫🇷 <a href=\"{FRENCH_VIDEO_LINK}\">Vidéo version française</a>\n"
        )

    if lang == "ru":
        return (
            "<b>Внимательно прочитайте 🔴</b>\n\n"
            "1) Промокод: <code>PREDBOX2ROBOT</code>\n"
            f"🇷🇺 <a href=\"{ENGLISH_VIDEO_LINK}\">Видео на английском</a>\n"
        )


def send_start_message(chat_id: int):
    lang = get_lang(chat_id)
    text = main_message(lang)

    markup = types.InlineKeyboardMarkup()
    btn_open = types.InlineKeyboardButton(
        text=get_text("btn_open", lang),
        callback_data="open_predictor"
    )
    btn_change = types.InlineKeyboardButton(
        text=get_text("btn_change_lang", lang),
        callback_data="change_language"
    )
    markup.add(btn_open)
    markup.add(btn_change)

    bot.send_message(chat_id, text, reply_markup=markup)


def send_fake_window(chat_id: int, lang: str, seconds: int = 5):
    text = get_text("fake_window", lang)
    msg = bot.send_message(chat_id, text)

    def auto_delete():
        time.sleep(seconds)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            pass

    threading.Thread(target=auto_delete, daemon=True).start()


def send_language_menu(chat_id: int):
    markup = types.InlineKeyboardMarkup()
    btn_fr = types.InlineKeyboardButton("🇫🇷 Français", callback_data="set_lang_fr")
    btn_en = types.InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")
    btn_ar = types.InlineKeyboardButton("🇸🇦 العربية", callback_data="set_lang_ar")
    markup.row(btn_fr, btn_en)
    markup.row(btn_ru, btn_ar)

    bot.send_message(chat_id, LANG_SELECT_TEXT, reply_markup=markup)


# ================= Handlers =================

@bot.message_handler(commands=['start'])
def on_start(message: telebot.types.Message):
    chat_id = message.chat.id
    if chat_id not in user_lang:
        set_lang(chat_id, DEFAULT_LANG)
    send_start_message(chat_id)


@bot.callback_query_handler(func=lambda call: True)
def on_callback(call: telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_lang(chat_id)
    data = call.data

    if data == "open_predictor":
        bot.answer_callback_query(call.id)
        send_fake_window(chat_id, lang, seconds=5)
        return

    if data == "change_language":
        bot.answer_callback_query(call.id)
        send_language_menu(chat_id)
        return

    if data.startswith("set_lang_"):
        code = data.split("_")[-1]  # fr / en / ru / ar
        if code in ["fr", "en", "ru", "ar"]:
            set_lang(chat_id, code)
        bot.answer_callback_query(call.id, get_text("lang_changed", code))
        send_start_message(chat_id)
        return


@bot.message_handler(content_types=['text'])
def on_text(message: telebot.types.Message):
    chat_id = message.chat.id
    lang = get_lang(chat_id)
    bot.send_message(chat_id, get_text("unknown", lang))


# ================= تشغيل البوت =================

if __name__ == "__main__":
    bot.infinity_polling()
