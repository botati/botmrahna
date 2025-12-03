import time
import threading
import telebot
from telebot import types

# ============================================================
# إعدادات البوت
# ============================================================

BOT_TOKEN = "6819257727:AAHnRyaBSJZEMoyJcWjFHotvfuZFBbKrhYo"  # ضع التوكن هنا
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# تخزين لغة كل مستخدم في الذاكرة
user_lang = {}          # {chat_id: "ar" / "en" / "fr" / "ru"}
DEFAULT_LANG = "ar"

# ============================================================
# نصوص الواجهات لكل لغة
# ============================================================

TEXTS = {
    "start_title": {
        "ar": "افتح بشكل إلزامي",
        "en": "Read this carefully",
        "fr": "Lisez ceci attentivement",
        "ru": "Внимательно прочитайте"
    },
    "start_body": {
        "ar": (
            "عزيزي المستخدم،\n"
            "للحصول على موثوقية تصل إلى 99٪ يرجى اتباع هذه الخطوات دون استثناء:\n\n"
            "1) استخدم الرمز الترويجي: PREDBOX2ROBOT\n"
            "2) فعّل مكافأة CASINO + GAMME عند التسجيل\n"
            "3) قم بالتسجيل فقط عبر الروابط الرسمية الخاصة بنا\n\n"
            "اتباع التعليمات = أفضل توقعات ممكنة."
        ),
        "en": (
            "Dear user,\n"
            "To reach up to 99% accuracy, follow all the steps below:\n\n"
            "1) Use the promo code: PREDBOX2ROBOT\n"
            "2) Activate the CASINO + GAMME bonus during registration\n"
            "3) Register only through our official links\n\n"
            "Following the instructions = best possible predictions."
        ),
        "fr": (
            "Cher utilisateur,\n"
            "Pour atteindre jusqu'à 99 % de fiabilité, veuillez suivre toutes les étapes suivantes :\n\n"
            "1) Utilisez le code promo : PREDBOX2ROBOT\n"
            "2) Activez le bonus CASINO + GAMME lors de l'inscription\n"
            "3) Inscrivez-vous uniquement via nos liens officiels\n\n"
            "Suivre les instructions = meilleures prédictions possibles."
        ),
        "ru": (
            "Уважаемый пользователь,\n"
            "Чтобы достичь точности до 99 %, выполните все шаги ниже:\n\n"
            "1) Используйте промокод: PREDBOX2ROBOT\n"
            "2) Активируйте бонус CASINO + GAMME при регистрации\n"
            "3) Регистрируйтесь только по нашим официальным ссылкам\n\n"
            "Следуя инструкциям = максимальная точность прогнозов."
        ),
    },
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

# نص رسالة اختيار اللغة مثل الصورة
LANG_SELECT_TEXT = (
    "🇫🇷 Veuillez choisir votre langue préférée en cliquant sur le bouton...\n\n"
    "🇺🇸 Please choose your preferred language by clicking on the button...\n\n"
    "🇷🇺 Пожалуйста, выберите предпочитаемый язык, нажав на кнопку...\n\n"
    "🇸🇦 من فضلك، اختر اللغة المفضلة لديك بالضغط على الزر..."
)

# ============================================================
# دوال مساعدة
# ============================================================

def get_lang(chat_id: int) -> str:
    return user_lang.get(chat_id, DEFAULT_LANG)


def set_lang(chat_id: int, lang: str):
    user_lang[chat_id] = lang


def get_text(key: str, lang: str) -> str:
    data = TEXTS.get(key, {})
    # لو اللغة غير موجودة، نرجع الإنجليزية كافتراضي
    return data.get(lang, data.get("en", ""))


def send_start_message(chat_id: int):
    """إرسال رسالة /start مع أزرار فتح المتنبئ وتغيير اللغة (Inline)."""
    lang = get_lang(chat_id)
    title = get_text("start_title", lang)
    body = get_text("start_body", lang)

    text = f"*{title}*\n\n{body}"

    # بناء Inline Keyboard أسفل الرسالة
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
    """إرسال رسالة وهمية ثم حذفها بعد عدد ثواني."""
    text = get_text("fake_window", lang)
    msg = bot.send_message(chat_id, text)

    def auto_delete():
        time.sleep(seconds)
        try:
            bot.delete_message(chat_id, msg.message_id)
        except Exception:
            # إذا فشل الحذف (مثلا لا صلاحية)، نتجاهل الخطأ
            pass

    threading.Thread(target=auto_delete, daemon=True).start()


def send_language_menu(chat_id: int):
    """إرسال رسالة اختيار اللغة مع أزرار لكل لغة."""
    markup = types.InlineKeyboardMarkup()
    btn_fr = types.InlineKeyboardButton("🇫🇷 Français", callback_data="set_lang_fr")
    btn_en = types.InlineKeyboardButton("🇺🇸 English", callback_data="set_lang_en")
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="set_lang_ru")
    btn_ar = types.InlineKeyboardButton("🇸🇦 العربية", callback_data="set_lang_ar")

    # صفين كما في الصورة
    markup.row(btn_fr, btn_en)
    markup.row(btn_ru, btn_ar)

    bot.send_message(chat_id, LANG_SELECT_TEXT, reply_markup=markup)


# ============================================================
# Handlers
# ============================================================

@bot.message_handler(commands=['start'])
def on_start(message: telebot.types.Message):
    chat_id = message.chat.id
    # أول مرة: اللغة الافتراضية عربية
    if chat_id not in user_lang:
        set_lang(chat_id, DEFAULT_LANG)
    send_start_message(chat_id)


@bot.callback_query_handler(func=lambda call: True)
def on_callback(call: telebot.types.CallbackQuery):
    chat_id = call.message.chat.id
    lang = get_lang(chat_id)
    data = call.data

    # فتح المتنبئ (نافذة وهمية ثم تختفي)
    if data == "open_predictor":
        bot.answer_callback_query(call.id)  # لإزالة "Loading..."
        send_fake_window(chat_id, lang, seconds=5)
        return

    # فتح قائمة تغيير اللغة
    if data == "change_language":
        bot.answer_callback_query(call.id)
        send_language_menu(chat_id)
        return

    # تغيير اللغة حسب الزر
    if data.startswith("set_lang_"):
        code = data.split("_")[-1]  # fr / en / ru / ar
        if code in ["fr", "en", "ru", "ar"]:
            set_lang(chat_id, code)
        bot.answer_callback_query(call.id, get_text("lang_changed", code))

        # يمكن حذف رسالة اختيار اللغة أو تركها، هنا نتركها ونرسل ستارت جديد
        send_start_message(chat_id)
        return


@bot.message_handler(content_types=['text'])
def on_text(message: telebot.types.Message):
    # أي كتابة عشوائية: رسالة توضيح واستخدام الأزرار فقط
    chat_id = message.chat.id
    lang = get_lang(chat_id)
    bot.send_message(chat_id, get_text("unknown", lang))


# ============================================================
# تشغيل البوت
# ============================================================

if __name__ == "__main__":
    bot.infinity_polling()
