import base64
import json
import os
from openai import OpenAI
import requests
from zhipuai import ZhipuAI
from history import create_xlsx_file
import xlsxwriter
import csv
from datetime import datetime
import json
from openpyxl import Workbook, load_workbook

class LLM(object):
    def __init__(self,apikey=None):
        self.fix_json = '''
        我将给出存在格式问题的文本，你的任务是输出修正格式后的json字符串。
        输出时不要复述任务要求，直接给出修改好的json字符串。
        '''
        self.storyline_help = '''
        假设你是一位剧作家，
        你的任务是为我提供写作指导或帮助，我将在接下来的对话中给出###故事线###和###我的问题###。
        输出时不要复述任务要求。
        '''
        self.role_help = '''
        假设你是一位剧作家，
        你的任务是为我提供写作指导或帮助，我将在接下来的对话中给出###故事线###、###角色表###和###我的问题###。
        输出时不要复述任务要求。
        '''
        self.scene_help = '''
        假设你是一位剧作家，
        你的任务是为我提供写作指导或帮助，我将在接下来的对话中给出###故事线###、###故事大纲###和###我的问题###。
        故事大纲包括每一个情节的###情节名###、###情节阶段###、###场景名###、###梗概###和###角色表###。
        输出时不要复述任务要求。
        '''
        self.setting_world_create = '''
        假设你是一位剧作家，
        你的任务是根据我在接下来的对话中给出的###主题关键词###，设计一个故事的世界观。
        输出时不用复述任务要求，直接描述世界观。
        '''
        self.create_storyline = '''
        假设你是一位剧作家，
        你的任务是根据我在接下来的对话中提出的###要求###，对###现有故事线###进行修改或解答知识性疑问。
        如果###现有故事线###的内容为无，且###要求###的内容不是知识性提问，则根据###要求###生成一个简短的故事线。
        输出时不用复述任务要求，直接描述故事线或解答知识性疑问
        '''
        self.setting_role_create = '''
        假设你是一位剧作家，
        你的任务是根据我在接下来的对话中给出的###故事线###，设计出多个故事的主要角色，输出时参照###输出示例###只输出json字符串
        ###输出示例###
        [{
            "name": "***",
            "content": "***"
        },
        {
            "name": "***",
            "content": "***"
        },
        {
            "name": "***",
            "content": "***"
        },
        {
            "name": "***",
            "content": "***"
        },
        {
            "name": "***",
            "content": "***"
        }
        ]
        '''
        self.setting_outline_create = '''
        假设你是一位剧作家，
        你的任务是根据我在接下来的对话中给出的###故事线###和###角色表###，编写故事大纲，其中plotName指此情节的名字，
        plotStage指该情节处于整个故事的阶段，scene指情节发生的场景，beat指梗概。
        输出时参照###输出示例###只输出json字符串,"故事阶段"的值只能取{"Expositon","Inciting Incident","Conflict","Rising Action","Climax","Falling Action","Denouement"}其中之一
        ###输出示例###
        [{
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        },
        {
        "plotName": "***",
        "plotStage": "***",
        "scene": "***",
        "beat": "***",
        "characters":["**", "**", "**"]
        }
        ]
        '''
        self.setting_scene_create = '''
        假设你是一位剧作家，
        你的任务是根据我在接下来的对话中给出的###故事线###和###故事大纲###，给出多个场景。
        要求多个场景能够满足故事展开的需要，即所有情节均能找到对应场景。
        输出时参照###输出示例###只输出json字符串。
        ###输出示例###
        [
        {"场景名称": "***",
        "场景介绍": "***"
        },
        {"场景名称": "***",
        "场景介绍": "***"
        },
        {"场景名称": "***",
        "场景介绍": "***"
        },
        {"场景名称": "***",
        "场景介绍": "***"
        },
        {"场景名称": "***",
        "场景介绍": "***"
        }
        ]
        '''
        self.setting_dialogue_create = '''
        假设你是一位剧作家，
        你的任务是根据我在接下来的对话中给出的###故事线###和###本章大纲###编写本章的场景对话，注意对话为中文。
        输出时参照###输出示例###只输出json字符串,
        ###输出示例###
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
        self.apikey = apikey
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
        with open("./history/history.jsonl", 'a', encoding='utf-8') as f:
            json.dump({"time": current_time, "history": new_history}, f, ensure_ascii=False, indent=4)
            
        # self.save_json_to_excel(json_object=new_history,filepath=filepath)
        
    def ask(self,question,prompt,history=None,model_name=None):##model_name改为其他值（例如None）时，默认使用GLM
        if history is None:
            if model_name=="openai":
                client = OpenAI(api_key=self.apikey, base_url="https://api.xiaoai.plus/v1")
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": question},
                    ],
                    top_p=0.7,
                    stream=True,
                )
            else:
                client = ZhipuAI(api_key=self.apikey)
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
            if model_name=="openai":
                client = OpenAI(api_key=self.apikey, base_url="https://api.xiaoai.plus/v1")
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": question},
                    ],
                    top_p=0.7,
                    stream=True,
                )
            else:
                client = ZhipuAI(api_key=self.apikey)
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
        '''
        url = 'https://api.openai.com/v1/images/generations'
        headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'n': 1,  # 生成图片的数量
            'size': '256x256'  # 图片尺寸
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            image_data = response.json()
            image_b64 = image_data['data'][0]['b64_json']
            image_bytes = base64.b64decode(image_b64)
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            print("图片已生成并保存")
        else:
            print("请求失败：", response.status_code, response.text)
        self.save_history(question=prompt,answer="",prompt="",history=history)
        return image_b64'''
        client = ZhipuAI(api_key=self.apikey)
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