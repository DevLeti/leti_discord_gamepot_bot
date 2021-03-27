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
from discord.ext import commands, tasks

# 제작한 클래스들
import schedule
import user_custom
############################################################################

############################################################################
#schedule들이 들어있는 array.
# schedules array에 들어가는 element : [팟모집 msg, schedule_element, 생성유저 id]
# 팟모집 msg의 instance type : discord.Message
# schedule_element의 instace type : schedule.schedule
# 생성유저 고유 디스코드id의 instance type : string
schedules = [] 
############################################################################

############################################################################
# 시간 계산 함수
def get_time(plus_hour):
    time = datetime.datetime.today() + timedelta(minutes = plus_hour) 
    return time

def parse_time(time):
    beautiful_time = datetime.datetime.strptime(time,'%Y%m%d%H%M')
    return beautiful_time
############################################################################

client = discord.Client()

# 생성된 토큰을 입력해준다. 유출되면 안되므로 외부에서 끌어오기.
token = discord_token.token

# 봇이 구동되었을 때 보여지는 코드
@client.event
async def on_ready():
    print("다음으로 로그인합니다")
    print(client.user.name)
    print(client.user.id)
    print("================")
    my_background_task.start()

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
        embed.add_field(name="😀", value="직접설정", inline=False)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("1️⃣") #step
        await msg.add_reaction("2️⃣") #stun
        await msg.add_reaction("😀") #stun
        
############################################################################

############################################################################
# 상세시간 설정 함수
async def set_custom_time(root_channel, root_user):
     # 게임이름 받기
    try:
        question = discord.Embed(title="팟 시간을 알려주세요!\n")
        question.set_footer(text="yymmddHHMM(연/월/일/시간/분)\n형식으로 알려주세요!\n예)2104251340 : 2021년4월25일13시40분")
        time_question_message = await root_channel.send(embed = question)
        
        def check(message):
            return root_user == message.author
    
        message = await client.wait_for('message', timeout = 60.0, check = check) # 20
        
    except asyncio.TimeoutError:
        time_out_message = await root_channel.send("시간 초과로 취소되었습니다.")
        await asyncio.sleep(25) # 300
        await time_question_message.delete()
        await time_out_message.delete()
    else:
        time_str = message.content
        await message.delete()
        await time_question_message.delete()
        
        try:
            if(len(time_str) != 10): #2104251340 <- 길이가 안맞음 -> 잘못입력
                msg = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                await asyncio.sleep(2)
                await msg.delete()
                await set_custom_time(root_channel, root_user)

            print('time_str : ', time_str)
            time_instance = parse_time('20' + time_str) # datetime.datetime 타입으로 변환
            now = datetime.datetime.today()
            check_minute = int((time_instance - now).total_seconds()/60) # 서버시간이랑 비교
            if(check_minute < 0): # 과거 - 현재 = 음수이므로 음수면 잘못 입력한것임.
                msg = await root_channel.send("앗! 전 도르마무가 아니에요!\n과거 팟을 만들 수 없어요!\n다시 입력받겠습니다!")
                await asyncio.sleep(2)
                await msg.delete()
                await set_custom_time(root_channel, root_user)

            # 정상 입력됨
            return time_instance
        except:
            msg = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
            await asyncio.sleep(2)
            await msg.delete()
            await set_custom_time(root_channel, root_user)

##########################################################################################
async def set_custom_time_two_level(root_channel, root_user):
     # 게임이름 받기
    try:
        question1 = discord.Embed(title="월일을 알려주세요!\n")
        question1.set_footer(text="예)1025: 10월25일, 131:1월31일, 11:1월1일")
        month_day_question = await root_channel.send(embed = question1)
        
        def check(message):
            return root_user == message.author
        message = await client.wait_for('message', timeout = 60.0, check = check) # 20
    except asyncio.TimeoutError:
        time_out_message = await root_channel.send("시간 초과로 취소되었습니다.")
        await asyncio.sleep(25) # 300
        await month_day_question.delete()
        await time_out_message.delete()
    else: #월일 입력 성공
        month_day_str = message.content
        await message.delete()
        await month_day_question.delete()
        try:
            """
            월일 가능한 케이스
            1. 2자리 : 11 = 1월 1일, 22 = 2월2일, 39 = 3월9일
            2. 3자리 : 315 = 3월 15일, 225 = 2월25일
            3. 4자리 : 0425 : 4월 25일, 1225 = 12월 25일
            모두 판단하자
            한자리랑 5자리이상은 else로 빼서 날짜형식 에러 출력하고 다시 함수 호출시키기
            +) 버그 찾고싶어서 -125같이 입력하면 어떡하지?
                -> -12같이 3자리면 int 변환하면서 에러나서 except로 던짐, -225면 month < 0에서 걸러짐 : OK
            """
            # 31인 월 : 1,3,5,7,8,10,12
            # 30인 월 : 4,6,9,11
            # 28 또는 29인 월 : 2
            day31_month = [1,3,5,7,8,10,12]
            day30_month = [4,6,9,11]
            year = datetime.datetime.today().year # 서버시간에서 연도 추출
            # 입력이 두글자 11, 22,35,59
            if(len(month_day_str) == 2):
                month = int(month_day_str[0])
                day = int(month_day_str[1])
                if(month == 0 or day == 0): # 0월 3일 없고, 1월 0일은 없다.
                    #탕수육 먹고싶당
                    error_msg = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                    await asyncio.sleep(2)
                    await error_msg.delete()
                    await set_custom_time_two_level(root_channel, root_user)
            # 입력이 세글자
            elif(len(month_day_str) == 3): #만약 425면 4월 25일로 인식해야하니까
                month = int(month_day_str[0])
                day = int(month_day_str[1:3])
                if(month < 1): # 12이상일 수가 없으므로 0이하만 확인
                    month_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                    await asyncio.sleep(2)
                    await month_error.delete()
                    await set_custom_time_two_level(root_channel, root_user)
                else: #0이하 수 아닌것을 확인함
                    
                    # 1. 31일인 월인 경우
                    if(month in day31_month):
                        if(day < 1 or day > 31):
                            day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                            await asyncio.sleep(2)
                            await day_error.delete()
                            await set_custom_time_two_level(root_channel, root_user)
                    # 2. 30일인 월인 경우
                    elif(month in day30_month):
                        if(day < 1 or day > 30):
                                day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                                await asyncio.sleep(2)
                                await day_error.delete()
                                await set_custom_time_two_level(root_channel, root_user)
                    # 3. 2월인 경우
                    elif(month == 2):
                        year = datetime.datetime.today().year # 서버시간에서 연도 추출
                        if((year%4 == 0 and year%100!=0) or year%400==0): #윤년 계산
                            if(day < 1 or day > 29):
                                day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                                await asyncio.sleep(2)
                                await day_error.delete()
                                await set_custom_time_two_level(root_channel, root_user)
                        else: #평년
                            if(day < 1 or day > 28):
                                day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                                await asyncio.sleep(2)
                                await day_error.delete()
                                await set_custom_time_two_level(root_channel, root_user)
            #입력이 4글자
            elif(len(month_day_str) == 4):
                month = int(month_day_str[0:2])
                day = int(month_day_str[2:])
                if(month < 1 or month > 12): 
                    month_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                    await asyncio.sleep(2)
                    await month_error.delete()
                    await set_custom_time_two_level(root_channel, root_user)
                else: #0이하 12이상 월이 아닌것을 확인함
                    
                    # 1. 31일인 월인 경우
                    if(month in day31_month):
                        if(day < 1 or day > 31):
                            day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                            await asyncio.sleep(2)
                            await day_error.delete()
                            await set_custom_time_two_level(root_channel, root_user)
                    # 2. 30일인 월인 경우
                    elif(month in day30_month):
                        if(day < 1 or day > 30):
                                day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                                await asyncio.sleep(2)
                                await day_error.delete()
                                await set_custom_time_two_level(root_channel, root_user)
                    # 3. 2월인 경우
                    elif(month == 2):
                        if((year%4 == 0 and year%100!=0) or year%400==0): #윤년 계산
                            if(day < 1 or day > 29):
                                day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                                await asyncio.sleep(2)
                                await day_error.delete()
                                await set_custom_time_two_level(root_channel, root_user)
                        else: #평년
                            if(day < 1 or day > 28):
                                day_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                                await asyncio.sleep(2)
                                await day_error.delete()
                                await set_custom_time_two_level(root_channel, root_user)
            else:
                error_message = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                await asyncio.sleep(2)
                await error_message.delete()
                await set_custom_time_two_level(root_channel, root_user)
        except: #에러
            error_message = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
            await asyncio.sleep(2)
            await error_message.delete()
            await set_custom_time_two_level(root_channel, root_user)
                            
        else: #월일 케이스 통과, 가지고 있는 변수 : year, month, day
            try:
                question2 = discord.Embed(title="시간을 알려주세요!\n")
                question2.set_footer(text="0시~23시, 0분~59분\n예)1340 : 13시40분, 930 : 09시30분, 13 : 1시3분, 00: 0시0분")
                hour_minute_question = await client.wait_for('message', timeout = 60.0, check = check) # 20
            except asyncio.TimeoutError:
                    time_out_message = await root_channel.send("시간 초과로 취소되었습니다.")
                    await asyncio.sleep(25) # 300
                    await time_out_message.delete()
                    await hour_minute_question.delete()
            else:
                hour_minute_str = message.content
                await message.delete() # 질문회수
                await month_day_question.delete() # 질문회수
                """
                월일 가능한 케이스
                1. 2자리 : 00 = 0시0분 10 = 1시 0분 11 = 1시 1분, 22 = 2시2분, 39 = 3시9분
                2. 3자리 : 315 = 3시 15분, 225 = 2시25분
                    2-1. 125 : 1시 25분 또는 12시 5분으로 두가지 입력이 가능한 경우
                    물어봐서 맞는지 유무를 확인해보자.
                3. 4자리 : 0425 : 4시 25분, 1225 = 12시 25분,
                모두 판단하자
                한자리랑 5자리이상은 else로 빼서 날짜형식 에러 출력하고 다시 함수 호출시키기
                +) 버그 찾고싶어서 -125같이 입력하면 어떡하지?
                    -> -12같이 3자리면 int 변환하면서 에러나서 except로 던짐, -225면 month < 0에서 걸러짐 : OK
                """
                try:
                    # 1. 2자리
                    if(len(hour_minute_str) == 2):
                        hour = int(hour_minute_str[0])
                        minute = int(hour_minute_str[1])
                    # 2. 3자리
                    elif(len(hour_minute_str) == 3):
                        #125같이 모호한 자리수 판단하는 상호작용 추가
                    # 3. 4자리
                    elif(len(hour_minutes_str) == 4):
                        hour = int(hour_minutes_str[0:2])
                        minute = int(hour_minute_str[2:4])
                        if(hour < 0 or hour > 23):
                            hour_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                            await asyncio.sleep(2)
                            await hour_error.delete()
                            await set_custom_time_two_level(root_channel, root_user)
                        elif(minute < 0 or minute > 60):
                            minute_error = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                            await asyncio.sleep(2)
                            await minute_error.delete()
                            await set_custom_time_two_level(root_channel, root_user)
                except:
                    error_message = await root_channel.send("시간 형식이 잘못되었습니다.\n다시 입력받겠습니다!")
                    await asyncio.sleep(2)
                    await error_message.delete()
                    await set_custom_time_two_level(root_channel, root_user)
                else: #월일시간분 다 받음! month, day, hour, minute
                    time_instance = datetime.datetime(year = year, month = month, day = day, hour=hour, minute=minute)
                    return time_instance

# 팟 embed 생성 함수
def make_pot_embed(schedule):
    embed = discord.Embed(title="*팟 모집중!*", color=0xf88379)
    embed.add_field(name="팟을 연 사람", value=schedule.name(), inline=False)
    embed.add_field(name="어떤 게임?", value=schedule.what, inline=False)
    embed.add_field(name="몇시에 할까요?", value=schedule.when.strftime("%Y년 %m월 %d일 %H시 %M분"), inline=False)
    embed.add_field(name="누가 참여하나요?", value=schedule.display_participant(), inline=False)
    embed.set_footer(text='참여는 밑의 👍를 눌러주세요!')
    return embed

def make_ended_pot_embed(schedule):
    embed = discord.Embed(title="*마감된 팟!*", color=0xf88379)
    embed.add_field(name="팟을 연 사람", value=schedule.name(), inline=False)
    embed.add_field(name="어떤 게임?", value=schedule.what, inline=False)
    embed.add_field(name="몇시에 할까요?", value=schedule.when.strftime("%Y년 %m월 %d일 %H시 %M분"), inline=False)
    embed.add_field(name="누가 참여하나요?", value=schedule.display_participant(), inline=False)
    embed.set_footer(text='마감된 팟의 추가 참여는 불가해요😢')
    return embed
# 팟 추가
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
        
        message = await client.wait_for('message', timeout = 25.0, check = check) # 20
    except asyncio.TimeoutError:
         
        notice2 = await root_channel.send("시간 초과로 취소되었습니다.")
        await asyncio.sleep(25) # 300
        await notice1.delete()
        await notice2.delete()
    else:
        await message.delete()
        await notice1.delete()
        new.set_what(message.content)
        
        # 팟 올리기!
        embed = make_pot_embed(new)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("👍") #step
        
        # print(message.author.id)
        # print(root_user.id)
        # print(root_user.name)
        
        schedules.append([msg, new, message.author.id]) 
        print("스케쥴 추가됨, ", schedules)
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
        time_str = get_time(60)
        await new_schedule(root_channel,time_str, user)
    if str(reaction.emoji) == "2️⃣": #두시간후
        msg = await reaction.message.channel.send("두시간 후 팟을 설정합니다.")
        await asyncio.sleep(0.6) # 기다리고
        await msg.delete() # 보낸 메시지 삭제
        await reaction.message.delete()
        time_str = get_time(120)
        await new_schedule(root_channel, time_str, user)
    if str(reaction.emoji) == "😀": #1분후
        msg = await reaction.message.channel.send("시간을 설정합니다.")
        await asyncio.sleep(0.6) # 기다리고
        await msg.delete() # 보낸 메시지 삭제
        await reaction.message.delete()
        time_str = await set_custom_time(root_channel, user)
        await new_schedule(root_channel, time_str, user)
        # time_str = get_time(1)
        # await new_schedule(root_channel, time_str, user)
    if str(reaction.emoji) == "👍": #팟 인원 추가!
        for schedule in schedules:
            if(reaction.message.id == schedule[0].id):
                # print("팟 찾음")
                # print(reaction.message.author.name) # 만든사람 닉네임
                # print(reaction.message.author.id) # 만든사람 고유 discord id
                new_participant = user_custom.user(user.name, user.id)
                schedule[1].add_participant(new_participant)
                embed = make_pot_embed(schedule[1])
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
    # print("반응 제거 확인")
    # print("👍")
    if str(raw_reaction_event.emoji) == '👍':
        #반응이 삭제되었을 때!
        message_id = raw_reaction_event.message_id
        user_id = raw_reaction_event.user_id
        for schedule in schedules:
            if(raw_reaction_event.message_id == schedule[0].id):
                # print("팟 찾음")
                delete_participant = user_custom.user("Jone Doe", user_id) #이름은 상관X id만 있으면 됨
                schedule[1].delete_participant(delete_participant)
                embed = make_pot_embed(schedule[1])
                await schedule[0].edit(embed=embed)
    return None
############################################################################

############################################################################
# 1분마다 1시간, 30분, 15분, 10분, 5분, 마감 상태일 때 그 embed를 그대로 복사해서
# 해당 schedule[0] (msg)를 삭제 후 새로 보낸 msg를 남은 시간과 함께 보내기
# 


def check_time(pot_time):
    ################
    # 함수 검증 필요 #
    ################
    
    #################################################################
    # pot_time의 instance type은 datetime.datetime
    # datetime.datetime 끼리 빼면 return value는 datetime.timedelta
    # 그러면 datetime.timedelta(60 30 15 10 5) 각각 이퀄 확인하면 될듯?
    #################################################################
    
    now = datetime.datetime.today()
    if(pot_time - now == datetime.timedelta(minutes = 60)):
        return 60
    elif(pot_time - now == datetime.timedelta(minutes = 30)):
        return 30
    elif(pot_time - now == datetime.timedelta(minutes = 10)):
        return 10
    elif(pot_time - now == datetime.timedelta(minutes = 5)):
        return 5
    else:
        # 남은 분
        remain_minute = int((pot_time - now).total_seconds()/60)
        return remain_minute
    
@tasks.loop(seconds=30)
async def my_background_task():
    ################
    # 함수 검증 필요 #
    ################
    await client.wait_until_ready()
    print("background task 함수 접근")
    #schedule들이 들어있는 array를 순회하며 60/30/10/5분 후 마감이 되는 팟을 찾는 함수
    
    if len(schedules) == 0: #schedule이 하나도 없으면
        return None
    
    # schedules array에 들어가는 element : [팟모집 msg, schedule_element, 생성유저 id]
    for i in range (0, len(schedules)):
        pot_time = schedules[i][1].when # datetime.datetime
        remain_minute = check_time(pot_time)
        
        # 팟이 마감이 되었고 5분 지났는 지 확인
        if schedules[i][1].ended and remain_minute <= -5:
            await schedules[i][0].delete()
            schedules.remove(schedules[i])
            i = i - 1
            continue
        
        # 끝난 팟이 아니면 남은 시간 확인 후 알림
        if remain_minute == 60 or remain_minute == 30 or remain_minute == 10 or remain_minute == 5: # 60/30/15/10/5분 전
            # msg = await message.channel.send(embed=embed)
            # 해당 메시지 embed 가져와서
            embed = make_pot_embed(schedules[i][1])
            # schedules[i][0].embeds[0]
            # 팟 마감 남은시간 메시지 추가하고
            content = "팟이 " + str(check_time(pot_time)) + "분 후에 마감돼요!"
            
            # 메시지를 보낸 다음에
            new_msg = await schedules[i][0].channel.send(content = content,embed=embed)
            # 기존 메시지 삭제
            await schedules[i][0].delete()
            # 기존 메시지에 들어가는 곳에 new_msg로 갈아끼우기
            schedules[i][0] = new_msg
            
        elif remain_minute == 0 and not schedules[i][1].ended: # 마감!!
            # 해당 메시지 embed 가져와서
            embed = make_ended_pot_embed(schedules[i][1])
            # 팟 마감 남은시간 메시지 추가하고
            content = "팟이 마감되었어요!\n메시지는 5분 후 사라져요!"
            # 메시지를 보낸 다음에
            new_msg = await schedules[i][0].channel.send(content=content, embed=embed)
            # await new_msg.add_reaction("👍")
            # 기존 메시지 삭제
            await schedules[i][0].delete()
            # 기존 메시지에 들어가는 곳에 new_msg로 갈아끼우기
            schedules[i][0] = new_msg
            # 마감 되었다고 상태 바꾸기
            schedules[i][1].ended = True

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