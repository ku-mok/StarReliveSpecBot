from discord.ext import commands
import os
from wikiscraping import get_char_info
from utils import df_all_row_to_str, df_two_row_to_str
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(
        traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def starrelive(ctx, command, arg):
    command_list = {"all": 0, "act": 1, "skill": 2, "status": 3}
    if command not in command_list:
        await ctx.send("コマンドが見つかりません")
    elif command == "all":
        await ctx.send(arg + "の性能は")
        result = get_char_info(arg)
        await ctx.send(df_all_row_to_str(result))
    elif (command_list[command] >= 1 or command_list[command] <= 3):
        result = get.get_char_info(arg, command)
        await ctx.send(df_two_row_to_str(result))

    await ctx.send(arg)


bot.run(token)
