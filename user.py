class user:
    #d_id = discord 고유 d_id
    #name = discord에 설정된 nickname
    def __init__(self, name = "Jone Doe", d_id = "415465528178507776"):
        self.name = name # 언제 팟이랑 게임을 할지, str = "yyyymmddhhmm"
        self.d_id = d_id # 누가 팟을 잡았는지, str
    
    # Setter
    def setter(self, name, d_id):
        self.name = name # 언제 팟이랑 게임을 할지, str = "yyyymmddhhmm"
        self.d_id = d_id # 누가 팟을 잡았는지, str
    def set_d_id(self, d_id):
        self.d_id = d_id
        return True
    def set_name(self, name):
        self.name = name
        return True

    # Getter
    def getter(self):
        return self
    def d_id(self):
        return self.d_id
    def name(self):
        return self.name
    
    def display_info(self):
        print("user_name = {}".format(self.name))
        print("discord_id = {}".format(self.d_id))