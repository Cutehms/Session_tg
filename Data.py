from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
- مرحبا {}.
يعمل هذا البوت لمساعدتك بطريقة سهله للحصول على كود تيرمكس او جلسة سلسلة.

**قناة السورس**: @botatiiii
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton("- بدء استخراج جلسه .", callback_data="generate")],
        [InlineKeyboardButton(text="🔙رجوع", callback_data="home")]
    ]

    generate_button = [
        [InlineKeyboardButton("- بدء استخراج جلسه .", callback_data="generate")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("- بدء استخراج جلسه .", callback_data="generate")],
        [InlineKeyboardButton("𓌹●↯‌𝑫𝑨𝑫 𝑺𝑯𝑨𝑫𝑶𝑾↯●𓌺", url="https://t.me/KB_Shadow")],
        [
            InlineKeyboardButton("- طريقة الاستعمال ؟ .", callback_data="help"),
            InlineKeyboardButton("- حول البوت .", callback_data="about")
      ],
        [InlineKeyboardButton("𝑬𝑹𝑹𝑶𝑹🖤", url="https://t.me/botatiiii")],
    ]


    # Help Message
    HELP = """
**- اوامر البوت .**
/about - حول البوت
/help - طريقة الاستخدام
/start - بدء تشغيل البوت
/generate - بدء استخراج جلسه
/cancel - الغاء الاستخراج
/restart - اعادة تشغيل البوت
"""

    # About Message
    ABOUT = """
**- حول البوت .**
⚡ بوت تليجرام لاستخراج كود جلسة pyrogram و telethon:-

- **قناة السورس**: [𝙼𝙰𝚈 𝙱𝙾𝚃𝚂 𖣴](https://t.me/botatiiii)

- **لغة البوت**: [Python](http://www.python.org/)

[𝙷ٍْ𝙼ٍْ𝚂ْ 𓃠𝄬.. 𔘓](https://t.me/hms_01)
    """
