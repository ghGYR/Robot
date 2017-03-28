import requests
import json
import random


def Turning(message, userid):
    url = "http://www.tuling123.com/openapi/api"
    print(message, " ", userid)
    payload = {"key": "c8500f7e1a344755b0eefcbddc21f770", "info": message, "userid": userid}
    r = requests.post(url, data=payload)
    re = json.loads(r.text)
    print(re)
    furl = re.get("url")
    if furl is not None:
        pic = download(furl)
        return re['text'] + furl
    return re['text']


def download(furl):
    r = requests.get(furl)
    print(r.text)


# 设置用户类9
class user():

    def __init__(self, userid, authority):
        self.userid = userid
        # 服务权限
        self.GroupAuthority = {}
        self.authority = authority
    # 查询权限

    def GetAuthority(self, Group):
        # 查看是否有权限，否则赋值权限
        if Group not in self.GroupAuthority.keys():
            # 默认在该聊天环境下各项指令服务的权限
            self.GroupAuthority[Group] = {"isTalk2sb": self.authority[0], "chatting": self.authority[1]}

        return self.GroupAuthority[Group]


# 定义机器人属性
class Robot():

    def __init__(self, UserLists):
        self.serveList = {"isTalk2sb": self.isTalk2sb, "chatting": self.chatting}
        self.group = u"GYR"
        self.user = u"GYR"
        self.UserLists = UserLists

    # 服务控制
    def Serve(self, group, username, message):
        # 当前所在的聊天环境,即服务环境
        self.group = group
        # 服务对象
        self.user = self.UserLists[username]
        # 解析服务
        serve_name, serve_parames = self.analy(message)
        # 查看在当前聊天环境下的授权
        authority = self.user.GetAuthority(self.group)[serve_name]
        # 若获得服务授权就服务，否则停止服务，返回服务结果
        response = self.serveList[serve_name](serve_parames) if authority == 1 else self.RandomResponse()
        return response
 
    #   命令解析
    def analy(self, message):
        if message == u"不要说话":
            serve_name = "isTalk2sb"
            serve_parames = [0, self.UserLists.keys()]
        elif message == u"可以说话":
            serve_name = "isTalk2sb"
            serve_parames = [1, self.UserLists.keys()]
        else:
            serve_name = "chatting"
            serve_parames = message

        return serve_name, serve_parames

    # 具体服务
    # 聊天权限修改
    def isTalk2sb(self, serve_parames):
        for user in serve_parames[1]:
            ob = self.UserLists[user]
            if self.group not in ob.GroupAuthority.keys():
                ob.GroupAuthority[self.group] = {"isTalk2sb": ob.authority[0], "chatting": serve_parames[0]}
            else:
                ob.GroupAuthority[self.group]["chatting"] = serve_parames[0]
        # 从语料库中通过一定原则选取丰富的语料回答,可以是图片也可以是语言，以情绪和场景分类
        return "Roger"
    # 聊天服务

    def chatting(self, message):
        response = Turning(message, self.user.userid)
        return response

    def RandomResponse(self):
        num = random.randint(10, 40)
        response = '@%s@%s' % ('img', "../data/face_img/images/face_" + str(num) + ".gif")
        return response
