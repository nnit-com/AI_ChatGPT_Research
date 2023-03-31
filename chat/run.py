# -*- coding:utf-8 -*-
from flask import Flask
import pymysql
from flask import request, make_response
import hashlib
import sys
import receive
import reply
from WXBizMsgCrypt import WXBizMsgCrypt
import xml.etree.cElementTree as ET

app = Flask(__name__)

def sqlmsg(content):
    conn = pymysql.connect(
    host='39.98.39.18',
    port=3306,
    user='root',
    password='123456',
    database='rasa',
    charset='utf8'
    )
    # 获取一个光标
    cursor = conn.cursor()
    # 定义要执行的sql语句
    sql = 'insert into wechat(chat_content) values(%s);' 
    cursor.execute(sql, content)
    # 涉及写操作要注意提交
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    
@app.route("/")
def index():
    return "Hello World!"

@app.route("/wx", methods=["GET","POST"])
def weixin():
    sToken = 'iU2wMZWBgmGQU8mDpqfdBaNNz'
    sEncodingAESKey = 'MlWb4obghrqNgDqIC2DbnKX9NWrCxKRuAMp1HvH5OkU'
    sCorpID = 'ww91aa925a70a7121b'
    wxcpt = WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
    #获取url验证时微信发送的相关参数
    sVerifyMsgSig=request.args.get('msg_signature')
    sVerifyTimeStamp=request.args.get('timestamp')
    sVerifyNonce=request.args.get('nonce')
    sVerifyEchoStr=request.args.get('echostr')

    #验证url
    if request.method == 'GET':
        ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
        if (ret != 0 ):
            print("ERR: VerifyURL ret:" + str(ret)) 
            sys.exit(1)
        return make_response(sEchoStr) 
    #接收客户端消息
    else:
        sReqData = request.stream.read().decode('utf-8')
        print("***************post data: "+str(sReqData))
        ret,sMsg=wxcpt.DecryptMsg(sReqData,sVerifyMsgSig,sVerifyTimeStamp,sVerifyNonce)
        print("***************post data after parse:"+str(sMsg))
        if (ret != 0):
             print("ERR: VerifyURL ret: "+str(ret))
             sys.exit(1)
        
        recMsg = receive.parse_xml(sMsg)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = recMsg.Content
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            #sqlmsg(content)
            sRespData = replyMsg.send()
            print("***************send data before encrypt:"+str(sMsg))
            ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sVerifyNonce, sVerifyTimeStamp)
            print("***************send data after encrypt:"+str(sMsg))
            return sEncryptMsg
        else:
            print ("暂且不处理")
            return "success"
     
        # xml_tree = ET.fromstring(sMsg)
        # content = xml_tree.find("Content").text
        # #被动响应消息，将微信端发送的消息返回给微信端
        # sRespData = '''<xml>
        #                 <ToUserName><![CDATA[mycreate]]></ToUserName>
        #                 <FromUserName><![CDATA[wx177d1233ab4b730b]]></FromUserName>
        #                 <CreateTime>1348831860</CreateTime>
        #                 <MsgType><![CDATA[text]]></MsgType>
        #                 <Content><![CDATA[''' +content +''']]></Content>
        #                 <MsgId>1234567890123456</MsgId>
        #                 <AgentID>1000009</AgentID>
        #                 </xml>'''
        # ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sVerifyNonce, sVerifyTimeStamp)
        # if( ret!=0 ):
        #         print("post ERR: VerifyURL ret:" + str(ret)) 
        #         sys.exit(1)
        # return sEncryptMsg
       


#         # srecMsg = receive.parse_xml(sMsg)
#         if isinstance(recMasg, receive.Msg) and recMsg.MsgType == 'text':
#              sRespData = "<xml><ToUserName>ww1436e0e65a779aee</ToUserName><FromUserName>ChenJiaShun</FromUserName><CreateTime>1476422779</CreateTime><MsgType>text</MsgType><Content>你好</Content><MsgId>1456453720</MsgId><AgentID>1000002</AgentID></xml>"
#    ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
#    if( ret!=0 ):
#       print "ERR: EncryptMsg ret: " + str(ret)
#       sys.exit(1)

            # return recMsg
            # toUser = recMsg.FromUserName
            # fromUser = recMsg.ToUserName
            # content = recMsg.Content
            # replyMsg = reply.TextMsg(toUser, fromUser, content)
            # return replyMsg.send()
        # else:
        #     print ("暂且不处 ?)
        #     return "success"

if __name__ == "__main__":
    app.run(
      host='0.0.0.0',
      port= 9099,
      debug=False
    )

