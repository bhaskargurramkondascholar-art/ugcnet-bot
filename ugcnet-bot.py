from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import openai, os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

def handle_message(update, context):
    user_text = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert UGC NET teacher. Give clear, syllabus-aligned answers. Use headings and bullet points. Include 1–2 MCQs when helpful."},
            {"role": "user", "content": user_text}
        ]
    )
    ai_text = response.choices[0].message["content"]
    update.message.reply_text(ai_text)

def quiz(update, context):
    topic = " ".join(context.args) if context.args else "General Paper 1"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert UGC NET teacher."},
            {"role": "user", "content": f"Create 5 MCQs (A–D) for {topic}. After the 5 questions, give the answer key like: 1-C, 2-A... Keep options short."}
        ]
    )
    update.message.reply_text(response.choices[0].message["content"])

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CommandHandler("quiz", quiz))
    print("🤖 Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not OPENAI_KEY:
        raise RuntimeError("Missing TELEGRAM_TOKEN or OPENAI_API_KEY env vars.")
    main()
