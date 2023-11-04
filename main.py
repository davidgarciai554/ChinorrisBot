import discord
from discord.ext import commands
import os
import pytube
import qrcode
import requests
from googletrans import Translator
from PIL import Image, ImageDraw, ImageFont
import time
from dotenv import load_dotenv

load_dotenv()

my_secret = os.getenv('GCP_PROJECT_ID')

def __init__(self):
    self.client = discord.Client()


bot = commands.Bot(command_prefix='.', case_insensitive=True, help_command=None , intents=discord.Intents.all())
token = os.environ.get("TOKEN")
image_types = ["png", "jpeg", "gif", "jpg"]


@bot.event
async def on_ready():
    print('arriba estoy')


@bot.command(aliases=['p', 'youtube', 'y'])
async def play(ctx):
    link = await bot.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
    await ctx.send(f"{link}")


@bot.command(aliases=['hello', 'hi'])  # Hola
async def hola(ctx):
    await ctx.send(f'Hola <@{ctx.author.id}>')


# @bot.command(aliases=['audio'])  #Api para descargar audio de youtube
# async def mp3(ctx, *, url):
#     if 'youtube' in url:
#         source = 'youtube'
#         _url = url.split('v=')[-1]
#     await ctx.send('https://api.vevioz.com/@api/button/mp3/' + _url +
#                    f' , <@{ctx.author.id}>')


# @bot.command(aliases=['video'])  #Descargar video de youtube
# async def mp4(ctx, *, url):
#     if 'youtube' in url:
#         source = 'youtube'
#         _url = url.split('v=')[-1]
#     await ctx.send('https://api.vevioz.com/@api/button/videos/' + _url +
#                    f' , <@{ctx.author.id}>')


@bot.command()  # Generador de QR
async def qr(ctx, *, url):
    if not url:
        await ctx.send(f'No has mandado ningún enlace, {ctx.author.name}')
    else:
        try:
            response = requests.get(url)
            qr = qrcode.make(url)
            qr.save('output/output.png')
            await ctx.send(file=discord.File('output/output.png'))
        except requests.ConnectionError as exception:
            await ctx.send(f'No se pudo generar ningun QR, prueba de nuevo, {ctx.author.name}')


@bot.command(aliases=['catpicture', 'catphoto', 'cat'])  # Foto Gato
async def gato(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    if response.status_code == 200:
        data = response.json()[0]['url']
        await ctx.send(file=discord.File(downloadImage(data).name))
    else:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['dogpicture', 'dogphoto', 'dog'])  # Foto perro
async def perro(ctx):
    response = requests.get("https://random.dog/woof.json")
    if response.status_code == 200:
        data = response.json()['url']
        await ctx.send(file=discord.File(downloadImage(data).name))
    else:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['numberfact'])  # Dato de numero
async def datoNumero(ctx, *, numero):
    response = requests.get("http://numbersapi.com/" + numero)
    if response.status_code == 200:
        await ctx.send(translateToSpanish(response.text))
    else:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['vidhelp', 'vhelp'])  # Mandar ayuda de videos de memes
async def videohelp(ctx):
    files = os.listdir('vid')
    embed = discord.Embed(title="Videos Disponibles", color=discord.Color.red())
    for file in files:
        embed.add_field(name='Video ' + file,
                        value=file,
                        inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['vid', 'v'])  # Mandar videos de memes
async def video(ctx, *, vid):
    try:
        vid = 'vid/' + vid + '.mp4'
        await ctx.send(file=discord.File(vid))
    except:
        await ctx.send('No encontre el video')


@bot.command(aliases=['catfact'])  # Dato de gato
async def gatoDato(ctx):
    response = requests.get("https://catfact.ninja/fact")
    if response.status_code == 200:
        await ctx.send(translateToSpanish(response.json()['fact']))
    else:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['profile'])  # Sacar imagen de perfil
async def perfil(ctx, *, member: discord.Member = None):
    try:
        if not member:
            member = ctx.message.author
        userAvatar = member.avatar_url
        await ctx.send(userAvatar)
    except:
        await ctx.send('Lo siento no funciono! :C')


@bot.command()
async def hey(ctx, *members: discord.Member):
    try:
        if len(members) > 2:
            raise Exception
        elif len(members) == 2:
            member_1 = members[0]
            member_2 = members[1]
        else:
            member_1 = members[0]
            member_2 = ctx.message.author

        with requests.get(member_1.avatar_url) as r:
            img_data = r.content
        with open('input.png', 'wb') as handler:
            handler.write(img_data)

        with requests.get(member_2.avatar_url) as r:
            img_data = r.content
        with open('input2.png', 'wb') as handler:
            handler.write(img_data)

        main_img = Image.open('img/hey_no.png').convert('RGBA')
        main_img = main_img.resize((425, 425))
        size = 130
        img_1 = Image.open('input2.png').convert('RGBA');
        img_1 = img_1.resize((size, size));
        img_2 = Image.open('input.png').convert('RGBA');
        img_2 = img_2.resize((size, size));

        main_img.paste(img_1, (int(50), int(250)), img_1)
        main_img.paste(img_2, (int(65), int(10)), img_2)

        main_img.save('output/.png')
        await ctx.send(file=discord.File('output/output.png'))
    except:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['mm'])  # Sacar memes
async def memerandom(ctx):
    try:
        response = requests.get("https://meme-api.herokuapp.com/gimme/1")
        if response.status_code == 200:
            data = response.json()['memes'][0]['url']
            await ctx.send(file=discord.File(downloadImage(data).name))
        else:
            await ctx.send('Lo siento no funciono! :C')
    except:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['ayer'])  # Crear ayer vino
async def ayervino(ctx, *, texto):
    try:
        size_font = 35
        fnt = ImageFont.truetype("impact.ttf", size=size_font)

        main_img = Image.open('img/ayervino.png').convert('RGBA')
        main_img = main_img.resize((400, 400))

        width, height = main_img.size

        y = height - 35

        d = ImageDraw.Draw(main_img)
        d.text((int(width / 2), int(y - size_font)),
               texto,
               font=fnt,
               fill='white',
               stroke_width=3,
               stroke_fill='black',
               anchor="ms")
        main_img.save('output/output.png')
        await ctx.send(file=discord.File('output/output.png'))
    except:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['peso'])  # Crear ayer vino
async def pesodeser(ctx, *, texto):
    try:
        size_font = 25
        fnt = ImageFont.truetype("impact.ttf", size=size_font)

        main_img = Image.open('img/peso_de_ser.png').convert('RGBA')
        main_img = main_img.resize((400, 400))

        width, height = main_img.size

        y = height - 35

        d = ImageDraw.Draw(main_img)
        d.text((int(width / 2), int(y)),
               texto,
               font=fnt,
               fill='white',
               stroke_width=3,
               stroke_fill='black',
               anchor="ms")
        main_img.save('output/.png')
        await ctx.send(file=discord.File('output/output.png'))
    except:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['son'])  # Crear ayer vino
async def areyouwin(ctx, *, texto):
    try:
        size_font = 25
        fnt = ImageFont.truetype("impact.ttf", size=size_font)

        main_img = Image.open('img/areyouwin.png').convert('RGBA')
        main_img = main_img.resize((400, 400))

        width, height = main_img.size
        aux = 12

        if len(texto) > aux:
            texto = linea_salto(texto, aux)
            aux *= 2
        if len(texto) > aux:
            texto = linea_salto(texto, aux)
            aux *= 2

        d = ImageDraw.Draw(main_img)
        d.text((int(width / 2 - 10), int(size_font * 8 - aux)),
               texto,
               font=fnt,
               fill='white',
               stroke_width=3,
               stroke_fill='black',
               anchor="ls")
        main_img.save('output/output.png')
        await ctx.send(file=discord.File('output/output.png'))
    except Exception as e:
        print(e)
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['omg', 'cute'])  # Crear so cute
async def omgsocute(ctx, *, member: discord.Member = None):
    try:
        if not member:
            member = ctx.message.author
        with requests.get(member.avatar_url) as r:
            img_data = r.content
        with open('input.png', 'wb') as handler:
            handler.write(img_data)

        main_img = Image.open('img/omg_so_cute.png').convert('RGBA')
        main_img = main_img.resize((400, 400))

        image = Image.open('input.png').convert('RGBA')
        image = image.resize((125, 125))

        width, height = main_img.size
        _width, _height = image.size

        main_img.paste(image,
                       (int(width - _width - 10), int(height / 2 - _height / 2)), image)

        main_img.save('output/output.png')
        await ctx.send(file=discord.File('output/output.png'))
    except:
        await ctx.send('Lo siento no funciono! :C')


@bot.command(aliases=['useless'])  # Crear inutil
async def inutil(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    with requests.get(member.avatar_url) as r:
        img_data = r.content
    with open('input.png', 'wb') as handler:
        handler.write(img_data)

    main_img = Image.open('img/cosas_inutiles.png').convert('RGBA')
    main_img = main_img.resize((400, 400))

    image = Image.open('input.png').convert('RGBA')
    image = image.resize((200, 175))

    main_img.paste(image, (int(200), int(230)), image)

    main_img.save('output/output.png')
    await ctx.send(file=discord.File('output/output.png'))


@bot.command(aliases=['based'])  # Crear so cute
async def basado(ctx, *, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    with requests.get(member.avatar_url) as r:
        img_data = r.content
    with open('input.png', 'wb') as handler:
        handler.write(img_data)

    main_img = Image.new('RGB', (400, 400), color='white')

    img = Image.open('input.png').convert('RGBA')
    img = img.resize((400, 400))

    main_img.paste(img, (int(0), int(0)), img)

    main_img = main_img.convert('RGB');
    main_img.save('input.jpg', quality=1)

    main_img = Image.open('input.jpg').convert('RGBA');
    main_img.save('input.png', quality=-1)

    size_font = 70;
    fnt = ImageFont.truetype("impact.ttf", size=size_font);

    width, height = main_img.size

    y = height - 35;

    d = ImageDraw.Draw(main_img);
    d.text((int(width / 2), int(y)), 'BASADO', font=fnt, fill='white', stroke_width=3, stroke_fill='black', anchor="ms")
    main_img.save('output/output.png')
    await ctx.send(file=discord.File('output/output.png'))


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", color=discord.Color.blue())
    embed.add_field(name="Hola",
                    value="Devuelve un hola a quien me escriba.",
                    inline=False)
    # embed.add_field(name="mp3",
    #                 value="Para descargar audio de youtube.",
    #                 inline=False)
    # embed.add_field(name="mp4",
    #                 value="Para descargar video de youtube.",
    #                 inline=False)
    embed.add_field(name="Qr",
                    value="Le envias un link y te enviara el QR a ese link.",
                    inline=False)
    embed.add_field(name="Gato",
                    value="Te envio la foto de un gato super mono.",
                    inline=False)
    embed.add_field(name="Perro",
                    value="Te envio la foto de un perro super mono.",
                    inline=False)
    embed.add_field(name="DatoNumero",
                    value="Dame un numero y te doy tremenda data.",
                    inline=False)
    embed.add_field(name="GatoDato",
                    value="Te doy un dato sobre gatos.",
                    inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def MemeHelp(ctx):
    embed = discord.Embed(title="MemeHelp", color=discord.Color.green())
    embed.add_field(name="MemeRandom (mm)",
                    value="Te envio un meme de reddit to guapo.",
                    inline=False)
    embed.add_field(name="AyerVino (ayer)",
                    value="Crea un meme con la plantilla de apedra",
                    inline=False)
    embed.add_field(name="PesodeSer (peso)",
                    value="Crea un meme con la plantilla de levantando el peso de ser",
                    inline=False)
    embed.add_field(name="AreYouWin (son)",
                    value="Crea un meme con la plantilla de apedra",
                    inline=False)
    embed.add_field(name="OmgSoCute (omg , cute)",
                    value="Crea un meme con la plantilla de OmgSoCute",
                    inline=False)
    embed.add_field(name="Inutil (useless)",
                    value="Crea un meme con la plantilla de Cosas inutiles",
                    inline=False)
    embed.add_field(name="Hey",
                    value="Crea un meme con la plantilla de Hey no Hey Hi",
                    inline=False)
    await ctx.send(embed=embed)


def downloadImage(data):
    if data.endswith('.jpg') or data.endswith('.png') or data.endswith('.jpeg') or data.endswith(
            '.PNG') or data.endswith('.JPG') or data.endswith('.JPEG'):
        response = requests.get(data)
        file = open("output/output.png", "wb")
        file.write(response.content)
        file.close()
        return file
    elif data.endswith('.mp4') or data.endswith('.MP4'):
        response = requests.get(data)
        file = open("output/output.mp4", "wb")
        file.write(response.content)
        file.close()
        return file
    else:
        response = requests.get(data)
        file = open("output/output.gif", "wb")
        file.write(response.content)
        file.close()
        return file


def translateToSpanish(text):
    translator = Translator()
    translation = translator.translate(text, dest="es")
    return translation.text


def downloadAudioFromYoutube(url):
    yt = pytube.YouTube(url)
    print(yt.length)
    yt.streams.filter(res="144p").first().download(filename='audio.mp3')


def linea_salto(texto, numeros):
    if numeros < len(texto):
        if texto[numeros] == " ":
            texto = texto[:numeros] + "\n" + texto[numeros:].strip()
            return texto
        else:
            numeros += 1
            return linea_salto(texto, numeros)
    return texto


bot.run(token)
