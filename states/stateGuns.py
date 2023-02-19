'''States'''

# Импорты
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMChangeGun(StatesGroup):
    examination = State()
    edit_gun = State()
    to_the_mn = State()
    to_the_mn_exit = State()


class FSMMainMenu(StatesGroup):
    mn = State()
    wait_message = State()
    get_category = State()


class FSMStalkerInfo(StatesGroup):
    info = State()
    pick_category = State()


class FSMShop(StatesGroup):
    examination_guns = State()
    pick_shop_category = State()
    buy_gun = State()
    accept_gun = State()
    to_main_menu = State()

class FSMOuting(StatesGroup):
    wait_answer = State()
    pick_outing_category = State()
    pick_location = State()
    stat_fight = State()
    fight = State()
    end_screen = State()
    return_to_mn = State()

class outingForest(StatesGroup):
    stat_set = State()
    get_answer = State()
    get_continue1 = State()
    get_continue2 = State()
    fight_mn = State()

class outingitems(StatesGroup):
    get_item = State()
    
class passiveOuting(StatesGroup):
    try_join = State()


