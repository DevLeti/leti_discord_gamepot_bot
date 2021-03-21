import datetime
import user

class schedule:
    def __init__(self, who = user.user(), when = datetime.datetime.today(), what = "lol", participant = []):
        self.who = who # 누가 팟을 잡았는지, str
        self.when = when # 언제 팟이랑 게임을 할지, str = "yyyymmddhhmm"
        self.what = what # 무슨 게임을 할지, str
        self.participant = participant # 누가 같이 할지 = ["user 클래스 인스턴스"]
    
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
    def display_participant(self):
        participant_list = ""
        print("참여자 : ",end="")
        p_size = len(self.participant)
        for i in range(0, p_size):
            participant_list = participant_list + self.participant[i].name
            print(self.participant[i].name,end="")
            if(i != p_size - 1):
                participant_list = participant_list + ', '
                print(", ",end="")
            
    # 참여자 추가
    def add_participant(self, new_participant):
        if(new_participant in self.participant):
            return False
        else:
            self.participant.append(new_participant)
            return True
    
    def delete_participant(self, delete_participant):
        #delete_participant의 값은 디스코드id
        if(delete_participant in self.participant):
            self.participant.remove(self.participant.index(delete_participant))
            return True 
        else:
            return False # 참여자에 제거할 차람 없음