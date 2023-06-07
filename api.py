import json
import requests

import cipher

BASE_URL = r"https://kmsvip.xyz"
cookie = {}
proxy = {}


class APIError(Exception):  # Thanks, ChatGPT
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"API Error {self.code}: {self.message}"


def post(url: str, data: dict = None) -> dict:
    if data is None:
        data = "undefined"
    else:
        data = json.dumps(data)
    encrypted_data = cipher.encrypt(data)
    rsp = requests.post(
        url=BASE_URL + url,
        data={
            "data": encrypted_data,
            "sig": cipher.signature(encrypted_data)
        },
        cookies=cookie,
        proxies=proxy
    ).text
    rsp = json.loads(cipher.decrypt(rsp))
    if rsp["code"] == 0:
        return rsp["data"]
    else:
        raise APIError(rsp["code"], rsp["message"])


def setCookie(cookies: dict):
    global cookie
    cookie = cookies


def setProxy(proxies: dict):
    global proxy
    proxy = proxies


def getIndex() -> dict:
    """
    获取社交媒体及备用地址等多个网站URL。

    :return 网站URL，返回示例详见Readme
    """
    return post("/api/domain/index")


def getHotList(page: int, perPage: int = 7) -> dict:
    """
    获取热门视频列表。

    :param page: 获取第几页
    :param perPage: 一页上显示多少个项目；即返回多少个视频，默认为7
    :return: 热门视频列表，返回示例详见Readme；请注意除了返回perPage个视频外，还会返回一个广告
    """
    return post("/api/videos/listHot", {
        "page": page,
        "perPage": perPage
    })


def getAllList(page: int, perPage: int = 7) -> dict:
    """
    获取视频广场列表。

    :param page: 获取第几页
    :param perPage: 一页上显示多少个项目；即返回多少个视频，默认为7
    :return: 热门视频列表，返回示例详见Readme；请注意除了返回perPage个视频外，还会返回一个广告
    """
    return post("/api/videos/listAll", {
        "page": page,
        "perPage": perPage
    })


def getCenterList() -> dict:
    """
    获取系统公告列表。

    :return: 系统公告列表，返回示例详见Readme
    """
    return post("/api/notice/listCenter")


def getDetail(mvId: str, uId: str = "12345", type: int = 0) -> dict:
    """
    获取视频详细信息。

    :param mvId: 视频ID，即视频对象里的mv_id
    :param uId: 当前登录用户ID，未登录可留空
    :param type: 未知，默认为0
    :return: 视频详细信息，返回示例详见Readme
    """
    return post("/api/videos/detail", {
        "uId": uId,
        "mvId": mvId,
        "type": type
    })


def getCommentsList(mvId: str, page: int) -> dict:
    """
    获取视频评论列表。

    :param mvId: 视频ID，即视频对象里的mv_id
    :param page: 获取第几页
    :return: 视频评论列表，一次最多返回20个，返回示例详见Readme
    """
    return post("/api/community/listComments", {
        "mvId": mvId,
        "page": page
    })


def videoLike(mvId: str) -> dict:
    """
    给视频点赞。

    :param mvId: 视频ID，即视频对象里的mv_id
    :return: 成功返回空列表，失败抛出异常
    """
    return post("/api/community/videoLike", {
        "mvId": mvId
    })


def videoCollect(mvId: str, uId: str) -> dict:
    """
    收藏视频。

    :param mvId: 视频ID，即视频对象里的mv_id
    :param uId: 当前登录用户ID
    :return: 成功返回空列表，失败抛出异常
    """
    return post("/api/community/videoCollect", {
        "mvId": mvId,
        "uId": uId
    })


def subscribeUser(uId: str, subscribeId: str) -> dict:
    """
    关注用户。

    :param uId: 当前登录用户ID
    :param subscribeId: 要关注的用户ID
    :return: 成功返回空列表，失败抛出异常
    """
    return post("/api/community/attentionUser", {
        "uId": uId,
        "attentionId": subscribeId
    })


def addComment(mvId: str, uId: str, mcText: str) -> dict:
    """
    在视频下方评论。

    :param mvId: 视频ID，即视频对象里的mv_id
    :param uId: 当前登录用户ID
    :param mcText: 评论内容
    :return: 评论详细信息，返回示例详见Readme
    """
    return post("/api/community/addComment", {
        "mvId": mvId,
        "uId": uId,
        "mcText": mcText
    })


def userRegister(email: str, password: str, name: str) -> dict:
    """
    注册账号。

    :param email: 电子邮箱
    :param password: 密码，有意思的是它是明文传输的：）
    :param name: 昵称
    :return: 账号信息，请注意返回内容需要经过URLEncode后添加进cookie中logindata键值对
    """
    return post("/api/users/register", {
        "email": email,
        "password": password,
        "name": name
    })


def userLogin(email: str, password: str) -> dict:
    """
    登录账号。

    :param email: 电子邮箱
    :param password: 密码，有意思的是它是明文传输的：）
    :return: 账号信息，请注意返回内容需要经过URLEncode后添加进cookie中logindata键值对
    """
    return post("/api/users/login", {
        "email": email,
        "password": password,
    })


def editPassword(uId: str, password: str, nPassword: str, rePassword: str = None) -> dict:
    """
    更改账号密码。

    :param uId: 当前登录用户ID
    :param password: 旧密码
    :param nPassword: 新密码
    :param rePassword: 重复输入新密码，可不填
    :return: 账号信息，请注意返回内容需要经过URLEncode后添加进cookie中logindata键值对
    """
    if rePassword is None:
        rePassword = nPassword
    return post("/api/users/editPsd", {
        "uId": uId,
        "password": password,
        "nPassword": nPassword,
        "rePassword": rePassword
    })


def feedback(uId: str, mfText: str) -> dict:
    """
    发送反馈。

    :param uId: 当前登录用户ID
    :param mfText: 反馈文本内容
    :return: 成功返回空列表，失败抛出异常
    """
    return post("/api/users/feedback", {
        "uId": uId,
        "mfText": mfText,
        "ip": "127.0.0.1",
        "mfDeviceid": "pc"
    })


def getUserInfo(uId: str, page: int, perPage: int = 12, meId: str = "12345") -> dict:
    """
    获取用户信息。

    :param uId: 想要获取的用户ID
    :param page: 获取第几页
    :param perPage: 一页上显示多少个项目；即返回多少个视频，默认为12
    :param meId: 当前登录用户ID，未登录可留空
    :return: 用户信息详细信息，返回示例详见Readme
    """
    return post("/api/users/getUserInfo", {
        "uId": uId,
        "page": page,
        "perPage": perPage,
        "meId": meId
    })


def getVideoCollectList(uId: str, page: int, perPage: int = 12) -> dict:
    """
    获取收藏夹。

    :param uId: 当前登录用户ID
    :param page: 获取第几页
    :param perPage: 一页上显示多少个项目；即返回多少个视频，默认为12
    :return: 收藏夹详细信息，返回示例详见Readme
    """
    return post("/api/community/videoCollectList", {
        "uId": uId,
        "page": page,
        "perPage": perPage
    })


def getSubscribeList(uId: str, page: int, perPage: int = 10) -> dict:
    """
    获取关注列表。

    :param uId: 当前登录用户ID
    :param page: 获取第几页
    :param perPage: 一页上显示多少个项目；即返回多少个项目，默认为10
    :return: 关注列表详细信息，返回示例详见Readme
    """
    return post("/api/community/attentionList", {
        "uId": uId,
        "page": page,
        "perPage": perPage
    })
