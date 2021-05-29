import random
import discord
import urllib.request
import aiohttp
import os
import json
import asyncio
from dotenv import load_dotenv
from PIL import Image, ImageDraw
from io import BytesIO
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

load_dotenv()

IMGFLIP_USERNAME = os.getenv("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.getenv("IMGFLIP_PASSWORD")

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            data = await r.read()
    return json.loads(data)


async def error_api(ctx):
    embed = discord.Embed(color=0xed4245, title="Something went wrong",
                          description="Wait a bit and retry, and contact the bot support if it happens again")
    await ctx.send(embed=embed, hidden=True)


class Fun(commands.Cog):
    def __init__(self, gigachad):
        self.gigachad = gigachad

    @cog_ext.cog_slash(name="caption",
                       description="🎭 Caption a meme, 25 meme templates available!",
                       options=[
                           create_option(
                               name="template",
                               description="Choose a meme template",
                               option_type=3,
                               required=True,
                               choices=[
                                   create_choice(name="Two Buttons", value="87743020"),
                                   create_choice(name="Distracted Boyfriend", value="112126428"),
                                   create_choice(name="Drake Yikes", value="181913649"),
                                   create_choice(name="Batman Slaps Robin", value="438680"),
                                   create_choice(name="Trade Offer", value="309868304"),
                                   create_choice(name="Change my Mind", value="129242436"),
                                   create_choice(name="UNO Draw 25", value="217743513"),
                                   create_choice(name="Woman Yelling at Cat", value="188390779"),
                                   create_choice(name="Inhaling Seagull", value="114585149"),
                                   create_choice(name="Giga Chad", value="190327839"),
                                   create_choice(name="Another Woman", value="110163934"),
                                   create_choice(name="Same Pictures", value="180190441"),
                               ]
                           ),
                           create_option(
                               name="top_caption",
                               description="Write the top text",
                               option_type=3,
                               required=True
                           ),
                           create_option(
                               name="bottom_caption",
                               description="Write the bottom text",
                               option_type=3,
                               required=True
                           ),
                       ])
    async def caption(self, ctx: SlashContext, template: int, top_caption: str, bottom_caption: str):
        try:
            pload = {'font': 'impact', 'username': 'Thorgal108', 'password': 'zrRyU&D!FxpK3T3',
                     'template_id': template, 'text1': bottom_caption, 'text0': top_caption}
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.imgflip.com/caption_image', data=pload) as r:
                    data = await r.read()
            json_data = json.loads(data)
            embed = discord.Embed(color=0x2f3136)
            embed.set_image(url=json_data['data']['url'])
            embed.set_author(name='Click to access the post', url=json_data['data']['page_url'])
            embed.set_footer(text="Made with the imgflip.com API")
            await ctx.send(embed=embed, hidden=False)

        except:
            await error_api(ctx)

    @cog_ext.cog_slash(name="Meme", description='🎲 Get a random meme!',
                       options=[
                           create_option(
                               name="subreddit",
                               description="Get a meme from a particular subreddit",
                               option_type=3,
                               required=False,
                           )])
    async def meme(self, ctx: SlashContext, subreddit=None):
        try:
            if subreddit is None:
                json_data = await fetch('https://meme-api.herokuapp.com/gimme')
            else:
                json_data = await fetch(f'https://meme-api.herokuapp.com/gimme/{subreddit}')
            nsfw = json_data['nsfw']
            if nsfw:
                await ctx.send(content="Sorry, the meme was NSFW. Try another one!", hidden=True)
                return
            embed = discord.Embed(color=0x2f3136, url=json_data['postLink'], title=json_data['title'])
            embed.set_footer(text=f"r/{json_data['subreddit']} | u/{json_data['author']}")
            embed.set_image(url=json_data['url'])
            await ctx.send(embed=embed, hidden=False)

        except:
            await error_api(ctx)

    @cog_ext.cog_slash(name="chadmeter", description="📏 Scientifically measure your Chad level",
                       options=[
                           create_option(
                               name="user",
                               description="Check the chad lever of another user",
                               option_type=6,
                               required=False,
                           )])
    async def chadmeter(self, ctx: SlashContext, user: discord.user = True):
        chadlevel = random.randint(0, 100)
        if ctx.author.id == 541940250428047370:
            if user:
                chadlevel = 100

        if user:
            message = f'Your Chad level is {chadlevel}%!'
        else:
            appinfo = await self.gigachad.application_info()
            if user.id == appinfo.owner.id or self.gigachad.user.id:
                chadlevel = 100
            message = f"{user.mention}'s Chad level is `{chadlevel}%`!"
        embed = discord.Embed(title="📏 Chadmeter", description=message, color=0x2f3136)
        embed.set_footer(icon_url=self.gigachad.user.avatar_url, text="Chadmeter never lies, Copyrighted © method")
        embed.set_thumbnail(
            url="https://preview.redd.it/23td86ox29j51.png?auto=webp&s=c617e39e98b1e601cc91168369bd6ea38cd55f89")
        await ctx.send(embed=embed, hidden=False)

    @cog_ext.cog_slash(name="gigachadify", description="💫 Gigadify yourself or another user!",
                       options=[
                           create_option(
                               name="user",
                               description="GigaChadify another user!",
                               option_type=6,
                               required=False,
                           )])
    async def gigachadify(self, ctx: SlashContext, user: discord.user = True):
        if user is True:
            asset = ctx.author.avatar_url_as(size=128)
            prefix = "You look gorgeous, surely not as good as I do, but still..."
        else:
            asset = user.avatar_url_as(size=128)
            prefix = "They look gorgeous, surely not as good as I do, but still..."
        urllib.request.urlretrieve('https://i.imgur.com/gZJihTV.png', "gigachad.png")
        im1 = Image.open("gigachad.png")
        data = BytesIO(await asset.read())
        im2 = Image.open(data)
        im2 = im2.resize((175, 175))
        mask_im = Image.new("L", im2.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse([(0, 0), (175, 175)], fill=255)
        mask_im.save('mask_circle.jpg', quality=95)
        im2 = im2.rotate(7)
        im1.paste(im2, (300, 85), mask_im)
        im1.save("test.jpg", quality=95)
        footer = "Feel free to use this picture of yourself in your resume, or on any dating site"
        file = discord.File("test.jpg")
        attachment = "attachment://test.jpg"
        if user is not True:
            if user.id == self.gigachad.user.id:
                prefix = "I am Giga Chad. I gigachadify, I can't be gigachidified."
                footer = "Yep. That's me"
                file = discord.File("gigachad.png")
                attachment = "attachment://gigachad.png"
        embed = discord.Embed(title=prefix, color=0x2f3136)
        embed.set_footer(icon_url=self.gigachad.user.avatar_url, text=footer)
        embed.set_image(url=attachment)
        await ctx.send(file=file, embed=embed)

    @cog_ext.cog_slash(name="quote", description="💬 Get an inspiring quote to get closer to being a Giga Chad")
    async def quote(self, ctx: SlashContext):
        try:
            json_data = await fetch("https://api.fisenko.net/quotes")
            quote = json_data['text']
            author = json_data['author']
            embed = discord.Embed(title="💬 Inspiring quote", color=0x2f3136,
                                  description=f"<:quote1:845745030912278598> \n**{quote}** \n <:blank:845752143226077245>"
                                              "<:blank:845752143226077245><:blank:845752143226077245> "
                                              "<:blank:845752143226077245> "
                                              "<:blank:845752143226077245><:blank:845752143226077245> "
                                              f"<:blank:845752143226077245><:quote2:845745030978994216> \n - {author}")
            embed.set_footer(text="I hope this quote inspired you to become a Giga Chad")
            await ctx.send(embed=embed, hidden=False)

        except:
            await error_api(ctx)

    @cog_ext.cog_slash(name="advice", description="💡 Get some advice from Giga Chad")
    async def advice(self, ctx: SlashContext):
        try:
            json_data = await fetch('https://api.adviceslip.com/advice')
            advice = json_data['slip']['advice']
            embed = discord.Embed(title="💡 Helpful Advice", color=0x2f3136,
                                  description=f"🗣 {advice}")
            embed.set_footer(text="Follow or not this advice, up to you")
            await ctx.send(embed=embed, hidden=False)
        except:
            await error_api(ctx)


def setup(bot):
    bot.add_cog(Fun(bot))
