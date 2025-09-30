import telebot
from telebot import types

bot_token = '8316791092:AAHde0I_yk40PHY4ded3I3ceZ0ExWEzf7C4'
bot = telebot.TeleBot(bot_token)

channels = {}

user_data = {}

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    add_channel_button = types.InlineKeyboardButton("📺 اضف قناة", callback_data="add_channel")
    publish_button = types.InlineKeyboardButton("📝 نشر منشور جديد", callback_data="publish_message")
    new_button = types.InlineKeyboardButton("🧘🏻نشر محفوظ", callback_data="new_button")
    markup.add(add_channel_button, publish_button)
    markup.add(new_button)
    bot.send_message(chat_id, "- مرحبًا بك عزيزي في بوت ادارة محتوى القناة \n- يمكنك من خلال البوت نشر رسائل تضهر مع زر شفاف في قناتك من خلال الأزرار أدناه .", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {'channel_id': None, 'button_name': None, 'button_content': None}
    show_main_menu(chat_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id

    if call.data == "add_channel":
        msg = bot.send_message(chat_id, "- أرسل يوزر القناة مثال : @x_596 .")
        bot.register_next_step_handler(msg, save_channel)

    elif call.data == "publish_message":
        if user_data[chat_id]['channel_id']:
            msg = bot.send_message(chat_id, "- أرسل محتوى الرسالة :")
            bot.register_next_step_handler(msg, get_message_content)
        else:
            bot.send_message(chat_id, "- بعدك مضايف قناة حتى انشرلك بيها  .")

    elif call.data == "new_button":
        if user_data[chat_id]['button_name'] and user_data[chat_id]['button_content']:
            msg = bot.send_message(chat_id, "- أرسل محتوى الرسالة :")
            bot.register_next_step_handler(msg, get_only_message_content)
        else:
            msg = bot.send_message(chat_id, "- أرسل محتوى الرسالة :")
            bot.register_next_step_handler(msg, get_new_message_content)

def save_channel(message):
    chat_id = message.chat.id
    channel_id = message.text

    if channel_id.startswith("@"):
        try:
           
            chat_info = bot.get_chat(channel_id)
            channel_id = str(chat_info.id)
            user_data[chat_id]['channel_id'] = channel_id
            bot.send_message(chat_id, f"- تم حفظت القتاة تكدر تبلش بلنشر حبيبي  .")
        except Exception as e:
            bot.send_message(chat_id, "- اليوزر غلط على ما اعتقد حاول تتأكد من عنده  .")
            print(e)
    elif channel_id.startswith("-100"):
        user_data[chat_id]['channel_id'] = channel_id
        bot.send_message(chat_id, f"- تم حفظ القناة بنجاح .")
    else:
        bot.send_message(chat_id, "- اليوزر غلط على ما اعتقد تأكد من يوزر القناة .")

def get_new_message_content(message):
    chat_id = message.chat.id
    message_content = message.text
    msg = bot.send_message(chat_id, "- شتريد اسم الزر؟ :")
    bot.register_next_step_handler(msg, get_new_button_name, message_content)

def get_new_button_name(message, message_content):
    chat_id = message.chat.id
    button_name = message.text
    msg = bot.send_message(chat_id, "- ارسل الرابط الي تريد تخليه للزر")
    bot.register_next_step_handler(msg, get_new_button_content, message_content, button_name)

def get_new_button_content(message, message_content, button_name):
    chat_id = message.chat.id
    button_content = message.text

    if not (button_content.startswith("http://") or button_content.startswith("https://")):
        bot.send_message(chat_id, "- حبيبي لازم.ترسل رابط فقط .")
        return

    if user_data[chat_id]['channel_id']:
        channel_id = user_data[chat_id]['channel_id']
        user_data[chat_id]['button_name'] = button_name
        user_data[chat_id]['button_content'] = button_content
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(button_name, url=button_content)
        markup.add(button)
        bot.send_message(channel_id, message_content, reply_markup=markup)
        bot.send_message(chat_id, "-تم عزيزي نشرته الك بلقتاة تكدر تروح وتتأكد .")
    else:
        bot.send_message(chat_id, "- ما ضايف قناة ضيف قناة وبعدها تكدر تنشر  .")
        
def get_only_message_content(message):
    chat_id = message.chat.id
    message_content = message.text

    if user_data[chat_id]['channel_id'] and user_data[chat_id]['button_name'] and user_data[chat_id]['button_content']:
        channel_id = user_data[chat_id]['channel_id']
        button_name = user_data[chat_id]['button_name']
        button_content = user_data[chat_id]['button_content']
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(button_name, url=button_content)
        markup.add(button)
        bot.send_message(channel_id, message_content, reply_markup=markup)
        bot.send_message(chat_id, "-تم عزيزي نشرته الك بلقناة تكدر تروح وتتأكد .")
    else:
        bot.send_message(chat_id, "- بعدك مضايف قناة،  او يمكن غلط منك مضايف محتوى للزر الي قبله ! .")

def get_message_content(message):
    chat_id = message.chat.id
    message_content = message.text
    msg = bot.send_message(chat_id, "- أشتريد أسم الزر؟  :")
    bot.register_next_step_handler(msg, get_button_name, message_content)


def get_button_name(message, message_content):
    chat_id = message.chat.id
    button_name = message.text
    msg = bot.send_message(chat_id, "- ارسل الرابط الي يصير بـ الزر:")
    bot.register_next_step_handler(msg, get_button_content, message_content, button_name)


def get_button_content(message, message_content, button_name):
    chat_id = message.chat.id
    button_content = message.text

    if not (button_content.startswith("http://") or button_content.startswith("https://")):
        bot.send_message(chat_id, "- ميصير ترسل هيج، تكدر ترسل رابط فقط .")
        return

    if user_data[chat_id]['channel_id']:
        channel_id = user_data[chat_id]['channel_id']
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(button_name, url=button_content)
        markup.add(button)
        bot.send_message(channel_id, message_content, reply_markup=markup)
        bot.send_message(chat_id, "- تم يروحي نشرت المنشور .")
    else:
        bot.send_message(chat_id, "- بعدك ماضايف اي قناة.  ")


bot.infinity_polling()
