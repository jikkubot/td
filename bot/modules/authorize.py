from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands

@run_async
def authorize(update,context):
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    msg = ''
    with open('authorized_chats.txt', 'a') as file:
        if len(message_) == 2:
            chat_id = int(message_[1])
            if chat_id not in AUTHORIZED_CHATS:
                file.write(f'{chat_id}\n')
                AUTHORIZED_CHATS.add(chat_id)
                msg = 'Cʜᴀᴛ Aᴜᴛʜᴏʀɪᴢᴇᴅ!'
            else:
                msg = 'Usᴇʀ Aʟʀᴇᴀᴅʏ Aᴜᴛʜᴏʀɪᴢᴇᴅ!'
        else:
            if reply_message is None:
                # Trying to authorize a chat
                chat_id = update.effective_chat.id
                if chat_id not in AUTHORIZED_CHATS:
                    file.write(f'{chat_id}\n')
                    AUTHORIZED_CHATS.add(chat_id)
                    msg = 'Cʜᴀᴛ Aᴜᴛʜᴏʀɪᴢᴇᴅ!'
                else:
                    msg = 'Aʟʀᴇᴀᴅʏ Aᴜᴛʜᴏʀɪᴢᴇᴅ Cʜᴀᴛ!'
            else:
                # Trying to authorize someone in specific
                user_id = reply_message.from_user.id
                if user_id not in AUTHORIZED_CHATS:
                    file.write(f'{user_id}\n')
                    AUTHORIZED_CHATS.add(user_id)
                    msg = 'Pᴇʀsᴏɴ Aᴜᴛʜᴏʀɪᴢᴇᴅ Tᴏ Usᴇ Tʜᴇ Bᴏᴛ!'
                else:
                    msg = 'Pᴇʀsᴏɴ Aʟʀᴇᴀᴅʏ Aᴜᴛʜᴏʀɪᴢᴇᴅ Tᴏ Usᴇ Tʜᴇ Bᴏᴛ!'
        sendMessage(msg, context.bot, update)


@run_async
def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    message_ = update.message.text.split(' ')
    if len(message_) == 2:
            chat_id = int(message_[1])
            if chat_id in AUTHORIZED_CHATS:
                AUTHORIZED_CHATS.remove(chat_id)
                msg = 'Cʜᴀᴛ UɴAᴜᴛʜᴏʀɪᴢᴇᴅ!'
            else:
                msg = 'Usᴇʀ Aʟʀᴇᴀᴅʏ UɴAᴜᴛʜᴏʀɪᴢᴇᴅ!'
    else:
        if reply_message is None:
            # Trying to unauthorize a chat
            chat_id = update.effective_chat.id
            if chat_id in AUTHORIZED_CHATS:
                AUTHORIZED_CHATS.remove(chat_id)
                msg = 'Cʜᴀᴛ UɴAᴜᴛʜᴏʀɪᴢᴇᴅ!'
            else:
                msg = 'Aʟʀᴇᴀᴅʏ UɴAᴜᴛʜᴏʀɪᴢᴇᴅ Cʜᴀᴛ!'
        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id in AUTHORIZED_CHATS:
                AUTHORIZED_CHATS.remove(user_id)
                msg = 'Pᴇʀsᴏɴ UɴAᴜᴛʜᴏʀɪᴢᴇᴅ Tᴏ Usᴇ Tʜᴇ Bᴏᴛ!'
            else:
                msg = 'Pᴇʀsᴏɴ Aʟʀᴇᴀᴅʏ UɴAᴜᴛʜᴏʀɪᴢᴇᴅ Tᴏ Usᴇ Tʜᴇ Bᴏᴛ!'
    with open('authorized_chats.txt', 'a') as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)


@run_async
def sendAuthChats(update,context):
    users = ''
    for user in AUTHORIZED_CHATS :
        users += f"{user}\n" 
    users = users if users != '' else "None"
    sendMessage(f'Aᴜᴛʜᴏʀɪᴢᴇᴅ Cʜᴀᴛs Aʀᴇ : \n<code>{users}</code>\n', context.bot, update)


send_auth_handler = CommandHandler(command=BotCommands.AuthorizedUsersCommand, callback=sendAuthChats,
                                    filters=CustomFilters.owner_filter)
authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter)

dispatcher.add_handler(send_auth_handler)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)


