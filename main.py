import telebot
from telebot import types

# ضع التوكن الخاص بك هنا
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# تخزين لغة كل مستخدم في الذاكرة {chat_id: "ar" or "en"}
user_lang = {}

DEFAULT_LANG = "ar"


def get_lang(chat_id: int) -> str:
    """إرجاع لغة المستخدم (افتراضي عربي)"""
    return user_lang.get(chat_id, DEFAULT_LANG)


def set_lang(chat_id: int, lang: str):
    """تعديل لغة المستخدم"""
    user_lang[chat_id] = lang


# ===================== النصوص باللغتين =====================

def main_message(lang: str) -> str:
    """النص الرئيسي الذي يشبه الرسالة في الصورة"""
    if lang == "ar":
        return (
            "*افتح بشكل إلزامي 🔴*\n"
            "عزيزي المستخدم،\n"
            "للحصول على موثوقية تصل إلى 99٪ يرجى اتباع هذه الخطوات دون استثناء:\n\n"
            "1️⃣ *استخدم الرمز الترويجي*: `PREDBOX2ROBOT`\n"
            "2️⃣ *فعّل مكافأة CASINO + GAMME عند التسجيل*\n"
            "3️⃣ *سجّل فقط عبر هذا الرابط (مثال)*:\n"
            "🔗 https://example.com/melbet  \n"
            "`/PREDBOX2ROBOT (MELBET)`\n\n"
            "🎥 *فيديو النسخة الفرنسية*\n"
            "🎥 *فيديو النسخة الإنجليزية*\n\n"
            "4️⃣ *سجّل فقط عبر هذا الرابط (مثال)*:\n"
            "🔗 https://example.com/1xcasino  \n"
            "`(1XCASINO)`\n\n"
            "🎥 *فيديو النسخة الفرنسية*\n"
            "🎥 *فيديو النسخة العربية*\n\n"
            "ℹ️ هذه الإجراءات تسمح بالمزامنة الصحيحة مع الخوارزميات، بدون ذلك ستكون النتائج جزئية ولا يمكن ضمان الدقة.\n\n"
            "▶️ *اتّبع التعليمات = تحصل على أفضل التوقعات.*"
        )
    else:
        return (
            "*Read this carefully 🔴*\n"
            "Dear user,\n"
            "To reach up to 99% accuracy, please follow *all* steps below:\n\n"
            "1️⃣ *Use the promo code*: `PREDBOX2ROBOT`\n"
            "2️⃣ *Activate CASINO + GAMME bonus during registration*\n"
            "3️⃣ *Register only through this link (example)*:\n"
            "🔗 https://example.com/melbet  \n"
            "`/PREDBOX2ROBOT (MELBET)`\n\n"
            "🎥 *French version video*\n"
            "🎥 *English version video*\n\n"
            "4️⃣ *Register only through this link (example)*:\n"
            "🔗 https://example.com/1xcasino  \n"
            "`(1XCASINO)`\n\n"
            "🎥 *French version video*\n"
            "🎥 *Arabic version video*\n\n"
            "ℹ️ These steps allow correct synchronization with the algorithms. "
            "Without them, the results may be partial and accuracy cannot be guaranteed.\n\n"
            "▶️ *Follow the instructions = get the best predictions.*"
        )


def predictor_extra(lang: str) -> str:
    """رسالة إضافية عند الضغط على فتح المتنبئ / Open predictor"""
    if lang == "ar":
        return (
            "📊 *لوحة المتنبئ*\n"
            "هنا يمكنك إضافة شرح مفصل عن البوت:\n"
            "• كيف تعمل الإشارات\n"
            "• أوقات التحديث\n"
            "• أي تحذيرات أو ملاحظات\n\n"
            "يمكنك تعديل هذا النص كما تريد ليتوافق مع نظامك."
        )
    else:
        return (
            "📊 *Predictor panel*\n"
            "Here you can add detailed information about your bot:\n"
            "• How the signals work\n"
            "• Update times\n"
            "• Any warnings or notes\n\n"
            "You can edit this text to match your system."
        )


def unknown_text(lang: str) -> str:
    if lang == "ar":
        return "❓ لم أفهم رسالتك، من فضلك استخدم الأزرار بالأسفل."
    else:
        return "❓ I didn't understand that, please use the buttons below."


def lang_changed_to(lang: str) -> str:
    if lang == "ar":
        return "✅ تم تغيير اللغة إلى *العربية*."
    else:
        return "✅ Language changed to *English*."


# ===================== الكيبورد =====================

def build_main_keyboard(lang: str) -> types.ReplyKeyboardMarkup:
    """يبني الكيبورد السفلي حسب اللغة"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if lang == "ar":
        btn_predictor = types.KeyboardButton("فتح المتنبئ")
        btn_lang = types.KeyboardButton("تغيير اللغة 🇬🇧")
    else:
        btn_predictor = types.KeyboardButton("Open predictor")
        btn_lang = types.KeyboardButton("Change language 🇸🇦")

    markup.row(btn_predictor)
    markup.row(btn_lang)
    return markup


# ===================== الهاندلرز =====================

@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    chat_id = message.chat.id

    # لو أول مرة، نخليه عربي افتراضي
    if chat_id not in user_lang:
        set_lang(chat_id, DEFAULT_LANG)

    lang = get_lang(chat_id)
    text = main_message(lang)
    keyboard = build_main_keyboard(lang)

    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_text(message: telebot.types.Message):
    chat_id = message.chat.id
    text = (message.text or "").strip()
    lang = get_lang(chat_id)

    # ----- تغيير اللغة -----
    if text in ["تغيير اللغة", "تغيير اللغة 🇬🇧", "Change language", "Change language 🇸🇦"]:
        new_lang = "en" if lang == "ar" else "ar"
        set_lang(chat_id, new_lang)

        bot.send_message(chat_id, lang_changed_to(new_lang),
                         reply_markup=build_main_keyboard(new_lang))
        # نعيد إرسال الرسالة الرئيسية بالشكل الجديد
        bot.send_message(chat_id, main_message(new_lang),
                         reply_markup=build_main_keyboard(new_lang))
        return

    # ----- فتح المتنبئ / Open predictor -----
    if text in ["فتح المتنبئ", "Open predictor"]:
        bot.send_message(chat_id, predictor_extra(lang),
                         reply_markup=build_main_keyboard(lang))
        return

    # ----- أي نص آخر -----
    bot.send_message(chat_id, unknown_text(lang),
                     reply_markup=build_main_keyboard(lang))


# ===================== تشغيل البوت =====================

if __name__ == "__main__":
    # يشغّل البوت باستمرار
    bot.infinity_polling()
