import json
import socketserver
import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from excel import ExcelOp
from llm import LLM

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer, config):
        super().__init__(request, client_address, server)
        self.apikey = config["apikey"] 
        self.world_setting_path = config["world_setting_path"]
        self.characters_path = config["characters_path"]
        self.outline_path = config["outline_path"]
        self.scene_path = config["scene_path"]
        self.dialogue_path = config["dialogue_path"]
        self.picture_path = config["picture_path"]

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        type = self.headers.get('Content-Type')
        if type == "json":
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_error(400, 'Invalid JSON')
            action = data["action"]
            if action == "upload_storyline":
                #content_length = int(self.headers['Content-Length'])
                #data = self.rfile.read(content_length)
                with open(self.world_setting_path, 'wb') as f:
                    f.truncate(0)
                    f.write(data["data"]["storyline"])
                self.send_response(200)
            elif action == "get_storyline_help":
                #with open(self.world_setting_path, 'wb') as processed_file:
                #    storyline = processed_file.read()
                storyline = data["data"]["storyline"]
                history = data["data"]["history"] ##列表格式
                input = data["data"]["user_input"]
                question = ""
                question += "\n###故事线###:"+storyline
                question += "\n###我的问题###:"+input
                l = LLM(apikey=self.apikey)
                answer = l.ask(question=question,prompt=l.storyline_help,history=history)
                self.send_response(200)
                #self.send_header('Content-type', 'text/plain')
                #self.end_headers()
                response_string = answer
                self.wfile.write(response_string.encode('utf-8'))
            elif action == "get_saved_storyline":
                with open(self.world_setting_path, 'r', encoding='utf-8') as f:
                    storyline = f.read()
                f.close()
                self.send_response(200)
                response_string = storyline
                self.wfile.write(response_string.encode('utf-8'))
            elif action == "init_character_generation":
                with open(self.world_setting_path,"r",encoding="utf-8") as f:
                    storyline = f.read()
                f.close()
                question += "\n###故事线###:"+storyline
                l = LLM(apikey=self.apikey)
                answer = l.ask(question=question,prompt=l.setting_role_create)
                characters = l.analyze_answer(answer)
                print(characters)
                l.save_json_to_excel(json_object=characters,filepath=self.characters_path)
                self.send_response(200)
                self.wfile.write(characters) ##这里的characters数据类型为字典
            elif action == "get_character_help":
                with open(self.world_setting_path,"r",encoding="utf-8") as f:
                    storyline = f.read()
                f.close()
                e = ExcelOp(file=self.characters_path)
                characters = e.get_json_all()
                history = data["data"]["history"] ##列表格式
                input = data["data"]["user_input"]
                question = ""
                question += "\n###故事线###:"+storyline
                question += "\n###角色表###:"+characters
                question += "\n###我的问题###:"+input
                l = LLM(apikey=self.apikey)
                answer = l.ask(question=question,prompt=l.role_help,history=history)
                self.send_response(200)
                response_string = answer
                self.wfile.write(response_string.encode('utf-8'))
            elif action == "save_character_asset":
                l = LLM(apikey=self.apikey)
                l.save_json_to_excel(json_object=data["data"],filepath=self.characters_path)
                self.send_response(200)
            elif action == "init_plot_generation":
                with open(self.world_setting_path,"r",encoding="utf-8") as f:
                    storyline = f.read()
                f.close()
                e = ExcelOp(file=self.characters_path)
                characters = e.get_json_all()
                question = ""
                question += "\n###故事线###:"+storyline
                question += "\n###角色表###:"+characters
                l = LLM(apikey=self.apikey)
                answer = l.ask(question=question,prompt=l.setting_outline_create)
                plot = l.analyze_answer(answer)
                l.save_json_to_excel(json_object=plot,filepath=self.outline_path)
                self.send_response(200)
                self.wfile.write(plot)
            elif action == "update_plot":
                plot = data["data"]
                l = LLM(apikey=self.apikey)
                l.save_json_to_excel(json_object=plot,filepath=self.outline_path)
            elif action == "init_scene_generation":
                with open(self.world_setting_path,"r",encoding="utf-8") as f:
                    storyline = f.read()
                f.close()
                e = ExcelOp(file=self.outline_path)
                plot = e.get_json_all()
                question = ""
                question += "\n###故事线###:"+storyline
                question += "\n###角色表###:"+plot
                l = LLM(apikey=self.apikey)
                answer = l.ask(question=question,prompt=l.setting_scene_create)
                scene = l.analyze_answer(answer)
                l.save_json_to_excel(json_object=scene,filepath=self.scene_path)
                self.send_response(200)
                self.wfile.write(scene)
            elif action == "save_scene_asset":
                scene = data["data"]
                l = LLM(apikey=self.apikey)
                l.save_json_to_excel(json_object=scene,filepath=self.scene_path)
            elif action == "init_dialogue_generation":
                e = ExcelOp(file=self.outline_path)
                number = int(data["data"]["plot_number"])
                if number>=2:
                    outline_pass = e.get_json_by_row(number)
                else:
                    outline_pass = "无"
                outline_now = e.get_json_by_row(number+1)
                question = ""
                question += "\n###前情提要###:"+outline_pass
                question += "\n###本章大纲###:"+outline_now
                l = LLM(apikey=self.apikey)
                answer = l.ask(question=question,prompt=l.setting_dialogue_create)
                dialogue = l.analyze_answer(answer)
                l.add_json_to_excel(json_object=dialogue,filepath=self.dialogue_path)
                self.send_response(200)
                self.wfile.write(dialogue)
            elif action == "save_dialogue_asset":
                number = int(data["data"]["plot_number"])
                dialogue = data["data"]["dialogue"]
                l = LLM(apikey=self.apikey)
                l.update_json_to_excel(json_object=dialogue,filepath=self.dialogue_path,sheet_index=number-1)
            else:
                self.send_error(400, 'Bad request.')
        elif type == "png/jpg":
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_error(400, 'Invalid JSON')
            action = data["action"]
            if action == "create_picture":
                prompt = data["data"]["user_input"]
                name = data["data"]["name"]
                filepath = self.picture_path+"/"+name+".png"
                l = LLM(apikey=self.apikey)
                picture = l.create_picture(filepath=filepath,prompt=prompt) ##这里picture是base_64编码的json格式字符串
                self.send_response(200)
                self.wfile.write(picture)
            else:
                self.send_error(400, 'Bad request.')
if __name__ == '__main__':
    info_dict = {
   "apikey": "e4ab8bb5cc7cc6eb620f9cde3093b8b4.FauytagDuxsJpEuD",
   "world_setting_path": "./剧本信息/世界观设定/storyline.txt",
   "characters_path": "./剧本信息/角色设定/characters.xlsx",
   "outline_path": "./剧本信息/故事大纲/outline.xlsx",
   "scene_path": "./剧本信息/场景/scene.xlsx",
   "dialogue_path": "./剧本信息/对话/dialogue_path.xlsx",
   "picture_path": "./剧本信息/图片"
    }
    handler = Handler(config=info_dict)
    server = HTTPServer(('0.0.0.0', 8000), handler)
    print('Serving HTTP on port 8000 (http://192.168.0.152:8000/) ...')
    server.serve_forever()