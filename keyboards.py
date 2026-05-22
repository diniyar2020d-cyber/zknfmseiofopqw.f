from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="💳 Реквизиты до 30к", callback_data="requisites")],
        [InlineKeyboardButton(text="⚡️ Быстрый перевод", callback_data="fast_transfer")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="info")],
        [InlineKeyboardButton(text="🏆 Наши лучшие мажорики", callback_data="top_users")]
    ])

def back_button(callback="main_menu"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data=callback)]
    ])

def profile_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Баланс / Вывод", callback_data="balance_withdraw")],
        [InlineKeyboardButton(text="🏷 Тег", callback_data="change_tag")],
        [InlineKeyboardButton(text="📝 Описание", callback_data="change_desc")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

def withdraw_methods():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 CryptoBot", callback_data="withdraw_cryptobot")],
        [InlineKeyboardButton(text="💎 USDT BNB", callback_data="withdraw_usdt")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="profile")]
    ])

def settings_menu(anon_status):
    text = "Включена" if anon_status else "Выключена"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪞 Создать зеркало", callback_data="create_mirror")],
        [InlineKeyboardButton(text=f"🔒 Анонимность: {text}", callback_data="toggle_anon")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

def country_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Россия", callback_data="country_Россия")],
        [InlineKeyboardButton(text="🇺🇿 Узбекистан", callback_data="country_Узбекистан")],
        [InlineKeyboardButton(text="🇰🇿 Казахстан", callback_data="country_Казахстан")],
        [InlineKeyboardButton(text="🇹🇯 Таджикистан", callback_data="country_Таджикистан")],
        [InlineKeyboardButton(text="🇺🇦 Украина", callback_data="country_Украина")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

def requisites_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Сообщить о переводе", callback_data="report_transfer")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="requisites")]
    ])

def fast_transfer_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Запрос карты", url=f"https://t.me/PAYS_MAJOR")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

def info_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Профиты", url="https://t.me/+4nIwWSfYJkw3NTQx")],
        [InlineKeyboardButton(text="💬 Общий чат", url="https://t.me/+K88Uc24hbNQ4YzMy")],
        [InlineKeyboardButton(text="📰 Инфо канал", url="https://t.me/+pDJS0g7ZXXkxMjRh")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

def top_period_buttons():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📅 За все время", callback_data="top_all")],
        [InlineKeyboardButton(text="📆 За сутки", callback_data="top_day")],
        [InlineKeyboardButton(text="📊 За неделю", callback_data="top_week")],
        [InlineKeyboardButton(text="🗓 За месяц", callback_data="top_month")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])

def admin_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Профиты", callback_data="admin_profits")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="💳 Реквизиты", callback_data="admin_requisites")],
        [InlineKeyboardButton(text="⚖️ Балансы", callback_data="admin_balances")],
        [InlineKeyboardButton(text="📤 Запросы на вывод", callback_data="admin_withdraws")],
        [InlineKeyboardButton(text="📢 Оповестить", callback_data="admin_notify")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])

def admin_profits_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Выдать профит", callback_data="admin_give_profit")],
        [InlineKeyboardButton(text="❌ Удалить последний", callback_data="admin_remove_profit")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_panel")]
    ])

def admin_users_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Сколько всего", callback_data="admin_count_users")],
        [InlineKeyboardButton(text="🔨 Забанить", callback_data="admin_ban_user")],
        [InlineKeyboardButton(text="✍️ Написать", callback_data="admin_msg_user")],
        [InlineKeyboardButton(text="🔓 Разбанить", callback_data="admin_unban_user")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_panel")]
    ])

def admin_requisites_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Замена", callback_data="admin_replace_req")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data="admin_delete_req")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_panel")]
    ])

def admin_withdraw_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀 Посмотреть", callback_data="admin_view_withdraws")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="admin_panel")]
    ])

def approve_buttons(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Принять", callback_data=f"approve_{user_id}"),
         InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject_{user_id}")]
    ])

def check_actions(req_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Залито", callback_data=f"check_accept_{req_id}"),
         InlineKeyboardButton(text="❌ Не залито", callback_data=f"check_reject_{req_id}")]
    ])