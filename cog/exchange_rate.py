import discord
import aiohttp
import cog.functions as f
from discord.ext import commands

TOKEN = f.get_api()


async def exchangeRate(cFrom: str, cTo: str):
    url = f"https://exchangerate-api.p.rapidapi.com/rapid/latest/{cFrom}"
    headers = {
        'x-rapidapi-key': TOKEN,
        'x-rapidapi-host': "exchangerate-api.p.rapidapi.com"
        }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as r:
            if r.status == 200:
                json_response = await r.json()
                return json_response['rates'][cTo]
            else:
                return


class ExchangeRate(commands.Cog, name='Conversión',
                   description='Convierte cantidades'
                               ' de dinero entre monedas.'):

    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(aliases=['exch', 'convertir', 'conv'],
                      help='Convierte una cantidad de dinero'
                           ' entre dos monedas.')
    async def exchange(self, ctx, currency_from: str,
                       currency_to: str, amount: int = None):
        fromCurrency = str.upper(currency_from)
        toCurrency = str.upper(currency_to)
        exchange = float(await exchangeRate(fromCurrency, toCurrency))

        if amount is not None:
            result = round(exchange * amount)
            e = discord.Embed(color=f.rbColor())
            e.set_author(name='Conversión de monedas',
                         icon_url='https://cdn0.iconfinder.com/data/icons/'
                                  'business-cool-vector-3/128/120-512.png',
                         url='https://rapidapi.com/exchangerateapi/api/'
                             'exchangerate-api/')
            e.add_field(name=f'La conversión de ${amount} {fromCurrency}'
                             f' a {toCurrency} es:',
                        value=f'${result} {toCurrency}, a fecha de hoy.')
            await ctx.send(embed=e)
        else:
            e = discord.Embed(color=f.rbColor())
            e.set_author(name='Tasa de cambio',
                         icon_url='https://cdn0.iconfinder.com/data/icons/'
                                  'business-cool-vector-3/128/120-512.png',
                         url='https://rapidapi.com/exchangerateapi/api/'
                             'exchangerate-api/')
            e.add_field(name=f'Por cada $1 {fromCurrency}, deberás pagar:',
                        value=f'${exchange} {toCurrency}, a fecha de hoy.')
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(ExchangeRate(bot))
