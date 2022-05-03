import re
import os
import json
import asyncio
import requests

from plugins.stockmarketindia import *
from bot import Bot
from json import loads
from typing import List
from googlefinance import getQuotes
from script import Script
from pyrogram import filters
from pyrogram import Client as ufs
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


if bool(os.environ.get("WEBHOOK", False)):
    pass
else:
    pass

symbols = "GOOG, AAPL"


@ufs.on_message(filters.private & filters.command(["start"]))
async def start(bot: Bot, message: Message):
    buttons = [
        [
            InlineKeyboardButton('💡 مساعدة', callback_data="help"),
            InlineKeyboardButton('🧾 حول البوت', callback_data="about")],
        [
            InlineKeyboardButton('🚫 اغلاق', callback_data="close_btn")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text=Script.PM_START_TEXT.format(message.from_user.mention),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        reply_to_message_id=message.message_id
    )


@ufs.on_message(filters.private & filters.command(["help"]))
async def help(bot: Bot, message: Message):
    buttons = [
        [
            InlineKeyboardButton('🔙 رجوع', callback_data="help"),
            InlineKeyboardButton('🧾 حول البوت ', callback_data="about")],
        [
            InlineKeyboardButton('🚫 اغلاق', callback_data="close_btn")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text=Script.HELP_STRINGS.format(message.from_user.mention),
        parse_mode="html",
        reply_markup=reply_markup,
        disable_web_page_preview=True)


@ufs.on_message(filters.private & filters.command(["auth"]))
async def auth(bot: Bot, message: Message):
    auth_button = [
        [InlineKeyboardButton("Auth Url", url="https://dashboard.heroku.com/account/applications/authorizations/new")],
        [InlineKeyboardButton("⬅️ رجوع", callback_data="start"),
         InlineKeyboardButton("❌  اغلاق", callback_data="close_btn")]
    ]

    reply_markup = InlineKeyboardMarkup(auth_button)
    await message.reply_text(
        text=Script.AUTH_STRING.format(message.from_user.mention),
        parse_mode="html",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        reply_to_message_id=message.message_id)


def buildUrl(symbols):
    symbol_list = ','.join([symbol for symbol in symbols])
    # a deprecated but still active & correct api
    return 'https://www.google.com/finance/quote/q=' \
        + symbol_list


@ufs.on_message(filters.private & filters.command(["token"]))
async def token(bot: Bot, message: Message):        # , args: List[str]
    args = message.command
    if len(args) >= 1:
        try:
            token = args[1]
        except:
            await message.reply_text("رمز ايبي كي غلط حياتي")
            return
    else:
        await message.reply_text("ايبي كي خلي عدل")
        return

    params = {'q': 'NASDAQ:AAPL', 'output': 'json'}
    response = requests.get('https://finance.google.com/finance', params=params, allow_redirects=False, timeout=10.0)
    print(response.status_code)
    jsonstr = response.text[4:]  # remove first part (not json data)
    data = loads(jsonstr)
    print(data)
    print("t=", data[0]['t'])
    # print(response.content)

    # json_content = get_content(build_url())
    #
    # stock_resp_list = json.loads(json_content)
    #
    # list_stock = list()
    # for stock_resp in stock_resp_list:
    #     isPositive = False if stock_resp["cp"] != None and len(stock_resp["cp"]) > 0 and stock_resp["cp"][
    #         0] == '-' else True
    #
    #     colored_cp = stock_resp["cp"]
    #     if isPositive:
    #         colored_cp = Color.green(stock_resp["cp"])
    #     else:
    #         colored_cp = Color.red(stock_resp["cp"])
    #
    #     list_stock.append(Stock(stock_resp["t"], stock_resp["l"], stock_resp["c"], colored_cp, stock_resp["lt"]))
    # stock_list = list_stock

    # json = getQuotes('AAPL')

    # await message.reply_text(str(json.dumps(getQuotes('AAPL'), indent=2)))
    # await message.reply_text(str(stock_list))

    # content = json.dumps(getQuotes('AAPL'), indent=2)

    # useragent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #              'Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'
    #              )
    #
    # accounts_header = {
    #     "User-Agent": useragent,
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
    #               "application/signed-exchange;v=b3;q=0.9",
    # }
    #
    # # account_path = "https://api.heroku.com/account"
    # content = requests.get(path, headers=accounts_header)
    # if content.status_code != 200:
    #     return await message.edit_text(
    #         text=f"Your heroku token was expired or heroku account was deleted please use /auth and login again")

    content = requests.get("https://finance.google.com/finance?q=AAPL&output=json")
    fin_data = json.loads(content.content[6:-2].decode('unicode_escape'))

    # print out some quote data
    print('Opening Price: {}'.format(fin_data['op']))
    print('Price/Earnings Ratio: {}'.format(fin_data['pe']))
    print('52-week high: {}'.format(fin_data['hi52']))
    print('52-week low: {}'.format(fin_data['lo52']))
    # await message.reply_text(str(content.json()['Index']))
    # h_name = content.json()['name']

    # msg = await message.reply_text("Checking Your Token With Heroku")
    # await asyncio.sleep(1)
    # msg = await msg.edit_text("Checking Your Token With Heroku ▫")
    # await asyncio.sleep(1)
    # msg = await msg.edit_text("Checking Your Token With Heroku ▫▫")
    # await asyncio.sleep(1)
    # msg = await msg.edit_text("Checking Your Token With Heroku ▫▫▫")
    # await asyncio.sleep(1)
    # msg = await msg.edit_text("Checking Your Token With Heroku ▫▫▫▫")
    # await asyncio.sleep(1)
    # msg = await msg.edit_text("Checking Your Token With Heroku ▫▫▫▫▫")
    # await asyncio.sleep(1)
    # await msg.delete()


# ------------------------------------ All-n-One Input fn --------------------------------- #
@ufs.on_message(filters.private & filters.text & filters.reply)
async def force_reply_msg(bot, message: Message):
    print("Hi")
