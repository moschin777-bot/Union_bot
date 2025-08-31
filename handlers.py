from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import main_kb,unions_kb
from config import CHANNELS,ADMIN_ID
import sqlite3,os
from datetime import datetime

router=Router()

class LeadForm(StatesGroup):
    title=State();desc=State();price=State();region=State();contact=State()

def init_db():
    conn=sqlite3.connect('users.db');cur=conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,tg_id INTEGER,unions TEXT,contact TEXT,regdate TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS leads(id INTEGER PRIMARY KEY,user_id INTEGER,title TEXT,desc TEXT,price TEXT,region TEXT,contact TEXT,created TEXT)')
    conn.commit();conn.close()
init_db()

def add_user(tg_id:int):
    conn=sqlite3.connect('users.db');cur=conn.cursor();cur.execute('SELECT id FROM users WHERE tg_id=?',(tg_id,))
    if not cur.fetchone():cur.execute('INSERT INTO users(tg_id,unions,contact,regdate) VALUES(?,?,?,?)',(tg_id,'','',datetime.now().isoformat()));conn.commit();conn.close()

@router.message(F.text.in_({'/start'}))
async def start_cmd(m:Message):
    add_user(m.from_user.id)
    await m.answer('Добро пожаловать в СОЮЗ!',reply_markup=main_kb())

@router.message(F.text=='👤 Личный кабинет')
async def cabinet(m:Message):
    add_user(m.from_user.id)
    conn=sqlite3.connect('users.db');cur=conn.cursor();cur.execute('SELECT unions,contact,regdate FROM users WHERE tg_id=?',(m.from_user.id,));u=cur.fetchone();conn.close()
    unions=u[0] if u and u[0] else 'нет';contact=u[1] if u and u[1] else '-';reg=u[2] if u and u[2] else '-'
    text=f'📌 Личный кабинет\nКонтакты: {contact}\nСОЮЗы: {unions}\nРегистрация: {reg}'
    await m.answer(text,reply_markup=unions_kb())

@router.callback_query(F.data.startswith('union:'))
async def union_toggle(cq:CallbackQuery):
    code=cq.data.split(':')[1]
    conn=sqlite3.connect('users.db');cur=conn.cursor();cur.execute('SELECT unions FROM users WHERE tg_id=?',(cq.from_user.id,));row=cur.fetchone();unions=row[0].split(',') if row and row[0] else []
    if code in unions:unions.remove(code);action='❌ Вышли из СОЮЗа'
    else:unions.append(code);action='✅ Вступили в СОЮЗ'
    cur.execute('UPDATE users SET unions=? WHERE tg_id=?',(','.join(unions),cq.from_user.id));conn.commit();conn.close()
    await cq.message.edit_text(action+f' ({code})')

@router.message(F.text=='➕ Заявка')
async def new_lead(m:Message,state:FSMContext):
    await state.set_state(LeadForm.title);await m.answer('Введите название заявки:')

@router.message(LeadForm.title)
async def lf_title(m:Message,state:FSMContext):
    await state.update_data(title=m.text);await state.set_state(LeadForm.desc);await m.answer('Описание:')

@router.message(LeadForm.desc)
async def lf_desc(m:Message,state:FSMContext):
    await state.update_data(desc=m.text);await state.set_state(LeadForm.price);await m.answer('Цена/условия:')

@router.message(LeadForm.price)
async def lf_price(m:Message,state:FSMContext):
    await state.update_data(price=m.text);await state.set_state(LeadForm.region);await m.answer('Регион:')

@router.message(LeadForm.region)
async def lf_region(m:Message,state:FSMContext):
    await state.update_data(region=m.text);await state.set_state(LeadForm.contact);await m.answer('Контакт:')

@router.message(LeadForm.contact)
async def lf_contact(m:Message,state:FSMContext):
    data=await state.get_data();data['contact']=m.text
    conn=sqlite3.connect('users.db');cur=conn.cursor();cur.execute('SELECT id FROM users WHERE tg_id=?',(m.from_user.id,));u=cur.fetchone();uid=u[0]
    cur.execute('INSERT INTO leads(user_id,title,desc,price,region,contact,created) VALUES(?,?,?,?,?,?,?)',(uid,data['title'],data['desc'],data['price'],data['region'],data['contact'],datetime.now().isoformat()))
    conn.commit();conn.close();await m.answer('✅ Заявка сохранена.');await state.clear()

@router.message(F.text=='/admin')
async def admin(m:Message):
    if ADMIN_ID and m.from_user.id==ADMIN_ID:
        conn=sqlite3.connect('users.db');cur=conn.cursor();cur.execute('SELECT COUNT(*) FROM leads');cnt=cur.fetchone()[0];await m.answer(f'Всего заявок: {cnt}');conn.close()
    else:await m.answer('Недоступно.')
