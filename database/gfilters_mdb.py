import pymongo
from info import DATABASE_URI, DATABASE_NAME
from pyrogram import enums
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]



async def add_gfilter(gfilters, text, reply_text, btn, file, alert):
    mycol = mydb[str(gfilters)]
    # mycol.create_index([('text', 'text')])

    data = {
        'text':str(text),
        'reply':str(reply_text),
        'btn':str(btn),
        'file':str(file),
        'alert':str(alert)
    }

    try:
        mycol.update_one({'text': str(text)},  {"$set": data}, upsert=True)
    except:
        logger.exception('Some error occured!', exc_info=True)
             
     
async def find_gfilter(gfilters, name):
    mycol = mydb[str(gfilters)]
    
    query = mycol.find( {"text":name})
    # query = mycol.find( { "$text": {"$search": name}})
    try:
        for file in query:
            reply_text = file['reply']
            btn = file['btn']
            fileid = file['file']
            try:
                alert = file['alert']
            except:
                alert = None
        return reply_text, btn, alert, fileid
    except:
        return None, None, None, None


async def get_gfilters(gfilters):
    mycol = mydb[str(gfilters)]

    texts = []
    query = mycol.find()
    try:
        for file in query:
            text = file['text']
            texts.append(text)
    except:
        pass
    return texts


async def delete_gfilter(message, text, gfilters):
    mycol = mydb[str(gfilters)]
    
    myquery = {'text':text }
    query = mycol.count_documents(myquery)
    if query == 1:
        mycol.delete_one(myquery)
        await message.reply_text(
            f"'`{text}`'  𝖣𝖾𝗅𝖾𝗍𝖾𝖽. 𝖨'𝗅𝗅 𝗇𝗈𝗍 𝗋𝖾𝗌𝗉𝗈𝗇𝖽 𝗍𝗈 𝗍𝗁𝖺𝗍 𝗀𝖿𝗂𝗅𝗍𝖾𝗋 𝖺𝗇𝗒𝗆𝗈𝗋𝖾.",
            quote=True,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    else:
        await message.reply_text("𝖢𝗈𝗎𝗅𝖽𝗇'𝗍 𝖿𝗂𝗇𝖽 𝗍𝗁𝖺𝗍 𝗀𝖿𝗂𝗅𝗍𝖾𝗋!", quote=True)

async def del_allg(message, gfilters):
    if str(gfilters) not in mydb.list_collection_names():
        await message.edit_text("𝖭𝗈𝗍𝗁𝗂𝗇𝗀 𝗍𝗈 𝖱𝖾𝗆𝗈𝗏𝖾!")
        return

    mycol = mydb[str(gfilters)]
    try:
        mycol.drop()
        await message.edit_text(f"𝖠𝗅𝗅 𝗀𝖿𝗂𝗅𝗍𝖾𝗋𝗌 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝗋𝖾𝗆𝗈𝗏𝖾𝖽!")
    except:
        await message.edit_text("𝖢𝗈𝗎𝗅𝖽𝗇'𝗍 𝗋𝖾𝗆𝗈𝗏𝖾 𝖺𝗅𝗅 𝗀𝖿𝗂𝗅𝗍𝖾𝗋𝗌!")
        return

async def count_gfilters(gfilters):
    mycol = mydb[str(gfilters)]

    count = mycol.count()
    return False if count == 0 else count


async def gfilter_stats():
    collections = mydb.list_collection_names()

    if "CONNECTION" in collections:
        collections.remove("CONNECTION")

    totalcount = 0
    for collection in collections:
        mycol = mydb[collection]
        count = mycol.count()
        totalcount += count

    totalcollections = len(collections)

    return totalcollections, totalcount
