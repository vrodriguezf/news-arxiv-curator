File: ../news-arxiv-curator/bot/handlers.py
from telegram import Update, ForceReply
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters
from database.db import add_keyword_user, remove_keyword_user, get_keywords_user, edit_keyword_user
from parsing.parser import parse_newsletter, filter_articles
import logging

async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}!\n'
        'I can help you filter arXiv newsletters based on your keywords.\n'
        'Use /add_keyword [keyword] to add a keyword.\n'
        'Use /remove_keyword [keyword] to remove a keyword.\n'
        'Use /list_keywords to list your keywords.\n'
        'Use /filter_newsletter to filter a newsletter text you send.',
        reply_markup=ForceReply(selective=True),
    )

async def add_keyword(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /add_keyword [keyword]')
        return
    keyword = context.args[0]
    add_keyword_user(user_id, keyword)
    await update.message.reply_text(f'Keyword "{keyword}" added.')

async def remove_keyword(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if len(context.args) != 1:
        await update.message.reply_text('Usage: /remove_keyword [keyword]')
        return
    keyword = context.args[0]
    remove_keyword_user(user_id, keyword)
    await update.message.reply_text(f'Keyword "{keyword}" removed.')

async def list_keywords(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    keywords = get_keywords_user(user_id)
    if keywords:
        keywords_list = '\n'.join(keywords)
        await update.message.reply_text(f'Your keywords:\n{keywords_list}')
    else:
        await update.message.reply_text('You have no keywords. Use /add_keyword to add some.')

async def filter_newsletter(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    keywords = get_keywords_user(user_id)
    if not keywords:
        await update.message.reply_text('You have no keywords. Use /add_keyword to add some.')
        return
    newsletter_text = update.message.text.replace('/filter_newsletter', '', 1).strip()
    if not newsletter_text:
        await update.message.reply_text('Please send the newsletter text after the command.')
        return
    articles = parse_newsletter(newsletter_text)
    filtered = filter_articles(articles, keywords)
    if filtered:
        response = 'Filtered Articles:\n\n'
        for article in filtered:
            response += f"Title: {article['title']}\nLink: {article['link']}\n\n"
    else:
        response = 'No articles match your keywords.'
    await update.message.reply_text(response)

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add_keyword", add_keyword))
    application.add_handler(CommandHandler("remove_keyword", remove_keyword))
    application.add_handler(CommandHandler("list_keywords", list_keywords))
    application.add_handler(CommandHandler("filter_newsletter", filter_newsletter))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_newsletter))