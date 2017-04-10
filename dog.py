from robot import*
from function import *
from random import random
import os
import re
import sys
sys.path.append("../itchat/")
import itchat
# 生成机器人
dog = Robot()


# 注册功能
@dog.Register_ServeAnaly()
# 注册message到serve的解析服务
def SeverAanly(Msg):
    if Msg.text == "查看我的服务":
        return ["SaveMessage", "Look Info"]
    if Msg.text in ["不要说话", "说话", "别说话", "不要开腔", "可以说话"]:
        return ["SaveMessage", "Talk_Consol"]
    elif Msg. type == "Text":
        return ["SaveMessage", "CHAT"]
    elif Msg.type == "Picture" or Msg.type == "Video" or Msg.type == "Recording":
        return ["SaveMessage", "Download"]
    else:
        return []


@dog.register_ServeFun("CHAT")
def chatting(Msg):
    chat_random = dog.GetParames(dog.user, dog.Chat, "CHAT")
    is_talk = dog.GetGroupParames(dog.Chat, "Talk")
    if is_talk < 1:
        return None
    if random() <= chat_random / 100:
        if Msg.type == "Picture" or Msg.type == "Video":
            return None
        else:
            rep = Turning(Msg.text, dog.user.userid)
            print("reponse to%s@%s#%s" % (dog.Chat, dog.user.username, rep))
            itchat.send(rep, Msg['FromUserName'])
            saveresponse("reponse to@%s#%s" % (dog.user.username, rep))
    return None


@dog.register_ServeFun("Download")
def Download(Msg):
    Authority = dog.GetParames(dog.user, dog.Chat, "Download")
    if Authority == 1:
        if Msg.type == "Picture":
            path = "../data/image"
        elif Msg.type == "Video":
            path = "../data/video"
        elif Msg.type == "Recording":
            path = "../data/voice"
        if not os.path.exists(path):
            print("创建文件目录")
            os.makedirs(path)
        Msg.Text(path + "/" + Msg.FileName)
    else:
        print("No download Authority")
    return None


@dog.register_ServeFun("SaveMessage")
def SaveMessage(Msg):
    Authority = dog.GetParames(dog.user, dog.Chat, "SaveMessage")
    if Authority == 1:
        path = "../data/messages"
        if not os.path.exists(path):
            print("创建对话目录")
            os.makedirs(path)
        m = Msg.Text if type(Msg.Text) is str else Msg.type
        message = dog.user.username + "##" + m
        with open(path + "/" + dog.Chat + ".txt", "a", encoding="utf-8") as f:
            f.write(message + "\n")
        print(dog.Chat + "@" + message)
    else:
        print("No Save Authority")
    return None


@dog.register_ServeFun("Look Info")
def look_info(Msg):
    Authority = dog.GetParames(dog.user, dog.Chat, "Look Info")
    if Authority == 1:
        rep = "@" + dog.user.username + ":" + str(dog.user.ChatParames[dog.Chat])
    else:
        return itchat.send("没有授权", Msg['FromUserName'])
    print("reponse to%s@%s#%s" % (dog.Chat, dog.user.username, rep))
    itchat.send(rep, Msg['FromUserName'])


@dog.register_ServeFun("Talk_Consol")
def Talk_Consol(Msg):
    Authority = dog.GetParames(dog.user, dog.Chat, "Talk_Consol")
    is_talk = dog.GetGroupParames(dog.Chat, "Talk")
    if Msg.Text in ["可以说话", "说话"]:
        if Authority == 1:
            if is_talk == 0:
                dog.SetGroupParames(dog.Chat, "Talk", 1)
                rep = "终于可以说话了，汪汪！"
            else:
                rep = "在说话啊，汪汪！"
        else:
            rep = "偏不说话，汪~"
    if Msg.Text in ["不要说话", "别说话", "不要开腔"]:
        if Authority == 1:
            if is_talk == 1:
                dog.SetGroupParames(dog.Chat, "Talk", 0)
                rep = "不说就不说嘛，汪~"
            else:
                rep = "汪~"
        else:
            rep = "偏要说话啊，汪汪！"
    print("reponse to%s@%s#%s" % (dog.Chat, dog.user.username, rep))
    itchat.send(rep, Msg['FromUserName'])
    saveresponse("reponse to@%s#%s" % (dog.user.username, rep))


def saveresponse(response):
    path = "../data/messages"
    with open(path + "/" + dog.Chat + ".txt", "a", encoding="utf-8") as f:
        f.write(response + "\n")
# print(dog.ServeFunList.keys())
