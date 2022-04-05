from asyncio.exceptions import TimeoutError
from Data import Data
from pyrogram import Client, filters
from telethon import TelegramClient
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(
        "- يرجى تحديد نوع الجلسه المراد استخراجها .",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("كود بايروجرام", callback_data="pyrogram"),
            InlineKeyboardButton("كود تـلـيـثـون", callback_data="telethon")
        ]])
    )


async def generate_session(bot, msg, telethon=False):
    await msg.reply("- بدء استخراج جلسة {}...".format("Telethon" if telethon else "Pyrogram"))
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, '- حسنا يرجى ارسال ال API_ID`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('ال `API_ID` غير صالح قم بكتابة /restart ثم اعد المحاوله..', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, '- حسنا يرجى ارسال ال API_HASH`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    api_hash = api_hash_msg.text
    phone_number_msg = await bot.ask(user_id, '- الان يرجى ارسال رقمك بشكل كامل\n**مثال**: `+14154566376`', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    phone_number = phone_number_msg.text
    await msg.reply("- جاري ارسال الكود لحسابك...")
    if telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    else:
        client = Client(":memory:", api_id, api_hash)
    await client.connect()
    try:
        if telethon:
            code = await client.send_code_request(phone_number)
        else:
            code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('حدث خطأ قم بكتابة /restart ثم اعد المحاوله..', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('رقم الهاتف الذي ارسلته غير صالح قم بكتابة /restart ثم اعد المحاوله..', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = await bot.ask(user_id, "قم بإرسال الكود الذي وصلك عبر تليجرام بالشكل التالي ( `1 2 3 4 5` )\nمع وجود فواصل بين كل رقم و الآخر\nللإلغاء ارسل /cancel\nللعوده للبدايه ارسل /restart\n\n**قناة السورس** @FA9SH", filters=filters.text, timeout=600)
        if await cancelled(api_id_msg):
            return
    except TimeoutError:
        await msg.reply('بلغ الحد الزمني 10 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى..', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    phone_code = phone_code_msg.text.replace(" ", "")
    try:
        if telethon:
            await client.sign_in(phone_number, phone_code, password=None)
        else:
            await client.sign_in(phone_number, code.phone_code_hash, phone_code)
    except (PhoneCodeInvalid, PhoneCodeInvalidError):
        await msg.reply('عفوا الكود غير صحيح.\nيرجى البدء في إنشاء جلسه جديده.', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneCodeExpired, PhoneCodeExpiredError):
        await msg.reply('انتهت صلاحيهة الكود ، يرجى البدء في إنشاء الجلسه مره اخرى..', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (SessionPasswordNeeded, SessionPasswordNeededError):
        try:
            two_step_msg = await bot.ask(user_id, 'لقد مكّن حسابك التحقق على خطوتين. يرجى تقديم كلمة المرور.', filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply('بلغ الحد الزمني 5 دقائق. يرجى البدء في إنشاء الجلسة مرة أخرى..', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        try:
            password = two_step_msg.text
            if telethon:
                await client.sign_in(password=password)
            else:
                await client.check_password(password=password)
            if await cancelled(api_id_msg):
                return
        except (PasswordHashInvalid, PasswordHashInvalidError):
            await two_step_msg.reply('كلمة المرور التي ارسلتها غير صحيحه.\nيرجى البدء في إنشاء جلسه جديده.', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = "**كود جلسة {} بالاسفل** \n\n`{}` \n\n**قناة السورس**: @botatiiii\n**جروب الدعم**: @hmsrobot".format("Telethon" if telethon else "Pyrogram", string_session)
    try:
        await client.send_message("me", text)
    except KeyError:
        pass
    await client.disconnect()
    await phone_code_msg.reply("تم الاستخراج بنجاح.!\nكود`{}`\nقم بتفقد الرسائل المحفوظه.".format("Telethon" if telethon else "Pyrogram"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("◍ تم الغاء الاستخراج\n√", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("◍ تمت اعادة تشغيل البوت\n√", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("◍ تم الغاء الاستخراج\n√", quote=True)
        return True
    else:
        return False
