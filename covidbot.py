#imports
import requests
import json
import discord

TOKEN = ""

client = discord.Client()

#method to get output from json file
def getCountryStats(countryCode):
    url = f"https://corona-stats.online/{countryCode}?format=json"
    resp = requests.get(url)
    resp = json.loads(resp.text)
    resp = resp["data"][0]
    dict = {
        "todayCases": resp["todayCases"],
        "totalCases": resp["cases"],
        "totalDeaths": resp["deaths"],
        "todayDeaths": resp["todayDeaths"],
        "recovered": resp["recovered"],
        "active": resp["active"],
        "tests": resp["tests"],
        "flag": resp["countryInfo"]["flag"]
    }
    return dict

def getWorldStats():
    url = f"https://corona-stats.online/ZA?format=json"
    resp = requests.get(url)
    resp = json.loads(resp.text)
    resp = resp["worldStats"]
    dict = {
        "todayCases": resp["todayCases"],
        "totalCases": resp["cases"],
        "totalDeaths": resp["deaths"],
        "todayDeaths": resp["todayDeaths"],
        "recovered": resp["recovered"],
        "active": resp["active"],
    }
    return dict

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith("!c19"): # !c19 US
        parts = message.content.split()
        if len(parts) < 2:
            embed = discord.Embed(title="Help", description="How to use the bot")
            embed.add_field(name="Usage", value="!c19 country/code")
            msg = "Click here for country codes: https://datahub.io/core/country-list#resource-data"
            embed.add_field(name="Code", value=msg)
            await message.channel.send(embed=embed)
        else:
            code = parts[1]
            embed = discord.Embed(title=code, description=f"Stats for {code}")
            if code.lower() == "world":
                d = getWorldStats()
            else:
                d = getCountryStats(code)

            embed.add_field(name="Today's Cases 👀", value=d["todayCases"])
            embed.add_field(name="Total Cases 👀", value=d["totalCases"])
            embed.add_field(name="Today's Deaths 😵", value=d["todayDeaths"])
            embed.add_field(name="Total Deaths 😵", value=d["totalDeaths"])
            embed.add_field(name="Recovered 😀", value=d["recovered"])

            if code.lower() != "world":
                embed.add_field(name="Active 🤒", value=d["active"])
                embed.add_field(name="Tests 👨‍🔬", value=d["tests"])
                embed.set_thumbnail(url=d["flag"])
            
            
            await message.channel.send(embed=embed)
    
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

client.run("Njc5NDI0NTYxNDg5Mzc5MzMw.XkznFg.i8c-Vb9zrMiQzYPjlOINEX3RPfk")
