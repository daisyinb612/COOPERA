from flask import Flask, request, jsonify, send_file
import requests
from excel import ExcelOp
from llm import LLM
from flask_cors import CORS
import json
 
app = Flask(__name__)
CORS(app)


 
# Configuration dictionary
info_dict = {
   "apikey": "e4ab8bb5cc7cc6eb620f9cde3093b8b4.FauytagDuxsJpEuD",
   "world_setting_path": "./opera_info/storyline/storyline.txt",
   "characters_path": "./opera_info/character/characters.json",
   "outline_path": "./opera_info/outline/outline.json",
   "scene_path": "./opera_info/scene/scene.json",
   "dialogue_path": "./opera_info/dialog/dialogue_path.json",
   "picture_path": "./opera_info/img",
   "wav_path": "../../front-end/public/"
}
 
@app.route('/upload_storyline', methods=['POST'])
def upload_storyline():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    if action == "upload_storyline":
        with open(info_dict['world_setting_path'], 'w', encoding='utf-8') as f:
            f.write(data["data"]["storyline"])
        storyline = data["data"]["storyline"]
        question = "\n###故事线###:" + storyline
        l = LLM(apikey=info_dict["apikey"])
        answer = l.ask(question=question, prompt=l.setting_role_create)
        plot = l.analyze_answer(answer)
        with open(info_dict['characters_path'], 'w', encoding='utf-8') as f:
            json.dump(plot, f, indent=4, ensure_ascii=False)
        return jsonify(plot)
    else:
        return jsonify({"error": "Invalid action type."}), 401
 
@app.route('/get_storyline_help', methods=['POST'])
def get_storyline_help():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402

    storyline = data["data"]["storyline"]
    history = data["data"]["history"]
    user_input = data["data"]["user_input"]

    question = "\n###故事线###:" + storyline + "\n###我的问题###:" + user_input
    l = LLM(apikey=info_dict["apikey"])
    answer = l.ask(question=question, prompt=l.storyline_help, history=history)
    print("Yes")

    return jsonify({"answer": answer})
 
@app.route('/get_saved_storyline', methods=['GET'])
def get_saved_storyline():
    with open(info_dict['world_setting_path'], 'r', encoding='utf-8') as f:
        storyline = f.read()
    return jsonify({"storyline": storyline})
 
# @app.route('/init_character_generation', methods=['POST'])
# def init_character_generation():
#     with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
#         storyline = f.read()
#     question = "###故事线###:" + storyline
#     l = LLM(apikey=info_dict["apikey"])
#     answer = l.ask(question=question, prompt=l.setting_role_create)
#     characters = l.analyze_answer(answer)
#     l.save_json_to_excel(json_object=characters, filepath=info_dict["characters_path"])
#     return jsonify(characters)
 
@app.route('/get_character_help', methods=['POST'])
def get_character_help():
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    with open(info_dict['characters_path'], "r", encoding="utf-8") as f:
        characters = json.load(f)
    data = request.get_json()
    history = data["data"]["history"]
    user_input = data["data"]["user_input"]
    question = "\n###故事线###:" + storyline + "\n###角色表###:"
    for character in characters:
        question += character["name"] + ": " + character["content"] + "\n"
    question += "\n###我的问题###:" + user_input
    l = LLM(apikey=info_dict["apikey"])
    answer = l.ask(question=question, prompt=l.role_help, history=history)
    return jsonify({"answer": answer})
 
# @app.route('/save_character_asset', methods=['POST'])
# def save_character_asset():
#     data = request.get_json()
#     l = LLM(apikey=info_dict["apikey"])
#     l.save_json_to_excel(json_object=data["data"], filepath=info_dict["characters_path"])
#     return jsonify({})
 
@app.route('/init_plot_generation', methods=['POST'])
def init_plot_generation():
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    characters = request.get_json()["data"]["characters"]
    question = "\n###故事线###:" + storyline + "\n###角色表###:"
    for character in characters:
        question += "角色名： "+character["name"] + "角色描述:  " + character["content"]+"角色音色： " + character["per"] + "\n"
    l = LLM(apikey=info_dict["apikey"])
    answer = l.ask(question=question, prompt=l.setting_outline_create)
    plot = l.analyze_answer(answer)
    with open(info_dict['outline_path'], 'w', encoding='utf-8') as f:
        json.dump(plot, f, indent=4, ensure_ascii=False)
    scene = [{"name": x["scene"], "url": ""} for x in plot]
    with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
        json.dump(scene, f, indent=4, ensure_ascii=False)
        
    return jsonify(plot)
 
@app.route('/update_plot', methods=['POST'])
def update_plot():
    data = request.get_json()
    plot = data["data"]
    l = LLM(apikey=info_dict["apikey"])
    with open(info_dict['outline_path'], 'w', encoding='utf-8') as f:
        json.dump(plot, f, indent=4, ensure_ascii=False)
    return jsonify({})
 
# @app.route('/init_scene_generation', methods=['POST'])
# def init_scene_generation():
#     with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
#         storyline = f.read()
#     with open(info_dict['outline_path'], "r", encoding="utf-8") as f:
#         plot = json.load(f)
#     question = "\n###故事线###:" + storyline + "\n###角色表###:" + plot
#     l = LLM(apikey=info_dict["apikey"])
#     answer = l.ask(question=question, prompt=l.setting_scene_create)
#     scene = l.analyze_answer(answer)
#     l.save_json_to_excel(json_object=scene, filepath=info_dict["scene_path"])
#     return jsonify(scene)
 
@app.route('/save_scene_asset', methods=['POST'])
def save_scene_asset():
    data = request.get_json()
    index = data["data"]["index"]
    scene = data["data"]["scene"]
    l = LLM(apikey=info_dict["apikey"])
    with open(info_dict['scene_path'], 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    old_data[index] = scene
    print(scene)
    with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=4, ensure_ascii=False)
    return jsonify({})

@app.route("/delete_scene_asset", methods=['POST'])
def delete_scene_asset():
    data = request.get_json()
    index = data["data"]["index"]
    with open(info_dict['scene_path'], 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    old_data.pop(index)
    with open(info_dict['scene_path'], 'w', encoding='utf-8') as f:
        json.dump(old_data, f, indent=4, ensure_ascii=False)
    return jsonify({})

@app.route("/generate_audio", methods=['POST'])
def generate_audio():
    data = request.get_json()
    text = data["data"]["text"]
    wav = get_wav(text)
    return jsonify({"wav": wav})
    

 
@app.route('/init_dialogue_generation', methods=['POST'])
def init_dialogue_generation():
    data = request.get_json()
    e = ExcelOp(file=info_dict["outline_path"])
    number = int(data["data"]["plot_number"])
    outline_pass = e.get_json_by_row(number + 1) if number >= 2 else "无"
    outline_now = e.get_json_by_row(number + 1)
    question = "\n###前情提要###:" + outline_pass + "\n###本章大纲###:" + outline_now
    l = LLM(apikey=info_dict["apikey"])
    answer = l.ask(question=question, prompt=l.setting_dialogue_create)
    dialogue = l.analyze_answer(answer)
    l.add_json_to_excel(json_object=dialogue, filepath=info_dict["dialogue_path"])
    return jsonify(dialogue)
 
@app.route('/save_dialogue_asset', methods=['POST'])
def save_dialogue_asset():
    data = request.get_json()
    number = int(data["data"]["plot_number"])
    dialogue = data["data"]["dialogue"]
    l = LLM(apikey=info_dict["apikey"])
    l.update_json_to_excel(json_object=dialogue, filepath=info_dict["dialogue_path"], sheet_index=number - 1)
    return jsonify({})

@app.route('/create_scene_picture', methods=['POST'])
def create_scene_picture():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 402

        action = data.get("action")
        if action == "create_scene_picture":
            prompt = "请生成场景图片， 场景的名称为："+data["data"]["name"]
            if data["data"]["user_input"] != "":
                prompt += "场景的描述为："+data["data"]["user_input"]
            name = data["data"]["name"]
            l = LLM(apikey=info_dict["apikey"])
            picture = l.create_picture(prompt=prompt)
            return jsonify({"image": picture})
        else:
            return jsonify({"error": "Invalid action type."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/create_character_picture', methods=['POST'])
def create_character_picture():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 402

        action = data.get("action")
        if action == "create_character_picture":
            prompt = "请生成角色图片， 角色的名称为："+data["data"]["name"]+"，角色的描述为"+data["data"]["user_input"]
            name = data["data"]["name"]
            l = LLM(apikey=info_dict["apikey"])
            picture = l.create_picture(prompt=prompt)
            return jsonify({"image": picture})
        else:
            return jsonify({"error": "Invalid action type."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/update_character", methods=['POST'])
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
    

@app.route("/delete_character", methods=['POST'])
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
    
# @app.route('/get_character_image_help', methods=['POST'])
# def get_character_image_help():
#     try:
#         data = request.get_json()
#         if not data:
#             return jsonify({"error": "Invalid JSON"}), 402
#         action = data.get("action")
#         if action == "get_character_image_help":
#             prompt = data["data"]["user_input"]
#             l = LLM(apikey=info_dict["apikey"])
#             picture = l.create_picture(filepath=filepath, prompt=prompt)
#             return jsonify({"image": picture})
#         else:
#             return jsonify({"error": "Invalid action type."}), 401
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500  

@app.route('/get_scene_help', methods=['POST'])
def get_scene_help():
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    with open(info_dict['outline_path'], "r", encoding="utf-8") as f:
        plot = json.load(f)

    data = request.get_json()
    history = data["data"]["history"]
    question = "\n###故事线###：" + storyline + "\n###故事大纲###："

    for i in range(len(plot)):
        plotName = plot[i]["plotName"]
        plotStage = plot[i]["plotStage"]
        scene = plot[i]["scene"]
        beat = plot[i]["beat"]
        characters = ', '.join(plot[i]["characters"])
        question += f"\n第{i + 1}章：情节名"   +  plotName + "，情节阶段" + plotStage + "，场景" + scene + "，梗概" + beat + "，角色表" + characters
    l = LLM(apikey=info_dict["apikey"])
    answer = l.ask(question=question, prompt=l.role_help, history=history)
    return jsonify({"answer": answer})

@app.route('/generate_dialogue', methods=['POST'])
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
    question = "\n###故事线###:" + storyline + "\n###故事大纲###：章节：" + plotName + "，情节阶段" + plotStage + "，场景名字" + sceneName + ', 场景描述' + sceneContent + "，梗概" + beat + "，角色表"
    for character in characters:
        question += character + " "
    l = LLM(apikey=info_dict["apikey"])
    answer = l.ask(question=question, prompt=l.setting_dialogue_create)
    scene = l.analyze_answer(answer)
    l.save_json_to_excel(json_object=scene, filepath=info_dict["scene_path"])
    return jsonify(scene)


@app.route("/upload_dialogue", methods=['POST'])
def upload_dialogue():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    if action == "upload_dialogue":
        with open(info_dict['dialogue_path'], 'w', encoding='utf-8') as f:
            json.dump(data["data"], f, indent=4, ensure_ascii=False)

        return jsonify({"message": "Dialogue uploaded successfully."})
    else:
        return jsonify({"error": "Invalid action type."}), 401
    
@app.route("/generate_script", methods=['GET'])
def generate_script():
    res = {
        "storylines": "",
        "dialogues": ""
    }
    with open(info_dict['world_setting_path'], "r", encoding="utf-8") as f:
        storyline = f.read()
    res["storylines"] = storyline
    with open(info_dict['dialogue_path'], "r", encoding="utf-8") as f:
        dialogue = json.load(f)
    res["dialogues"] = dialogue
    return jsonify(res)

@app.route("/do_tts", methods=['POST'])
def do_tts():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 402
    action = data.get("action")
    if action == "do_tts":
        text = data["data"]["text"]
        id_speaker = data["data"]["id_speaker"] #1为男声，0为女声
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
            return send_file(info_dict['wav_path'] + data["data"]["filename"], mimetype="audio/wav")
        
        else:
            print(f'Failed to retrieve the file. Status code: {response.status_code}')
            print(response.text)
    else:
        return jsonify({"error": "Invalid action type."}), 401
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)