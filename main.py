import discord
from discord.ext import commands
import requests
import json
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# API key and bot token
bot_token = #''

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.command()
async def RENT_COST(ctx, *, ship_name: str):
    try:
        parts = name_and_scu.rsplit(' ', 1)
        if len(parts) != 1:
            await ctx.send("Invalid format. Use: `!RENT_COST <Ship Name>`")
            return

        ShipName = parts[0]
        commodities_url = "https://uexcorp.space/api/2.0/vehicles_rentals_prices_all"
        headers = {'Content-Type': 'application/json'}

        response = requests.get(commodities_url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()

                if 'data' not in data or not data['data']:
                    await ctx.send("No data found!")
                    return

                for item in data['data']:
                    if (item.get("vehicle_name")).upper() == ShipName.upper():
                        rent_price = item.get("price_rent")
                        terminal = item.get("terminal_name")
                        break

                await ctx.send(f"The Rental Price is {rent_price}")
                await ctx.send(f"The Terminal Name is {terminal}")
            except json.JSONDecodeError:
                await ctx.send("Error: The API response is not in the expected JSON format.")
        elif response.status_code == 401:
            await ctx.send("Error: Unauthorized access. Check your API key.")
        else:
            await ctx.send(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            await ctx.send(f"Error details: {response.text}")
    except Exception as e:
        await ctx.send(f"Error: {e}")


bot.run(bot_token)
