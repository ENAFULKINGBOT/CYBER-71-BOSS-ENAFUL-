from pyrogram import Client, filters
from PIL import Image
from PIL.ExifTags import TAGS
import os

API_ID = 39534141  
API_HASH = "699bb01ac7873fabc7212db10dc9ffdc"

BOT_TOKEN = "8791984040:AAEVM_nSXiLgEWbqBjYhDaCXbsGeoFfNA3Q"

app = Client("king_metadata_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_name = message.from_user.first_name
    await message.reply_text(
        f"👋 স্বাগতম {user_name}!\n\n"
        "আমি একটি প্রফেশনাল ফটো মেটাডেটা বট। যেকোনো ছবি পাঠান সেটির গোপন তথ্য দেখতে।\n\n"
        "👑 **Powered By:** @KING_OF_ENAFUL"
    )

@app.on_message(filters.photo)
async def get_photo_info(client, message):
    status_msg = await message.reply_text("🔍 আপনার ছবি বিশ্লেষণ করা হচ্ছে...")
    
    file_path = await message.download()
    
    try:
        img = Image.open(file_path)
        exif_data = {}
        info = img._getexif()
        
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value

        width, height = img.size
        file_size = round(os.path.getsize(file_path) / 1024, 2)

        response = (
            "📸 **PHOTO METADATA ANALYSIS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **ইউজার:** {message.from_user.first_name}\n"
            "👑 **App Made By:** @KING_OF_ENAFUL\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📁 **File:** `{os.path.basename(file_path)}`\n"
            f"⚖️ **Size:** {file_size} KB\n"
            f"📐 **Resolution:** {width}x{height}\n\n"
            "🔹 **DEVICE DETAILS:**\n"
            f"📱 **Brand:** {exif_data.get('Make', 'Unknown')}\n"
            f"📸 **Model:** {exif_data.get('Model', 'Unknown')}\n"
            f"📅 **Captured:** {exif_data.get('DateTime', 'Unknown')}\n"
            "━━━━━━━━━━━━━━━━━━━━"
        )
        
        await status_msg.edit_text(response)
    
    except Exception as e:
        await status_msg.edit_text("❌ দুঃখিত, এই ছবির মেটাডেটা পাওয়া যায়নি।")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

print("বটটি এখন লাইভ আছে... @KING_OF_ENAFUL")
app.run()

