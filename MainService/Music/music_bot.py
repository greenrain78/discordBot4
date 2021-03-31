import discord
from discord.ext import commands

from MainService.Music.music_engine import YTDLSource


class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def music(self, ctx):
        """
        music 명령어
        음악 재생 명령어
        """
        if ctx.invoked_subcommand is None:
            text = f"해당 명령어가 없습니다.\n" \
                   f"명령어를 제대로 입력해 주세요.\n" \
                   f"잘 모르시면 $help music"
            await ctx.send(text)

    @music.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """
        디코 봇을 음성채널에 연결
        Joins a voice channel
        """

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @music.command()
    async def play(self, ctx, *, query):
        """
        저장된 음성파일을 재생
        Plays a file from the local filesystem
        """

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @music.command()
    async def yt(self, ctx, *, url):
        """
        유튜브 영상을 다운받아서 재생
        Plays from a url (almost anything youtube_dl supports)
        """
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @music.command()
    async def stream(self, ctx, *, url):
        """
        유튜브 영상을 스트리밍으로 재생
        Streams from a url (same as yt, but doesn't predownload)
        """

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @music.command()
    async def volume(self, ctx, volume: int):
        """
        볼륨 조절
        Changes the player's volume
        """

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @music.command()
    async def stop(self, ctx):
        """
        디코봇 음성체널에서 연결 해제
        disconnects the bot from voice
        """

        await ctx.voice_client.disconnect()

    @music.command()
    async def resume(self, ctx):
        """
        음악 일시정지
        Stops the bot from voice
        """
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            ctx.voice_client.resume()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
