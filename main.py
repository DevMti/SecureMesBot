# Imports for source
import logging
import random
import mysql.connector
import string
import random


# Imports from aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


# Bot token
API_TOKEN = 'bottoken'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher and dp
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Db information
mydb = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)
mycur = mydb.cursor()

# Sendmessage state
class SendanonymousMessage(StatesGroup):
    target = State()
    anonymousMessage = State()

# Creat random link
def getLink():
    # Creation lines
    source = string.ascii_letters + string.digits
    link = ''.join((random.choice(source) for i in range(5))) + '-' + ''.join((random.choice(source) for i in range(5)))
        
    # Check link is in db or not(use link)
    mycur.execute("SELECT x FROM y WHERE z")
    myresult = mycur.fetchall()
    if not myresult:
        return link
    else:
        # Try again
        return getLink()

# Send anonymous message
@dp.message_handler(regexp='/start secure-')
async def StartSending(message: types.Message, state: FSMContext):

    # Chat reaction
    await message.answer_chat_action(action='typing')

    # Get chat member ship
    joined = await bot.get_chat_member(chat_id="@OnTopTm",user_id=message.from_user.id)

    # Get raw link
    link = message.text.replace('/start secure-','')

    # If user joined channel or not
    if joined['status'] != 'left':
        # Check user is in db ot not(add user to db)
        mycur.execute("SELECT * FROM Users WHERE bot_id='5458175742' AND id='%s'" %link)
        myresult = mycur.fetchall()
        
        # If's for sending message
        if not myresult:
            # If link is not true
            await message.answer("🚫 لینک اشتباهه\n\nبه منوی اصلی برگشتی")
        elif myresult[0][1] == 0:
            # If user changed the link
            await message.answer("🚫 کاربری که سعی داری بهش پیام ارسال کنی لینکشو عوض کرده\n\nشروع مجدد👈 /start")
        elif myresult[0][1] == message.from_user.id:
            # If user is trying to send fake message
            await message.answer("🚫 نمیتونی به خودت پیام ارسال کنی\n\nشروع مجدد👈 /start")
        else:
            # Set state
            await SendanonymousMessage.target.set()
            await SendanonymousMessage.next()
            await state.update_data(target=int(myresult[0][1]))

            # back keyboard and awnser user
            keyboard_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
            keyboard_markup.add(types.KeyboardButton("🔙 Back"))
            await message.answer(
                "💬 پیام خودتون رو ارسال کنید\n\nهویت شما و دریافت کننده توسط ربات به هیچ عنوان فاش نخواهد شد. برای لغو👈 /cancel",
                reply_markup=keyboard_markup
            )
    else:
        # Ask user to join into channel
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
        keyboard_markup.add(types.InlineKeyboardButton("عضو شدم ✅",url='t.me/SecureMesBot?start=secure-' + link))
        await message.answer('💬 ابتدا در چنل ما عضو شید و بعد دوباره با لینک زیر تلاش کنید\n\n🌐 @OnTopTm 🌐 @OnTopTm 🌐 @OnTopTm\n🌐 @OnTopTm 🌐 @OnTopTm 🌐 @OnTopTm \n🌐 @OnTopTm 🌐 @OnTopTm 🌐 @OnTopTm\n\nلینک ادامه به ارسال پیام👇',reply_markup=keyboard_markup)

    # Check user is in db ot not(add user to db)
    mycur.execute("SELECT x FROM y WHERE z")
    myresult = mycur.fetchall()
    if not myresult:
        mycur.execute("INSERT INTO x (a, b, c) VALUES ('%s', 'b', '%d')" %(getLink(),message.from_user.id))
        mydb.commit()


# Start and help section
@dp.message_handler(commands=['start','help'])
async def send_welcome(message: types.Message):

    # Chat reaction
    await message.answer_chat_action(action='typing')

    # Check membership
    joined = await bot.get_chat_member(chat_id="@OnTopTm",user_id=message.from_user.id)

    # Main menu keyboard
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    keyboard_markup.add(types.KeyboardButton("🔗 لینک من"))

    # if user joined channel or not
    if joined['status'] != 'left':
        await message.answer(
            text='💬 به علت اتفاقات اخیر در کشور عزیزمون متوجه امنیت کم برخی از ربات های ناشناس شدیم\nبه همین خاطر این ربات طراحی شد تا پیام رو از فرستنده به گیرنده بدون هرگونه شنود و وقفه ارسال کنه\nبرای جلب اعتماد شما سورس ربات اوپن شده تا در صورت وجود هرگونه شک به ربات میتونید به شخصه کد هارو مشاهده و برسی کنید.\n\n🌐 @OnTopTM \n🔗 GitHub: LINK',
            reply_markup=keyboard_markup
        )
    else:
        # Ask user to join channel
        await message.answer('💬 ابتدا در چنل ما عضو شید و بعد دوباره با لینک زیر تلاش کنید\n\n🌐 @OnTopTm 🌐 @OnTopTm 🌐 @OnTopTm\n🌐 @OnTopTm 🌐 @OnTopTm 🌐 @OnTopTm \n🌐 @OnTopTm 🌐 @OnTopTm 🌐 @OnTopTm\n\nشروع مجدد👈 /start')

    # Check user is in db or not(add user to db)
    mycur.execute("SELECT x FROM y WHERE z")
    myresult = mycur.fetchall()
    if not myresult:
        mycur.execute("INSERT INTO x (a, b, c) VALUES ('%s', 'b', '%d')" %(getLink(),message.from_user.id))
        mydb.commit()


# Get link
@dp.message_handler(text=['🔗 لینک من'])
async def create_test(message: types.Message):

    # Chat reaction
    await message.answer_chat_action(action='typing')

    # Get link
    mycur.execute("SELECT x FROM z WHERE y")
    myresult = mycur.fetchall()
    
    # Awnser user with link
    await message.answer(f"میتونی هروقت که احساس نا امنی از طرف ارسال کننده های ناشناس کردی لینک خودتو با دستور /change عوض کنی!\n\n💬 لینک فعلی شما:\nt.me/SecureMesBot?start=secure-{myresult[0][0]}")


# Change link
@dp.message_handler(commands='change')
async def change_link(message: types.Message):

    # Chat reaction
    await message.answer_chat_action(action='typing')

    # Update last link
    mycur.execute("UPDATE x SET z WHERE y")
    mydb.commit()

    # Creat New Link
    mycur.execute("INSERT INTO x (a, b, c) VALUES ('%s', 'b', '%d')" %(getLink(),message.from_user.id))
    mydb.commit()

    # Awnser user with link
    mycur.execute("SELECT z FROM x WHERE y")
    myresult = mycur.fetchall()
    await message.answer(f"💬 لینک جدید شما:\nt.me/SecureMesBot?start=secure-{myresult[0][0]}")


# Allow user to cancel any action
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='🔙 Back', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    
    # Chat reaction
    await message.answer_chat_action(action='typing')

    current_state = await state.get_state()
    if current_state is None:
        return

    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('💬 لغو شد.\n\nشروع مجدد👈 /start', reply_markup=types.ReplyKeyboardRemove())


# Check name. name gotta be text
@dp.message_handler(lambda message: message.text, state=SendanonymousMessage.anonymousMessage)
async def process_emoji_invalid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Send message
        await message.answer("💬 پیام شما ارسال شد\n\nشروع مجدد👈 /start",reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(data['target'],'      ‌   ‌     \n' + message.text)

    # Finish conversation
    await state.finish()


# Check name. name gotta be text
@dp.message_handler(content_types=types.ContentType.ANY, state=SendanonymousMessage.anonymousMessage)
async def process_emoji_invalid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # Send message
        await message.answer("💬 پیام شما ارسال شد\n\nشروع مجدد👈 /start",reply_markup=types.ReplyKeyboardRemove())
        await message.copy_to(data['target'])

    # Finish conversation
    await state.finish()


# Start Bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
