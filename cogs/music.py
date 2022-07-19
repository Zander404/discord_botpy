import discord
from discord.ext import commands
import typing
import wavelink


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.create_node())

    async def create_node(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host='127.0.0.1', port='2333', password='youshallnotpass', region='asia')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music is ready')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node {node.identifier} is ready.')

    @commands.command(name='join', aliases=['connect', 'summon'])
    async def join_command(self, ctx: commands.Context, channel: typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected:
                return await ctx.send('O bot já está sendo usado em outro canal')

        await channel.connect(cls=wavelink.Player)
        mbed = discord.Embed(
            title='Conectado', description=f'O bot foi conectado ao canal {channel.name}', color=0x00ff00)
        await ctx.send(embed=mbed)

    @commands.command(name='leave', aliases=['disconnect'])
    async def leave_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send('Não há nenhum bot conectado ao canal')

        await player.disconnect()
        mbed = discord.Embed(
            title='Desconectado', description=f'O bot foi desconectado do canal {player.channel.name}', color=0x00ff00)
        await ctx.send(embed=mbed)

    @commands.command(name='play', aliases=['p'])
    async def play_command(self, ctx: commands.Context, *, search: str):
        search = await wavelink.YouTubeTrack.search(query=search, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(search)
        mbed = discord.Embed(
            title='Tocando', description=f'O bot está tocando {search.title}', color=0x00ff00)
        await ctx.send(embed=mbed)

    @commands.command(name='stop')
    async def stop_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send('Não há nenhum bot conectado ao canal')

        if player.is_playing:
            await player.stop()
            mbed = discord.Embed(
                title='Parado', description=f'O bot parou de tocar', color=0x00ff00)
            await ctx.send(embed=mbed)

        else:
            return await ctx.send('Nada está sendo tocado')

    @commands.command(name='pause')
    async def pause_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send('Não há nenhum bot conectado ao canal')
        if not player.is_pause:
            if player.is_playing:
                player.pause()
                mbed = discord.Embed(
                    title='Pausado', description=f'O bot pausou a música', color=0x00ff00)
                await ctx.send(embed=mbed)

            else:
                return await ctx.send('Nada está sendo tocado')

        else:
            return await ctx.send('O bot já está pausado')

    @commands.command(name='resume')
    async def resume_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send('Não há nenhum bot conectado ao canal')

        if player.is_pause:
            player.resume()
            mbed = discord.Embed(
                title='Resumido', description=f'O bot resumiu a música', color=0x00ff00)
            return await ctx.send(embed=mbed)
        else:
            return await ctx.send('O bot já está tocando')

    @commands.command(name='volume')
    async def volume_command(self, ctx: commands.Context, volume: int):
        if to > 100:
            return await ctx.send('O volume não pode ser maior que 100')
        if to < 1:
            return await ctx.send('O volume não pode ser menor que 0')

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        await player.set_volume(to)
        mbed = discord.Embed(
            title='Volume', description=f'O bot alterou o volume para {to}', color=0x00ff00)
        await ctx.send(embed=mbed)

    @commands.command(name='queue')
    async def queue_command(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send('Não há nenhum bot conectado ao canal')

        if not player.queue.queue:
            return await ctx.send('Não há nada na fila')

        queue = player.queue.queue
        queue_list = ''
        for track in queue:
            queue_list += f'{track.title}\n'
        mbed = discord.Embed(
            title='Fila', description=f'{queue_list}', color=0x00ff00)
        await ctx.send(embed=mbed)


def setup(client):
    client.add_cog(Music(client))
