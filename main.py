import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, Contact, CallbackQuery
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN as token, Admins
from button import menu, contact_button
from check import CheksupChanel

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

uc_message = None
pr_message = None




#Start va majburiy obuna

@dp.message(CheksupChanel())
async def obuna(message: Message):
    Kanal_link = 't.me/ParsifalPubg'
    kanallar = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='OBUNA BOLING :)', url=Kanal_link)]
        ]
    )
    await message.answer_photo(
        photo='https://codecapsules.io/wp-content/uploads/2023/08/comparing-telegram-bot-hosting-providerspng.png',
        caption='Kanalga obuna boling',
        reply_markup=kanallar
    )
@dp.message(Command('start'))
async def CommandStart(message: types.Message):
    first_name = message.from_user.first_name
    url = message.from_user.url
    user_id = message.from_user.id
    await message.reply(f"Assalom alaykum \n<a href='{url}'>{first_name}</a>", reply_markup=menu)
    for admin_id in Admins:
        if admin_id != user_id:
            await bot.send_message(chat_id=admin_id, text=f" 👉<a href='{url}'>{first_name}</a>👈 Start bosdi")




@dp.message(F.text == "UC xarid qilish")
async def uc_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in Admins:
        if uc_message:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="UC narxini yangilash", callback_data="update_uc")],
                    [InlineKeyboardButton(text="UC narxini o'chirish", callback_data="delete_uc")]
                ]
            )
            await message.answer(f"UC narxlari:\n{uc_message}", reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="UC narxini yuklash", callback_data="upload_uc")]
                ]
            )
            await message.answer("Hozircha UC narxi mavjud emas. UC narxini yuklash uchun tugmani bosing.", reply_markup=keyboard)
    else:
        if uc_message:
            await message.answer(f"UC narxlari:\n{uc_message}")
        else:
            await message.answer("Kechirasiz, bizda hozircha UC narxlari yuklanmagan iltimos keyinroq tekshirib koring.")




@dp.message(F.text == "Admin bilan boglanish📞")
async def admin_bilan_boglanish(message: types.Message):
    await message.answer("Bog'lanish turini tanlang", reply_markup=contact_button)


@dp.message(F.text == "📞Qong'iroq qilish📞")
async def raqam_sorash(message: types.Message):
    await message.answer(
        "Iltimos, raqamingizni ulashing, tez orada siz bilan bog'lanamiz.",
        reply_markup=contact_button
    )


@dp.message(F.contact)
async def kontakt_qabul_qilish(message: types.Message):
    contact: Contact = message.contact
    first_name = message.from_user.first_name
    url = message.from_user.url

    for admin_id in Admins:
        if admin_id != message.from_user.id:
            await bot.send_message(
                admin_id,
                f"👉 <a href='{url}'>{first_name}</a> 👈 Siz bilan bog'lanmoqchi.\n"
                f"📞 Telefon raqami: {contact.phone_number}",
                parse_mode=ParseMode.HTML
            )
    await message.answer("Raqamingiz adminga yuborildi, tez orada bog'lanamiz.", reply_markup=menu)
user_message_flags = {}

@dp.message(F.text == "✍️Xabar qoldirish")
async def start_message_writing(message: types.Message):
    user_id = message.from_user.id
    # Foydalanuvchi yozayotganini belgilang
    user_message_flags[user_id] = True
    await message.answer("Iltimos, adminga yubormoqchi bo'lgan xabaringizni yozib qoldiring. Iltimos barcha xabaringizni bittada jonating.")


@dp.message(lambda msg: msg.from_user.id in user_message_flags and user_message_flags[msg.from_user.id])
async def handle_user_message(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text
    first_name = message.from_user.first_name
    url = message.from_user.url

    # Xabarni barcha adminlarga yuborish
    for admin_id in Admins:
        await bot.send_message(
            chat_id=admin_id,
            text=f"👤 <a href='{url}'>{first_name}</a> sizga xabar qoldirdi:\n\n📩 {user_text}",
            parse_mode=ParseMode.HTML
        )
    # Javob beriladi va yozish belgisi o'chiriladi
    await message.answer("Xabaringiz adminga yetkazildi. Tez orada siz bilan bog'lanishadi. Agar yana xabar yozmoqchi bolsangiz ✍️Xabar qoldirish tugmasini qayta ishga tushiring", reply_markup=menu)
    user_message_flags.pop(user_id, None)

@dp.message(F.text == "Orqaga🔙")
async def orqaga(message: types.Message):
    await message.answer(f"Siz asosiy menudasiz", reply_markup=menu)






@dp.message(F.text == "🔥Popular xarid qilish")
async def pr_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id in Admins:
        if pr_message:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Popular narxini yangilash", callback_data="update_pr")],
                    [InlineKeyboardButton(text="Popular narxini o'chirish", callback_data="delete_pr")]
                ]
            )
            await message.answer(f"Popular narxlari:\n{pr_message}", reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Popular narxini yuklash", callback_data="upload_pr")]
                ]
            )
            await message.answer("Hozircha Popular narxlari mavjud emas. Popular narxini yuklash uchun tugmani bosing.", reply_markup=keyboard)
    else:
        if pr_message:
            await message.answer(f"Popular narxlari:\n{pr_message}")
        else:
            await message.answer("Kechirasiz, bizda hozircha Popular narxi yuklanmagan iltimos keyinroq urinib koring.")

@dp.callback_query(F.data == "update_uc")
async def update_uc(callback: CallbackQuery):
    await callback.message.answer("Yangi UC narxini yuboring.")
    global uc_message
    uc_message = None

@dp.callback_query(F.data == "delete_uc")
async def delete_uc(callback: CallbackQuery):
    global uc_message
    uc_message = None
    await callback.message.answer("UC yangiliklari o‘chirildi.")

@dp.callback_query(F.data == "upload_uc")
async def upload_uc(callback: CallbackQuery):
    await callback.message.answer("Yangi narxini yuboring.")

@dp.callback_query(F.data == "update_pr")
async def update_pr(callback: CallbackQuery):
    await callback.message.answer("Yangi Popular narxini yuboring.")
    global pr_message
    pr_message = None

@dp.callback_query(F.data == "delete_pr")
async def delete_pr(callback: CallbackQuery):
    global pr_message
    pr_message = None
    await callback.message.answer("Popular narxini o‘chirildi.")

@dp.callback_query(F.data == "upload_pr")
async def upload_pr(callback: CallbackQuery):
    await callback.message.answer("Yangi Popular narxini yuboring.")

@dp.message()
async def save_admin_message(message: types.Message):
    user_id = message.from_user.id
    global uc_message, pr_message
    if user_id in Admins:
        if uc_message is None:
            uc_message = message.text
            await message.answer("UC narxi yangilandi.")
        elif pr_message is None:
            pr_message = message.text
            await message.answer("Popular narxi yangilandi.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot faoliyatini tugatdi")
