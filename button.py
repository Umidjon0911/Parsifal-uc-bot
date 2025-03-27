from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="UC xarid qilish"), KeyboardButton(text="🔥Popular xarid qilish")],
        [KeyboardButton(text="Admin bilan boglanish📞")]
    ],
    resize_keyboard=True
)

contact_button=ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✍️Xabar qoldirish"), KeyboardButton(text="📞Qong'iroq qilish📞", request_contact=True)],
        [KeyboardButton(text="Orqaga🔙")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

from config import Admins
def get_menu(user_id):
    """ Foydalanuvchi admin yoki yo‘qligiga qarab menyu yaratish """
    buttons = [
        [KeyboardButton(text="UC sotib olish")],
        [KeyboardButton(text="Admin bilan boglanish📞")]
    ]

    if user_id in Admins:
        buttons.append([KeyboardButton(text="UC Narxlarini yangilash")])  # Admin tugmasi

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
