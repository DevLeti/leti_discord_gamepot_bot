import datetime
import user_custom

class schedule:
    def __init__(self, who = user_custom.user(), when = datetime.datetime.today(), what = "lol", ended = False):
        self.who = who # 누가 팟을 잡았는지, str
        self.when = when # 언제 팟이랑 게임을 할지, datime.datetime
        self.what = what # 무슨 게임을 할지, str
        self.participant = [] # 누가 같이 할지 = ["user 클래스 인스턴스"]
        self.ended = ended # 마감 여부 = False
    
    # Setter
    def setter(self, who, when, what, participant):
        self.who = who # 누가 팟을 잡았는지, str
        self.when = when # 언제 팟이랑 게임을 할지, str = "yyyymmddhhmm"
        self.what = what # 무슨 게임을 할지, str
        self.participant = participant # 누가 같이 할지 = ["유저디스코드id값"]
    def set_who(self, user_type):
        self.who = user_type
        return True
    def set_when(self, when):
        self.when = when
        return True
    def set_what(self, what):
        self.what = what
        return True
    def set_participant(self, participant):
        self.participant = participant
        return True
    def set_ended(self, ended):
        self.ended = ended
        return True
    
    # Getter
    def getter(self):
        return self
    def who(self):
        return self.who
    def name(self):
        return self.who.name
    def d_id(self):
        return self.who.d_id
    def when(self):
        return self.when
    def what(self):
        return self.what
    def participant(self):
        return self.participant
    def ended(self):
        return self.ended
    def display_participant(self):
        print("display_participant 진입")
        participant_list = ""
        p_size = len(self.participant)
        if(p_size == 0):
            participant_list = "아무도 없어요!"
        else:
            for i in range(0, p_size):
                participant_list = participant_list + self.participant[i].name
                if(i != p_size - 1):
                    participant_list = participant_list + ', '
        print(participant_list)
        return participant_list
            
    # 참여자 추가
    def add_participant(self, new_participant): # new_participant = user타입 인스턴스
        if not self.ended:
            for i in range(0,len(self.participant)) :
                if(new_participant.d_id == self.participant[i].d_id):
                    print("이미 있음")
                    return False
            self.participant.append(new_participant)
            return True
        else:
            print("팟 마감으로 추가 불가")
    
    def delete_participant(self, delete_participant): # delete_participant = user타입 인스턴스
        if not self.ended:
            #delete_participant의 값은 디스코드id
            for i in range(0,len(self.participant)) :
                if(delete_participant.d_id == self.participant[i].d_id):
                    del self.participant[i]
                    return True
            return False # 참여자에 제거할 사람이 없음
        else:
            print("팟 마감으로 제거 불가")
            return False