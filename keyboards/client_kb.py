from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base.sqlite_db import have_gun

# Главное меню INLINE
kb_main_menu_myprofile = InlineKeyboardButton(text='Информация о сталкере', callback_data='info_about_stalker')
kb_main_menu_inventory = InlineKeyboardButton(text='Инвентарь', callback_data='Inventory')
kb_main_menu_travel = InlineKeyboardButton(text='Отправиться на вылазку', callback_data='outing')
kb_main_menu_market = InlineKeyboardButton(text='Торговая лавка', callback_data='shop')
kb_main_menu_test = InlineKeyboardButton(text='Помощь', callback_data='help')
kb_main_menu_restart = InlineKeyboardButton(text='Перезапустить меню', callback_data='/start')

kb_main_menu = InlineKeyboardMarkup(row_width=2)
kb_main_menu.add(kb_main_menu_myprofile, kb_main_menu_inventory).add(kb_main_menu_travel).add(kb_main_menu_market,
                                                                                              kb_main_menu_test).add(kb_main_menu_restart)

# Информация о сталкере INLINE
ikb_stalker_info = InlineKeyboardMarkup(row_width=2)
ikb_stalker_info_gun = InlineKeyboardButton(text='Поменять оружие', callback_data='edit_gun')
ikb_stalker_info_costume = InlineKeyboardButton(text='Поменять костюм', callback_data='edit_costume')
ikb_stalker_info_main_menu = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
ikb_stalker_info.add(ikb_stalker_info_gun, ikb_stalker_info_costume).add(ikb_stalker_info_main_menu)

# Случайные события REPLY
kb_client_random_events_kubiki = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# Вернуться в главное меню ONLY 1 INLINE
ikb_return_to_main_menu = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [InlineKeyboardButton(text='Вернуться в главное меню',
                                                                         callback_data='to_main_menu')]
                                               ])

# Торговая лавка
ikb_shop_guns = InlineKeyboardButton(text='Оружия', callback_data='gun_shop')
ikb_shop_costumes = InlineKeyboardButton(text='Костюмы', callback_data='costume_shop')
ikb_shop_main_menu = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
ikb_shop = InlineKeyboardMarkup(row_width=2).add(ikb_shop_guns, ikb_shop_costumes).add(ikb_shop_main_menu)

# Отправиться на вылазку
ikb_outing_active = InlineKeyboardButton(text='Активная вылазка', callback_data='active_outing')
ikb_outing_passive = InlineKeyboardButton(text='Афк вылазка', callback_data='passive_outing')
ikb_outing_main_menu = InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')
ikb_outing = InlineKeyboardMarkup(row_width=2).add(ikb_outing_active, ikb_outing_passive).add(ikb_outing_main_menu)

# Активная вылазка
ikb_outing_ac_1 = InlineKeyboardButton(text='Зараженный лес', callback_data='forest')
ikb_outing_ac_back = InlineKeyboardButton(text='Вернуться назад', callback_data='back')
ikb_outing_ac = InlineKeyboardMarkup(row_width=3).add(ikb_outing_ac_1).add(ikb_outing_ac_back)


# Случайное событие НЕЗНАКОМЕЦ
ikb_outing_anonimous_no = InlineKeyboardButton(text='Свернуть с тропинки', callback_data='no')
ikb_outing_anonimous_yes = InlineKeyboardButton(text='Идти дальше', callback_data='yes')
ikb_outing_anonimous = InlineKeyboardMarkup(row_width=2).add(ikb_outing_anonimous_yes, ikb_outing_anonimous_no)

# Дальше
ikb_next = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Дальше', callback_data='next'))
# ********************* ИНЛАЙН КЛАВИАТУРА *******************
ikb_client_kubiki_number1 = InlineKeyboardButton(text='1', callback_data=1)
ikb_client_kubiki_number2 = InlineKeyboardButton(text='2', callback_data=2)
ikb_client_kubiki_number3 = InlineKeyboardButton(text='3', callback_data=3)
ikb_client_kubiki_number4 = InlineKeyboardButton(text='4', callback_data=4)
ikb_client_kubiki_number5 = InlineKeyboardButton(text='5', callback_data=5)
ikb_client_kubiki_number6 = InlineKeyboardButton(text='6', callback_data=6)

ikb_client_kubiki_number = InlineKeyboardMarkup(row_width=3).add(ikb_client_kubiki_number1, ikb_client_kubiki_number2,
                                                                 ikb_client_kubiki_number3).add(
    ikb_client_kubiki_number4, ikb_client_kubiki_number5, ikb_client_kubiki_number6)

ikb_client_kubiki_onl_cansel = InlineKeyboardMarkup(row_width=1)



def ikb_shop_guns_pick():
    if have_gun():
        pass

    ikb_shop_guns_pick_1 = InlineKeyboardButton(text=f'1', callback_data=1)
    ikb_shop_guns_pick_2 = InlineKeyboardButton(text='2', callback_data=2)
    ikb_shop_guns_pick_3 = InlineKeyboardButton(text='3', callback_data=3)
    ikb_shop_guns_pick_4 = InlineKeyboardButton(text='4', callback_data=4)
    ikb_shop_guns_pick_5 = InlineKeyboardButton(text='5', callback_data=5)
    ikb_shop_guns_pick_6 = InlineKeyboardButton(text='6', callback_data=6)
    ikb_shop_guns_pick_back = InlineKeyboardButton(text='Вернуться назад', callback_data='back_to_shop')

    ikb_shop_guns_pick = InlineKeyboardMarkup(row_width=3).add(ikb_shop_guns_pick_1, ikb_shop_guns_pick_2,
                                                               ikb_shop_guns_pick_3).add(ikb_shop_guns_pick_back)

ikb_shop_yes = InlineKeyboardButton(text='Купить', callback_data='yes')
ikb_shop_no = InlineKeyboardButton(text='Назад', callback_data='no')
ikb_shop_pick = InlineKeyboardMarkup(row_width=2).add(ikb_shop_yes, ikb_shop_no)


def ikb_outing_fight_stat1(x):
    ikb_outing_stats_atack = InlineKeyboardButton(text='Атаковать ⚔️', callback_data='atack')
    ikb_outing_stats_run = InlineKeyboardButton(text='Убежать 🏳️', callback_data='run')
    ikb_outing_stats_item = InlineKeyboardButton(text='Использовать предмет 🔮', callback_data='item')
    ikb_outing_stats_speed = InlineKeyboardButton(text=f"Скорость: {x} 🚀", callback_data='speed')

    return InlineKeyboardMarkup(row_width=2).add(ikb_outing_stats_atack, ikb_outing_stats_run).add(
        ikb_outing_stats_item).add(ikb_outing_stats_speed)

def ikb_outing_fight_stat2():
    ikb_outing_stats_atack = InlineKeyboardButton(text='Атаковать ⚔️', callback_data='atack')
    ikb_outing_stats_run = InlineKeyboardButton(text='Убежать 🏳️', callback_data='run')
    ikb_outing_stats_item = InlineKeyboardButton(text='Использовать предмет 🔮', callback_data='item')
    ikb_outing_stats_speed = InlineKeyboardButton(text=f"Скорость: 2x 🚀", callback_data='speed')

    return InlineKeyboardMarkup(row_width=2).add(ikb_outing_stats_atack, ikb_outing_stats_run).add(
        ikb_outing_stats_item).add(ikb_outing_stats_speed)