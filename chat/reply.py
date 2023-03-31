
# -*- coding: utf-8 -*-#
# filename: reply.py
import time
import urllib.request
import json

class Msg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = "self.rasa_serve(content.decode('utf-8'))"

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        print("***************XML:"+ XmlForm)
        return XmlForm.format(**self.__dict)

    def rasa_serve(self,content):
        connection = urllib.request.http.client.HTTPConnection('39.98.39.18:9098') # 端口看你的需求进行修改
        values = {
        "sender": "Rasa",
        "message": content
        }
        json_foo = json.dumps(values)
        connection.request('POST', '/webhooks/rest/webhook', json_foo)
        response = connection.getresponse()
        res = (response.read().decode("utf-8"))
        res = json.loads(res)
        for i in res:
            return i['text']
        return '亲，已经为你转接人工客服，请耐心等候！'

class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Image>
            </xml>
            """
        return XmlForm.format(**self.__dict)
