from config import *

inline_keyboard = InlineKeyboardMarkup(row_width=1)
inline_keyboard.add(
    InlineKeyboardButton(text="Product1", callback_data='product_buying'),
    InlineKeyboardButton(text="Product2", callback_data='product_buying'),
    InlineKeyboardButton(text="Product3", callback_data='product_buying'),
    InlineKeyboardButton(text="Product4", callback_data='product_buying')
)

