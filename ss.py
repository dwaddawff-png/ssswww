import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = "9128249912:AAFZm-iYoCgnzsvCDDvAlf_a1EDwVzHOdLA"

# ID чата/аккаунта поддержки:
SUPPORT_CHAT_ID = 8268632797

# Username администратора для сотрудничества:
ADMIN_USERNAME = "@qumikov"

# Ваш адрес TON-кошелька для реквизитов:
TON_WALLET_ADDRESS = "UQAxbUdljg2LHSVADTfugzjAZDiV4Zdb7BgxkjaCdyHvYHhj"

# Адрес для раздела Crypto Bot:
CRYPTO_BOT_WALLET_ADDRESS = "UQBcw028jG1QiAe4xqypr00KlLsLD6vbcrIvyoyvhe6ezuJ1"

# Ссылка на ваш профиль Telegram (@flipskoi):
PROFILE_URL = "https://t.me/flipskoi"

# Ссылка на профиль для оплаты звёздами (Scam Offers 300 Stars / Tracker 200 Stars):
STARS_PROFILE_URL = "https://t.me/abamovver"

# Токен Crypto Pay API (из @CryptoBot -> Crypto Pay -> Create App). Можно оставить пустым "", если не подключён:
CRYPTO_PAY_TOKEN = ""
CRYPTO_PAY_API_URL = "https://pay.crypt.bot/api"
# =================================================

CLEAN_ADMIN_USERNAME = ADMIN_USERNAME.lstrip("@")
ADMIN_CHAT_URL = f"https://t.me/{CLEAN_ADMIN_USERNAME}"
FORMATTED_ADMIN_USERNAME = f"@{CLEAN_ADMIN_USERNAME}"


class SupportStates(StatesGroup):
    waiting_for_message = State()


TEXTS = {
    "ru": {
        "welcome": "🚀 Welcome to our services!\n\nВыбери необходимое действие:",
        "buy": "💻 Купить услуги",
        "lang": "↺ Язык",
        "support": "👤 Поддержка",
        "coop": "🤝 Сотрудничество",
        "choose_lang": "🌐 Выберите язык / Choose language:",
        "lang_changed": "✅ Язык изменён на русский.",
        "select_service": "💻 Выберите интересующую вас услугу:",
        "scam_offers_title": "🎉 SCAM OFFERS\n\nВыберите удобный способ оплаты:",
        "tracker_title": "✓✓ TRACKER\n\nВыберите удобный способ оплаты:",
        "ton_payment_text": (
            "💼 Оплата через TON\n\n"
            "Сеть: TON\n"
            "Сумма: {amount} TON\n\n"
            "Реквизиты для оплаты:\n"
            "{wallet}"
        ),
        "copy_address_btn": "Ⓑ Скопировать адрес",
        "crypto_bot_btn": "💎 Crypto Bot",
        "paid_btn": "👤 Оплатил",
        "back_btn": "↩️ Назад",
        "copied_alert": "Адрес скопирован (или нажмите на блок ниже)",
        "copied_msg": "📋 Адрес для копирования (нажмите на него):\n<code>{wallet}</code>",
        "crypto_no_token": (
            "💎 Crypto Bot\n\n"
            "Реквизиты для перевода:\n"
            "<code>{wallet}</code>"
        ),
        "crypto_error": "⚠️ Не удалось создать счёт в Crypto Bot. Проверьте токен и баланс.",
        "crypto_invoice_msg": (
            "💎 Счёт в Crypto Bot создан!\n\n"
            "Сумма: <b>{amount} TON</b>\n"
            "Адрес получателя: <code>{wallet}</code>\n\n"
            "Нажмите кнопку ниже для оплаты:"
        ),
        "crypto_pay_link_btn": "💳 Оплатить в Crypto Bot",
        "paid_user_msg": "✅ Заявка об оплате отправлена! Ожидайте подтверждения от поддержки.",
        "coop_msg": (
            "🤝 <b>Сотрудничество</b>\n\n"
            "Все вопросы по поводу сотрудничества и партнёрки обсуждаются с моим администратором в ЛС. {admin}"
        ),
        "admin_pm_btn": "✉️ Написать администратору",
        "support_prompt": (
            "💬 Напишите ваш вопрос или опишите проблему одним сообщением.\n"
            "Мы передадим его в поддержку и ответим здесь в боте."
        ),
        "support_sent": "✅ Сообщение отправлено в поддержку! Ожидайте ответ здесь.",
        "support_cancelled": "❌ Диалог с поддержкой отменён.",
        "support_no_chat": "⚠️ Чат поддержки пока не настроен (укажите SUPPORT_CHAT_ID).",
        "cancel_btn": "❌ Отменить",
    },
    "en": {
        "welcome": "🚀 Welcome to our services!\n\nChoose the required action:",
        "buy": "💻 Buy services",
        "lang": "↺ Language",
        "support": "👤 Support",
        "coop": "🤝 Cooperation",
        "choose_lang": "🌐 Choose language / Выберите язык:",
        "lang_changed": "✅ Language changed to English.",
        "select_service": "💻 Select the service you are interested in:",
        "scam_offers_title": "🎉 SCAM OFFERS\n\nChoose a convenient payment method:",
        "tracker_title": "✓✓ TRACKER\n\nChoose a convenient payment method:",
        "ton_payment_text": (
            "💼 Payment via TON\n\n"
            "Network: TON\n"
            "Amount: {amount} TON\n\n"
            "Payment details:\n"
            "{wallet}"
        ),
        "copy_address_btn": "Ⓑ Copy address",
        "crypto_bot_btn": "💎 Crypto Bot",
        "paid_btn": "👤 Paid",
        "back_btn": "↩️ Back",
        "copied_alert": "Tap the address block below to copy",
        "copied_msg": "📋 Tap to copy address:\n<code>{wallet}</code>",
        "crypto_no_token": (
            "💎 Crypto Bot\n\n"
            "Transfer details:\n"
            "<code>{wallet}</code>"
        ),
        "crypto_error": "⚠️ Failed to create Crypto Bot invoice. Check token and settings.",
        "crypto_invoice_msg": (
            "💎 Crypto Bot invoice created!\n\n"
            "Amount: <b>{amount} TON</b>\n"
            "Recipient address: <code>{wallet}</code>\n\n"
            "Tap the button below to pay:"
        ),
        "crypto_pay_link_btn": "💳 Pay in Crypto Bot",
        "paid_user_msg": "✅ Payment notification sent! Please wait for support confirmation.",
        "coop_msg": (
            "🤝 <b>Cooperation</b>\n\n"
            "Все вопросы по поводу сотрудничества и партнёрки обсуждаются с моим администратором в ЛС. {admin}"
        ),
        "admin_pm_btn": "✉️ Message administrator",
        "support_prompt": (
            "💬 Type your question or describe the issue in one message.\n"
            "We will forward it to support and reply right here in the bot."
        ),
        "support_sent": "✅ Your message has been sent to support! Please wait for a reply here.",
        "support_cancelled": "❌ Support chat cancelled.",
        "support_no_chat": "⚠️ Support chat is not configured yet (set SUPPORT_CHAT_ID).",
        "cancel_btn": "❌ Cancel",
    },
    "uk": {
        "welcome": "🚀 Welcome to our services!\n\nОберіть потрібну дію:",
        "buy": "💻 Купити послуги",
        "lang": "↺ Мова",
        "support": "👤 Підтримка",
        "coop": "🤝 Співпраця",
        "choose_lang": "🌐 Оберіть мову / Choose language:",
        "lang_changed": "✅ Мову змінено на українську.",
        "select_service": "💻 Оберіть послугу, яка вас цікавить:",
        "scam_offers_title": "🎉 SCAM OFFERS\n\nОберіть зручний спосіб оплати:",
        "tracker_title": "✓✓ TRACKER\n\nОберіть зручний спосіб оплати:",
        "ton_payment_text": (
            "💼 Оплата через TON\n\n"
            "Мережа: TON\n"
            "Сума: {amount} TON\n\n"
            "Реквізити для оплати:\n"
            "{wallet}"
        ),
        "copy_address_btn": "Ⓑ Скопіювати адресу",
        "crypto_bot_btn": "💎 Crypto Bot",
        "paid_btn": "👤 Оплатив",
        "back_btn": "↩️ Назад",
        "copied_alert": "Натисніть на блок з адресою нижче, щоб скопіювати",
        "copied_msg": "📋 Натисніть на адресу, щоб скопіювати:\n<code>{wallet}</code>",
        "crypto_no_token": (
            "💎 Crypto Bot\n\n"
            "Реквізити для переказу:\n"
            "<code>{wallet}</code>"
        ),
        "crypto_error": "⚠️ Не вдалося створити рахунок у Crypto Bot. Перевірте токен.",
        "crypto_invoice_msg": (
            "💎 Рахунок у Crypto Bot створено!\n\n"
            "Сума: <b>{amount} TON</b>\n"
            "Адреса отримувача: <code>{wallet}</code>\n\n"
            "Натисніть кнопку нижче для оплати:"
        ),
        "crypto_pay_link_btn": "💳 Оплатити в Crypto Bot",
        "paid_user_msg": "✅ Заявку про оплату надіслано! Очікуйте підтвердження підтримки.",
        "coop_msg": (
            "🤝 <b>Співпраця</b>\n\n"
            "Все вопросы по поводу сотрудничества и партнёрки обсуждаются с моим администратором в ЛС. {admin}"
        ),
        "admin_pm_btn": "✉️ Написати адміністратору",
        "support_prompt": (
            "💬 Напишіть ваше запитання або опишіть проблему одним повідомленням.\n"
            "Ми передамо його в підтримку та відповімо тут у боті."
        ),
        "support_sent": "✅ Повідомлення надіслано в підтримку! Очікуйте відповідь тут.",
        "support_cancelled": "❌ Діалог із підтримкою скасовано.",
        "support_no_chat": "⚠️ Чат підтримки ще не налаштовано (вкажіть SUPPORT_CHAT_ID).",
        "cancel_btn": "❌ Скасувати",
    },
}

user_languages: dict[int, str] = {}


def get_user_lang(user_id: int) -> str:
    return user_languages.get(user_id, "ru")


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["buy"], callback_data="menu_buy")],
            [
                InlineKeyboardButton(text=t["lang"], callback_data="menu_lang"),
                InlineKeyboardButton(text=t["support"], callback_data="menu_support"),
            ],
            [InlineKeyboardButton(text=t["coop"], callback_data="menu_coop")],
        ]
    )


def languages_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
            [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_lang_uk")],
            [InlineKeyboardButton(text=t["back_btn"], callback_data="back_to_menu")],
        ]
    )


def services_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎉 Scam Offers", callback_data="service_scam_offers"),
                InlineKeyboardButton(text="✓✓ Трекер", callback_data="service_tracker"),
            ],
            [InlineKeyboardButton(text=t["back_btn"], callback_data="back_to_menu")],
        ]
    )


def scam_offers_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💎 3 TON", callback_data="pay_ton_scam_offers_3"),
                InlineKeyboardButton(text="★ 300 Stars", url=STARS_PROFILE_URL),
            ],
            [InlineKeyboardButton(text=t["back_btn"], callback_data="menu_buy")],
        ]
    )


def tracker_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💎 2 TON", callback_data="pay_ton_tracker_2"),
                InlineKeyboardButton(text="★ 200 Stars", url=STARS_PROFILE_URL),
            ],
            [InlineKeyboardButton(text=t["back_btn"], callback_data="menu_buy")],
        ]
    )


def ton_payment_keyboard(lang: str, service_code: str, amount: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t["copy_address_btn"], callback_data="copy_ton_address"),
                InlineKeyboardButton(
                    text=t["crypto_bot_btn"],
                    callback_data=f"cryptobot_{service_code}_{amount}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t["paid_btn"],
                    callback_data=f"paid_{service_code}_{amount}",
                ),
                InlineKeyboardButton(text=t["back_btn"], callback_data=f"service_{service_code}"),
            ],
        ]
    )


def cancel_support_keyboard(lang: str) -> InlineKeyboardMarkup:
    t = TEXTS[lang]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t["cancel_btn"], callback_data="cancel_support")],
        ]
    )


async def create_crypto_pay_invoice(amount: str, description: str) -> str | None:
    if not CRYPTO_PAY_TOKEN:
        return None

    headers = {"Crypto-Pay-API-Token": CRYPTO_PAY_TOKEN}
    payload = {
        "asset": "TON",
        "amount": amount,
        "description": description,
        "payload": f"ton_transfer:{CRYPTO_BOT_WALLET_ADDRESS}:{amount}",
        "paid_btn_name": "callback",
        "paid_btn_url": PROFILE_URL,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{CRYPTO_PAY_API_URL}/createInvoice",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                data = await resp.json()
                if data.get("ok") and data.get("result"):
                    return data["result"].get("pay_url")
    except Exception:
        return None

    return None


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    lang = get_user_lang(message.from_user.id)
    await message.answer(
        TEXTS[lang]["welcome"],
        reply_markup=main_menu_keyboard(lang),
    )


@dp.callback_query(F.data == "menu_lang")
async def open_languages(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]["choose_lang"],
        reply_markup=languages_keyboard(lang),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: CallbackQuery) -> None:
    new_lang = callback.data.removeprefix("set_lang_")
    if new_lang in TEXTS:
        user_languages[callback.from_user.id] = new_lang

    t = TEXTS[new_lang]
    await callback.answer(t["lang_changed"], show_alert=False)
    await callback.message.edit_text(
        t["welcome"],
        reply_markup=main_menu_keyboard(new_lang),
    )


@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]["welcome"],
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_buy")
async def open_services(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]["select_service"],
        reply_markup=services_keyboard(lang),
    )
    await callback.answer()


@dp.callback_query(F.data == "service_scam_offers")
async def open_scam_offers(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]["scam_offers_title"],
        reply_markup=scam_offers_keyboard(lang),
    )
    await callback.answer()


@dp.callback_query(F.data == "service_tracker")
async def open_tracker(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]["tracker_title"],
        reply_markup=tracker_keyboard(lang),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("pay_ton_"))
async def open_ton_payment(callback: CallbackQuery) -> None:
    raw = callback.data.removeprefix("pay_ton_")
    parts = raw.rsplit("_", 1)
    service_code = parts[0]
    amount = parts[1] if len(parts) == 2 else "3"

    lang = get_user_lang(callback.from_user.id)
    text = TEXTS[lang]["ton_payment_text"].format(
        amount=amount,
        wallet=TON_WALLET_ADDRESS,
    )
    await callback.message.edit_text(
        text,
        reply_markup=ton_payment_keyboard(lang, service_code, amount),
    )
    await callback.answer()


@dp.callback_query(F.data == "copy_ton_address")
async def copy_ton_address(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    await callback.answer(TEXTS[lang]["copied_alert"], show_alert=False)
    await callback.message.answer(
        TEXTS[lang]["copied_msg"].format(wallet=TON_WALLET_ADDRESS),
        parse_mode="HTML",
    )


@dp.callback_query(F.data.startswith("cryptobot_"))
async def create_cryptobot_payment(callback: CallbackQuery) -> None:
    raw = callback.data.removeprefix("cryptobot_")
    parts = raw.rsplit("_", 1)
    service_code = parts[0]
    amount = parts[1] if len(parts) == 2 else "3"

    lang = get_user_lang(callback.from_user.id)
    if not CRYPTO_PAY_TOKEN:
        await callback.answer()
        await callback.message.answer(
            TEXTS[lang]["crypto_no_token"].format(wallet=CRYPTO_BOT_WALLET_ADDRESS),
            parse_mode="HTML",
        )
        return

    pay_url = await create_crypto_pay_invoice(
        amount=amount,
        description=f"{service_code} ({amount} TON) -> {CRYPTO_BOT_WALLET_ADDRESS}",
    )
    await callback.answer()

    if not pay_url:
        await callback.message.answer(TEXTS[lang]["crypto_error"])
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["crypto_pay_link_btn"], url=pay_url)]
        ]
    )
    await callback.message.answer(
        TEXTS[lang]["crypto_invoice_msg"].format(amount=amount, wallet=CRYPTO_BOT_WALLET_ADDRESS),
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@dp.callback_query(F.data.startswith("paid_"))
async def confirm_paid(callback: CallbackQuery, bot: Bot) -> None:
    raw = callback.data.removeprefix("paid_")
    parts = raw.rsplit("_", 1)
    service_code = parts[0]
    amount = parts[1] if len(parts) == 2 else "3"

    user = callback.from_user
    lang = get_user_lang(user.id)
    username = f"@{user.username}" if user.username else "без username"

    await callback.answer()
    await callback.message.answer(TEXTS[lang]["paid_user_msg"])

    if SUPPORT_CHAT_ID:
        notice = (
            f"💸 <b>Пользователь нажал «Оплатил»</b>\n"
            f"Пользователь: {user.full_name} ({username})\n"
            f"ID: <code>{user.id}</code>\n"
            f"Услуга: <code>{service_code}</code>\n"
            f"Сумма: <b>{amount} TON</b>\n"
            f"Кошелёк: <code>{TON_WALLET_ADDRESS}</code>\n"
            f"Кошелёк Crypto Bot: <code>{CRYPTO_BOT_WALLET_ADDRESS}</code>"
        )
        await bot.send_message(chat_id=SUPPORT_CHAT_ID, text=notice, parse_mode="HTML")


@dp.callback_query(F.data == "menu_coop")
async def on_cooperation(callback: CallbackQuery) -> None:
    lang = get_user_lang(callback.from_user.id)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["admin_pm_btn"], url=ADMIN_CHAT_URL)],
            [InlineKeyboardButton(text=TEXTS[lang]["back_btn"], callback_data="back_to_menu")],
        ]
    )
    await callback.message.edit_text(
        TEXTS[lang]["coop_msg"].format(admin=FORMATTED_ADMIN_USERNAME),
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@dp.callback_query(F.data == "menu_support")
async def start_support(callback: CallbackQuery, state: FSMContext) -> None:
    lang = get_user_lang(callback.from_user.id)
    if not SUPPORT_CHAT_ID:
        await callback.answer()
        await callback.message.answer(TEXTS[lang]["support_no_chat"])
        return

    await state.set_state(SupportStates.waiting_for_message)
    await callback.message.edit_text(
        TEXTS[lang]["support_prompt"],
        reply_markup=cancel_support_keyboard(lang),
    )
    await callback.answer()


@dp.callback_query(F.data == "cancel_support")
async def cancel_support(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    lang = get_user_lang(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]["support_cancelled"],
    )
    await callback.message.answer(
        TEXTS[lang]["welcome"],
        reply_markup=main_menu_keyboard(lang),
    )
    await callback.answer()


@dp.message(SupportStates.waiting_for_message)
async def forward_to_support(message: Message, state: FSMContext, bot: Bot) -> None:
    user = message.from_user
    lang = get_user_lang(user.id)
    username = f"@{user.username}" if user.username else "без username"

    header = (
        f"📩 Новое обращение в поддержку\n"
        f"Пользователь: {user.full_name} ({username})\n"
        f"ID: <code>{user.id}</code>\n\n"
        f"Чтобы ответить, сделайте Reply на это сообщение."
    )

    await bot.send_message(chat_id=SUPPORT_CHAT_ID, text=header, parse_mode="HTML")
    await message.copy_to(chat_id=SUPPORT_CHAT_ID)

    await state.clear()
    await message.answer(TEXTS[lang]["support_sent"])
    await message.answer(
        TEXTS[lang]["welcome"],
        reply_markup=main_menu_keyboard(lang),
    )


@dp.message(F.chat.id == SUPPORT_CHAT_ID, F.reply_to_message)
async def reply_from_support(message: Message, bot: Bot) -> None:
    replied_text = message.reply_to_message.text or message.reply_to_message.caption or ""
    target_user_id: int | None = None

    for line in replied_text.splitlines():
        if line.startswith("ID:"):
            raw_id = line.removeprefix("ID:").strip()
            if raw_id.isdigit():
                target_user_id = int(raw_id)
            break

    if not target_user_id:
        return

    await bot.send_message(
        chat_id=target_user_id,
        text="💬 <b>Ответ от поддержки:</b>",
        parse_mode="HTML",
    )
    await message.copy_to(chat_id=target_user_id)
    await message.reply("✅ Ответ отправлен пользователю.")


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())