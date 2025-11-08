import logging
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ==================== НАСТРОЙКА ЛОГГИРОВАНИЯ ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = "8584130099:AAEIdpFVbesoqjJlF2YOsHYOsmwA5dGqJGQ"

# ==================== БАЗА ДАННЫХ ТОВАРОВ ====================
PRODUCTS_DATABASE = {
    "pattaya_amph_2": {"location_key": "pattaya", "product_type": "amph", "quantity_key": "2g", "price": "100$", "emoji": "⚡"},
    "pattaya_amph_5": {"location_key": "pattaya", "product_type": "amph", "quantity_key": "5g", "price": "240$", "emoji": "⚡"},
    "pattaya_ecstasy_1": {"location_key": "pattaya", "product_type": "ecstasy", "quantity_key": "1pc", "price": "90$", "emoji": "💊"},
    "pattaya_ecstasy_3": {"location_key": "pattaya", "product_type": "ecstasy", "quantity_key": "3pcs", "price": "240$", "emoji": "💊"},
    "pattaya_lyrica_10": {"location_key": "pattaya", "product_type": "lyrica", "quantity_key": "10pcs", "price": "250$", "emoji": "💊"},
    "pattaya_ogkush_2": {"location_key": "pattaya", "product_type": "ogkush", "quantity_key": "2g", "price": "150$", "emoji": "🌿"},
    "pattaya_ogkush_3": {"location_key": "pattaya", "product_type": "ogkush", "quantity_key": "3g", "price": "220$", "emoji": "🌿"},
    "pattaya_ogkush_5": {"location_key": "pattaya", "product_type": "ogkush", "quantity_key": "5g", "price": "350$", "emoji": "🌿"},
    
    "bangkok_amph_2": {"location_key": "bangkok", "product_type": "amph", "quantity_key": "2g", "price": "110$", "emoji": "⚡"},
    "bangkok_amph_5": {"location_key": "bangkok", "product_type": "amph", "quantity_key": "5g", "price": "260$", "emoji": "⚡"},
    "bangkok_ecstasy_1": {"location_key": "bangkok", "product_type": "ecstasy", "quantity_key": "1pc", "price": "95$", "emoji": "💊"},
    "bangkok_ecstasy_3": {"location_key": "bangkok", "product_type": "ecstasy", "quantity_key": "3pcs", "price": "260$", "emoji": "💊"},
    "bangkok_coke_1": {"location_key": "bangkok", "product_type": "coke", "quantity_key": "1g", "price": "400$", "emoji": "💎"},
    "bangkok_ogkush_2": {"location_key": "bangkok", "product_type": "ogkush", "quantity_key": "2g", "price": "160$", "emoji": "🌿"},
    "bangkok_ogkush_3": {"location_key": "bangkok", "product_type": "ogkush", "quantity_key": "3g", "price": "230$", "emoji": "🌿"},
    "bangkok_ogkush_5": {"location_key": "bangkok", "product_type": "ogkush", "quantity_key": "5g", "price": "370$", "emoji": "🌿"},
    
    "phuket_amph_2": {"location_key": "phuket", "product_type": "amph", "quantity_key": "2g", "price": "105$", "emoji": "⚡"},
    "phuket_amph_5": {"location_key": "phuket", "product_type": "amph", "quantity_key": "5g", "price": "250$", "emoji": "⚡"},
    "phuket_ecstasy_1": {"location_key": "phuket", "product_type": "ecstasy", "quantity_key": "1pc", "price": "95$", "emoji": "💊"},
    "phuket_ecstasy_3": {"location_key": "phuket", "product_type": "ecstasy", "quantity_key": "3pcs", "price": "250$", "emoji": "💊"},
    "phuket_lyrica_10": {"location_key": "phuket", "product_type": "lyrica", "quantity_key": "10pcs", "price": "260$", "emoji": "💊"},
    "phuket_coke_1": {"location_key": "phuket", "product_type": "coke", "quantity_key": "1g", "price": "420$", "emoji": "💎"},
    "phuket_ogkush_2": {"location_key": "phuket", "product_type": "ogkush", "quantity_key": "2g", "price": "155$", "emoji": "🌿"},
    "phuket_ogkush_3": {"location_key": "phuket", "product_type": "ogkush", "quantity_key": "3g", "price": "225$", "emoji": "🌿"},
    "phuket_ogkush_5": {"location_key": "phuket", "product_type": "ogkush", "quantity_key": "5g", "price": "360$", "emoji": "🌿"},
    
    "chiangmai_amph_2": {"location_key": "chiangmai", "product_type": "amph", "quantity_key": "2g", "price": "95$", "emoji": "⚡"},
    "chiangmai_amph_5": {"location_key": "chiangmai", "product_type": "amph", "quantity_key": "5g", "price": "220$", "emoji": "⚡"},
    "chiangmai_ecstasy_1": {"location_key": "chiangmai", "product_type": "ecstasy", "quantity_key": "1pc", "price": "85$", "emoji": "💊"},
    "chiangmai_ecstasy_3": {"location_key": "chiangmai", "product_type": "ecstasy", "quantity_key": "3pcs", "price": "230$", "emoji": "💊"},
    "chiangmai_ogkush_2": {"location_key": "chiangmai", "product_type": "ogkush", "quantity_key": "2g", "price": "140$", "emoji": "🌿"},
    "chiangmai_ogkush_3": {"location_key": "chiangmai", "product_type": "ogkush", "quantity_key": "3g", "price": "210$", "emoji": "🌿"},
    "chiangmai_ogkush_5": {"location_key": "chiangmai", "product_type": "ogkush", "quantity_key": "5g", "price": "330$", "emoji": "🌿"},
    
    "hatyai_amph_2": {"location_key": "hatyai", "product_type": "amph", "quantity_key": "2g", "price": "90$", "emoji": "⚡"},
    "hatyai_amph_5": {"location_key": "hatyai", "product_type": "amph", "quantity_key": "5g", "price": "200$", "emoji": "⚡"},
    "hatyai_ecstasy_1": {"location_key": "hatyai", "product_type": "ecstasy", "quantity_key": "1pc", "price": "80$", "emoji": "💊"},
    "hatyai_ogkush_2": {"location_key": "hatyai", "product_type": "ogkush", "quantity_key": "2g", "price": "130$", "emoji": "🌿"},
    "hatyai_ogkush_3": {"location_key": "hatyai", "product_type": "ogkush", "quantity_key": "3g", "price": "190$", "emoji": "🌿"},
    "hatyai_ogkush_5": {"location_key": "hatyai", "product_type": "ogkush", "quantity_key": "5g", "price": "300$", "emoji": "🌿"},
    
    "seminyak_amph_2": {"location_key": "seminyak", "product_type": "amph", "quantity_key": "2g", "price": "120$", "emoji": "⚡"},
    "seminyak_amph_5": {"location_key": "seminyak", "product_type": "amph", "quantity_key": "5g", "price": "280$", "emoji": "⚡"},
    "seminyak_ecstasy_1": {"location_key": "seminyak", "product_type": "ecstasy", "quantity_key": "1pc", "price": "100$", "emoji": "💊"},
    "seminyak_lyrica_10": {"location_key": "seminyak", "product_type": "lyrica", "quantity_key": "10pcs", "price": "280$", "emoji": "💊"},
    "seminyak_coke_1": {"location_key": "seminyak", "product_type": "coke", "quantity_key": "1g", "price": "450$", "emoji": "💎"},
    "seminyak_ogkush_2": {"location_key": "seminyak", "product_type": "ogkush", "quantity_key": "2g", "price": "170$", "emoji": "🌿"},
    "seminyak_ogkush_3": {"location_key": "seminyak", "product_type": "ogkush", "quantity_key": "3g", "price": "250$", "emoji": "🌿"},
    "seminyak_ogkush_5": {"location_key": "seminyak", "product_type": "ogkush", "quantity_key": "5g", "price": "400$", "emoji": "🌿"},
    
    "ubud_amph_2": {"location_key": "ubud", "product_type": "amph", "quantity_key": "2g", "price": "110$", "emoji": "⚡"},
    "ubud_amph_5": {"location_key": "ubud", "product_type": "amph", "quantity_key": "5g", "price": "250$", "emoji": "⚡"},
    "ubud_ecstasy_1": {"location_key": "ubud", "product_type": "ecstasy", "quantity_key": "1pc", "price": "95$", "emoji": "💊"},
    "ubud_lyrica_10": {"location_key": "ubud", "product_type": "lyrica", "quantity_key": "10pcs", "price": "260$", "emoji": "💊"},
    "ubud_ogkush_2": {"location_key": "ubud", "product_type": "ogkush", "quantity_key": "2g", "price": "160$", "emoji": "🌿"},
    "ubud_ogkush_3": {"location_key": "ubud", "product_type": "ogkush", "quantity_key": "3g", "price": "230$", "emoji": "🌿"},
    "ubud_ogkush_5": {"location_key": "ubud", "product_type": "ogkush", "quantity_key": "5g", "price": "370$", "emoji": "🌿"},
    
    "bukit_amph_2": {"location_key": "bukit", "product_type": "amph", "quantity_key": "2g", "price": "130$", "emoji": "⚡"},
    "bukit_ecstasy_1": {"location_key": "bukit", "product_type": "ecstasy", "quantity_key": "1pc", "price": "105$", "emoji": "💊"},
    "bukit_lyrica_10": {"location_key": "bukit", "product_type": "lyrica", "quantity_key": "10pcs", "price": "290$", "emoji": "💊"},
    "bukit_coke_1": {"location_key": "bukit", "product_type": "coke", "quantity_key": "1g", "price": "470$", "emoji": "💎"},
    "bukit_ogkush_2": {"location_key": "bukit", "product_type": "ogkush", "quantity_key": "2g", "price": "180$", "emoji": "🌿"},
    "bukit_ogkush_3": {"location_key": "bukit", "product_type": "ogkush", "quantity_key": "3g", "price": "260$", "emoji": "🌿"},
    "bukit_ogkush_5": {"location_key": "bukit", "product_type": "ogkush", "quantity_key": "5g", "price": "420$", "emoji": "🌿"},
    
    "canggu_amph_2": {"location_key": "canggu", "product_type": "amph", "quantity_key": "2g", "price": "115$", "emoji": "⚡"},
    "canggu_amph_5": {"location_key": "canggu", "product_type": "amph", "quantity_key": "5g", "price": "270$", "emoji": "⚡"},
    "canggu_ecstasy_1": {"location_key": "canggu", "product_type": "ecstasy", "quantity_key": "1pc", "price": "98$", "emoji": "💊"},
    "canggu_lyrica_10": {"location_key": "canggu", "product_type": "lyrica", "quantity_key": "10pcs", "price": "270$", "emoji": "💊"},
    "canggu_ogkush_2": {"location_key": "canggu", "product_type": "ogkush", "quantity_key": "2g", "price": "165$", "emoji": "🌿"},
    "canggu_ogkush_3": {"location_key": "canggu", "product_type": "ogkush", "quantity_key": "3g", "price": "240$", "emoji": "🌿"},
    "canggu_ogkush_5": {"location_key": "canggu", "product_type": "ogkush", "quantity_key": "5g", "price": "380$", "emoji": "🌿"},
    
    "marina_amph_2": {"location_key": "marina", "product_type": "amph", "quantity_key": "2g", "price": "150$", "emoji": "⚡"},
    "marina_amph_5": {"location_key": "marina", "product_type": "amph", "quantity_key": "5g", "price": "350$", "emoji": "⚡"},
    "marina_ecstasy_1": {"location_key": "marina", "product_type": "ecstasy", "quantity_key": "1pc", "price": "120$", "emoji": "💊"},
    "marina_coke_1": {"location_key": "marina", "product_type": "coke", "quantity_key": "1g", "price": "500$", "emoji": "💎"},
    "marina_ogkush_2": {"location_key": "marina", "product_type": "ogkush", "quantity_key": "2g", "price": "200$", "emoji": "🌿"},
    "marina_ogkush_3": {"location_key": "marina", "product_type": "ogkush", "quantity_key": "3g", "price": "290$", "emoji": "🌿"},
    "marina_ogkush_5": {"location_key": "marina", "product_type": "ogkush", "quantity_key": "5g", "price": "470$", "emoji": "🌿"},
    
    "deira_amph_2": {"location_key": "deira", "product_type": "amph", "quantity_key": "2g", "price": "140$", "emoji": "⚡"},
    "deira_amph_5": {"location_key": "deira", "product_type": "amph", "quantity_key": "5g", "price": "320$", "emoji": "⚡"},
    "deira_ecstasy_1": {"location_key": "deira", "product_type": "ecstasy", "quantity_key": "1pc", "price": "110$", "emoji": "💊"},
    "deira_lyrica_10": {"location_key": "deira", "product_type": "lyrica", "quantity_key": "10pcs", "price": "300$", "emoji": "💊"},
    "deira_ogkush_2": {"location_key": "deira", "product_type": "ogkush", "quantity_key": "2g", "price": "190$", "emoji": "🌿"},
    "deira_ogkush_3": {"location_key": "deira", "product_type": "ogkush", "quantity_key": "3g", "price": "270$", "emoji": "🌿"},
    "deira_ogkush_5": {"location_key": "deira", "product_type": "ogkush", "quantity_key": "5g", "price": "430$", "emoji": "🌿"},
    
    "jumeirah_amph_2": {"location_key": "jumeirah", "product_type": "amph", "quantity_key": "2g", "price": "160$", "emoji": "⚡"},
    "jumeirah_amph_5": {"location_key": "jumeirah", "product_type": "amph", "quantity_key": "5g", "price": "370$", "emoji": "⚡"},
    "jumeirah_coke_1": {"location_key": "jumeirah", "product_type": "coke", "quantity_key": "1g", "price": "550$", "emoji": "💎"},
    "jumeirah_ogkush_2": {"location_key": "jumeirah", "product_type": "ogkush", "quantity_key": "2g", "price": "210$", "emoji": "🌿"},
    "jumeirah_ogkush_3": {"location_key": "jumeirah", "product_type": "ogkush", "quantity_key": "3g", "price": "310$", "emoji": "🌿"},
    "jumeirah_ogkush_5": {"location_key": "jumeirah", "product_type": "ogkush", "quantity_key": "5g", "price": "490$", "emoji": "🌿"}
}

# Добавляем callback_data в базу данных
for product_id, product_data in PRODUCTS_DATABASE.items():
    product_data['callback_data'] = product_id

# ==================== ТЕКСТЫ И ПЕРЕВОДЫ ====================
TEXTS = {
    'ru': {
        'start': """Привет, ты попал в Mendeleev Shop
Если хочешь расслабиться/отдохнуть после насыщенного дня то ты по адресу!

узнать список товаров - /price
нужного товара нет в списке - /custom

Дабы обеспечить полную анонимность и безопасность пользователей оплата доступна только через @CryptoBot

Наши отзывы @mendeotz_ru
Вечное зеркало бота t.me/mirror_mende""",
        'choose_region': "Выберите регион:",
        'choose_city_thailand': "Выберите город в Тайланде:",
        'choose_area_bali': "Выберите район на Бали:",
        'choose_area_dubai': "Выберите район в Дубае:",
        'custom_order': "Если нужного вам товара нет в списке, обратитесь к @supp_mende чтобы сделать кастомный заказ",
        'go_to_payment': "💬 Обратитесь к @supp_mende для оформления заказа",
        'products_in': "Доступные товары в {}:",
        'custom_button': "Кастомный заказ",
        'thailand': "Тайланд", 'bali': "Бали", 'dubai': "Дубай",
        'pattaya': "Паттайя", 'bangkok': "Бангкок", 'phuket': "Пхукет", 'chiangmai': "Чиангмай", 'hatyai': "Хатъяй",
        'seminyak': "Семиньяк", 'ubud': "Убуд", 'bukit': "Букит", 'canggu': "Чангу",
        'marina': "Дубай Марина", 'deira': "Дейра", 'jumeirah': "Джумейра",
        'amph': "Амфетамин", 'ecstasy': "Экстази Tesla", 'lyrica': "Lyrica Pfizer",
        'coke': "Кокс VHQ+ Colombia 97%", 'ogkush': "Шишки OG KUSH",
        'desc_amph': "Резко повышает энергию и концентрацию. Появляется бодрость, уверенность и желание что-то делать.",
        'desc_ecstasy': "Вызывает мощную эйфорию, чувство любви и доверия, прилив энергии, усиливает музыку и тактильные ощущения.",
        'desc_lyrica': "Рецептурный препарат, вызывает расслабление, эйфорию и сонливость. Усиливает эффекты других веществ.",
        'desc_coke': "Быстро вызывает прилив энергии и уверенности. Человек становится разговорчивым, активным и чувствует себя на подъёме.",
        'desc_ogkush': "Мощный индика-доминантный гибрид. Вызывает глубокое расслабление, эйфорию и повышает аппетит. Идеально для вечера.",
        '2g': "2 г", '5g': "5 г", '1g': "1 г", '3g': "3 г", '1pc': "1 шт", '3pcs': "3 шт", '10pcs': "10 шт"
    },
    'en': {
        'start': """Hello, you've reached Mendeleev Shop
If you want to relax/unwind after a busy day, you're in the right place!

view product list - /price
item you need is not in the list - /custom

To ensure complete anonymity and security for users, payment is only available via @CryptoBot

Our reviews @mendeotz_en
Eternal mirror bot t.me/mirror_mende""",
        'choose_region': "Choose region:",
        'choose_city_thailand': "Choose city in Thailand:",
        'choose_area_bali': "Choose area in Bali:",
        'choose_area_dubai': "Choose area in Dubai:",
        'custom_order': "If the product you need is not in the list, contact @supp_mende to make a custom order",
        'go_to_payment': "💬 Contact @supp_mende to place an order",
        'products_in': "Available products in {}:",
        'custom_button': "Custom Order",
        'thailand': "Thailand", 'bali': "Bali", 'dubai': "Dubai",
        'pattaya': "Pattaya", 'bangkok': "Bangkok", 'phuket': "Phuket", 'chiangmai': "Chiang Mai", 'hatyai': "Hat Yai",
        'seminyak': "Seminyak", 'ubud': "Ubud", 'bukit': "Bukit", 'canggu': "Canggu",
        'marina': "Dubai Marina", 'deira': "Deira", 'jumeirah': "Jumeirah",
        'amph': "Amphetamine", 'ecstasy': "Ecstasy Tesla", 'lyrica': "Lyrica Pfizer",
        'coke': "Coke VHQ+ Colombia 97%", 'ogkush': "OG KUSH Buds",
        'desc_amph': "Sharply increases energy and concentration. There is vigor, confidence and a desire to do something.",
        'desc_ecstasy': "Causes powerful euphoria, feelings of love and trust, energy boost, enhances music and tactile sensations.",
        'desc_lyrica': "Prescription drug, causes relaxation, euphoria and drowsiness. Enhances the effects of other substances.",
        'desc_coke': "Quickly causes a surge of energy and confidence. The person becomes talkative, active and feels uplifted.",
        'desc_ogkush': "Powerful indica-dominant hybrid. Causes deep relaxation, euphoria and increases appetite. Perfect for evening.",
        '2g': "2g", '5g': "5g", '1g': "1g", '3g': "3g", '1pc': "1 pc", '3pcs': "3 pcs", '10pcs': "10 pcs"
    }
}

# ==================== СТАТИСТИКА ====================
class Statistics:
    def __init__(self):
        self.stats_file = 'statistics.json'
        self.stats = self.load_stats()
    
    def load_stats(self):
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'total_users': 0, 'active_today': 0,
                'commands': {'start': 0, 'price': 0, 'custom': 0},
                'regions': {'thailand': 0, 'bali': 0, 'dubai': 0},
                'products': {}
            }
    
    def save_stats(self):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")
    
    def track_command(self, command):
        if command in self.stats['commands']:
            self.stats['commands'][command] += 1
        self.save_stats()
    
    def track_region(self, region):
        if region in self.stats['regions']:
            self.stats['regions'][region] += 1
        self.save_stats()
    
    def track_product_view(self, product_id):
        if product_id not in self.stats['products']:
            self.stats['products'][product_id] = 0
        self.stats['products'][product_id] += 1
        self.save_stats()

stats = Statistics()

# ==================== ОСНОВНЫЕ ФУНКЦИИ ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats.track_command('start')
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose your language / Пожалуйста, выберите язык:", reply_markup=reply_markup)

async def send_welcome_message(chat_id, context, language):
    text = TEXTS[language]['start']
    keyboard = [[InlineKeyboardButton(TEXTS[language]['custom_button'], callback_data="custom_order")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        await context.bot.send_photo(chat_id=chat_id, photo=open(r'C:\Users\proki\Desktop\бот\photo.jpg', 'rb'), caption=text, reply_markup=reply_markup)
    except FileNotFoundError:
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats.track_command('custom')
    lang = context.user_data.get('language', 'ru')
    await update.message.reply_text(TEXTS[lang]['custom_order'])

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats.track_command('price')
    lang = context.user_data.get('language', 'ru')
    keyboard = [
        [InlineKeyboardButton(TEXTS[lang]['thailand'], callback_data="region_thailand")],
        [InlineKeyboardButton(TEXTS[lang]['bali'], callback_data="region_bali")],
        [InlineKeyboardButton(TEXTS[lang]['dubai'], callback_data="region_dubai")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(TEXTS[lang]['choose_region'], reply_markup=reply_markup)

async def send_product_info(query, product_data, language):
    location_name = TEXTS[language][product_data['location_key']]
    product_name = TEXTS[language][product_data['product_type']]
    quantity = TEXTS[language][product_data['quantity_key']]
    description = TEXTS[language][f"desc_{product_data['product_type']}"]
    
    if language == 'ru':
        caption = f"""🏙️ Город: {location_name}
🎯 Товар: {product_name}
📦 Количество: {quantity}
💵 Цена: {product_data['price']}

📝 Описание:
{description}"""
    else:
        caption = f"""🏙️ City: {location_name}
🎯 Product: {product_name}
📦 Quantity: {quantity}
💵 Price: {product_data['price']}

📝 Description:
{description}"""

    keyboard = [[InlineKeyboardButton("💳 Перейти к оплате" if language == 'ru' else "💳 Go to payment", callback_data="go_to_payment")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(caption, reply_markup=reply_markup)

# ==================== КЛАВИАТУРЫ ДЛЯ РЕГИОНОВ ====================
def get_thailand_cities_keyboard(language):
    return [
        [InlineKeyboardButton(TEXTS[language]['pattaya'], callback_data="city_pattaya")],
        [InlineKeyboardButton(TEXTS[language]['bangkok'], callback_data="city_bangkok")],
        [InlineKeyboardButton(TEXTS[language]['phuket'], callback_data="city_phuket")],
        [InlineKeyboardButton(TEXTS[language]['chiangmai'], callback_data="city_chiangmai")],
        [InlineKeyboardButton(TEXTS[language]['hatyai'], callback_data="city_hatyai")],
    ]

def get_bali_areas_keyboard(language):
    return [
        [InlineKeyboardButton(TEXTS[language]['seminyak'], callback_data="area_seminyak")],
        [InlineKeyboardButton(TEXTS[language]['ubud'], callback_data="area_ubud")],
        [InlineKeyboardButton(TEXTS[language]['bukit'], callback_data="area_bukit")],
        [InlineKeyboardButton(TEXTS[language]['canggu'], callback_data="area_canggu")],
    ]

def get_dubai_areas_keyboard(language):
    return [
        [InlineKeyboardButton(TEXTS[language]['marina'], callback_data="dubai_marina")],
        [InlineKeyboardButton(TEXTS[language]['deira'], callback_data="dubai_deira")],
        [InlineKeyboardButton(TEXTS[language]['jumeirah'], callback_data="dubai_jumeirah")],
    ]

# ==================== УМНЫЕ ФУНКЦИИ СОЗДАНИЯ КНОПОК ====================
def create_product_button(product_data, language):
    emoji = product_data['emoji']
    product_name = TEXTS[language][product_data['product_type']]
    quantity = TEXTS[language][product_data['quantity_key']]
    price = product_data['price']
    
    if language == 'ru':
        button_text = f"{emoji} {product_name} ({quantity}) - {price}"
    else:
        button_text = f"{emoji} {product_name} ({quantity}) - {price}"
    
    return InlineKeyboardButton(button_text, callback_data=product_data['callback_data'])

def get_products_keyboard_by_city(city_key, language):
    city_products = []
    for product_id, product_data in PRODUCTS_DATABASE.items():
        if product_data['location_key'] == city_key:
            city_products.append(product_data)
    
    city_products.sort(key=lambda x: (x['product_type'], x['quantity_key']))
    
    keyboard = []
    for product_data in city_products:
        button = create_product_button(product_data, language)
        keyboard.append([button])
    
    return keyboard

# ==================== ОБРАБОТЧИКИ МЕНЮ ГОРОДОВ ====================
async def send_city_products_menu(query, city_key, language):
    city_name = TEXTS[language][city_key]
    keyboard = get_products_keyboard_by_city(city_key, language)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(TEXTS[language]['products_in'].format(city_name), reply_markup=reply_markup)

# ==================== ГЛАВНЫЙ ОБРАБОТЧИК КНОПОК ====================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_data = context.user_data
    lang = user_data.get('language', 'ru')

    if data == "lang_ru":
        user_data['language'] = 'ru'
        await send_welcome_message(query.message.chat_id, context, 'ru')
        await query.message.delete()
        return
    elif data == "lang_en":
        user_data['language'] = 'en'
        await send_welcome_message(query.message.chat_id, context, 'en')
        await query.message.delete()
        return
    elif data == "custom_order":
        await query.message.reply_text(TEXTS[lang]['custom_order'])
        return
    elif data == "go_to_payment":
        await query.message.reply_text(TEXTS[lang]['go_to_payment'])
        return
    elif data in PRODUCTS_DATABASE:
        stats.track_product_view(data)
        product_data = PRODUCTS_DATABASE[data]
        await send_product_info(query, product_data, lang)
        return
    elif data == "region_thailand":
        stats.track_region('thailand')
        keyboard = get_thailand_cities_keyboard(lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(TEXTS[lang]['choose_city_thailand'], reply_markup=reply_markup)
        return
    elif data == "region_bali":
        stats.track_region('bali')
        keyboard = get_bali_areas_keyboard(lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(TEXTS[lang]['choose_area_bali'], reply_markup=reply_markup)
        return
    elif data == "region_dubai":
        stats.track_region('dubai')
        keyboard = get_dubai_areas_keyboard(lang)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(TEXTS[lang]['choose_area_dubai'], reply_markup=reply_markup)
        return
    elif data == "city_pattaya":
        await send_city_products_menu(query, 'pattaya', lang)
        return
    elif data == "city_bangkok":
        await send_city_products_menu(query, 'bangkok', lang)
        return
    elif data == "city_phuket":
        await send_city_products_menu(query, 'phuket', lang)
        return
    elif data == "city_chiangmai":
        await send_city_products_menu(query, 'chiangmai', lang)
        return
    elif data == "city_hatyai":
        await send_city_products_menu(query, 'hatyai', lang)
        return
        
    # ==================== ОБРАБОТЧИКИ ДЛЯ БАЛИ ====================
    elif data == "area_seminyak":
        await send_city_products_menu(query, 'seminyak', lang)
        return
        
    elif data == "area_ubud":
        await send_city_products_menu(query, 'ubud', lang)
        return
        
    elif data == "area_bukit":
        await send_city_products_menu(query, 'bukit', lang)
        return
        
    elif data == "area_canggu":
        await send_city_products_menu(query, 'canggu', lang)
        return

    # ==================== ОБРАБОТЧИКИ ДЛЯ ДУБАЯ ====================
    elif data == "dubai_marina":
        await send_city_products_menu(query, 'marina', lang)
        return
        
    elif data == "dubai_deira":
        await send_city_products_menu(query, 'deira', lang)
        return
        
    elif data == "dubai_jumeirah":
        await send_city_products_menu(query, 'jumeirah', lang)
        return

# ==================== ЗАПУСК БОТА ====================
def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("custom", custom))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("🤖 Бот запускается...")
    application.run_polling()

if __name__ == '__main__':
    main()