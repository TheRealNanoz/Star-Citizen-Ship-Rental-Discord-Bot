import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import os
import asyncio
from bs4 import BeautifulSoup
import html
from getpass import getpass
import io
import aiohttp

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)
MY_GUILD = discord.Object(id=guild_id)





# bot token and guild ID
bot_token = ''
guild_id = #enter number here





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
    await bot.tree.sync(guild=MY_GUILD)
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')


@bot.tree.command(name = "rent_cost", description = "This displayes rent for a ship or vehicle", guild=MY_GUILD)
async def RENT_COST(interaction: discord.Interaction, ship_name: str):
    try:
        ShipName = ship_name
        ship_url = "https://api.uexcorp.space/2.0/vehicles_rentals_prices_all"
        headers = {'Content-Type': 'application/json'}

        response = requests.get(ship_url, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()

                if 'data' not in data or not data['data']:
                    await interaction.response.send_message("No data found!")
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
                        embed.add_field(name="Rental Price", value=f"{int(rent_price):,} aUEC")
                        embed.add_field(name="Terminal", value=terminal)
                        
                        # If we found an image URL, add it to the embed
                        if image_url:
                            embed.set_image(url=image_url)
                        else:
                            print("No image to embed")  # Debugging: Log if no image is available
                        
                        await interaction.response.send_message(embed=embed)  # Send the embed message
                        break

                # If no matching vehicle is found
                if not shipFound:
                    await interaction.response.send_message(f"Error: There is no ship located in the UEX rental database with the name {ShipName}")
                    
            except json.JSONDecodeError:
                await interaction.response.send_message("Error: The API response is not in the expected JSON format.")
        else:
            await interaction.response.send_message(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            await interaction.response.send_message(f"Error details: {response.text}")
            
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

@bot.tree.command(name="buy_cost", description = "this displays cost of a ship in aUEC and $", guild=MY_GUILD) # mostly copied from RENT_COST as they are similar API's
async def BUY_COST(interaction: discord.Interaction, ship_name: str):
    try:
        ShipName = ship_name
        ship_url = "https://api.uexcorp.space/2.0/vehicles_purchases_prices_all"
        ship_url_2 = "https://api.uexcorp.space/2.0/vehicles_prices"
        headers = {'Content-Type': 'application/json'}

        response = requests.get(ship_url, headers=headers)
        response2 = requests.get(ship_url_2, headers=headers)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'data' not in data or not data['data']:
                    await interaction.response.send_message("No data found!")
                    return
                
                shipFound = False
                image_url = None  # Make sure image_url is initialized

                # Loop over the vehicles in the response
                for item in data['data']:
                    if item.get("vehicle_name").upper() == ShipName.upper():
                        buy_price = item.get("price_buy")
                        terminal = item.get("terminal_name")
                        shipFound = True
                        
                        # Attempt to get the image URL for the vehicle
                        image_url = get_vehicle_image(ShipName)
                        
                        if image_url:
                            print(f"Found image URL: {image_url}")  # Debugging: Ensure the image URL is found
                        else:
                            print("Could not find an image for the vehicle")  # Debugging: Log if no image is found

                        ## Send a response with the vehicle's details
                        #embed = discord.Embed(title=f"Vehicle: {ShipName}")
                        #embed.add_field(name="Purchase Price", value=f"{int(buy_price):,} aUEC")
                        #embed.add_field(name="Terminal", value=terminal)
                        
                        # If we found an image URL, add it to the embed
                        if not image_url:
                            #embed.set_image(url=image_url)
                            print("No image to embed")  # Debugging: Log if no image is available
                            break
                        
                        #await interaction.response.send_message(embed=embed)  # Send the embed message
                        value1 = True
                        break

                # If no matching vehicle is found
                if not shipFound:
                    value1 = False
                #    await interaction.response.send_message(f"Error: There is no ship located in the UEX ingame purchase database with the name {ShipName}")
                    
            except json.JSONDecodeError:
                await interaction.response.send_message("Error: The API response is not in the expected JSON format.")
        else:
            await interaction.response.send_message(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            await interaction.response.send_message(f"Error details: {response.text}")
        ###
        if response2.status_code == 200:
            try:
                data2 = response2.json()
                if 'data' not in data2 or not data2['data']:
                    await interaction.response.send_message("No data found!")
                    return
                
                shipFound2 = False
                image_url2 = None  # Make sure image_url is initialized

                # Loop over the vehicles in the response
                for item in data2['data']:
                    if item.get("vehicle_name").upper() == ShipName.upper():
                        price = item.get("price")
                        shipFound = True
                        value2 = True
                        break
                # If no matching vehicle is found
                if not shipFound:
                    value2 = False
                #    await interaction.response.send_message(f"Error: There is no ship located in the UEX purchase database with the name {ShipName}")
                    
            except json.JSONDecodeError:
                await interaction.response.send_message("Error: The API response is not in the expected JSON format.")
        else:
            await interaction.response.send_message(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            await interaction.response.send_message(f"Error details: {response.text}")
        ###



        if (value1 == True) and (value2 == True):
            embed = discord.Embed(title=f"Vehicle: {ShipName}")
            embed.add_field(name="Purchase Price", value=f"{int(buy_price):,} aUEC")
            embed.add_field(name="Real Price (USD)", value=f"${int(price):,}")
            embed.add_field(name="Terminal", value=terminal)
            embed.set_image(url=image_url)
            await interaction.response.send_message(embed=embed)
        elif (value1 == True) and (value2 != True):
            embed = discord.Embed(title=f"Vehicle: {ShipName}")
            embed.add_field(name="Purchase Price", value=f"{int(buy_price):,} aUEC")
            embed.add_field(name="Terminal", value=terminal)
            embed.set_image(url=image_url)
            await interaction.response.send_message(embed=embed)
        elif (value1 != True) and (value2 == True):
            embed = discord.Embed(title=f"Vehicle: {ShipName}")
            embed.add_field(name="Purchase Price", value="N/A")
            embed.add_field(name="Real Price (USD)", value=f"${int(price):,}")
            embed.set_image(url=image_url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("An error occurred in field generation")



        ###
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

@bot.tree.command(name = "rent_list", description = "provides a list of all rentable vehicles in game", guild=MY_GUILD)
async def RENT_LIST(interaction: discord.Interaction):
    try:
        ship_url = "https://api.uexcorp.space/2.0/vehicles_rentals_prices_all"
        headers = {'Content-Type': 'application/json'}
        response = requests.get(ship_url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()

                if 'data' not in data or not data['data']:
                    await interaction.response.send_message("No data found!")
                    return
                await interaction.response.send_message("# List Of Vehicle Prices")
                await interaction.response.send_message("### VehicleName | Rent (1 day)")
                shown_vehicles = set()
                for item in data['data']:
                    if item.get("vehicle_name") in shown_vehicles:
                        continue
                    shown_vehicles.add(item.get("vehicle_name"))
                    await interaction.response.send_message(f"- {item.get("vehicle_name")}: **{int(item.get("price_rent")):,}** aUEC ")
            except json.JSONDecodeError:
                await interaction.response.send_message("Error: The API response is not in the expected JSON format.")
        elif response.status_code == 401:
            await interaction.response.send_message("Error: Unauthorized access. Check your API key.")
        else:
            await interaction.response.send_message(f"Error: Failed to retrieve data. Status code: {response.status_code}")
            await interaction.response.send_message(f"Error details: {response.text}")
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}")

if bot_token == '':
    print("Cannot run bot without a token: ")
    print("Do you wish to either:")
    print("1. input the bot token for this session only")
    print("2. modify the locally saved code to permanently store bot token")
    user_response = int(input("Enter (1-2): "))
    if user_response == 1:
        bot_token = getpass("Copy and paste your bot token here: ")
    elif user_response == 2:
        print("Ending program! please modify bot_token variable in main.py!")
        exit()
bot.run(bot_token)
