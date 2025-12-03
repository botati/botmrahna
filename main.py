import time
import threading
import telebot
from telebot import types

# ================= إعداد البوت =================

BOT_TOKEN = "7622372235:AAFZiFw7zMejH9NLBCFX2TD9BulvRJZiXnU"   # ضع التوكن هنا
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

user_lang = {}          # {chat_id: "ar" / "en" / "fr" / "ru"}
DEFAULT_LANG = "ar"

# ضع هنا روابط قنوات الفيديو
FRENCH_VIDEO_LINK  = "https://t.me/YourFrenchChannel"   # فيديو النسخة الفرنسية
ENGLISH_VIDEO_LINK = "https://t.me/YourEnglishChannel"  # فيديو النسخة الإنجليزية
ARABIC_VIDEO_LINK  = "https://t.me/YourArabicChannel"   # فيديو النسخة العربية

# ================= نصوص ثابتة =================

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
    if lang == "ar":
        return (
            "<b>اقرأ بشكل إلزامي 🔴</b>\n\n"
            "<blockquote>سارع بالبدء باللعب الآن مع 💸King of Betting🎰!\n"
            "🎯 الفرصة أمامك… اضغط وابدأ اللعب الآن!\n\n"
            "اتبع الخطوات لتشغيل البوت بالطريقة الصحيحة ✅</blockquote>\n\n"

            "١️⃣ تسجل بالبرومو كود:\n"
            "<code>Gooo33</code>\n\n"

            "٢️⃣ تعمل إيداع 300 ج\n\n"

            "٣️⃣ ابعت سكرين شوت من الإيداع ويكون التسجيل بنفس البروموكود 👈 <b>Gooo33</b>\n\n"

            "<b>المنصة التي ستختارها:</b> 🔽🔽\n\n"

            "<blockquote>رابط التسجيل في جوبيت ❤️\n"
            "https://promogooo.click/Gooo33</blockquote>\n"

            "<blockquote>رابط التسجيل في لاكي بيري 🟡\n"
            "https://slim.link/Gooo33_REG</blockquote>\n"

            "<blockquote>رابط التسجيل في باري بلس ⬛️\n"
            "https://pari-pulse.com/Go3</blockquote>\n"

            "<blockquote>رابط التسجيل في فاست بيري 😍\n"
            "https://fastpaff.top/L?tag=d_4498338m_105372c_&site=4498338&ad=105372</blockquote>\n\n"

            "<b>ابعت هنا ⬇️📱</b>\n"
            "@HAH33tito33\n\n"

            "<b>لينك قناة التليجرام 👇</b>\n"
            "https://t.me/+GqKpGbFjOaBjYTQ8\n"
        )

    if lang == "en":
        return (
            "<b>Read Carefully 🔴</b>\n\n"
            "<blockquote>Start playing now with 💸King of Betting🎰!\n"
            "🎯 Your chance is here… click and start playing now!\n\n"
            "Follow the steps to activate the bot correctly ✅</blockquote>\n\n"

            "1️⃣ Register using the promo code:\n"
            "<code>Gooo33</code>\n\n"

            "2️⃣ Make a deposit of 300 EGP\n\n"

            "3️⃣ Send a screenshot of your deposit using the promo code 👈 <b>Gooo33</b>\n\n"

            "<b>Choose your platform:</b> 🔽🔽\n\n"

            "<blockquote>Jupit registration link ❤️\n"
            "https://promogooo.click/Gooo33</blockquote>\n"

            "<blockquote>LuckyBerry registration 🟡\n"
            "https://slim.link/Gooo33_REG</blockquote>\n"

            "<blockquote>PariPlus registration ⬛️\n"
            "https://pari-pulse.com/Go3</blockquote>\n"

            "<blockquote>FastBerry registration 😍\n"
            "https://fastpaff.top/L?tag=d_4498338m_105372c_&site=4498338&ad=105372</blockquote>\n\n"

            "<b>Send here ⬇️📱</b>\n"
            "@HAH33tito33\n\n"

            "<b>Telegram channel link 👇</b>\n"
            "https://t.me/+GqKpGbFjOaBjYTQ8\n"
        )

    if lang == "fr":
        return (
            "<b>À lire attentivement 🔴</b>\n\n"
            "<blockquote>Commencez à jouer maintenant avec 💸King of Betting🎰 !\n"
            "🎯 Votre chance est ici… cliquez et commencez à jouer maintenant !\n\n"
            "Suivez les étapes pour activer correctement le bot ✅</blockquote>\n\n"

            "1️⃣ Inscrivez-vous avec le code promo :\n"
            "<code>Gooo33</code>\n\n"

            "2️⃣ Faites un dépôt de 300 EGP\n\n"

            "3️⃣ Envoyez une capture d’écran de votre dépôt avec le code promo 👈 <b>Gooo33</b>\n\n"

            "<b>Choisissez votre plateforme :</b> 🔽🔽\n\n"

            "<blockquote>Lien d’inscription Jupit ❤️\n"
            "https://promogooo.click/Gooo33</blockquote>\n"

            "<blockquote>Inscription LuckyBerry 🟡\n"
            "https://slim.link/Gooo33_REG</blockquote>\n"

            "<blockquote>Inscription PariPlus ⬛️\n"
            "https://pari-pulse.com/Go3</blockquote>\n"

            "<blockquote>Inscription FastBerry 😍\n"
            "https://fastpaff.top/L?tag=d_4498338m_105372c_&site=4498338&ad=105372</blockquote>\n\n"

            "<b>Envoyez ici ⬇️📱</b>\n"
            "@HAH33tito33\n\n"

            "<b>Lien du canal Telegram 👇</b>\n"
            "https://t.me/+GqKpGbFjOaBjYTQ8\n"
        )

    if lang == "ru":
        return (
            "<b>Внимательно прочитайте 🔴</b>\n\n"
            "<blockquote>Начните играть прямо сейчас с 💸King of Betting🎰!\n"
            "🎯 Ваш шанс здесь… нажмите и начните играть!\n\n"
            "Следуйте шагам, чтобы правильно активировать бота ✅</blockquote>\n\n"

            "1️⃣ Зарегистрируйтесь с промокодом:\n"
            "<code>Gooo33</code>\n\n"

            "2️⃣ Пополните депозит на 300 EGP\n\n"

            "3️⃣ Отправьте скриншот вашего депозита с промокодом 👈 <b>Gooo33</b>\n\n"

            "<b>Выберите платформу:</b> 🔽🔽\n\n"

            "<blockquote>Ссылка регистрации Jupit ❤️\n"
            "https://promogooo.click/Gooo33</blockquote>\n"

            "<blockquote>Регистрация LuckyBerry 🟡\n"
            "https://slim.link/Gooo33_REG</blockquote>\n"

            "<blockquote>Регистрация PariPlus ⬛️\n"
            "https://pari-pulse.com/Go3</blockquote>\n"

            "<blockquote>Регистрация FastBerry 😍\n"
            "https://fastpaff.top/L?tag=d_4498338m_105372c_&site=4498338&ad=105372</blockquote>\n\n"

            "<b>Отправить сюда ⬇️📱</b>\n"
            "@HAH33tito33\n\n"

            "<b>Ссылка на Telegram-канал 👇</b>\n"
            "https://t.me/+GqKpGbFjOaBjYTQ8\n"
        )


def send_start_message(chat_id: int):
    lang = get_lang(chat_id)
    text = main_message(lang)

    markup = types.InlineKeyboardMarkup()

    # ========= زر ميني-آب لفتح المتنبئ =========
    webapp = types.WebAppInfo(
        url="https://your-miniapp-url.com"  # ضع هنا رابط الميني أب الخاص بك
    )
    btn_open = types.InlineKeyboardButton(
        text=get_text("btn_open", lang),
        web_app=webapp
    )
    # ===========================================

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
        # هذا الفرع لن يُستَخدم الآن لأن زر فتح المتنبئ أصبح WebApp
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
