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

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('VALORANT'))

@bot.slash_command(description="Sends the bot's invite link.")
async def invite(ctx: discord.ApplicationContext):
    await ctx.send_response("https://discord.com/api/oauth2/authorize?client_id=898298976153591070&permissions=0&scope=applications.commands%20bot")

@bot.slash_command(description="Sends the bot's latency.")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond('Pong! {0}ms'.format(math.floor(bot.latency*1000)))

@bot.slash_command(guild_ids=guild_ids,description="Sends valorant logo")
async def logo(ctx: discord.ApplicationContext):
    await ctx.send_response("https://commons.wikimedia.org/wiki/File:Valorant_logo.svg#/media/File:Valorant_logo_-_pink_color_version.svg")

@bot.slash_command(description="Sends the regional leaderboard.")
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
@bot.slash_command(description="Sends the player's data.")
async def valodata(ctx: discord.ApplicationContext,username: Option(str, 'Enter Username', required = True),tag: Option(str, 'Enter Tagline', required = True),region: Option(str, 'Select Region na/eu/ap/kr', required = True, choices = ["na", "eu", "ap", "kr", "latam", "br"])):
    embed = discord.Embed(
            title = f"Fetching player details of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
    await ctx.respond(embed=embed)
    try:
        endpoint="https://api.henrikdev.xyz/valorant/v2/mmr/"+region+"/"+username+"/"+tag
        data=(requests.get(endpoint).json())
        embed= discord.Embed(
            title=f"{data["data"]["name"]}#{data["data"]["tag"]}",
            color=discord.Colour.from_rgb(253,69,86)
        )
        embed.add_field(name="MMR",value=str(data["data"]["current_data"]['elo']), inline=True)
        embed.add_field(name="Rank",value=str(data["data"]['current_data']["currenttierpatched"]), inline=True)
        embed.add_field(name="Highest Rank", value=str(data["data"]["highest_rank"]['patched_tier'])+" - "+str(data["data"]["highest_rank"]['season']),inline=True)

        embed.set_footer(text="Made by Seemant Samal",icon_url="https://media.licdn.com/dms/image/C4D03AQEAhmEuzrwbTA/profile-displayphoto-shrink_400_400/0/1642796814277?e=1701907200&v=beta&t=YZySICjOG10NUGtD8L2VPd5xOlSz7tG7r47IE9Tptic")
        embed.set_author(name="Bottomix Alpha")
        embed.set_thumbnail(url=data["data"]['current_data']["images"]["small"])

    
        await ctx.edit(embed=embed)
    except Exception as exp:
        embed = discord.Embed(
            title = f"Failed to fetch player details of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        await ctx.edit(embed=embed)


@bot.slash_command(description="Get mmr history")
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

@bot.slash_command(description="Get mmr history without graph")
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
            embed.add_field(name = "Date", value = f"<t:{res[count]["date_raw"]}>", inline = True)
            count += 1
        
        await ctx.edit(embed = embed)
    except:
        embed = discord.Embed(
            title = f"Failed to mmr history of {username}#{tag}",
            color = discord.Colour.from_rgb(253,68,86)
        )
        await ctx.edit(embed=embed)
@bot.slash_command(description="Get account details")
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
            title = f"Account details of {username}#{tag}",
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