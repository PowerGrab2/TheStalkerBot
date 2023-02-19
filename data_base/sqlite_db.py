import sqlite3 as sq
from items.guns_items import *

async def sql_start():
    '''Создание бд'''
    global db, cur
    db = sq.connect('Stalker_game.db')
    cur = db.cursor()
    if db:
        print('База даных запущена')
    db.execute("CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, name TEXT, credits TEXT, energy INTEGER DEFAULT 5, current_gun TEXT DEFAULT 'pistol_pmm', exp INT DEFAULT 0, is_admin INTEGER DEFAULT 0)")
    db.execute("CREATE TABLE IF NOT EXISTS guns(user_id TEXT PRIMARY KEY, name TEXT, pistol_pmm INTEGER DEFAULT 1, pistol_marta INTEGER DEFAULT 0, drobovik_obrez INTEGER DEFAULT 0)")
    db.execute("CREATE TABLE IF NOT EXISTS items(user_id TEXT PREIMARY KEY, name TEXT, med INTEGER DEFAULT 0, grenade INTEGER DEFAULT 0)")
    db.commit()


async def sql_create_profile(user_id, user_name, name):
    '''Установка значений новому пользователю в бд'''
    user = cur.execute("SELECT 1 FROM users WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:

        if user_name is not None:
            cur.execute("INSERT INTO users(user_id, name, credits) VALUES(?, ?, ?)", (user_id, '@' + user_name, 100))
            cur.execute("INSERT INTO guns(user_id, name) VALUES(?, ?)", (user_id, '@' + user_name))
            cur.execute("INSERT INTO items(user_id, name) VALUES(?, ?)", (user_id, '@' + user_name))
            db.commit()
            
        else:
            cur.execute("INSERT INTO users(user_id, name, credits) VALUES(?, ?, ?)", (user_id, name, 100))
            cur.execute("INSERT INTO guns(user_id, name) VALUES(?, ?)", (user_id, name))
            cur.execute("INSERT INTO items(user_id, name) VALUES(?, ?)", (user_id, name))
            db.commit()


async def exemination_username(user_id, user_name, name):
    '''Проверка не изменил ли пользователь @'''
    user = cur.execute(f"SELECT name FROM users WHERE user_id == '{user_id}'").fetchone()
    if user != name:
        if user != user_name:
            cur.execute("UPDATE users SET name ='@{key2}' WHERE user_id == '{key}'".format(key = user_id, key2=user_name))
            cur.execute("UPDATE guns SET name ='@{key2}' WHERE user_id == '{key}'".format(key=user_id, key2=user_name))
            cur.execute("UPDATE items SET name ='@{key2}' WHERE user_id == '{key}'".format(key=user_id, key2=user_name))
            db.commit()

    else:
        if user != name:
            cur.execute("UPDATE users SET name = '{name}' WHERE user_id == '{key}'".format(key=user_id, name=name))
            cur.execute("UPDATE guns SET name = '{name}' WHERE user_id == '{key}'".format(key=user_id, name=name))
            cur.execute("UPDATE items SET name = '{name}' WHERE user_id == '{key}'".format(key=user_id, name=name))
            db.commit()





async def get_credit_balance(user_id):
    '''Вернуть текущий баланс кредитов'''
    return cur.execute("SELECT credits FROM users WHERE user_id =='{key}'".format(key=user_id)).fetchone()[0]

async def minus_credit_balance(user_id, credit):
    '''Отнять кредиты у пользователя'''
    cur.execute("UPDATE users SET credits = credits - '{credits}' WHERE user_id=='{key}'".format(key=user_id, credits=credit))
    db.commit()

async def plus_credit_balance(user_id, credit):
    '''Добавить кредиты пользователю'''
    cur.execute("UPDATE users SET credits = credits + '{credits}' WHERE user_id=='{key}'".format(key=user_id, credits=credit))
    db.commit()

async def have_gun(user_id, gun_name):
    '''Проверка на оружие True\False'''
    return cur.execute("SELECT {key} FROM guns WHERE user_id == '{userkey}'".format(key=gun_name, userkey=user_id)).fetchone()[0]

async def is_admin_function(user_id):
    '''Являеться ли пользователь админом'''
    return cur.execute("SELECT is_admin FROM users WHERE user_id =='{user_id}'".format(user_id=user_id)).fetchone()[0]

async def edit_current_gun(user_id, gun_name):
    '''Изменить текущее оружие'''
    cur.execute("UPDATE users SET current_gun == '{gun_name}' WHERE user_id =='{user_id}'".format(user_id=user_id, gun_name=gun_name))
    db.commit()

async def buy_gun(user_id, gun_name):
    '''Купить оружие'''
    if await have_gun(user_id, gun_name):
        return 2
    else:
        cur.execute(f"UPDATE guns SET {gun_name} = 1 WHERE user_id == {user_id}")
        db.commit()


async def current_gun(user_id):
    '''Вернуть текущее оружие'''
    current_gun_name = cur.execute("SELECT current_gun FROM users WHERE user_id =='{key}'".format(key=user_id)).fetchone()[0]
    if current_gun_name == pistol_pmm['console_name']:
        return pistol_pmm
    elif current_gun_name == pistol_marta['console_name']:
        return pistol_marta
    elif current_gun_name == drobovik_obrez['console_name']:
        return drobovik_obrez

async def current_exp(user_id):
    '''Вернуться текущий опыт'''
    return cur.execute(f"SELECT exp FROM users WHERE user_id == {user_id}").fetchone()[0]

async def plus_exp(user_id, exp):
    '''Получить exp'''
    cur.execute(f"UPDATE users SET exp = exp + {int(exp)} WHERE user_id == {user_id}")
    db.commit

async def current_energy(user_id):
    '''Вернуться текущую енергию'''
    return cur.execute(f"SELECT energy FROM users WHERE user_id == {user_id}").fetchone()[0]

async def minus_energy(user_id, energy):
    '''Убрать енергию'''
    cur.execute(f"UPDATE users SET energy = energy - {int(energy)} WHERE user_id == {user_id}")
    db.commit()

async def get_count_item(user_id, item):
    '''Получить количество item`a'''
    return cur.execute(f"SELECT {item} FROM items WHERE user_id == {user_id}").fetchone()[0]

async def minus_count_item(user_id, item):
    '''Убрать аптечку item`a'''
    cur.execute(f"UPDATE items SET {item} = {item} - 1 WHERE user_id == {user_id}")
    db.commit()
