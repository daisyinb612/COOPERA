import base64
import json
import os
from openai import OpenAI
import requests
from zhipuai import ZhipuAI
import xlsxwriter
import csv
from datetime import datetime
import json
from openpyxl import Workbook, load_workbook


model = 'openai'  # 'openai' or 'zhipu'
api_key_openai = 'sk-EKAaP4tPWto6iGcj1fC9493751D040588690679dFcB8D3Aa'
api_key_zhipu = '3847066edd68874c24f3a9dc6a7c5c02.xH11Vl8gBlyeh8yK'


class LLM(object):
    def __init__(self):
        self.fix_json = '''
        I will provide text with formatting issues, and your task is to output the corrected JSON string. 
        When outputting, do not repeat the task requirements, just provide the corrected JSON string.
        '''
        self.storyline_help = '''
        Assume you are a drama playwriting teacher, and your task is to provide me with guidance or help in writing a summary of a playwriting. 
        Please guide me in using two or three sentences to summarize the story I want to tell. When outputting, do not repeat the task requirements.
        Please provide concise and effective guidance in three sentences or less.If the input is Chinese, please output Chinese.
        '''
        self.role_help = '''
        Assume you are a drama playwriting teacher,and your task is to provide me with guidance or help in crafting characters.
        I will provide ###LOGLINE###, ###CHARACTERLIST###, and ###MYQUESTION### in the following conversation. When outputting, do not repeat the task requirements.
        Please provide concise and effective guidance in three sentences or less.If the input is Chinese, please output Chinese.
        '''
        self.scene_help = '''
        Assume you are a drama playwriting teacher,and your task is to provide me with guidance or help in crafting scenes.
        I will provide ###LOGLINE###、###OUTLINE###和###MYQUSETION### in the following conversation.
        The story outline includes###PLOTNAME###、###PLOTSTAGE###、###PLOTNAME###、###PLOTBEAT###and###CHARACTERLISTE###for each plot。
        When outputting, do not repeat the task requirements.
        Please provide concise and effective guidance in three sentences or less.If the input is Chinese, please output Chinese.
        '''
        self.setting_role_create = '''
        Assume you are a playwright. 
        Our task is to design the main characters of a stage play based on the ###LOGLINE### I provide in the following conversation. When outputting, refer to the ###OutputExample### and only output a JSON string.
        "content" refers to the character's description, "name" refers to the character's name, and "per" refers to the character's voice code: Female Voice, Male Voice. Please choose the appropriate voice based on the character's traits.
        "related" should be filled with the names of other roles related to the current role.If the input ###LOGLINE### is Chinese, please output Chinese.
        ###OutputExample###
        [{
            "name": "***",
            "content": "***",
            "per": "Female Voice",
            "image": "",
            "related":["***"]
        },
        {
            "name": "***",
            "content": "***",
            "per": "Male Voice",
            "image": "",
            "related":["***","***"]
        }
        ]
        '''
        self.setting_outline_create = '''
        Assume you are a playwright.
        Our task is to write a drama playwright outline based on the ###LOGLINE### and ###CHARACTERLISTE### 
        I provide in the following conversation. The purpose of the outline is to determine the structure of the play script.
        Outline often contains three plots or five plots.
        The "plotName" refers to the name of this plot.Only characters mentioned in the character list should appear in the story plots as protagonist.
        characters refers to the characters appearing in this plot, with name being the character's name, content being the character's description, and per being the character's voice code.
        All this information should be consistent with the information in the character list and should not be changed. 
        The value of "plotStage" can only be one of {"exposition", "incident", "conflict", "rising", "climax", "falling", "end"}.
        When outputting, refer to ###OutputExample### and only output the JSON string.
        If the ###LOGLINE### is Chinese, please output Chinese.
        ###OutputExample###
        [{
        "plotName": "***",
        "plotStage": "***",
        "scene": {
            "name": "***",
            "content": "***"
        }
        "beat": "***",
        "characters":[
            {
                "name": "***",
                "content": "***",
                "per": "Female Voice"
            },{
                "name": "***",
                "content": "***",
                "per": "Male Voice"
            }
        ]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": {
            "name": "***",
            "content": "***"
        },
        "beat": "***",
        "characters":[
            {
                "name": "***",
                "content": "***"
                "per": "Female Voice"
            },{
                "name": "***",
                "content": "***"
                "per": "Male Voice"
            }
        ]
        }
        ]
        '''
        self.setting_dialogue_create = '''
        Assume you are a playwright.
        Your task is to write the dialogue for this chapter based on the ###LOGLINE###,###OUTLINE### and ###CHARACTERLIST###,I will provide in the following conversation.
        Pay attention to ensuring the dialogue matches the characters' personalities. You can appropriately add character actions in parentheses within the dialogue.
        When outputting, refer to ###OutputExample### and only output the JSON string.
        If the ###LOGLINE### is Chinese, please output Chinese.
        ###OutputExample###
        [
        {"number": "1",
        "character": "***",
        "content":"***"
        },
        {"number": "2",
        "character": "***",
        "content":"***"
        },
        {"number": "3",
        "character": "***",
        "content": "***"
        },
        ]
        '''
        self.history = None

    def save_history(self,question,answer,prompt,history=None):
        if history == None:
            new_history = [{"role": "system", "content": prompt}]
        else:
            new_history = [{"role": "system", "content": prompt}]
            for row in history:
                new_history.append(row)
        new_history.append({"role": "user", "content": question})
        new_history.append({"role": "assistant", "content": answer})
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open("./opera_info/history/history.json", 'a', encoding='utf-8') as f:
            json.dump({"time": current_time, "history": new_history}, f, ensure_ascii=False, indent=4)
        
    def ask(self,question,prompt,history=None):##model_name改为其他值（例如None）时，默认使用GLM
        if history is None:
            if model=="openai":
                try:
                    client = OpenAI(api_key=api_key_openai, base_url="https://api.xiaoai.plus/v1")
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": question},
                        ],
                        top_p=0.7,
                        stream=True,
                    )
                    print('current model is openai')
                except Exception as e:
                    print('openai error:', e)
                    print('current model is zhipu')
                    client = ZhipuAI(api_key=api_key_zhipu)
                    response = client.chat.completions.create(
                        model="glm-4",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": question},
                        ],
                        top_p=0.7,
                        temperature=0.95,
                        max_tokens=8192,
                        stream=True,
                    )
        else:
            new_message = [{"role": "system", "content": prompt}]
            for row in history:
                new_message.append(row)
            new_message.append({"role": "user", "content": question})
            if model=="openai":
                try:
                    client = OpenAI(api_key=api_key_openai, base_url="https://api.xiaoai.plus/v1")
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": question},
                        ],
                        top_p=0.7,
                        stream=True,
                    )
                    print('current model is openai')
                except Exception as e:
                    print('openai error:', e)
                    client = ZhipuAI(api_key=api_key_zhipu)
                    response = client.chat.completions.create(
                        model="glm-4",
                        messages=new_message,
                        top_p=0.7,
                        temperature=0.95,
                        max_tokens=8192,
                        stream=True,
                    )
        answer = ''
        print('思考中', end='')
        for trunk in response:
            if trunk.choices[0].delta.content:
                print(trunk.choices[0].delta.content, end='')
                answer += trunk.choices[0].delta.content
        print('\n')
        # print(answer)
        # print('\n')
        print('提问完成')
        print('\n')
        self.save_history(question=question,answer=answer,prompt=prompt,history=history)
        return answer

    def create_picture(self,prompt,history=None):
        print(prompt)
        if model == 'openai':
            client = OpenAI(
                base_url="https://xiaoai.plus/v1",
                api_key=api_key_openai
            )   
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                print(response)
                image_url = response.data[0].url
                self.save_history(question=prompt,answer="",prompt="",history=history)
                print('current model is openai')
                return image_url
            # 失败就用ZhipuAI
            except Exception as e:
                print('openai error:', e)
                print('current model is zhipu')
                client = ZhipuAI(api_key=api_key_zhipu)
                response = client.images.generations(
                    model="cogview-3", 
                    prompt=prompt,
                )
                print(response.data[0].url)
                self.save_history(question=prompt,answer="",prompt="",history=history)
                return response.data[0].url

    def analyze_answer(self,text):
        try:
            first_index = text.find('[')
            last_index = text.rfind(']')
            text = text[first_index:last_index+1]
            print(text)
            json_object = json.loads(text)
            print(text)
            return json_object
        except:
            print("模型输出格式不符合json格式，将重新使用模型修正格式问题")
            text = self.ask(question=text,prompt=self.fix_json)
            json_object = self.analyze_answer(text=text)
            return json_object