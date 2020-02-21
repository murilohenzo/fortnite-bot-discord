from request import FortniteClient
import discord
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = '/'

client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name='Type /help'))


@client.event
async def on_message(message):
    if message.content.startswith(COMMAND_PREFIX + 'help'):
        await message.channel.send(
            'Este bot é alimentado pela API gratuita do Fortnite Tracker, que fornece estatísticas vitalícias para jogadores no PC, Xbox ou PS4.' + '\n`Comandos`\n' +
            '`/stats <platform> <nickname>` recuperar estatísticas em geral.\n' + '`/statsmode <platform> <nickname> <mode>` recuperar estatísticas para modo específico.\n'
            + '`/recentmatch <platform> <nickname>` recuperar estatístcas de partidas recentes.')
    elif message.content.startswith(COMMAND_PREFIX + 'stats'):
        words = message.content.split(' ', 2)

        if len(words) < 3:
            await message.channel.send('Usar: ' + COMMAND_PREFIX + 'stats <pc,xbl,psn> <nickname>')
            return

        platform = words[1].lower()

        if platform == 'xbox':
            platform = 'xbl'
        elif platform == 'ps4':
            platform = 'psn'

        if platform not in ('pc', 'xbl', 'psn'):
            await message.channel.send('Usar: ' + COMMAND_PREFIX + 'stats <pc,xbl,psn> <nickname>')
            return
        else:
            data = FortniteClient.get_account_info(platform, words[2])
            if len(data.keys()) == 1:
                await message.channel.send('Error: Player Not Found')
            elif data:

                name = data['epicName']
                platform = data['platformNameLong']
                matches_played = data['status']['Matches Played']
                wins = data['status']['Wins']
                win_percent = data['status']['Win%']
                kills = data['status']['Kills']
                kd = data['status']['k/d']
                score = data['status']['Score']

                embed = discord.Embed(title="Lifetime Stats for " + words[2], color=0x00ff00)

                embed.add_field(name="Platform", value=platform + '\n', inline=False)
                embed.add_field(name="Player", value=name + '\n', inline=False)
                embed.add_field(name="Matches Played", value=matches_played + '\n', inline=False)
                embed.add_field(name="Wins", value=wins + '\n', inline=False)
                embed.add_field(name="Win percent", value=win_percent + '\n', inline=False)
                embed.add_field(name="Kills", value=kills + '\n', inline=False)
                embed.add_field(name="K/D", value=kd + '\n', inline=False)
                embed.add_field(name="Score", value=score + '\n', inline=False)

                await message.channel.send(embed=embed)
            else:
                await message.channel.send('Failed to get data. Double check spelling of your nickname.')

    elif message.content.startswith(COMMAND_PREFIX + 'statusmode'):
        words = message.content.split()
        if len(words) < 4:
            await message.channel.send('Usar: ' + COMMAND_PREFIX + 'statusmode <pc,xbl,psn> <nickname> <mode>')
            return

        platform = words[1].lower()

        if platform == 'xbox':
            platform = 'xbl'
        elif platform == 'ps4':
            platform = 'psn'

        if platform not in ('pc', 'xbl', 'psn'):
            await message.channel.send('Usar: ' + COMMAND_PREFIX + 'statusmode <pc,xbl,psn> <nickname> <mode>')
            return
        else:
            data = FortniteClient.get_account_info(platform, words[2])
            if len(data.keys()) == 1:
                await message.channel.send('`Error: Player Not Found`')
            elif data:

                mode = words[3].lower()

                if mode == 'duo':
                    mode = 'duo'
                elif mode == 'solo':
                    mode = 'solo'
                elif mode == 'squad':
                    mode = 'squad'

                if mode not in ('solo', 'duo', 'squad'):
                    await message.channel.send(
                        'Usar: ' + COMMAND_PREFIX + 'statusmode <pc,xbl,psn> <nickname> <solo, duo, squad>')
                else:
                    name = data['epicName']
                    platform = data['platformNameLong']
                    matches_played = data['status']['status by mode'][0][mode]['matches']
                    wins = data['status']['status by mode'][0][mode]['wins']
                    kills = data['status']['status by mode'][0][mode]['kills']
                    kills_match = data['status']['status by mode'][0][mode]['kills/Macth']
                    kd = data['status']['status by mode'][0][mode]['k/d']
                    score = data['status']['status by mode'][0][mode]['score']
                    score_per_match = data['status']['status by mode'][0][mode]['scorePerMatch']

                    embed = discord.Embed(title="Stats by " + words[3], color=0x00ff00)
                    embed.add_field(name="Platform", value=platform + '\n', inline=False)
                    embed.add_field(name="Player", value=name + '\n', inline=False)
                    embed.add_field(name="Matches Played", value=matches_played + '\n', inline=False)
                    embed.add_field(name="Wins", value=wins + '\n', inline=False)
                    embed.add_field(name="Kills", value=kills + '\n', inline=False)
                    embed.add_field(name="kills/Macth", value=kills_match + '\n', inline=False)
                    embed.add_field(name="K/D", value=kd + '\n', inline=False)
                    embed.add_field(name="Score", value=score + '\n', inline=False)
                    embed.add_field(name="scorePerMatch", value=score_per_match + '\n', inline=False)

                    await message.channel.send(embed=embed)
            else:
                await message.channel.send('Failed to get data. Double check spelling of your nickname.')

    elif message.content.startswith(COMMAND_PREFIX + 'recentmatch'):
        words = message.content.split()
        print(words)
        if len(words) < 3:
            await message.channel.send('Usar: ' + COMMAND_PREFIX + 'recentmatch <pc,xbl,psn> <nickname>')
            return

        platform = words[1].lower()

        if platform == 'xbox':
            platform = 'xbl'
        elif platform == 'ps4':
            platform = 'psn'

        if platform not in ('pc', 'xbl', 'psn'):
            await message.channel.send('Usar: ' + COMMAND_PREFIX + 'recentmatch <pc,xbl,psn> <nickname>')
            return
        else:
            data = FortniteClient.recentmatches(platform, words[2])
            if len(data.keys()) == 1:
                await message.channel.send('`Error: Player Not Found`')
            elif data:
                for i in range(len(data['recentMatches'])):
                    value = data['recentMatches'][i]['top1']
                    if data['recentMatches'][i]['top1'] > 0:
                        data['recentMatches'][i]['top1'] = str(value) + ' 🏆'
                    elif data['recentMatches'][i]['top1'] == 0:
                        data['recentMatches'][i]['top1'] = ' ⛔'
                    embed = discord.Embed(title="Recent Matches", color=0x00ff00)
                    embed.add_field(name="Mode", value=str(data['recentMatches'][i]['playlist']) + '\n', inline=False)
                    embed.add_field(name="Kills", value=str(data['recentMatches'][i]['kills']) + '\n', inline=False)
                    embed.add_field(name="Score", value=str(data['recentMatches'][i]['score']) + '\n', inline=False)
                    embed.add_field(name="Wins", value=str(data['recentMatches'][i]['top1']) + '\n', inline=False)
                    embed.add_field(name="Hour", value=str(data['recentMatches'][i]['dateCollected']) + '\n',
                                    inline=False)
                    await message.channel.send(embed=embed)
            else:
                await message.channel.send('Failed to get data. Double check spelling of your nickname.')

@client.event
async def on_ready():
    print(f'{client.user.name} Está conectado ao Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Olá {member.name}, Bem vindo ao server!'
    )

client.run(BOT_TOKEN)
