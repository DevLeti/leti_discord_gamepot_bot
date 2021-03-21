# https://discord.com/api/oauth2/authorize?client_id=821942697802596353&permissions=617536&scope=bot

#### 봇 기능 url
# https://code-200.tistory.com/98 reminder
# https://mandu-mandu.tistory.com/91 주기적으로 공지메세지 보내는 기능, 이걸로 팟 시간 확인하면 될듯?
# https://discordpy.readthedocs.io/en/latest/api.html#id7 공식 discordpy api reference인듯?

### datetime
# https://dojang.io/mod/page/view.php?id=2463

#### 이모지 리스트
# https://tmrtkr.tistory.com/108 일반 메세지 이모지
# https://foxtrotin.tistory.com/277 embed로 이모지
# https://emojipedia.org/symbols/ 이모지 리스트\

############################################################################
# 시간 모듈
import datetime
from datetime import timedelta

#token
import discord_token

#디스코드 봇을 위한 모듈
import asyncio
import discord
from discord import Webhook, AsyncWebhookAdapter
import aiohttp

# 제작한 클래스들
import schedule
import user_custom
############################################################################

############################################################################
# 시간 계산 함수
def get_time(plus_hour):
    time = datetime.datetime.today() + timedelta(hours = plus_hour)
    return time

def parse_time(time):
    beautiful_time = datetime.datetime.strptime(time,'%Y%m%d%H%M')
    print(beautiful_time)
############################################################################

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

############################################################################
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
        await message.delete()
        embed = discord.Embed(title="시간 설정",description="몇 시간 후가 좋을까요?", color=0x00aaaa)
        embed.add_field(name="1", value="1시간 후 설정", inline=False)
        embed.add_field(name="2", value="2시간 후 실행", inline=False)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("1️⃣") #step
        await msg.add_reaction("2️⃣") #stun
############################################################################

############################################################################
# 팟 추가
schedules = [] # element = [팟모집 msg의 id, 'schedule_element','생성유저 id']
async def new_schedule(root_channel, time, root_user): #time = "yyyymmddHHMM", root_user = 밑에 root_user
    
    print("팟 추가 함수 접근")
    global schedules
    new = schedule.schedule()
    new.set_when(time) #시간
    
    #여기가 문제인가?
    new.set_who(user_custom.user(root_user.name, root_user.id)) #팟 만든 사람
    # new.add_participant(user_custom.user(root_user.name, root_user.id))#참여자에 만든사람 기본 탑재
    print(new.participant)
    
    #본인확인
    def check(message):
        return root_user == message.author
    
    # 게임이름 받기
    try:
        question = discord.Embed(title="같이 할 게임을 알려주세요!\n")
        question.set_footer(text="'게임이름'만 알려주세요!")
        notice1 = await root_channel.send(embed = question)
        
        # notice1 = await root_channel.send("어떤 게임을 하실 건가요?\n'게임이름'만 알려주세요")
        message = await client.wait_for('message', timeout = 20.0, check = check)
    except asyncio.TimeoutError:
        message.delete()
        notice2 = await root_channel.send("시간 초과로 취소됩니다.")
        await asyncio.sleep(300)
        await notice1.delete()
        await notice2.delete()
    else:
        await message.delete()
        await notice1.delete()
        new.set_what(message.content)
        
        # 팟 올리기!
        embed = discord.Embed(title="*팟 모집중!*", color=0xf88379)
        embed.add_field(name="팟을 연 사람", value=new.name(), inline=False)
        embed.add_field(name="어떤 게임?", value=new.what, inline=False)
        embed.add_field(name="몇시에 할까요?", value=new.when.strftime("%Y년 %m월 %d일 %H시 %M분"), inline=False)
        embed.add_field(name="누가 참여하나요?", value="아직 없어요!", inline=False)
        embed.set_footer(text='참여는 밑의 👍를 눌러주세요!')
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("👍") #step
        
        # print(message.author.id)
        # print(root_user.id)
        # print(root_user.name)
        
        schedules.append([msg.id, new, message.author.id]) 
        print(schedules)
############################################################################

############################################################################
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
    if str(reaction.emoji) == "👍": #팟 인원 추가!
        for schedule in schedules:
            if(reaction.message.id == schedule[0]):
                print("팟 찾음")
                print(reaction.message.author.name)
                print(reaction.message.author.id)
                new_participant = user_custom.user(user.name, user.id)
                schedule[1].add_participant(new_participant)
                embed = discord.Embed(title="*팟 모집중!*", color=0xf88379)
                embed.add_field(name="팟을 연 사람", value=schedule[1].name(), inline=False)
                embed.add_field(name="어떤 게임?", value=schedule[1].what, inline=False)
                embed.add_field(name="몇시에 할까요?", value=schedule[1].when.strftime("%Y년 %m월 %d일 %H시 %M분"), inline=False)
                embed.add_field(name="누가 참여하나요?", value=schedule[1].display_participant(), inline=False)
                embed.set_footer(text='참여는 밑의 👍를 눌러주세요!')
                await reaction.message.edit(embed=embed)
        # TODO
        # 구현하기
    return None
############################################################################

############################################################################
@client.event
async def on_raw_reaction_remove(raw_reaction_event):
    
    ###############################################
    # raw말고 on_reaction_remove는 왜 반응이 없을까? # -> cache 뮈시기가 있는데... 해석해야함
    ###############################################
    # 아 뭔가 이거 아닌데...
    
    print("반응 제거 확인")
    print("👍")
    if str(raw_reaction_event.emoji) == '👍':
        #반응이 삭제되었을 때!
        message_id = raw_reaction_event.message_id
        user_id = raw_reaction_event.user_id
        for schedule in schedules:
            if(raw_reaction_event.message_id == schedule[0]):
                print("팟 찾음")
                delete_participant = user_custom.user("Jone Doe", user_id) #이름은 상관X id만 있으면 됨
                schedule[1].delete_participant(delete_participant)
                embed = discord.Embed(title="*팟 모집중!*", color=0xf88379)
                embed.add_field(name="팟을 연 사람", value=schedule[1].name(), inline=False)
                embed.add_field(name="어떤 게임?", value=schedule[1].what, inline=False)
                embed.add_field(name="몇시에 할까요?", value=schedule[1].when.strftime("%Y년 %m월 %d일 %H시 %M분"), inline=False)
                embed.add_field(name="누가 참여하나요?", value=schedule[1].display_participant(), inline=False)
                embed.set_footer(text='참여는 밑의 👍를 눌러주세요!')
                
                ##################
                #구현 해야할 부분!!#
                ##################
                # message_id와 embed를 가지고 메세지를 수정해야 할 때, webhook을 이용해야 할까?
                # webhook을 사용할 때, webhook url이 public이어도 괜찮은가?
                
                # async with aiohttp.ClientSession() as session:
                #     webhook = Webhook.from_url('url-here', adapter=AsyncWebhookAdapter(session))
                #     await webhook.edit_message(message_id=message_id, embed=embed)
                # await reaction.message.edit(embed=embed)
    return None
############################################################################

client.run(token) # 구동

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