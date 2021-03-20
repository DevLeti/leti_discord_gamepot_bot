class schedule:
    def __init__(self, who = "Jone Doe", when = "200011311230", what = "lol", participant = []):
        self.who = who # 누가 팟을 잡았는지, str
        self.when = when # 언제 팟이랑 게임을 할지, str = "yyyymmddhhmm"
        self.what = what # 무슨 게임을 할지, str
        self.participant = participant # 누가 같이 할지 = ["유저디스코드id값"]
    
    # Setter
    def setter(self, who, when, what, participant):
        self.who = who # 누가 팟을 잡았는지, str
        self.when = when # 언제 팟이랑 게임을 할지, str = "yyyymmddhhmm"
        self.what = what # 무슨 게임을 할지, str
        self.participant = participant # 누가 같이 할지 = ["유저디스코드id값"]
    def set_who(self, name):
        self.who = name
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
    def get_who(self):
        return self.who
    def get_when(self):
        return self.when
    def get_what(self):
        return self.what
    def get_participant(self):
        return self.participant
    
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