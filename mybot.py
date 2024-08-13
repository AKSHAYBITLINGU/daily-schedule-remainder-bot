from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN  = os.getenv("BOT_TOKEN")
BOT_USERNAME = os.getenv("BOT_USERNAME")


my_shedule = {
    'monday':[
        {"type":"class","status":"yes","name":'ISL',"timein":'8:00',"timeout":'9:00',"venue":'A18-1A'},
        {"type":"class","status":"yes","name":'MFODS',"timein":'9:00',"timeout":'10:00',"venue":'A18-1A'},
        {"type":"class","status":"yes","name":'OS',"timein":'10:00',"timeout":'11:00',"venue":'A17-1B'},
        {"type":"class","status":"no","name":'',"timein":'11:00',"timeout":'12:00',"venue":''},
        {"type":"class","status":"no","name":'',"timein":'12:00',"timeout":'13:00',"venue":''},
        {"type":"lab","status":"yes","name":'CN',"timein":'14:00',"timeout":'16:00',"venue":'NA'},
    ],
    'tuesday':[
        {"type":"class","status":"yes","name":'CN',"timein":'8:00',"timeout":'9:00',"venue":'A17-1A'},
        {"type":"class","status":"yes","name":'AI',"timein":'9:00',"timeout":'10:00',"venue":'A11-1A'},
        {"type":"class","status":"no","name":'',"timein":'10:00',"timeout":'11:00',"venue":''},
        {"type":"class","status":"yes","name":'ISL',"timein":'11:00',"timeout":'12:00',"venue":'A18-1A'},
        {"type":"class","status":"yes","name":'MFODS',"timein":'12:00',"timeout":'13:00',"venue":'A18-1A'},
        {"type":"lab","status":"no","name":'',"timein":'12:00',"timeout":'13:00',"venue":'A18-1A'},
        {"type":"class","status":"yes","name":'NLP',"timein":'18:30',"timeout":'20:00',"venue":'A18-1A'},
    ],
    'wednesday':[
        {"type":"class","status":"yes","name":'OS',"timein":'8:00',"timeout":'9:00',"venue":'A17-1B'},
        {"type":"class","status":"no","name":'',"timein":'9:00',"timeout":'10:00',"venue":''},
        {"type":"class","status":"no","name":'',"timein":'10:00',"timeout":'11:00',"venue":''},
        {"type":"class","status":"yes","name":'CN',"timein":'11:00',"timeout":'12:00',"venue":'A17-1A'},
        {"type":"class","status":"yes","name":'AI',"timein":'12:00',"timeout":'13:00',"venue":'A11-1A'},
        {"type":"lab","status":"yes","name":'OS',"timein":'14:00',"timeout":'16:00',"venue":'A11-PC-LAB'},
        {"type":"class","status":"yes","name":'NLP',"timein":'18:30',"timeout":'20:00',"venue":'A18-1A'},
    ],
    'thursday':[
        {"type":"class","status":"no","name":'',"timein":'8:00',"timeout":'9:00',"venue":''},
        {"type":"class","status":"yes","name":'ISL',"timein":'9:00',"timeout":'10:00',"venue":'A18-1A'},
        {"type":"class","status":"yes","name":'MFODS',"timein":'10:00',"timeout":'11:00',"venue":'A18-1A'},
        {"type":"class","status":"yes","name":'OS',"timein":'11:00',"timeout":'12:00',"venue":'A17-1B'},
        {"type":"class","status":"no","name":'',"timein":'12:00',"timeout":'13:00',"venue":''},
        {"type":"lab","status":"no","name":'',"timein":'',"timeout":'',"venue":''},
    ],
    'friday':[
        {"type":"class","status":"no","name":'',"timein":'8:00',"timeout":'9:00',"venue":''},
        {"type":"class","status":"yes","name":'CN',"timein":'9:00',"timeout":'10:00',"venue":'A17-1A'},
        {"type":"class","status":"yes","name":'AI',"timein":'10:00',"timeout":'11:00',"venue":'A18-1A'},
        {"type":"class","status":"no","name":'',"timein":'11:00',"timeout":'12:00',"venue":''},
        {"type":"class","status":"yes","name":'ISL',"timein":'12:00',"timeout":'13:00',"venue":'A18-1A'},
        {"type":"lab","status":"yes","name":'NA',"timein":'14:00',"timeout":'16:00',"venue":'NA'},
    ]
}

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# helper functions
def schedule_message(schedule: list) -> str:
    final_msg: str = ""
    final_msg += "Akshay Your Have:\n"
    for i in schedule:
        if i['status'] == 'yes':
            final_msg += f"{i['name']} {i['type']} from {i['timein']} to {i['timeout']} in {i['venue']}\n"
        else:
            if i['type'] == 'class':
                final_msg += f"No {i['type']} from {i['timein']} to {i['timeout']}\n"
            else:
                final_msg += f"No {i['type']} today!\n"
    return final_msg

# Commands
async def start_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey User, How Can I Help You")

async def help_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("this is the help from me!")

async def schedule_command(update : Update, context : ContextTypes.DEFAULT_TYPE):
    today_datetime = datetime.now()
    day = today_datetime.strftime('%A').lower()
    today_schedule = my_shedule[day]
    if day == "saturday" or day == 'sunday':
        await update.message.reply_text("No Class Today:)")
        return
    schedule_msg = schedule_message(today_schedule)
    await update.message.reply_text(schedule_msg)
    
# Handle Responses
async def handle_response(text : str) -> str :
    processed : str = text.lower()

    if "hello" in processed:
        return 'hey there'
    return "i dont understand what you are saying"

# Handle Messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in ({message_type}):"({text})"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = await handle_response(text)

    print("Bot:", response)
    await update.message.reply_text(response)

# errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error: {context.error}')


if __name__ == "__main__":
    print("Starting Bot....")
    app = Application.builder().token(BOT_TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("schedule", schedule_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls on bot
    print("Polling...")
    app.run_polling(poll_interval=1)