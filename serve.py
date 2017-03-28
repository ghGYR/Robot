# coding=utf8
import sys
sys.path.append("../itchat/")
from itchat.content import *
import itchat
from msg_pro import*

msgpro = {
    TEXT: Text_pro,
    PICTURE: Picture_pro,
    VIDEO: Video_pro,
    NOTE: Note_pro,
    SHARING: Other_pro,
    RECORDING: Other_pro,
    VOICE: Other_pro,
    ATTACHMENT: Other_pro,
    FRIENDS: Other_pro,
    SYSTEM: Other_pro}
# 私聊
@itchat.msg_register(INCOME_MSG, isFriendChat=True)
def friendChat_pro(msg):
    # 获得发送者昵称(包括手机端自己)
    friend = itchat.search_friends(userName=msg.FromUserName)
    friendname = msg.FromUserName if friend is None else friend["NickName"]
    # 获取私聊名
    if friendname == myName:
        filename = itchat.search_friends(userName=msg.ToUserName)["NickName"]
    else:
        filename = friendname
    # 处理消息
    message, response = msgpro[msg.type](msg, friendname, filename)
    # 打印消息
    print("%s##%s" % (friendname, message))
    # 保存收到的消息
    SaveMessage("friends/" + filename, friendname + "##" + message)
    # 保存回复的消息
    if response is not None:
        SaveMessage("friends/" + filename, "auto-" + myName + "##" + response)
    return response


# 群聊
@itchat.msg_register(INCOME_MSG, isGroupChat=True)
def GroupChat_pro(msg):
    # 获得群聊名
    Room = itchat.search_chatrooms(userName=msg.FromUserName)
    RoomName = msg.FromUserName if Room is None else Room["NickName"]
    # 获得发送者昵称（包括手机端自己）
    who = msg.ActualNickName
    # 处理消息
    message, response = msgpro[msg.type](msg, who, RoomName)
    # 打印消息
    print("%s@%s##%s" % (RoomName, who, message))
    # 保存收到的消息
    SaveMessage("groups/" + RoomName, who + "##" + message)
    # 保存回复的消息
    if response is not None:
        SaveMessage("groups/" + RoomName, "auto-" + myName + "##" + response)
    return response


# 登陆
itchat.auto_login(enableCmdQR=True, hotReload=True, statusStorageDir='cache.pkl')
# 运行
myName = itchat.search_friends()["NickName"]
itchat.run(debug=True)


# 解析消息，来自哪里
# 自动回复
# 实现获取消息来源，是否为群消息，来自哪里，是否@我，是否为图片，表情，其它消息定义
# 群里每天打招呼
# 发红包，投食，然后可以干一项事情，心情好的话，可以不用。
# 积累语料
# 指定命令的功能，如查询天气，歌曲推荐，新闻时讯，消息提醒
# 表情包，高兴，生气，不感兴趣，卖萌，猥琐。。。。。。
# 消息保存，按房间
# 根据联系人建立好感度
# 好感度与对话数量，投食数量（红包，骨头），（夸奖，责骂）有关系，影响互动效果
# 个人状态与心情和生理状态有关
