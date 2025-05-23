import logging
import math  # добавьте этот импорт

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Определяем состояния диалога
NAIMENOVANIE, VLJANIYE, KOLVO_PROEZDOV = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу выполнить расчет.\n"
                                    "Введи ник:")
    return NAIMENOVANIE

async def get_naimenovanie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['naimenovanie'] = update.message.text
    await update.message.reply_text("Введи влияние:")
    return VLJANIYE

async def get_vliyanie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        vliyanie = float(update.message.text)
        context.user_data['vliyanie'] = vliyanie
        await update.message.reply_text("Введи количество откатов:")
        return KOLVO_PROEZDOV
    except ValueError:
        await update.message.reply_text("Введи количество влияния.")
        return VLJANIYE

async def get_kolvo_proezdov(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        kolvo = int(update.message.text)
        if kolvo == 0:
            await update.message.reply_text("Количество откатов не может быть нулём. Попробуй снова (/start).")
            return KOLVO_PROEZDOV
        context.user_data['kolvo_proezdov'] = kolvo

        # Выполняем расчет по логике
        vliyanie = context.user_data['vliyanie']
        rezultat = vliyanie / kolvo

        if vliyanie < 100:
            result_text = "Неоткат."
        else:
            vliyanie_minus_110 = vliyanie - 110
            answer = vliyanie_minus_110 / rezultat
            answer_ceil = math.ceil(answer)
            result_text = f"Перекат на: {answer_ceil} раза."

        #Отправляем результат пользователю
        await update.message.reply_text(result_text)
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("Введите число для количества откатов.")
        return KOLVO_PROEZDOV

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Диалог отменен.')
    return ConversationHandler.END

def main():
    #Токен бота
    application = ApplicationBuilder().token('ваш ключ').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAIMENOVANIE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_naimenovanie)],
            VLJANIYE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_vliyanie)],
            KOLVO_PROEZDOV: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_kolvo_proezdov)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    print("А я в жопу кончил.")
    application.run_polling()

if __name__ == '__main__':
    main()
