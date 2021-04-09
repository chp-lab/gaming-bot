# -- coding: utf-8 --

from flask_restful import Resource
from flask import request
import requests
from database import Database
from module import Module

class Hooking(Resource):
    onechat_uri = "https://chat-api.one.th"
    onechat_dev_token = "Bearer Af58c5450f3b45c71a97bc51c05373ecefabc49bd2cd94f3c88d5b844813e69a17e26a828c2b64ef889ef0c10e2aee347"
    onechat_url1 = onechat_uri + '/message/api/v1/push_quickreply'
    def menu_send(self, user_id, bot_id):
        TAG = "menu_send:"
        # web_vue_url1 = "https://web-meeting-room.herokuapp.com/"
        web_vue_url1 = "https://onesmartaccess.herokuapp.com/"
        req_body = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "ให้ช่วยอะไรดี",
            "quick_reply":
                [
                    {
                        "label": "อัพเดทโปรไฟล์",
                        "type": "text",
                        "message": "ขออัพเดทโปรไฟล์หน่อยครับ",
                        "payload": "profile_update"
                    }
                ]
        }
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        result = requests.post(self.onechat_url1, json=req_body, headers=headers)
        print(TAG, result.text)
    def send_msg(self, one_id, reply_msg):
        TAG = "send_msg:"
        bot_id = "B37913f508a675e7db24970fdb7c191f8"
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        payload = {
            "to": one_id,
            "bot_id": bot_id,
            "type": "text",
            "message": reply_msg,
            "custom_notification": "เปิดอ่านข้อความใหม่จากทางเรา"
        }
        r = requests.post(self.onechat_uri + "/message/api/v1/push_message", headers=headers, json=payload)
        # self.menu_send(one_id, bot_id)
        return r

    def is_user_exist(self, one_email):
        TAG = "is_user_exist:"
        cmd = """SELECT users.one_email FROM users WHERE users.one_email='%s' """ %(one_email)
        database = Database()
        res = database.getData(cmd)
        print(TAG, "res=", res)
        if(res[0]['len'] > 0):
            return True
        else:
            return False

    def add_new_user(self, email, name, one_id):
        TAG = "add_new_user:"
        database = Database()
        print(TAG, "add user to our system")
        sql = """INSERT INTO `users` (`one_email`, `name`, `one_id`) VALUES ('%s', '%s', '%s')""" \
              % (email, name, one_id)
        insert = database.insertData(sql)
        return insert

    def post(self):
        TAG = "Hooking:"
        module = Module()
        
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)

        if("event" not in data):
            return {
                "type": True,
                "message": "success",
                "elapsed_time_ms": 0,
                "len": 0,
                "result": "testing"
            }
        
        # auth_token = "6dN6MBba5Uw1TwmJfX9jX1vtKDnHUawY73n&D7KQzcGo.fSAUa&jsp)sWrD@Qd4Q"
        
        # auth_key = "Authorization"
        # if(auth_key not in request.headers):
        #     return module.unauthorized()
        # recv_auth = request.headers.get("Authorization")
        # if(recv_auth != "Bearer " + auth_token):
            # return module.unauthorized()
        

        database = Database()
        module = Module()
        onechat_uri = self.onechat_uri
        data = request.json
        onechat_dev_token = "Bearer Af58c5450f3b45c71a97bc51c05373ecefabc49bd2cd94f3c88d5b844813e69a17e26a828c2b64ef889ef0c10e2aee347"
        # qr_code_api = "https://api.qrserver.com/v1/create-qr-code/"
        headers = {"Authorization": onechat_dev_token}

        print(TAG, "data=", data)
        print(TAG, request.headers)
        if(data['event'] == "message"):
            bot_id = data['bot_id']
            user_id = data['source']['user_id']
            email = data['source']['email']
            one_id = data['source']['one_id']
            name = data['source']['display_name']
            user_exist = self.is_user_exist(email)
            # real is user_exist
            # edit line bellow
            if(user_exist):
                print(TAG, "user exist!")
            else:
                print(TAG, "usr not exist!")
                # self.send_msg(one_id, "คุณเพศอะไร")
                req_body = {
                    "to": user_id,
                    "bot_id": bot_id,
                    "message": "คุณเพศอะไร",
                    "quick_reply":
                        [
                            {
                                "label": "ชาย",
                                "type": "text",
                                "message": "ผู้ชายครับ",
                                "payload": {"gen": "man"}
                            },
                            {
                                "label": "หญิง",
                                "type": "text",
                                "message": "ผู้หญิงค่ะ",
                                "payload": {"gen": "woman"}
                            },
                            {
                                "label": "ไม่ระบุ",
                                "type": "text",
                                "message": "ไม่ระบุ",
                                "payload": {"gen": "not_specified"}
                            }
                        ]
                }
                headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
                result = requests.post(self.onechat_url1, json=req_body, headers=headers)
                print(TAG, result.text)

                return {
                    "type": True,
                    "message": "testing",
                    "elapsed_time_ms": 0,
                    "len": 0,
                    "result": "testing"
                }

            print(TAG, "bot_id=", bot_id)
            print(TAG, "user_id=", user_id)


        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
