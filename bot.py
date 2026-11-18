import telebot
from telebot import types
import requests

# BotFather'dan olgan TOKENingizni shu yerga yozing
TOKEN = "9104235627:AAFQq64za98Lu3rt4NZKP4k7TlBjTR1-A9g"
bot = telebot.TeleBot(TOKEN)

# /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_uz = types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='lang_uz')
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')
    markup.add(btn_uz, btn_ru, btn_en)
    
    bot.send_message(
        message.chat.id, 
        "🤖 **TradingView Bot**ga xush kelibsiz!\n\nIltimos, o'zingizga qulay tilni tanlang:\n👇 Please select your language:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Tilni tanlash tugmalari
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'lang_uz':
        bot.answer_callback_query(call.id, "O'zbek tili tanlandi 🇺🇿")
        send_main_menu(call.message.chat.id, 'uz')
    elif call.data == 'lang_ru':
        bot.answer_callback_query(call.id, "Выбран русский язык 🇷🇺")
        send_main_menu(call.message.chat.id, 'ru')
    elif call.data == 'lang_en':
        bot.answer_callback_query(call.id, "English selected 🇬🇧")
        send_main_menu(call.message.chat.id, 'en')

# Asosiy menyu
def send_main_menu(chat_id, lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    if lang == 'uz':
        btn1 = types.KeyboardButton("📈 Real Bitcoin (BTC) Signali")
        btn2 = types.KeyboardButton("💱 Real Valyuta (USD/UZS)")
        text = "Quyidagi bo'limlardan birini tanlang:"
    elif lang == 'ru':
        btn1 = types.KeyboardButton("📈 Реальный сигнал Bitcoin (BTC)")
        btn2 = types.KeyboardButton("💱 Реальная валюта (USD/UZS)")
        text = "Выберите один из разделов ниже:"
    else:
        btn1 = types.KeyboardButton("📈 Real Bitcoin (BTC) Signal")
        btn2 = types.KeyboardButton("💱 Real Currency (USD/UZS)")
        text = "Choose one of the options below:"
        
    markup.add(btn1, btn2)
    bot.send_message(chat_id, text, reply_markup=markup)

# Tugmalar bosilganda real internet ma'lumotlarini olib tahlil qilish
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    
    if "Bitcoin" in text or "BTC" in text:
        try:
            url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
            res = requests.get(url, timeout=10).json()
            price = float(res['lastPrice'])
            price_change = float(res['priceChangePercent'])
            
            if price_change >= 0:
                signal = "🟢 BUY (Sotib olish)"
            else:
                signal = "🔴 SELL (Sotish)"
                
            reply_text = (
                f"📈 **Real Bitcoin (BTC) Tahlili:**\n\n"
                f"💵 Joriy narx: ${price:,.2f}\n"
                f"📊 24s o'zgarish: {price_change}%\n\n"
                f"🎯 **Tavsiya:** {signal}\n\n"
                f"*Eslatma: Bu avtomatik texnik tahlil!*"
            )
        except Exception as e:
            reply_text = f"Ma'lumotni olishda xatolik yuz berdi: {e}"
            
        bot.reply_to(message, reply_text, parse_mode="Markdown")
        
    elif "Valyuta" in text or "Currency" in text or "USD/UZS" in text:
        try:
            url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
            res = requests.get(url, timeout=10).json()
            usd_rate = 0
            for item in res:
                if item['Ccy'] == 'USD':
                    usd_rate = float(item['Rate'])
            
            reply_text = (
                f"💱 **Real Valyuta kursi (Markaziy bank):**\n\n"
                f"💵 1 USD = {usd_rate:,.2f} so'm\n\n"
                f"📊 **Tavsiya:** Valyuta barqaror. Xarid qilish uchun qulay vaqtni tanlang.\n\n"
                f"*Eslatma: Markaziy bank ma'lumotlari asosida.*"
            )
        except Exception as e:
            reply_text = f"Valyuta ma'lumotini olishda xatolik yuz berdi: {e}"
            
        bot.reply_to(message, reply_text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "Iltimos, menyudagi tugmalardan foydalaning.")

print("Bot ishga tushdi...")
bot.infinity_polling()
