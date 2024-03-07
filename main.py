import json
import discord
from discord.commands import Option
import os
import dotenv
import requests
import math
import pandas as pd
from random import *

dotenv.load_dotenv()
guild_ids=["1028695205949476904"]

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('VALORANT'))

    

@bot.slash_command(guild_ids=guild_ids, description="Meme.")
async def atomix(ctx: discord.ApplicationContext):
    embed = discord.Embed(
            title = f"Fetching memes",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    try:
        embed = discord.Embed()
        endpoint = "https://api.imgflip.com/get_memes"
        res = requests.get(endpoint).json()
        random_int = randint(1, 100)
        embed.set_image(url=res["data"]["memes"][random_int]["url"])
        embed.set_footer(text="Data fetched from imgflip")
        await ctx.edit(embed=embed)
    except:
        await ctx.edit("Failed to fetch a meme :()")

@bot.slash_command(guild_ids=guild_ids, description="Sends the bot's latency.")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond('Pong! {0}ms'.format(math.floor(bot.latency*1000)))

@bot.slash_command(guild_ids=guild_ids,description="Sends valorant logo")
async def logo(ctx: discord.ApplicationContext):
    await ctx.send_response("https://commons.wikimedia.org/wiki/File:Valorant_logo.svg#/media/File:Valorant_logo_-_pink_color_version.svg")

@bot.slash_command(guild_ids=guild_ids, description="Sends the regional leaderboard.")
async def lb(ctx: discord.ApplicationContext,region: Option(str, 'Select Region na/eu/ap/kr', required = True, choices = ["na", "eu", "ap", "kr", "latam", "br"]), top: Option(int, 'Enter number of entries (Default=10)', default = 10)):
    embed = discord.Embed(
            title = f"Fetching leaderboard of {region}",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    try:
        endpoint="https://api.henrikdev.xyz/valorant/v1/leaderboard/"+region
        data=(requests.get(endpoint).json())
        lb="Leaderboard: "+region.upper()
        for i in range(1,top+1):
            lb+="\n"+str(i)+". "+str(data[i]["gameName"])+"#"+str(data[i]["tagLine"])+" - "+str(data[i]["rankedRating"])
        await ctx.edit(content=lb)
    except:
        embed = discord.Embed(
            title = f"Failed to fetch leaderboard of {region}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        await ctx.edit(embed=embed)
@bot.slash_command(guild_ids=guild_ids, description="Sends the player's data.")
async def valodata(ctx: discord.ApplicationContext,username: Option(str, 'Enter Username', required = True),tag: Option(str, 'Enter Tagline', required = True),region: Option(str, 'Select Region na/eu/ap/kr', required = True, choices = ["na", "eu", "ap", "kr", "latam", "br"])):
    embed = discord.Embed(
            title = f"Fetching player details of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    try:
        endpoint="https://api.henrikdev.xyz/valorant/v1/mmr/"+region+"/"+username+"/"+tag
        data=(requests.get(endpoint).json())
        embed= discord.Embed(
            title="Player Profile",
            color=discord.Colour.from_rgb(253,69,86)
        )
        embed.add_field(name="Username", value=str(data["data"]["name"])+"#"+str(data["data"]["tag"]),inline=True)
        embed.add_field(name="MMR",value=str(data["data"]["elo"]), inline=True)
        embed.add_field(name="Rank",value=str(data["data"]["currenttierpatched"]), inline=True)

        embed.set_footer(text="Made by Seemant Samal",icon_url="https://media.licdn.com/dms/image/C4D03AQEAhmEuzrwbTA/profile-displayphoto-shrink_400_400/0/1642796814277?e=1701907200&v=beta&t=YZySICjOG10NUGtD8L2VPd5xOlSz7tG7r47IE9Tptic")
        embed.set_author(name="Bottomix Alpha")
        embed.set_thumbnail(url=data["data"]["images"]["small"])

    
        await ctx.edit(embed=embed)
    except:
        embed = discord.Embed(
            title = f"Failed to fetch player details of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        await ctx.edit(embed=embed)
    # await ctx.edit(content="Username: "+str(data["data"]["name"])+"#"+str(data["data"]["tag"])+"\nElo: "+str(data["data"]["elo"])+"\nRank: "+str(data["data"]["currenttierpatched"]))

@bot.slash_command(guild_ids=guild_ids, description="Sends an embed for testing.")
async def embedtest(ctx: discord.ApplicationContext):
    embed= discord.Embed(
        title="Embed Title",
        description="This is embed description",
        color=discord.Colour.blurple()
    )
    embed.add_field(name="Region", value="APAC", inline=True)
    embed.add_field(name="Player", value="seemax#2569", inline=True)
    embed.add_field(name="MMR", value="661", inline=True)
    embed.set_author(name="Author Name", icon_url="https://media.valorant-api.com/playercards/fc209787-414b-10d0-dcac-04832fc2c654/displayicon.png")
    embed.set_thumbnail(url="https://media.valorant-api.com/playercards/fc209787-414b-10d0-dcac-04832fc2c654/smallart.png")
    embed.set_image(url="https://media.valorant-api.com/playercards/fc209787-414b-10d0-dcac-04832fc2c654/wideart.png")
    await ctx.respond(embed=embed)

@bot.slash_command(guild_ids=guild_ids, description="Get mmr history")
async def mmr_history(ctx: discord.ApplicationContext, username: Option(str, 'Enter Username', required = True), tag: Option(str, 'Enter tag',required = True),region: Option(str, 'Select Region na/eu/ap/kr', required = True, choices = ["na", "eu", "ap", "kr", "latam", "br"])):
    embed = discord.Embed(
            title = f"Fetching account details of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    embed = discord.Embed(
        title = "MMR History",
        description = "Your mmr history with a graph",
        color = discord.Colour.from_rgb(253,68,86)
    )
    endpoint_url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/{region}/{username}/{tag}" 
    try:
        res = requests.get(endpoint_url).json()
        date_list = []
        elo_list = []

        for mmr in res["data"]:
            date_for_plt = mmr["date_raw"]
            elo = mmr["elo"]
            date_list.append(date_for_plt)
            elo_list.append(elo)
        df = pd.DataFrame(
            {'mmr': elo_list},
            index = date_list
        )
        lines = df.plot.line()
        fig = lines.get_figure()
        fig.savefig("mmr_history.png")
        chart = discord.File("mmr_history.png",filename="mmr_history.png")
        embed.set_image(url = "attachment://mmr_history.png")
        await ctx.edit(embed = embed, file=chart)
    except:
        embed = discord.Embed(
            title = f"Failed to fetch mmr history of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        await ctx.edit(embed=embed)

@bot.slash_command(guild_ids=guild_ids, description="Get mmr history without graph")
async def mmr_history_text(ctx: discord.ApplicationContext, username: Option(str, 'Enter Username', required = True), tag: Option(str, 'Enter tag',required = True),region: Option(str, 'Select Region na/eu/ap/kr', required = True, choices = ["na", "eu", "ap", "kr", "latam", "br"])):
    embed = discord.Embed(
            title = f"Fetching player data of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    embed = discord.Embed(
        title = f"MMR History of {username}#{tag}",
        description = f"{username}#{tag} mmr history",
        color = discord.Colour.from_rgb(253,68,86)
    )
    endpoint_url = f"https://api.henrikdev.xyz/valorant/v1/mmr-history/{region}/{username}/{tag}" 
    try:
        res = requests.get(endpoint_url)
        res = res.json()["data"]

        count = 0
        while count<5:

            embed.add_field(name = "Tier", value = res[count]["currenttierpatched"], inline=True)
            embed.add_field(name = "MMR", value = res[count]["elo"], inline=True)
            embed.add_field(name = "Date", value = res[count]["date"], inline = True)
            count += 1
        
        await ctx.edit(embed = embed)
    except:
        embed = discord.Embed(
            title = f"Failed to mmr history of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        await ctx.edit(embed=embed)
@bot.slash_command(guild_ids=guild_ids, description="Get account details")
async def account_details(ctx: discord.ApplicationContext, username: Option(str, 'Enter Username', required = True), tag: Option(str, 'Enter tag',required = True)):
    embed = discord.Embed(
            title = f"Fetching account details of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    
    try:
        endpoint_url = f"https://api.henrikdev.xyz/valorant/v1/account/{username}/{tag}?force=true"
        res = requests.get(endpoint_url)
        res = res.json()["data"]
        embed = discord.Embed(
            title = f"Account details of {username}/{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        embed.add_field(name="Region", value = res["region"])
        embed.add_field(name="Account Level", value = res["account_level"])
        embed.set_thumbnail(url = res["card"]["small"])
        await ctx.edit(embed = embed)
    except:
        embed = discord.Embed(
            title = f"Failed to fetch account data due to some internal error of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
bot.run(os.getenv("TOKEN"))