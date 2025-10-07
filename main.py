import discord
import requests

# ===== TOKENS =====
DISCORD_TOKEN = "MTQyNTA4ODA2ODUyMzY1NTI3OA.G3FDyb.lUtURCBWkIAOmdKnn_5W5jMhZYGcloVMvd6SG8"
GROQ_API_KEY = "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"
# ==================

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        user_input = message.content.replace(f"<@!{bot.user.id}>", "").strip()
        if not user_input:
            await message.reply("👋 Mention me with something and I’ll reply!")
            return

        await message.channel.typing()

        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are a helpful AI bot."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.8
            }

            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            if response.status_code == 200:
                reply_text = result["choices"][0]["message"]["content"].strip()
                await message.reply(reply_text)
            else:
                await message.reply(f"⚠️ API Error {response.status_code}: {result}")

        except Exception as e:
            await message.reply(f"⚠️ Error: {e}")

bot.run(DISCORD_TOKEN)
