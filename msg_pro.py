# coding=utf8
from robot import*

# 不同类型的消息处理

# user用户名，服务权限
UsersLists = {"GYR": user("owner", [1, 1]), "Gavin": user("friend1", [0, 1]), "others": user("others", [0, 0])}
Dog = Robot(UsersLists)


def Text_pro(msg, UserName, Group):
    message = msg.Text
    # 针对不同人和不同聊天环境处理不同消息
    # 如果定制了服务的
    if UserName in Dog.UserLists.keys():
        response = Dog.Serve(Group, UserName, message)
    # 未定制服务的
    else:
        response = Dog.Serve(Group, "others", message)
    return message, response


def Picture_pro(msg, user, Group):
    # print(msg)
    message = "Picture:" + msg.FileName
    msg.Text("../data/image/" + msg.FileName)
    num = random.randint(1, 20)
    response = '@%s@%s' % ('img', "../data/face_img/images/face_" + str(num) + ".gif")
    return message, response


def Video_pro(msg, user, Group):
    # print(msg)
    message = "Video:" + msg.FileName
    msg.Text("../data/video/" + msg.FileName)
    num = random.randint(1, 20)
    response = '@%s@%s' % ('img', "../data/face_img/images/face_" + str(num) + ".gif")

    return message, response


def Note_pro(msg, user, Group):
    message = "Note:" + msg.Text
    num = random.randint(1, 20)
    response = '@%s@%s' % ('img', "../data/face_img/images/face_" + str(num) + ".gif")
    return message, response


def Other_pro(msg, user, Group):
    return msg.type, "receive"


# 工具
def SaveMessage(filename, Message):
    Path = "../data/messages/"
    Format = ".txt"
    with open(Path + filename + Format, "a", encoding='utf-8') as f:
        f.write(Message + "\n")

# 用户权限
# 管理员权限 100 可以控制机器人在全局和局部环境下的权限
# 用户权限 50可以控制机器人在局部环境下的权限



