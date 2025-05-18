import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Contact, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN as token, Admins
from button import menu, contact_button
from check import CheksupChanel

logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Narxlar uchun global o‘zgaruvchilar
uc_message = None
pr_message = None

# Start va majburiy obuna
@dp.message(CheksupChanel())
async def check_subscription(message: Message):
    kanal_link = 'https://t.me/ParsifalPubg'
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='OBUNA BOLING :)', url=kanal_link)]
        ]
    )
    await message.answer_photo(
        photo='https://codecapsules.io/wp-content/uploads/2023/08/comparing-telegram-bot-hosting-providerspng.png',
        caption='Kanalga obuna bo‘ling!',
        reply_markup=markup
    )

@dp.message(Command("start"))
async def start_handler(message: Message):
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    url = message.from_user.url

    await message.answer(f"Assalomu alaykum, <a href='{url}'>{first_name}</a>", reply_markup=menu)

    for admin_id in Admins:
        if admin_id != user_id:
            await bot.send_message(admin_id, f" 👉<a href='{url}'>{first_name}</a>👈 start bosdi")

# UC narxlari
@dp.message(F.text == "UC xarid qilish")
async def handle_uc(message: Message):
    global uc_message
    user_id = message.from_user.id

    if user_id in Admins:
        if uc_message:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("UC narxini yangilash", callback_data="update_uc")],
                [InlineKeyboardButton("UC narxini o‘chirish", callback_data="delete_uc")]
            ])
            await message.answer(f"UC narxlari:\n{uc_message}", reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("UC narxini yuklash", callback_data="upload_uc")]
            ])
            await message.answer("Hozircha UC narxi mavjud emas.", reply_markup=markup)
    else:
        await message.answer(uc_message or "Hozircha UC narxlari mavjud emas.")

# Popular narxlari
@dp.message(F.text == "🔥Popular xarid qilish")
async def handle_popular(message: Message):
    global pr_message
    user_id = message.from_user.id

    if user_id in Admins:
        if pr_message:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("Popular narxini yangilash", callback_data="update_pr")],
                [InlineKeyboardButton("Popular narxini o‘chirish", callback_data="delete_pr")]
            ])
            await message.answer(f"Popular narxlari:\n{pr_message}", reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("Popular narxini yuklash", callback_data="upload_pr")]
            ])
            await message.answer("Hozircha Popular narxlari mavjud emas.", reply_markup=markup)
    else:
        await message.answer(pr_message or "Hozircha Popular narxi mavjud emas.")

# Admin bilan bog‘lanish
@dp.message(F.text == "Admin bilan boglanish📞")
async def contact_admin(message: Message):
    await message.answer("Bog‘lanish turini tanlang:", reply_markup=contact_button)

# Qo‘ng‘iroq qilish va raqam jo‘natish
@dp.message(F.text == "📞Qong'iroq qilish📞")
async def request_phone(message: Message):
    await message.answer("Iltimos, raqamingizni ulashing:", reply_markup=contact_button)

@dp.message(F.contact)
async def handle_contact(message: Message):
    contact: Contact = message.contact
    first_name = message.from_user.first_name
    url = message.from_user.url

    for admin_id in Admins:
        if admin_id != message.from_user.id:
            await bot.send_message(
                admin_id,
                f"👉 <a href='{url}'>{first_name}</a> siz bilan bog‘lanmoqchi.\n📞 Raqami: {contact.phone_number}"
            )

    await message.answer("Raqamingiz yuborildi, tez orada siz bilan bog‘lanamiz.", reply_markup=menu)

# Xabar qoldirish logikasi
user_message_flags = {}

@dp.message(F.text == "✍️Xabar qoldirish")
async def ask_for_message(message: Message):
    user_message_flags[message.from_user.id] = True
    await message.answer("Adminga yubormoqchi bo‘lgan xabaringizni yozing.")

@dp.message(lambda msg: user_message_flags.get(msg.from_user.id))
async def forward_to_admins(message: Message):
    user_id = message.from_user.id
    user_text = message.text
    first_name = message.from_user.first_name
    url = message.from_user.url

    for admin_id in Admins:
        await bot.send_message(
            admin_id,
            f"👤 <a href='{url}'>{first_name}</a> sizga xabar yubordi:\n📩 {user_text}"
        )

    await message.answer("Xabaringiz yuborildi.", reply_markup=menu)
    user_message_flags.pop(user_id, None)

# Orqaga tugmasi
@dp.message(F.text == "Orqaga🔙")
async def go_back(message: Message):
    await message.answer("Siz asosiy menyudasiz", reply_markup=menu)

# Callback querylar — UC va Popular narxlar
@dp.callback_query(F.data == "update_uc")
async def update_uc(callback: CallbackQuery):
    global uc_message
    uc_message = None
    await callback.message.answer("Yangi UC narxini yuboring.")

@dp.callback_query(F.data == "delete_uc")
async def delete_uc(callback: CallbackQuery):
    global uc_message
    uc_message = None
    await callback.message.answer("UC narxi o‘chirildi.")

@dp.callback_query(F.data == "upload_uc")
async def upload_uc(callback: CallbackQuery):
    await callback.message.answer("Yangi UC narxini yuboring.")

@dp.callback_query(F.data == "update_pr")
async def update_pr(callback: CallbackQuery):
    global pr_message
    pr_message = None
    await callback.message.answer("Yangi Popular narxini yuboring.")

@dp.callback_query(F.data == "delete_pr")
async def delete_pr(callback: CallbackQuery):
    global pr_message
    pr_message = None
    await callback.message.answer("Popular narxi o‘chirildi.")

@dp.callback_query(F.data == "upload_pr")
async def upload_pr(callback: CallbackQuery):
    await callback.message.answer("Yangi Popular narxini yuboring.")

# Admin narx yuborganida
@dp.message()
async def handle_prices(message: Message):
    global uc_message, pr_message
    user_id = message.from_user.id

    if user_id in Admins:
        if uc_message is None:
            uc_message = message.text
            await message.answer("UC narxi yangilandi.")
        elif pr_message is None:
            pr_message = message.text
            await message.answer("Popular narxi yangilandi.")

# Main
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to‘xtatildi.")
