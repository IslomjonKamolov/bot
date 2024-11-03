import logging
import json  # JSON moduli import qilinadi
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from config import BOT_TOKEN, ADMINS
from keyboard import menu, user_access, contact_send_btn, channel_list
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from functionsF import check_subscribe

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


class Form(StatesGroup):
    name = State()
    phone = State()
    age = State()
    confirm = State()


# /start uchun javob
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEbsGRnJ8o8shwIMav0QC1S9O6nNIC7tQACmQwAAj9UAUrPkwx5a8EilDYE')
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return

    await message.answer(
        f"Salom {message.from_user.full_name or 'foydalanuvchi'}👋! \nMen ArGraVning rasmiy botiman. \nMenga xabar yuborsangiz men sizga xabar haqidagi barcha ma'lumotlarni yuboraman!",
        reply_markup=menu,
    )
    user_name = message.from_user.full_name
    username = message.from_user.username
    user_id = message.from_user.id

    profile_link = (
        f"<a href='https://t.me/{username}'>{user_name}</a>" if username else user_name
    )

    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"Yangi foydalanuvchi {profile_link} qo'shildi boss 🫡",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


# /help buyruqi uchun javob
@dp.message(Command(commands=["help"]))
async def help_handler(message: types.Message):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    text = (
        "*Bot buyruqlari:*",
        "/start - _botni ishga tushurish._",
        "/help - _bot buyruqlarini ko'rish._",
    )
    await message.answer("\n".join(text), parse_mode="Markdown")


# Formni to'ldirishni boshlash
@dp.message(F.text == "Form to'ldirish")
async def start_form(message: types.Message, state: FSMContext):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    await message.answer(
        "<i>Hozir sizga bir nechta savollar beriladi.</i>\n<b>Har bit savolga to'g'ri javob bering‼️ </b>",
        parse_mode="HTML",
    )
    await message.answer(
        "<b>Ism, familiyangizni kiriting!</b>",
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="HTML",
    )
    await state.set_state(Form.name)


# Ismni qabul qilish
@dp.message(Form.name)
async def update_name(message: types.Message, state: FSMContext):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    await state.update_data(name=message.text)
    await message.answer("🕐 <b>Yoshingizni kiriting!</b>", parse_mode="HTML")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def update_age(message: types.Message, state: FSMContext):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    await state.update_data(age=message.text)
    await message.answer(
        "📞 <b>Telefon raqamingizni kiriting!</b>",
        parse_mode="HTML",
        reply_markup=contact_send_btn,
    )
    await state.set_state(Form.phone)


@dp.message(Form.phone)
async def update_phone(message: types.Message, state: FSMContext):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    await state.update_data(phone=message.contact.phone_number)
    print(message.contact.phone_number)

    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    phone = data.get("phone")

    await message.answer(
        f"<b>Ma'lumotnoma</b>\n"
        f"<b>Ismi:</b> <i>{name}</i>\n"
        f"<b>Yoshi:</b> <i>{age}</i>\n"
        f"<b>Telefon:</b> <i>{phone}</i>\n"
        f"<b>Telegram:</b> <i>@{message.from_user.username or message.from_user.full_name}</i>",
        parse_mode="HTML",
    )
    await message.answer("Bu ma'lumotlar to'g'rimi❓", reply_markup=user_access)
    await state.set_state(Form.confirm)


@dp.message(Form.confirm, F.text.in_(["Ha", "Yo'q"]))
async def confirmation_fun(message: types.Message, state: FSMContext):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    if message.text == "Ha":
        data = await state.get_data()
        name = data.get("name")
        age = data.get("age")
        phone = data.get("phone")

        await bot.send_message(
            6150443453,
            f"<b>Yangi ma'lumotlar:</b>\n"
            f"<b>Ism:</b> <i>{name}</i>\n"
            f"<b>Yosh:</b> <i>{age}</i>\n"
            f"<b>Manzil:</b> <i>{phone}</i>\n"
            f"<b>Telegram:</b> <i>@{message.from_user.username or message.from_user.full_name}</i>",
            parse_mode="HTML",
        )
        await message.answer(
            "✅ Ma'lumotlaringiz adminga yuborildi.",
            reply_markup=menu,
        )

    else:
        await message.answer("❌ Xabar yuborilmadi.", reply_markup=menu)

    await state.clear()


# Foydalanuvchiga xabar ma'lumotlarini yuborish
@dp.message()
async def echo(message: types.Message, state: FSMContext):
    is_subscribed = await check_subscribe(bot=bot, user_id=message.from_user.id)

    if not is_subscribed:
        await message.answer(
            "Bo'tdan foydalanish uchun quyidagi kanallarga obuna bo'ling va /start buyrug'ini yuboring‼️ \n 👇👇👇👇👇", reply_markup=channel_list
        )
        return
    if await state.get_state() is None:
        message_data = {
            "message_id": message.message_id,
            "date": message.date.isoformat(),
            "chat_id": message.chat.id,
            "from_user": {
                "id": message.from_user.id,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "username": message.from_user.username,
                "language_code": message.from_user.language_code,
            },
            "text": message.text,
        }
        message_json = json.dumps(message_data, indent=4)
        await message.answer(
            f"Xabar ma'lumotlari: \n```\n{message_json}\n```", parse_mode="Markdown"
        )


if __name__ == "__main__":
    dp.run_polling(bot)
