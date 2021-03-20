# https://discord.com/api/oauth2/authorize?client_id=821942697802596353&permissions=617536&scope=bot

#### 봇 기능 url
# https://code-200.tistory.com/98 reminder
# https://mandu-mandu.tistory.com/91 주기적으로 공지메세지 보내는 기능, 이걸로 팟 시간 확인하면 될듯?

### datetime
# https://dojang.io/mod/page/view.php?id=2463

#### 이모지 리스트
# https://tmrtkr.tistory.com/108 일반 메세지 이모지
# https://foxtrotin.tistory.com/277 embed로 이모지
# https://emojipedia.org/symbols/ 이모지 리스트\

import datetime
from datetime import timedelta

import discord_token
import asyncio
import discord
import schedule

def get_time(plus_hour):
    time = datetime.datetime.today() + timedelta(hours = plus_hour)
    time_str = str(time.year)
    
    if(time.month < 10):
        time_str = time_str + '0' + str(time.month)
    else:
        time_str = time_str + str(time.month)
        
    if(time.day < 10):
        time_str = time_str + '0' + str(time.day)
    else:
        time_str = time_str + str(time.day)
        
    if(time.hour >= 24):
        time_str = time_str + str(time.hour - 24)
    elif(time.hour < 10):
        time_str = time_str + '0' + str(time.hour)
    else:
        time_str = time_str + str(time.hour)
        
    if(time.minute < 10):
        time_str = time_str + '0' + str(time.minute)
    else:
        time_str = time_str + str(time.minute)
    return time_str

client = discord.Client()

# 생성된 토큰을 입력해준다.
token = discord_token.token

# 봇이 구동되었을 때 보여지는 코드
@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")

    
# 봇이 특정 메세지를 받고 인식하는 코드
@client.event
async def on_message(message):
    # 메세지를 보낸 사람이 봇일 경우 무시한다
    if message.author.bot:
        return None

    if message.content.startswith('%안녕'):
        channel = message.channel
        await channel.send('반가워!')
        
    if message.content.startswith('%팟추가'):
        embed = discord.Embed(title="시간 설정",description="몇 시간 후가 좋을까요?", color=0x00aaaa)
        embed.add_field(name="1", value="1시간 후 설정", inline=False)
        embed.add_field(name="2", value="2시간 후 실행", inline=False)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("1️⃣") #step
        await msg.add_reaction("2️⃣") #stun


schedules = [] # element = [겜팟 Embed, 'schedule_element','생성유저 id']
async def new_schedule(root_channel, time, root_user): #time = "yyyymmddHHMM", root_user = 밑에 root_user
    global schedules
    new = schedule.schedule()
    new.set_when(time)
    new.set_who(root_user)
    
    #본인확인
    def check(message):
        return root_user == message.author
    
    # 게임이름 받기
    try:
        notice1 = await root_channel.send("어떤 게임을 하실 건가요?\n'게임이름'만 알려주세요")
        message = await client.wait_for('message', timeout = 20.0, check = check)
    except asyncio.TimeoutError:
        notice2 = await root_channel.send("시간 초과로 취소됩니다.")
        await asyncio.sleep(300)
        await notice1.delete()
        await notice2.delete()
    else:
        await notice1.delete()
        new.set_what(message.content)
        new.add_participant(message.author)
        
        # 팟 올리기!
        embed = discord.Embed(title="*팟 모집중!*", color=0xf88379)
        embed.add_field(name="팟을 연 사람", value=root_user.name, inline=False)
        embed.add_field(name="어떤 게임?", value=new.get_what(), inline=False)
        embed.add_field(name="몇시에 할까요?", value=new.get_when(), inline=False)
        embed.set_footer(text='참여는 밑의 👍를 눌러주세요!')
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("👍") #step
        
        print(message.author.id)
        print(root_user.id)
        print(root_user.name)
        
        schedules.append([embed, new, message.author.id])

@client.event
async def on_reaction_add(reaction, user):
    def check(m):
        return m.channel.id == reaction.channel.id and m.author == reaction.author

    if user.bot == 1: #봇이면 패쓰
        return None
    root_channel = reaction.message.channel
    if str(reaction.emoji) == "1️⃣": #한시간후
        # user.name -> 유저이름
        msg = await reaction.message.channel.send("한시간 후 팟을 설정합니다.")
        await asyncio.sleep(0.6) # 기다리고
        await msg.delete() # 보낸 메시지 삭제
        await reaction.message.delete()
        time_str = get_time(1)
        await new_schedule(root_channel,time_str, user)
    if str(reaction.emoji) == "2️⃣": #두시간후
        msg = await reaction.message.channel.send("두시간 후 팟을 설정합니다.")
        await asyncio.sleep(0.6) # 기다리고
        await msg.delete() # 보낸 메시지 삭제
        await reaction.message.delete()
        time_str = get_time(2)
        await new_schedule(root_channel, time_str, user)
    if str(reaction.emoji) == "": #팟 인원 추가!
        # TODO
        # 구현하기
        return None

@client.event
async def on_reaction_remove(reaction, user):
    #반응이 삭제되었을 때!
    
    return None

client.run(token)

"""
        msg = message.channel.send("Sample message")
        await msg.add_reaction('🙌')
        
        def check_emoji(reaction, user):
            global msg
            return reaction.emoji == '🙌' and reaction.message.id == msg.id and user.bot == False
        
        try:
            reaction, user = await client.wait_for(event='reaction_add', timeout=60.0, check=check_emoji)
            # some action code when get emoji successfully
            pass
        except asyncio.TimeoutError:
            # some action code when get emoji timeout
            return
        """