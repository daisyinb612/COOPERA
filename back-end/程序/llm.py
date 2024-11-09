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
        # self.setting_world_create = '''
        # 假设你是一位话剧作家，
        # 你的任务是根据我在接下来的对话中给出的###主题关键词###，设计一个故事的世界观。
        # 输出时不用复述任务要求，直接描述世界观。
        # '''
        # self.create_storyline = '''
        # 假设你是一位话剧作家，
        # 你的任务是根据我在接下来的对话中提出的###要求###，对###现有故事线###进行修改或解答知识性疑问。
        # 如果###现有故事线###的内容为无，且###要求###的内容不是知识性提问，则根据###要求###生成一个简短的故事线。
        # 输出时不用复述任务要求，直接描述故事线或解答知识性疑问
        # '''
        self.setting_role_create = '''
        Assume you are a playwright. 
        Our task is to design the main characters of a stage play based on the ###LOGLINE### I provide in the following conversation. When outputting, refer to the ###OutputExample### and only output a JSON string.
        "content" refers to the character's description, "name" refers to the character's name, and "per" refers to the character's voice code: Female Voice, Male Voice. Please choose the appropriate voice based on the character's traits.
        ###OutputExample###
        [{
            "name": "***",
            "content": "***"
            "per": "Female Voice"
        },
        {
            "name": "***",
            "content": "***"
            "per": "Male Voice"
        }
        ]
        '''
        self.setting_outline_create = '''
        Assume you are a playwright.
        Our task is to write a drama playwright outline based on the ###LOGLINE### and ###CHARACTERLISTE### I provide in the following conversation. 
        Outline often contains three plots,five plots or seven plots.
        The "plotName" refers to the name of this plot.
        The purpose of the outline is to determine the structure of the play script.
        Please choose from the common structures: The Three-Act Structure, The Five-Act Structure, and The Seven-Act Structure, based on the story content.
        Accordingly, The Three-Act Structure should include 3 plots, The Five-Act Structure should include 5 plots, and The Seven-Act Structure should include 7 plots.
        plotStage refers to the stage of the story in which the plot occurs.scene refers to the setting where the plot takes place. 
        The sub-properties of scene are name, which is the name of the scene, and content, which is the description of the scene (only describing the setting, without involving the plot or characters). 
        beat refers to the summary of the plot.
        Only characters mentioned in the character list should appear in the story plots as protagonist.
        characters refers to the characters appearing in this plot, with name being the character's name, content being the character's description, and per being the character's voice code.
        All this information should be consistent with the information in the character list and should not be changed. 
        If new minor characters are needed, please provide complete information for the new characters, including name, content, and per.
        The value of "plotStage" can only be one of {"exposition", "incident", "conflict", "rising", "climax", "falling", "end"}.
        When outputting, refer to ###OutputExample### and only output the JSON string.
        If the input is Chinese, please output Chinese.
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
                "content": "***"
                "per": "Female Voice"
            },{
                "name": "***",
                "content": "***"
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
        # self.setting_scene_create = '''
        # Assume you are a playwright. 
        # Your task is to provide multiple scenes based on the ###LOGLINE### and ###OUTLINE### I will give in the following conversation. 。
        # he multiple scenes should meet the needs of the story's development, meaning all plot points should correspond to a scene. 
        # When outputting, refer to ###OutputExample### and only output the JSON string.
        # ###OutputExample###
        # [
        # {"sceneName": "***",
        # "sceneDescription": "***"
        # },
        # {"sceneName": "***",
        # "sceneDescription": "***"
        # },
        # {"sceneName": "***",
        # "sceneDescription": "***"
        # ]
        # '''
        self.setting_dialogue_create = '''
        Assume you are a playwright.
        Your task is to write the dialogue for this chapter based on the ###LOGLINE###,###OUTLINE### and ###CHARACTERLIST###,I will provide in the following conversation.
        Pay attention to ensuring the dialogue matches the characters' personalities. You can appropriately add character actions in parentheses within the dialogue.
        When outputting, refer to ###OutputExample### and only output the JSON string.
        If the input is Chinese, please output Chinese.
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
        {"number": "4",
        "character": "***",
        "content": "***"
        },
        {"number": "5",
        "character": "***",
        "content": "***"
        }
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
        # filepath = create_xlsx_file()
        #workbook = load_workbook(filepath)
        #for sheet_name in workbook.sheetnames:
        #    del workbook[sheet_name]
        #workbook.save(filepath)
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open("./opera_info/history/history.json", 'a', encoding='utf-8') as f:
            json.dump({"time": current_time, "history": new_history}, f, ensure_ascii=False, indent=4)
            
        # self.save_json_to_excel(json_object=new_history,filepath=filepath)
        
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
    
    def save_json_to_excel(self,json_object,filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()
        headers = json_object[0].keys()
        worksheet.write_row('A1', headers)
        for row_num, character in enumerate(json_object, start=1):
            for col_num, header in enumerate(headers):
                cell_value = character[header]
                if isinstance(cell_value, list):
                    cell_value = ", ".join(str(item) for item in cell_value)
                cell = worksheet.write(row_num, col_num, cell_value)
        workbook.close()

    def save_json_to_csv(self, json_object, filepath):
        try:
            os.remove(filepath)
        except OSError:
            pass
        headers = json_object[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for character in json_object:
                for key in character:
                    if isinstance(character[key], list):
                        character[key] = ", ".join(str(item) for item in character[key])
                writer.writerow(character)

    
    def add_json_to_excel(self,json_object,filepath):
        # 检查文件路径是否存在
        if os.path.exists(filepath):
            # 如果文件已存在，则加载它
            workbook = load_workbook(filepath)
        else:
            # 如果文件不存在，创建一个新的工作簿
            workbook = Workbook()
        # 获取工作簿的工作表数量，以便给新工作表命名
        sheet_index = len(workbook.sheetnames)-1
        worksheet_name = f'Sheet{sheet_index + 1}'
        worksheet = workbook.create_sheet(title=worksheet_name)
        
        headers = json_object[0].keys()
        for col_num, header in enumerate(headers, start=1):
           worksheet.cell(row=1, column=col_num, value=header)
        for row_num, character in enumerate(json_object, start=2):  # 开始于第二行，因为第一行是标题
            for col_num, header in enumerate(headers, start=1):
                cell_value = character[header]
                if isinstance(cell_value, list):
                    cell_value = ", ".join(str(item) for item in cell_value)
                worksheet.cell(row=row_num, column=col_num, value=cell_value)
        workbook.save(filepath)

    def update_json_to_excel(self, json_object, filepath, sheet_index):
        workbook = load_workbook(filepath)
        sheets = workbook.sheetnames
        if sheet_index < len(sheets):
            sheet_name = sheets[sheet_index]
            worksheet = workbook[sheet_name]
            for row in worksheet.iter_rows():
                for cell in row:
                    cell.value = None
            headers = json_object[0].keys()
            for col_num, header in enumerate(headers):
                worksheet.cell(row=1, column=col_num+1, value=header)
            for row_num, character in enumerate(json_object, start=2):
                for col_num, header in enumerate(headers):
                    worksheet.cell(row=row_num, column=col_num+1, value=character[header])
            workbook.save(filepath)
        else:
            print(f"Sheet index {sheet_index} is out of range.")
        workbook.close()