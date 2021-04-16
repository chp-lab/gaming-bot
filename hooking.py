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
                        "label": "อัพโหลดรูป",
                        "type": "text",
                        "message": "อัพโหลดรูป",
                        "payload": {"action": "image_rec"}
                    },
                    {
                        "label": "ทำความรู้จักผู้คน",
                        "type": "text",
                        "message": "มีใครโสดอยู่บ้าง",
                        "payload": {"action": "find_single"}
                    },
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

    def update_data(self, cmd):
        TAG = "update_data"
        database = Database()
        print(TAG, "cmd=", cmd)
        update = database.insertData(cmd)
        return update
    def send_quick_reply(self, one_id, req_body):
        TAG = "quick_reply"
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        result = requests.post(self.onechat_url1, json=req_body, headers=headers)
        print(TAG, result.text)

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
                self.send_msg(one_id, "สวัสดีค่ะ แนะนำตัวเองเเบื้องต้นพื่อหาผู้คนที่คุณสนใจ")
                req_body = {
                    "to": user_id,
                    "bot_id": bot_id,
                    "message": "เพศอะไร",
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

                add_user = self.add_new_user(email, name, one_id)
                print(TAG, "add=new_user=", add_user)

                return {
                    "type": True,
                    "message": "testing",
                    "elapsed_time_ms": 0,
                    "len": 0,
                    "result": "testing"
                }
                # # check that is req from INET employee
                # # covid_tk_uri = "https://api.covid19.inet.co.th/api/v1/health/"
                # # cv_token = "Bearer Q27ldU/si5gO/h5+OtbwlN5Ti8bDUdjHeapuXGJFoUP+mA0/VJ9z83cF8O+MKNcBS3wp/pNxUWUf5GrBQpjTGq/aWVugF0Yr/72fwPSTALCVfuRDir90sVl2bNx/ZUuAfA=="
                # # cv = requests.get(covid_tk_uri + one_id, headers={"Authorization": cv_token})
                # # print(TAG, "cv=", cv.json())
                # # cv_json = cv.json()
                # # print(TAG, "cv_json=", cv_json)
                # #
                # # if (cv_json["msg"] == "forbidden"):
                # #     print(TAG, "user not in our company")
                # #     # send message via bot to reject user
                # #     # api return
                # # else:
                # #     # add user to database
                # #     # process continue
                # # print(TAG, "add user to our system")
                # # sql = """INSERT INTO `users` (`one_email`, `name`, `one_id`) VALUES ('%s', '%s', '%s')""" \
                # #       % (email, name, one_id)
                # # insert = database.insertData(sql)
                # print(TAG, "insert=", insert)
                # add_user = self.add_new_user(email, name, one_id)
                # print(TAG, "add=new_user=", add_user)

            print(TAG, "bot_id=", bot_id)
            print(TAG, "user_id=", user_id)

            if('data' in data['message']):
                if("gen" in data['message']['data']):
                    gen = data['message']['data']["gen"]
                    print(TAG, "gen=", gen)
                    cmd = """UPDATE `users` SET `gender` = '%s' WHERE `users`.`one_email` = '%s'""" %(gen, email)
                    update = self.update_data(cmd)
                    print("gen update=", update)
                    self.send_msg(one_id, "อายุเท่าไหร่")
                elif("interested_gen" in data['message']['data']):
                    interested_gen = data['message']['data']['interested_gen']
                    print(TAG, "interested_gen=", interested_gen)
                    cmd = """UPDATE `users` SET `interested_in` = '%s' WHERE `users`.`one_email` = '%s'""" %(interested_gen, email)
                    update = self.update_data(cmd)
                    print(TAG, "interested_gen_update=", update)
                    req_body = {
                        "to": user_id,
                        "bot_id": bot_id,
                        "message": "ยืนยันข้อมูล",
                        "quick_reply":
                            [
                                {
                                    "label": "ถูกต้อง",
                                    "type": "text",
                                    "message": "ข้อมูลถูกต้อง",
                                    "payload": {"profile_confirm": "confirm"}
                                },
                                {
                                    "label": "ไม่ถูกต้อง",
                                    "type": "text",
                                    "message": "ข้อมูลไม่ถูกต้อง",
                                    "payload": {"profile_confirm": "eject"}
                                }
                            ]
                    }
                    self.send_quick_reply(one_id, req_body)
                elif ("profile_confirm" in data['message']['data']):
                    profile_confirm = data['message']['data']['profile_confirm']
                    if(profile_confirm == "confirm"):
                        self.send_msg(one_id, "ผู้คนยินดีที่รู้จักคุณ")
                        self.menu_send(user_id, bot_id)

                elif ("action" in data['message']['data']):
                    action = data['message']['data']['action']
                    if("action" == "find_single"):
                        self.send_msg(one_id, "พบกันเร็วๆ นี้ค่ะ")
                    elif("action" == "eject"):
                        print(TAG, "delete record")
                        cmd = """DELETE FROM `users` WHERE users.one_email=`%s`""" %(email)
                        self.send_msg(one_id, "ไว้คุยกันใหม่นะ")
                        return module.unauthorized()

            else:
                cmd = """SELECT users.age FROM users WHERE users.one_email='%s'""" %(email)
                res = database.getData(cmd)
                print(TAG, "check_age_dat=", res)
                if(res[0]['result'][0]['age'] is None):
                    age = data['message']['text']

                    if(not age.isnumeric()):
                        self.send_msg(one_id, "อายุเท่าไหร่คะ กระรุณาระบุเป็นตัวเลขค่ะ")
                        return module.wrongAPImsg()

                    age = int(age)

                    if(age == 0):
                        self.send_msg(one_id, "อายุเท่าไหร่คะ กระรุณาระบุเป็นตัวเลขที่ถูกต้องค่ะ")
                        return module.wrongAPImsg()
                    print(TAG, "age=", age)

                    if(age < 18 or age > 100):
                        self.send_msg(one_id, "อายุของคุณไม่อยู่ในช่วงที่กำหนด")
                        return module.unauthorized()
                    cmd = """UPDATE `users` SET `age` = '%s' WHERE `users`.`one_email` = '%s'""" % (age, email)
                    update = self.update_data(cmd)
                    print(TAG, "update=", update)
                    if(update[1] == 200):
                        req_body = {
                            "to": user_id,
                            "bot_id": bot_id,
                            "message": "สนใจในเพศไหน",
                            "quick_reply":
                                [
                                    {
                                        "label": "ชาย",
                                        "type": "text",
                                        "message": "ผู้ชายค่ะ",
                                        "payload": {"interested_gen": "man"}
                                    },
                                    {
                                        "label": "หญิง",
                                        "type": "text",
                                        "message": "ผู้หญิงครับ",
                                        "payload": {"interested_gen": "woman"}
                                    },
                                    {
                                        "label": "ไม่ระบุ",
                                        "type": "text",
                                        "message": "ไม่ระบุ",
                                        "payload": {"interested_gen": "not_specified"}
                                    }
                                ]
                        }
                        self.send_quick_reply(one_id, req_body)
                    else:
                        self.send_msg(one_id, "อายุเท่าไหร่คะ ระบุเป็นตัวเลข")
                else:
                    print("age valid")
                    self.menu_send(user_id, bot_id)
                    print(TAG, "menu sending")
        # elif(data['event'] == "add_friend"):
            # bot_id = data['bot_id']
            # user_id = data['source']['user_id']
            # email = data['source']['email']
        # else:
            # print(TAG, "unkown data")

        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
