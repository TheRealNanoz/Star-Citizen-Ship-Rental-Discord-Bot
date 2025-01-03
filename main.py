import discord
from discord.ext import commands
import requests
import json
import os
import asyncio
from bs4 import BeautifulSoup
import html

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# API key and bot token
bot_token = #''


from html import unescape  # For decoding &quot; and other HTML entities

def get_vehicle_image(vehicle_name_partial):
    url = "https://uexcorp.space/vehicles/home"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all vehicle divs
    vehicle_divs = soup.find_all("div", class_="vehicle")
    for vehicle_div in vehicle_divs:
        # Get the full vehicle name from the "vehicle-name" attribute
        full_vehicle_name = vehicle_div.get("vehicle-name", "")
        if not full_vehicle_name:
            continue

        # Exclude the first word and check for a match
        remaining_name = " ".join(full_vehicle_name.split()[1:])
        if remaining_name.lower() == vehicle_name_partial.lower():
            # Find the "photos" div within this vehicle div
            photos_div = vehicle_div.find("div", class_="photos")
            
            if photos_div:
                # Look for the image URL in the 'data-url' attribute
                image_url = photos_div.get("data-url", "")
                
                if image_url:
                    print(f"Extracted image URL: {image_url}")  # Debugging: Ensure the image URL is correctly extracted
                    return image_url
                else:
                    print(f"No image URL found in the data-url attribute for {remaining_name}")
    
    # Return None if no match is found
    return None


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

#@bot.command()
#async def RENT_COST(ctx, *, ship_name: str):
#    try:
#
#        ShipName = ship_name
#        ship_url = "https://uexcorp.space/api/2.0/vehicles_rentals_prices_all"
#        headers = {'Content-Type': 'application/json'}
#
#        response = requests.get(ship_url, headers=headers)
#        if response.status_code == 200:
#            try:
#                data = response.json()
#
#                if 'data' not in data or not data['data']:
#                    await ctx.send("No data found!")
#                    return
#                shipFound = False
#                for item in data['data']:
#                    if (item.get("vehicle_name")).upper() == ShipName.upper():
#                        rent_price = item.get("price_rent")
#                        terminal = item.get("terminal_name")
#                        shipFound = True # so that we can determine whether or not to respond with no ship found later
#                        image_url = get_vehicle_image(ShipName)
#                        if image_url:
#                            # Ensure the URL is properly formatted and a valid image URL
#                            await ctx.send(f"Here is the image of the vehicle: {image_url}")
#                        else:
#                            await ctx.send(f"Could not find an image for the vehicle: {ShipName}")
#
#
#                        break
#                if (shipFound == False): # will not run if the shipFound is true.. therefore acts as an error response
#                    await ctx.send(f"Error: There as no ship located in the UEX rental database with the name {ShipName}")
#
#                await ctx.send(f"The Rental Price is: {rent_price}")
#                await ctx.send(f"The Terminal Name is: {terminal}")
#            except json.JSONDecodeError:
#                await ctx.send("Error: The API response is not in the expected JSON format.")
#        elif response.status_code == 401:
#            await ctx.send("Error: Unauthorized access. Check your API key.")
#        else:
#            await ctx.send(f"Error: Failed to retrieve data. Status code: {response.status_code}")
#            await ctx.send(f"Error details: {response.text}")
#    except Exception as e:
#        await ctx.send(f"Error: {e}")


@bot.command()
async def RENT_COST(ctx, *, ship_name: str):
    try:
        ShipName = ship_name
        ship_url = "https://uexcorp.space/api/2.0/vehicles_rentals_prices_all"
        headers = {'Content-Type': 'application/json'}

        response = requests.get(ship_url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()

                if 'data' not in data or not data['data']:
                    await ctx.send("No data found!")
                    return
                
                shipFound = False
                image_url = None  # Make sure image_url is initialized

                # Loop over the vehicles in the response
                for item in data['data']:
                    if item.get("vehicle_name").upper() == ShipName.upper():
                        rent_price = item.get("price_rent")
                        terminal = item.get("terminal_name")
                        shipFound = True
                        
                        # Attempt to get the image URL for the vehicle
                        image_url = get_vehicle_image(ShipName)
                        
                        if image_url:
                            print(f"Found image URL: {image_url}")  # Debugging: Ensure the image URL is found
                        else:
                            print("Could not find an image for the vehicle")  # Debugging: Log if no image is found

                        # Send a response with the vehicle's details
                        embed = discord.Embed(title=f"Vehicle: {ShipName}")
                        embed.add_field(name="Rental Price", value=f"{rent_price:,} aUEC")
                        embed.add_field(name="Terminal", value=terminal)
                        
                        # If we found an image URL, add it to the embed
                        if image_url:
                            embed.set_image(url=image_url)
                        else:
                            print("No image to embed")  # Debugging: Log if no image is available
                        
                        await ctx.send(embed=embed)  # Send the embed message
                        break

                # If no matching vehicle is found
                if not shipFound:
                    await ctx.send(f"Error: There is no ship located in the UEX rental database with the name {ShipName}")
                    
            except json.JSONDecodeError:
                await ctx.send("Error: The API response is not in the expected JSON format.")
        else:
            await ctx.send(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            await ctx.send(f"Error details: {response.text}")
            
    except Exception as e:
        await ctx.send(f"Error: {e}")


@bot.command()
async def RENT_LIST(ctx):
    try:
        ship_url = "https://uexcorp.space/api/2.0/vehicles_rentals_prices_all"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(ship_url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()

                if 'data' not in data or not data['data']:
                    await ctx.send("No data found!")
                    return
                await ctx.send("# List Of Vehicle Prices")
                await ctx.send("### VehicleName | Rent (1 day)")
                shown_vehicles = set()
                for item in data['data']:
                    if item.get("vehicle_name") in shown_vehicles:
                        continue
                    shown_vehicles.add(item.get("vehicle_name"))
                    await ctx.send(f"- {item.get("vehicle_name")}: **{item.get("price_rent"):,}** aUEC ")
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
