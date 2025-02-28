import os
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from info import IMDB_TEMPLATE
from utils import extract_user, get_file_id, get_poster, last_online
import time
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ 𝖥𝗂𝗋𝗌𝗍 𝖭𝖺𝗆𝖾:</b> {first}\n<b>➲ 𝖫𝖺𝗌𝗍 𝖭𝖺𝗆𝖾:</b> {last}\n<b>➲ 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾:</b> {username}\n<b>➲ 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖨𝖣:</b> <code>{user_id}</code>\n<b>➲ 𝖣𝖺𝗍𝖺 𝖢𝖾𝗇𝗍𝗋𝖾:</b> <code>{dc_id}</code>",
            quote=True
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        _id = ""
        _id += (
            "<b>➲ 𝖢𝗁𝖺𝗍 𝖨𝖣</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>➲ 𝖴𝗌𝖾𝗋 𝖨𝖣</b>: "
                f"<code>{message.from_user.id if message.from_user else '𝖠𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌'}</code>\n"
                "<b>➲ 𝖱𝖾𝗉𝗅𝗂𝖾𝖽 𝖴𝗌𝖾𝗋 𝖨𝖣</b>: "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else '𝖠𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➲ 𝖴𝗌𝖾𝗋 𝖨𝖣</b>: "
                f"<code>{message.from_user.id if message.from_user else '𝖠𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(
            _id,
            quote=True
        )

@Client.on_message(filters.command(["info"]))
async def who_is(client, message):
    # https://github.com/SpEcHiDe/PyroGramBot/blob/master/pyrobot/plugins/admemes/whois.py#L19
    status_message = await message.reply_text(
        "`𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝗎𝗌𝖾𝗋 𝗂𝗇𝖿𝗈...`"
    )
    await status_message.edit(
        "`𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀 𝗎𝗌𝖾𝗋 𝗂𝗇𝖿𝗈...`"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("𝗇𝗈 𝗏𝖺𝗅𝗂𝖽 𝗎𝗌𝖾𝗋 𝗂𝖽 / 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗌𝗉𝖾𝖼𝗂𝖿𝗂𝖾𝖽")
    message_out_str = ""
    message_out_str += f"<b>➲𝖥𝗂𝗋𝗌𝗍 𝖭𝖺𝗆𝖾:</b> {from_user.first_name}\n"
    last_name = from_user.last_name or "<b>None</b>"
    message_out_str += f"<b>➲𝖫𝖺𝗌𝗍 𝖭𝖺𝗆𝖾:</b> {last_name}\n"
    message_out_str += f"<b>➲𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝖨𝖣:</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>None</b>"
    dc_id = from_user.dc_id or "[𝖴𝗌𝖾𝗋 𝖣𝗈𝖾𝗌𝗇'𝗍 𝖧𝖺𝗏𝖾 𝖺 𝖵𝖺𝗅𝗂𝖽 𝖣𝖯]"
    message_out_str += f"<b>➲𝖣𝖺𝗍𝖺 𝖢𝖾𝗇𝗍𝗋𝖾:</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➲𝖴𝗌𝖾𝗋 𝖭𝖺𝗆𝖾:</b> @{username}\n"
    message_out_str += f"<b>➲𝖴𝗌𝖾𝗋 𝖫𝗂𝗇𝗄:</b> <a href='tg://user?id={from_user.id}'><b>𝖢𝗅𝗂𝖼𝗄 𝖧𝖾𝗋𝖾</b></a>\n"
    if message.chat.type in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = (
                chat_member_p.joined_date or datetime.now()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>➲𝖩𝗈𝗂𝗇𝖾𝖽 𝗍𝗁𝗂𝗌 𝖢𝗁𝖺𝗍 𝗈𝗇:</b> <code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        buttons = [[
            InlineKeyboardButton('🔐 𝗖𝗹𝗼𝘀𝗲', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            reply_markup=reply_markup,
            caption=message_out_str,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        buttons = [[
            InlineKeyboardButton('🔐 𝗖𝗹𝗼𝘀𝗲', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            quote=True,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
    await status_message.delete()

@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 𝖨𝖬𝖣𝖡')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("𝖭𝗈 𝗋𝖾𝗌𝗎𝗅𝗍𝗌 𝖿𝗈𝗎𝗇𝖽")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('𝖧𝖾𝗋𝖾 𝗂𝗌 𝗐𝗁𝖺𝗍 𝗂𝗌 𝖿𝗈𝗎𝗇𝖽 𝗈𝗇 𝖨𝖬𝖣𝖡', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗆𝗈𝗏𝗂𝖾 / 𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, quer_y: CallbackQuery):
    i, movie = quer_y.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')}",
                    url=imdb['url'],
                )
            ]
        ]
    message = quer_y.message.reply_to_message or quer_y.message
    if imdb:
        caption = IMDB_TEMPLATE.format(
            query = imdb['title'],
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        caption = "𝖭𝗈 𝖱𝖾𝗌𝗎𝗅𝗍𝗌"
    if imdb.get('poster'):
        try:
            await quer_y.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await quer_y.message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await quer_y.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await quer_y.message.delete()
    else:
        await quer_y.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
    await quer_y.answer()
        

        
