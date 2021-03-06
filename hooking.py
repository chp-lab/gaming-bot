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
        # web_vue_url1 = "https://onesmartaccess.herokuapp.com/"
        req_body = {
            "to": user_id,
            "bot_id": bot_id,
            "message": "ให้ช่วยอะไรดี",
            "quick_reply":
                [
                    {
                        "label": "บันทึกรูปแนะนำตัว",
                        "type": "text",
                        "message": "บันทึกรูปแนะนำตัว",
                        "payload": {"action": "image_rec"}
                    },
                    {
                        "label": "random ผู้คน",
                        "type": "text",
                        "message": "มีใครโสดอยู่บ้าง",
                        "payload": {"action": "find_single"}
                    },
                    {
                        "label": "อัพเดทโปรไฟล์",
                        "type": "text",
                        "message": "ขออัพเดทโปรไฟล์หน่อยครับ",
                        "payload": {"action": "profile_update"}
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

    def gender_quest(self, user_id, bot_id):
        this_quest = {
                        "to": user_id,
                        "bot_id": bot_id,
                        "message": "คุณเพศอะไร",
                        "quick_reply":
                            [
                                {
                                    "label": "ชาย",
                                    "type": "text",
                                    "message": "ผมผู้ชายครับ",
                                    "payload": {"gen": "man"}
                                },
                                {
                                    "label": "หญิง",
                                    "type": "text",
                                    "message": "หนูผู้หญิงค่ะ",
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
        return this_quest

    def interested_quest(self, user_id, bot_id):
        this_quest = {
                        "to": user_id,
                        "bot_id": bot_id,
                        "message": "สนใจในเพศไหน",
                        "quick_reply":
                            [
                                {
                                    "label": "ชาย",
                                    "type": "text",
                                    "message": "สนใจผู้ชายค่ะ",
                                    "payload": {"interested_gen": "man"}
                                },
                                {
                                    "label": "หญิง",
                                    "type": "text",
                                    "message": "สนใจผู้หญิงครับ",
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
        return this_quest

    def data_valid_quest(self, user_id, bot_id):
        this_quest = {
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

        return this_quest

    def show_profile_data(self, user_id, bot_id):
        this_quest = {
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
        return this_quest

    def profile_verify(self, one_id, user_id, bot_id, email):
        TAG = "profile_verify:"

        database = Database()
        module = Module()

        cmd = """SELECT users.name, users.gender, users.age, users.interested_in , users.data_valid 
                                FROM users WHERE users.one_email='%s'""" % (email)

        res = database.getData(cmd)

        if (res[1] == 200):
            tmp_data = res[0]['result'][0]
            if (tmp_data['gender'] is None):
                req_body = self.gender_quest(user_id, bot_id)
                self.send_quick_reply(one_id, req_body)
            elif (tmp_data['age'] is None):
                print(TAG, "ask age")
                self.send_msg(one_id, "คุณอายุเท่าไหร่")
            elif (tmp_data['interested_in'] is None):
                print(TAG, "ask interested_in")
                req_body = self.interested_quest(user_id, bot_id)
                self.send_quick_reply(one_id, req_body)
            elif (tmp_data['data_valid'] is None):
                print(TAG, "profile not confirm")
                tmp_msg = "ยินดีที่ได้รู้จักคุณ %s อายุ %s สนใจใน %s ยืนยันข้อมูลถูกต้อง" % (
                    tmp_data['name'], tmp_data['age'], tmp_data['interested_in'])
                self.send_msg(one_id, tmp_msg)
                req_body = self.data_valid_quest(user_id, bot_id)
                self.send_quick_reply(one_id, req_body)
            else:
                print(TAG, "user data valid")
                self.menu_send(user_id, bot_id)
                print(TAG, "menu sending")
            return module.success()
        else:
            print(TAG, "fail on check user data_valid")
            return module.serveErrMsg()

    def send_image_car(self, user_id, bot_id, img_ln, button):
        TAG = "send_image_car:"
        headers = {"Authorization": self.onechat_dev_token, "Content-Type": "application/json"}
        print(TAG, "send_image_car, one_id=", user_id)
        payload = {
	        "bot_id": bot_id,
	        "to": user_id,
	        "elements": [
                {
                    "type": "link",
                    "image": img_ln,
                    "action": img_ln,
                    "payload": "",
                    "sign": "false",
                    "onechat_token": "false",
                    "button": button
                }
	        ]
        }
        r = requests.post(self.onechat_uri + "/bot-message/api/v1/image-carousel", headers=headers, json=payload)
        print(TAG, "r=", r.text)
        return r

    def post(self):
        TAG = "Hooking:"
        data = request.json
        print(TAG, "data=", data)
        print(TAG, request.headers)

        database = Database()
        module = Module()
        # onechat_uri = self.onechat_uri
        data = request.json
        # onechat_dev_token = "Bearer Af58c5450f3b45c71a97bc51c05373ecefabc49bd2cd94f3c88d5b844813e69a17e26a828c2b64ef889ef0c10e2aee347"
        # headers = {"Authorization": onechat_dev_token}

        print(TAG, "data=", data)
        print(TAG, request.headers)

        if('event' not in data):
            print(TAG, "event not found!")
            # assum OneChat iBeacon event detected
            print(TAG, "OneChat iBeacon detected")
            return module.success()
            # return module.wrongAPImsg()

        if(data['event'] != "message"):
            print(TAG, "event not support")
            return module.wrongAPImsg()

        bot_id = data['bot_id']
        user_id = data['source']['user_id']
        email = data['source']['email']
        one_id = data['source']['one_id']
        name = data['source']['display_name']

        print(TAG, "user_id=", user_id)
        print(TAG, "one email=", email)

        user_exist = self.is_user_exist(email)
        if (user_exist):
            print(TAG, "### user exist!")
            if ('data' in data['message']):
                tmp_data = data['message']['data']
                print(TAG, "mesage contain data=", tmp_data)

                if ("gen" in data['message']['data']):
                    gen = data['message']['data']["gen"]
                    print(TAG, "gen=", gen)
                    cmd = """UPDATE `users` SET `gender` = '%s' WHERE `users`.`one_email` = '%s'""" % (gen, email)
                    update = self.update_data(cmd)
                    print("gen update=", update)
                    self.send_msg(one_id, "คุณอายุเท่าไหร่คะ")
                elif ("interested_gen" in data['message']['data']):
                    interested_gen = data['message']['data']['interested_gen']
                    print(TAG, "interested_gen=", interested_gen)
                    cmd = """UPDATE `users` SET `interested_in` = '%s' WHERE `users`.`one_email` = '%s'""" % (
                    interested_gen, email)
                    update = self.update_data(cmd)
                    print(TAG, "interested_gen_update=", update)
                    req_body = self.show_profile_data(user_id, bot_id)
                    self.send_quick_reply(one_id, req_body)
                elif ("profile_confirm" in data['message']['data']):
                    profile_confirm = data['message']['data']['profile_confirm']
                    if (profile_confirm == "confirm"):
                        update = """UPDATE `users` SET `data_valid` = '%s' WHERE `users`.`one_email` = '%s'""" % (
                        1, email)
                        res = database.insertData(update)
                        print(TAG, "profile confirm=", res)
                        self.send_msg(one_id, "ผู้คนยินดีที่รู้จักคุณ")
                        self.menu_send(user_id, bot_id)
                        return module.success()
                    elif (profile_confirm == "eject"):
                        print(TAG, "delete record")
                        cmd = """DELETE FROM `users` WHERE users.one_email='%s'""" % (email)
                        res = database.insertData(cmd)
                        print(TAG, "delete data=", res)
                        self.send_msg(one_id, "ไว้คุยกันใหม่นะ")
                        return module.unauthorized()
                elif ("action" in data['message']['data']):
                    action = data['message']['data']['action']
                    if (action == "find_single"):
                        cmd = """SELECT users.name, users.interested_in FROM users WHERE users.one_email='%s'""" %(email)
                        print(TAG, "cmd=", cmd)
                        res = database.getData(cmd)
                        interested_in = res[0]['result'][0]['interested_in']

                        print(TAG, "interested in=", interested_in)

                        cmd ="""SELECT users.name, users.cover_image 
                        FROM users WHERE users.gender="%s" AND users.one_email != '%s'
                        ORDER BY RAND()
                        LIMIT 1""" %(interested_in, email)

                        print(TAG, "cmd=", cmd)
                        res = database.getData(cmd)
                        print(TAG, "single people=", res)
                        print(TAG, "res=", res)

                        results = res[0]['result']
                        for people in results:
                            p_name = people['name']
                            p_cover_img = people['cover_image']
                            # self.send_msg(one_id, p_name)
                            self.send_image_car(user_id, bot_id, p_cover_img, p_name)
                        self.menu_send(user_id, bot_id)
                        return module.success()
                    elif (action == "image_rec"):
                        self.send_msg(one_id, "ส่งรูปของคุณมาได้เลย")
                        return module.success()
                else:
                    print(TAG, "unnown message data in quick reply")
            elif('type' in data['message']):
                msg_type = data['message']["type"]
                print(TAG, "data contain type, msg_type=", msg_type)
                if (msg_type == "image"):
                    file_loc = data["message"]["file"]
                    action = "image_rec"
                    sent_from = email
                    sent_to = bot_id
                    res_msg = "บันทึกรูปภาพแนะนำตัวแล้ว"
                    cmd = """INSERT INTO `action_logs` (`action_id`, `action`, `message`, `sent_from`, `sent_to`, `response`, `responsed_at`, `created_at`) 
                    VALUES (NULL, '%s', '%s', '%s', '%s', '%s', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)""" %(action, file_loc, sent_from, sent_to, res_msg)
                    insert = database.insertData(cmd)
                    print(TAG, "insert cover image=", insert)
                    cmd = """UPDATE `users` SET `cover_image` = '%s' 
                    WHERE `users`.`one_email` = '%s'""" %(file_loc, email)
                    update = self.update_data(cmd)
                    print(TAG, "update cover_image=", update)
                    self.send_msg(one_id, res_msg)
                    self.menu_send()
                    return module.success()
                elif (msg_type == "text"):
                    cmd = """SELECT users.age FROM users WHERE users.one_email='%s'""" % (email)
                    res = database.getData(cmd)
                    print(TAG, "check_age_dat=", res)
                    if (res[0]['result'][0]['age'] is None):
                        age = data['message']['text']

                        if (not age.isnumeric()):
                            self.send_msg(one_id, "คุณอายุเท่าไหร่คะ กระรุณาระบุเป็นตัวเลขค่ะ")
                            return module.wrongAPImsg()

                        age = int(age)

                        if (age == 0):
                            self.send_msg(one_id, "คุณอายุเท่าไหร่คะ กระรุณาระบุเป็นตัวเลขที่ถูกต้องค่ะ")
                            return module.wrongAPImsg()
                        print(TAG, "age=", age)

                        if (age < 18 or age > 100):
                            self.send_msg(one_id, "อายุของคุณไม่อยู่ในช่วงที่กำหนด")
                            return module.unauthorized()
                        cmd = """UPDATE `users` SET `age` = '%s' WHERE `users`.`one_email` = '%s'""" % (age, email)
                        update = self.update_data(cmd)
                        print(TAG, "update=", update)
                        if (update[1] == 200):
                            print(TAG, "set age")
                            req_body = self.interested_quest(user_id, bot_id)
                            self.send_quick_reply(one_id, req_body)
                            return module.success()
                        else:
                            self.send_msg(one_id, "คุณอายุเท่าไหร่คะ ระบุเป็นตัวเลข")
                            return module.wrongAPImsg()

                        res = self.profile_verify(one_id, user_id, bot_id, email)
                        return res

                    else:
                        print(TAG, "age valid")
                        res = self.profile_verify(one_id, user_id, bot_id, email)
                        return res
                else:
                    self.send_msg(one_id, "ยังไม่รองรับข้อความประเภท " + msg_type)
                    return module.success()
            else:
                print(TAG, "this message is not support!")
        #first meet
        else:
            print(TAG, "usr not exist!")
            self.send_msg(one_id, "สวัสดีค่ะ แนะนำตัวเองเเบื้องต้นพื่อหาผู้คนที่คุณสนใจ")
            req_body = self.gender_quest(user_id, bot_id)
            self.send_quick_reply(one_id, req_body)
            add_user = self.add_new_user(email, name, one_id)
            print(TAG, "add=new_user=", add_user)

            return module.success()


        return {
            "type": True,
            "message": "success",
            "elapsed_time_ms": 0,
            "len": 0,
            "result": "testing"
        }
