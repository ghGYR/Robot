# 设置用户类
import json
import multiprocessing


class User():

    def __init__(self, username, userid, ChatParames={}):
        self.userid = userid
        self.username = username
        # 服务参数表
        self.ChatParames = ChatParames if type(ChatParames) is dict else {}


# 定义机器人属性
class Robot(multiprocessing.Process):

    def __init__(self):
        super(multiprocessing.Process, self).__init__()
        self.UserList = {}
        self.GroupParames = {}
        self.load("info.json")
        self.ServeFunList = {}

    # 设置用户参数

    def SetUser(self, UserName, userid, ChatParames={}):
        user = User(UserName, userid, ChatParames)
        self.UserList[UserName] = user
        self.SaveChange()
    # 查询用户参数

    def GetUser(self, UserName):
        if UserName not in self.UserList.keys():
            print(UserName, "#Not in UserList, Need to set:")
            userid = input("userid:")
            print("set serve parames in this chat:")
            ChatParames = {}
            ChatParames[self.Chat] = {}
            for serve in self.ServeFunList.keys():
                parames = int(input(serve + ":"))
                ChatParames[self.Chat][serve] = parames
            self.SetUser(UserName, userid, ChatParames)
        return self.UserList[UserName]
    # 注册服务功能

    def register_ServeFun(self, Serve_name):
        print("Adding Serve Function:", Serve_name)

        def wraper(fun):
            self.ServeFunList[Serve_name] = fun
            return fun
        print("Done")
        return wraper

    # 注册服务解析
    def Register_ServeAnaly(self):
        print("Register Serve Analy Function")

        def wrapper(fun):
            self.GetServeName = fun
            return fun
        return wrapper

    # 服务
    def MsgProExcute(self, Chat, UserName, Msg):
        # 当前所在的聊天环境,即处理环境
        self.Chat = Chat
        # 服务对象
        self.user = self.GetUser(UserName)
        # 解析服务
        serve_List = self.GetServeName(Msg)
        # print(serve_List)
        # 执行服务
        for serve_name in serve_List:
            if serve_name in self.ServeFunList.keys():
                fun = self.ServeFunList[serve_name]
                fun(Msg)

    def SetGroupParames(self, Chat, name, parame):
        if Chat not in self.GroupParames.keys():
            self.GroupParames[Chat] = {}
        self.GroupParames[Chat][name] = parame
        self.SaveChange()

    def GetGroupParames(self, Chat, name):
        if Chat not in self.GroupParames.keys():
            parame = int(input("set parames [%s][%s]" % (Chat, name)))
            self.SetGroupParames(Chat, name, parame)
        elif name not in self.GroupParames[Chat].keys():
            parame = int(input("set parames [%s][%s]" % (Chat, name)))
            self.SetGroupParames(Chat, name, parame)
        return self.GroupParames[Chat][name]
    # 获取服务参数

    def GetParames(self, user, Chat, FunName):
        if Chat in user.ChatParames.keys():
            if FunName not in user.ChatParames[Chat].keys():
                user.ChatParames[Chat][FunName] = int(input("set parames[%s[[%s][%s]" % (user.username, Chat, FunName)))
                self.SaveChange()
        else:
            user.ChatParames[Chat] = {}
            user.ChatParames[Chat][FunName] = int(input("set parames[%s[[%s][%s]" % (user.username, Chat, FunName)))
            self.SaveChange()
        return user.ChatParames[Chat][FunName]

    def SaveChange(self):
        user_info = []
        for user in self.UserList.values():
            info = [user.username, user.userid, user.ChatParames]
            user_info.append(info)
        robot_info = [user_info, self.GroupParames]
        # print(robot_info)
        with open("info.json", "w") as f:
            json.dump(robot_info, f)

    def load(self, file):
        try:
            print("import configure info")
            with open(file, "r", encoding='utf-8') as f:
                robot_info = json.load(f)
            user_info = robot_info[0]
            self.GroupParames = robot_info[1]
            for user in user_info:
                # print(user)
                self.UserList[user[0]] = User(user[0], user[1], user[2])
        except:
            print("No init configure info")
