import time
from flask import Flask, request, jsonify, send_file, send_from_directory, abort, render_template
import os
import networkx as nx
from pyvis.network import Network
import requests
from llm import LLM
from flask_cors import CORS
import json
from PIL import Image
from io import BytesIO
import threading

app = Flask(__name__, template_folder='template')
CORS(app)

global_llm = LLM()

async_tasks = {}

# Configuration dictionary
info_dict = {
    "world_setting_path": "./opera_info/storyline/storyline.txt",
    "characters_path": "./opera_info/character/characters.json",
    "characters_image_path": "./opera_info/character",
    "outline_path": "./opera_info/outline/outline.json",
    "scene_path": "./opera_info/scene/scene.json",
    "scene_image_path": "./opera_info/scene",
    "dialogue_path": "./opera_info/dialog/dialogue_path.json",
    "picture_path": "./opera_info/img",
    "wav_path": "./opera_info/audio/",
    "script_path": "./opera_info/script.txt",
    "change_path": "./opera_info/change/change.json"
}


@app.route('/api/save_changes', methods=['POST'])
def save_changes():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    if action == "save_changes":
        if not os.path.exists(info_dict['change_path']):
            os.makedirs(os.path.dirname(
                info_dict['change_path']), exist_ok=True)
        with open(info_dict['change_path'], 'a', encoding='utf-8') as f:
            f.write(data["data"]["changes"] + "\n")
        return jsonify({"message": "Changes saved successfully."})
    else:
        return jsonify({"error": "Invalid action type."}), 401


@app.route('/api/upload_storyline', methods=['POST'])
def upload_storyline():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    if action == "upload_storyline":
        with open(info_dict['world_setting_path'], 'w', encoding='utf-8') as f:
            f.write(data["data"]["storyline"])
        storyline = data["data"]["storyline"]
        question = "\n###LOGLINE###:" + storyline
        #
        answer = global_llm.ask(
            question=question, prompt=global_llm.setting_role_create)
        plot = global_llm.analyze_answer(answer)
        with open(info_dict['characters_path'], 'w', encoding='utf-8') as f:
            json.dump(plot, f, indent=4, ensure_ascii=False)
        return jsonify(plot)
    else:
        return jsonify({"error": "Invalid action type."}), 401


@app.route('/api/get_storyline_help', methods=['POST'])
def get_storyline_help():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402

    storyline = data["data"]["storyline"] if data["data"]["storyline"] else ""
    history = data["data"]["history"]
    user_input = data["data"]["user_input"]

    question = "\n###LOGLINE###:" + storyline + "\n###MYQUSETION###:" + user_input

    answer = global_llm.ask(
        question=question, prompt=global_llm.storyline_help, history=history)
    # print("Yes")

    return jsonify({"answer": answer})


@app.route('/api/get_saved_storyline', methods=['GET'])
def get_saved_storyline():
    with open(info_dict['world_setting_path'], 'r', encoding='utf-8') as f:
        storyline = f.read()
    return jsonify({"storyline": storyline})


@app.route('/api/get_character_help', methods=['POST'])
def get_character_help():
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    with open(info_dict['characters_path'], "r", encoding="utf-8") as f:
        characters = json.load(f)
    data = request.get_json()
    history = data["data"]["history"]
    user_input = data["data"]["user_input"]
    question = "\n###LOGLINE###:" + storyline + "\n###CHARACTERLISTE###:"
    for character in characters:
        question += character["name"] + ": " + character["content"] + "\n"
    question += "\n###MYQUSETION###:" + user_input

    answer = global_llm.ask(
        question=question, prompt=global_llm.role_help, history=history)
    return jsonify({"answer": answer})


@app.route('/api/check-task/<int:task_id>', methods=['GET'])
def check_task(task_id):
    task = async_tasks.get(task_id)
    if task:
        return jsonify({'status': task['status']})
    else:
        return jsonify({'status': 'not_found'}), 404


@app.route('/api/init_plot_generation', methods=['POST'])
def init_plot_generation():
    data = request.get_json()
    task_id = data.get("task_id")
    if task_id is None:
        def init_plot():
            with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
                storyline = f.read()
            characters = data["data"]["characters"]
            question = "\n###LOGLINE###:" + storyline + "\n###CHARACTERLISTE###:"
            for character in characters:
                question += "角色名： "+character["name"] + "角色描述:  " + \
                    character["content"]+"角色音色： " + character["per"] + "\n"

            answer = global_llm.ask(
                question=question, prompt=global_llm.setting_outline_create)
            plot = global_llm.analyze_answer(answer)
            if not os.path.exists(info_dict['outline_path']):
                os.makedirs(os.path.dirname(info_dict['outline_path']), exist_ok=True)
            with open(info_dict['outline_path'], 'w', encoding='utf-8') as f:
                json.dump(plot, f, indent=4, ensure_ascii=False)
            scene = []
            for x in plot:
                x['scene']['url'] = ""
                scene.append(x['scene'])
            if not os.path.exists(info_dict['scene_path']):
                os.makedirs(os.path.dirname(info_dict['scene_path']), exist_ok=True)
            with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
                json.dump(scene, f, indent=4, ensure_ascii=False)
            async_tasks[task_id]['status'] = 'completed'

        task_id = len(async_tasks)+1
        async_tasks[task_id] = {'status': 'processing'}

        threading.Thread(target=init_plot).start()
        return jsonify({'task_id': task_id})
    else:
        async_tasks.pop(task_id)
        with open(info_dict['outline_path'], 'r', encoding='utf-8') as f:
            plot = json.load(f)
        return plot


@app.route('/api/add_character', methods=['POST'])
def add_character():
    data = request.get_json()
    character = data["data"]
    with open(info_dict['characters_path'], 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    old_data.append(character)
    with open(info_dict['characters_path'], 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=4, ensure_ascii=False)
    return jsonify({})


@app.route('/api/update_plot', methods=['POST'])
def update_plot():
    data = request.get_json()
    plot = data["data"]

    with open(info_dict['outline_path'], 'w', encoding='utf-8') as f:
        json.dump(plot, f, indent=4, ensure_ascii=False)
    return jsonify({})


@app.route('/api/save_scene_asset', methods=['POST'])
def save_scene_asset():
    data = request.get_json()
    index = data["data"]["index"]
    scene = data["data"]["scene"]

    with open(info_dict['scene_path'], 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    old_data[index] = scene
    print('old data', scene)
    with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=4, ensure_ascii=False)
    return jsonify({})


@app.route('/api/add_scene', methods=['POST'])
def add_scene():
    data = request.get_json()
    scene = data["data"]
    with open(info_dict['scene_path'], 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    old_data.append(scene)
    with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=4, ensure_ascii=False)
    return jsonify({})


@app.route("/delete_scene_asset", methods=['POST'])
def delete_scene_asset():
    data = request.get_json()
    index = data["data"]["index"]
    # print('index', index)
    with open(info_dict['scene_path'], 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    old_data.pop(index)
    with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=4, ensure_ascii=False)
    return jsonify({})

@app.route('/api/create_scene_picture', methods=['POST'])
def create_scene_picture():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 402

        action = data.get("action")
        if action == "create_scene_picture":
            prompt = "Please create an illustration of an ancient Chinese scene using a unified, refreshing flat illustration style. Use the following colors and pay attention to the choice of main color tones and the proportion of their usage to ensure the background matches the scene description and conveys the appropriate atmosphere: light purple #DDA0DD, light green #90EE90, light blue #ADD8E6, dark purple #4B0082, dark gray #696969, beige #F5F5DC. The name of the scene is: " + \
                data["data"]["name"]
            if data["data"]["user_input"] != "":
                prompt += "the scene's description is:" + \
                    data["data"]["user_input"]
            name = data["data"]["name"]

            picture = global_llm.create_picture(prompt=prompt)
            print('generating picture done')
            req = requests.get(picture)
            image = Image.open(BytesIO(req.content))
            fileName = name+'.'+image.format.lower()
            with open(info_dict['scene_image_path']+'/'+fileName, 'wb') as f:
                f.write(req.content)
            return jsonify({"image": fileName})
        else:
            return jsonify({"error": "Invalid action type."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/create_character_picture', methods=['POST'])
def create_character_picture():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 402

        action = data.get("action")
        if action == "create_character_picture":
            prompt =  "Generates character avatars with white background. Use a fresh and unified color palette to generate an illustration-style image of a single character. Choose from the following colors: primary color red #CC0000, accent color gold #FFD700, accent color dark blue #191970, accent color silver #C0C0C0, accent color white #FFFFFF, and accent color dark red #8B0000. The character's name is: " + \
                data["data"]["name"]+",and the character's description is: " + \
                data["data"]["content"]
            name = data["data"]["name"]

            picture = global_llm.create_picture(prompt=prompt)
            req = requests.get(picture)
            image = Image.open(BytesIO(req.content))
            fileName = name+'.'+image.format.lower()
            # print(fileName)
            with open(info_dict['characters_image_path']+'/'+fileName, 'wb') as f:
                f.write(req.content)
            return jsonify({"image": fileName})
        else:
            return jsonify({"error": "Invalid action type."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/get_image', methods=['GET'])
def get_image():
    filename = request.args.get('filename')
    path = request.args.get('path')
    image_directory = f'./opera_info/' + str(path) + '/'

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    file_path = os.path.join(image_directory, filename)
    if os.path.exists(file_path):
        return send_from_directory(image_directory, filename)
    else:
        return abort(404, description="File not found")

@app.route('/api/get_json', methods=['GET'])
def get_json():
    filename = request.args.get('filename')
    path = request.args.get('path')
    json_directory = f'./opera_info/' + str(path) + '/'

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    file_path = os.path.join(json_directory, filename)
    if os.path.exists(file_path):
        return send_from_directory(json_directory, filename)
    else:
        return abort(404, description="File not found")

@app.route("/api/update_character", methods=['POST'])
def update_character():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    character = data["data"]["character"]
    index = data["data"]["index"]
    if action == "update_character":
        with open(info_dict['characters_path'], 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        old_data[index] = character
        with open(info_dict['characters_path'], 'w', encoding='utf-8') as f:
            json.dump(old_data, f, indent=4, ensure_ascii=False)
        return jsonify({"message": "Characters updated successfully."})
    else:
        return jsonify({"error": "Invalid action type."}), 401


@app.route("/api/delete_character", methods=['POST'])
def delete_character():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    index = data["data"]["index"]
    if action == "delete_character":
        with open(info_dict['characters_path'], 'r', encoding='utf-8') as f:
            old_data = json.load(f)

        old_data.pop(index)
        with open(info_dict['characters_path'], 'w', encoding='utf-8') as f:
            json.dump(old_data, f, indent=4, ensure_ascii=False)
        return jsonify({"message": "Characters updated successfully."})
    else:
        return jsonify({"error": "Invalid action type."}), 401


@app.route('/api/get_scene_help', methods=['POST'])
def get_scene_help():
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    with open(info_dict['scene_path'], "r", encoding="utf-8") as f:
        scene = json.load(f)

    data = request.get_json()
    history = data["data"]["history"]
    user_input = data['data']['user_input']
    question = "\n###LOGLINE###：" + storyline + "\n###SCENELIST###："

    for s in scene:
        scene_name = s['name']
        scene_content = s['content']
        question += "\nScene name: " + scene_name + ", Scene Content: " + scene_content
    question += '\n' + user_input

    answer = global_llm.ask(
        question=question, prompt=global_llm.scene_help, history=history)
    return jsonify({"answer": answer})


@app.route('/api/generate_dialogue', methods=['POST'])
def generate_dialogue():
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    data = request.get_json()["data"]
    plotName = data["plotName"]
    plotStage = data["plotStage"]
    sceneName = data["scene"]["name"]
    sceneContent = data["scene"]["content"]
    beat = data["beat"]
    characters = data["characters"]
    question = "\n###LOGLINE###:" + storyline + "\n###OUTLINE###：章节：" + plotName + "，情节阶段" + \
        plotStage + "，场景名字" + sceneName + ', 场景描述' + \
        sceneContent + "，梗概" + beat + "，角色表"
    for character in characters:
        question += "角色名： "+character["name"] + "角色描述:  " + \
            character["content"]+"角色音色： " + character["per"] + "\n"

    answer = global_llm.ask(
        question=question, prompt=global_llm.setting_dialogue_create)
    scene = global_llm.analyze_answer(answer)
    return jsonify(scene)


@app.route("/api/upload_dialogue", methods=['POST'])
def upload_dialogue():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    if action == "upload_dialogue":
        if not os.path.exists(info_dict['dialogue_path']):
            os.makedirs(os.path.dirname(
                info_dict['dialogue_path']), exist_ok=True)
        with open(info_dict['dialogue_path'], 'w', encoding='utf-8') as f:
            json.dump(data["data"], f, indent=4, ensure_ascii=False)

        return jsonify({"message": "Dialogue uploaded successfully."})
    else:
        return jsonify({"error": "Invalid action type."}), 401


@app.route("/api/generate_script", methods=['GET'])
def generate_script():
    res = {
        "storylines": "",
        "dialogues": ""
    }
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    res["storylines"] = storyline
    if not os.path.exists(info_dict['dialogue_path']):
        os.makedirs(os.path.dirname(
            info_dict['dialogue_path']), exist_ok=True)
    with open(info_dict['dialogue_path'], "r", encoding="utf-8") as f:
        dialogue = json.load(f)
    with open(info_dict['characters_path'], "r", encoding="utf-8") as f:
        characters_info = json.load(f)
    res["dialogues"] = dialogue
    with open(info_dict["script_path"], 'w', encoding='utf-8') as f:
        f.write("Storyline: "+storyline + "\n")
        for i in range(len(characters_info)):
            f.write(characters_info[i]["name"] + ": " +
                    characters_info[i]["content"] + "\n")
        f.write("\n")
        for i in range(len(dialogue)):
            f.write("第" + str(i + 1) + "章节：" + dialogue[i]["plotName"] + "，情节阶段：" + dialogue[i]
                    ["plotStage"] + "，场景：" + dialogue[i]["scene"]["name"] + "，梗概：" + dialogue[i]["beat"] + "\n")
            # 如果dialogue是属性
            if "dialogue" in dialogue[i]:

                for character in dialogue[i]["dialogue"]:
                    f.write(character["character"] + "：" +
                            character["content"] + "\n")
    return jsonify(res)


def del_brackets(s: str):
    left_bracket = -1
    for i in range(len(s)):
        if s[i] == '（':
            left_bracket = i
            continue
        if s[i] == '）':
            new_s = s[0:left_bracket] + s[i+1:]
            return new_s
    return s


@app.route("/api/do_tts", methods=['POST'])
def do_tts():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    if os.path.exists(info_dict['wav_path'] + data["data"]["filename"]):
        os.remove(info_dict['wav_path'] + data["data"]["filename"])

    action = data.get("action")
    if action == "do_tts":
        text = data["data"]["text"]
        text = del_brackets(text)
        print('do_tts text', text)
        try:
            from pathlib import Path
            from openai import OpenAI
            from llm import api_key_openai
            client = OpenAI(
                base_url="https://xiaoai.plus/v1",
                api_key=api_key_openai
            )

            speech_file_path = info_dict['wav_path'] + data["data"]["filename"]
            mapper = {
                0: 'nova',
                1: 'onyx'
            }
            id_speaker = mapper[data["data"]["id_speaker"]]
            response = client.audio.speech.create(
                model="tts-1",
                voice=id_speaker,
                input=text
            )
            response.stream_to_file(speech_file_path)
            return jsonify(info_dict['wav_path'] + data["data"]["filename"]), 200
        except Exception as e:
            print('openai failed due to: ', e)
            print('use baidu')
            id_speaker = data["data"]["id_speaker"]  # 1为男声，0为女声
            # print('id_speaker', id_speaker)
            url = "http://tsn.baidu.com/text2audio"
            header = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*"
            }
            body = {
                "tex": text,
                "tok": "24.bdff459dfc2bb287f10a5777d9265c92.2592000.1725624992.282335-102429250",
                "cuid": "FsvTrRLbtYgKul1z2dAHuO3yorA07eJ1",
                "ctp": 1,
                "lan": "zh",
                "per": id_speaker,
                "aue": 6
            }
            response = requests.post(url, headers=header, data=body)
            print('Status Code:', response.status_code)
            if response.status_code == 200:
                with open(info_dict['wav_path'] + data["data"]["filename"], 'wb') as f:
                    f.write(response.content)
                return jsonify(info_dict['wav_path'] + data["data"]["filename"]), 200
            else:
                print(
                    f'Failed to retrieve the file. Status code: {response.status_code}')
                print(response.text)
    else:
        return jsonify({"error": "Invalid action type."}), 401


@app.route('/api/fresh_backend', methods=['GET'])
def fresh_backend():
    try:
        from datetime import datetime
        now = datetime.now()
        user_id = now.strftime("%d-%m-%Y %H-%M-%S")
        print('user_id', user_id)
        # print(os.listdir('./'))

        sub_path = './opera_info'
        user_file_name = f'../../experiment_data/{user_id}'
        os.makedirs(user_file_name, exist_ok=True)
        os.makedirs(user_file_name + '/wav', exist_ok=True)
        os.makedirs(user_file_name + '/character_image', exist_ok=True)
        os.makedirs(user_file_name + '/scene_image', exist_ok=True)
        os.makedirs(f'/history', exist_ok=True)
        os.makedirs(sub_path + f'/character', exist_ok=True)
        os.makedirs(sub_path + f'/dialog', exist_ok=True)
        os.makedirs(sub_path + f'/outline', exist_ok=True)
        os.makedirs(sub_path + f'/scene', exist_ok=True)
        os.makedirs(sub_path + f'/storyline', exist_ok=True)
        os.makedirs(sub_path + f'/audio', exist_ok=True)

        history_path = sub_path + f'/history'
        history_files = os.listdir(history_path)
        history_files = [f for f in history_files if f.endswith('.json')]
        for f in history_files:
            os.rename(f'{history_path}/{f}', user_file_name + f'/{f}')

        change_path = sub_path + f'/change'
        change_files = os.listdir(change_path)
        change_files = [f for f in change_files if f.endswith('.json')]
        for f in change_files:
            os.rename(f'{change_path}/{f}', user_file_name + f'/{f}')

        wav_path = sub_path + f'/audio'
        wav_files = os.listdir(wav_path)
        wav_files = [f for f in wav_files if f.endswith('.wav')]
        for f in wav_files:
            os.rename(f'{wav_path}/{f}', user_file_name + f'/wav/{f}')

        character_path = sub_path + f'/character'
        character_files = os.listdir(character_path)
        character_image_files = [
            f for f in character_files if f.endswith('.jpeg') or f.endswith('.png')]

        character_files = [f for f in character_files if f.endswith('.json')]
        for f in character_files:
            os.rename(f'{character_path}/{f}', user_file_name + f'/{f}')

        for f in character_image_files:
            os.rename(f'{character_path}/{f}',
                      user_file_name + f'/character_image/{f}')

        dialogue_path = sub_path + f"/dialog"
        dialogue_files = os.listdir(dialogue_path)
        dialogue_files = [f for f in dialogue_files if f.endswith('.json')]
        for f in dialogue_files:
            os.rename(f'{dialogue_path}/{f}', user_file_name + f'/{f}')

        outline_path = sub_path + f"/outline"
        outline_files = os.listdir(outline_path)
        outline_files = [f for f in outline_files if f.endswith('.json')]
        for f in outline_files:
            os.rename(f'{outline_path}/{f}', user_file_name + f'/{f}')

        scene_path = sub_path + f"/scene"
        scene_files = os.listdir(scene_path)
        scene_image_files = [f for f in scene_files if f.endswith(
            '.jpeg') or f.endswith('.png')]
        scene_files = [f for f in scene_files if f.endswith('.json')]
        for f in scene_files:
            os.rename(f'{scene_path}/{f}', user_file_name + f'/{f}')

        for f in scene_image_files:
            os.rename(f'{scene_path}/{f}', user_file_name + f'/{f}')

        storyline_path = sub_path + f"/storyline"
        storyline_files = os.listdir(storyline_path)
        for f in storyline_files:
            os.rename(f'{storyline_path}/{f}', user_file_name + f'/{f}')

        return jsonify({'result': True, 'filename': str(user_id)}), 200
    except Exception as e:
        # print(e)
        return jsonify({"result": str(e)}), 400


@app.route('/api/get_audio', methods=['GET'])
def get_audio():
    # 从前端请求中获取音频文件名
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    # 检查文件是否存在
    AUDIO_DIRECTORY = f'./opera_info/audio/'
    file_path = os.path.join(AUDIO_DIRECTORY, filename)
    if os.path.exists(file_path):
        return send_from_directory(AUDIO_DIRECTORY, filename)
    else:
        return abort(404, description="File not found")


@app.route('/api/get_vis', methods=['POST'])
def get_vis():
    # 获取当前工作目录
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    file_path = os.path.join(current_dir, 'opera_info', 'character', 'characters.json')

    # 读取原始JSON文件
    with open(file_path, 'r') as file:
        characters = json.load(file)

    # 生成关系图
    G = nx.Graph()

    # 添加节点和边
    for character in characters:
        name = character['name']
        G.add_node(name)
        for related_name in character['related']:
            G.add_edge(name, related_name)

    net = Network(notebook=True, 
                  height="750px", 
                  width="100%", 
                  cdn_resources='in_line', #生成资源嵌入html
                  font_color="#000000",  #节点的颜色
                  )

    for character in characters:
        name = character["name"]
        if 'image' not in character:
            character['image'] = ""

        # image_path = character['image']
        # if image_path.startswith('/api/get_image'):
        #     image_path = f"{request.host_url}{image_path.lstrip('/')}"
        net.add_node(name, 
                     label=name, 
                     shape="circularImage",
                    #  image=image_path, 
                     image=character.get('image'),
                     size=30,  
                     title=name,
                     )

    for edge in G.edges():
        net.add_edge(edge[0],
                     edge[1],
                     color="#808080", 
                     width=2)

    # 生成HTML文件
    html_file_path = './template/character_relations.html'
    net.show(html_file_path)

    # 返回生成的HTML文件
    return jsonify({'path': html_file_path})

# @app.route('=/api/get_image', methods=['GET'])
# def serve_image():
#     filename = request.args.get('filename')
#     path = request.args.get('path')
#     return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), path), filename)

@app.route('/api/get_vis/get_html', methods=['GET'])
def get_html():
    return render_template("character_relations.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    
