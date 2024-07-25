import requests
import json
URL = 'http://localhost:8000/'

def test_upload_storyline():
    data = {
        'action': 'upload_storyline',
        'data': {
        'storyline': '在一个宁静的小镇上，年轻勇敢的少年杰克无意间在祖父的遗物中发现了一张藏宝图。杰克决定踏上寻宝之旅，途中结识了机智的女孩莉莉和忠诚的小狗巴克。三人克服重重困难，解开了一个又一个谜题。最终，他们找到了传说中的宝藏，并用它帮助小镇的人们过上了幸福美满的生活。而杰克、莉莉和巴克也成为了小镇上的英雄。'
    }
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL+ '/upload_storyline', data=json_data, headers=headers) #在使用flask_server时需要再url后添加具体端点信息，否则不需要
    assert response.status_code == 200

 
def test_get_storyline_help():
    '''
    print("以下为无消息历史的情况")
    data = {
        'action': 'get_storyline_help',
        'data': {
            'storyline': '在一个宁静的小镇上，年轻勇敢的少年杰克无意间在祖父的遗物中发现了一张藏宝图。杰克决定踏上寻宝之旅，途中结识了机智的女孩莉莉和忠诚的小狗巴克。三人克服重重困难，解开了一个又一个谜题。最终，他们找到了传说中的宝藏，并用它帮助小镇的人们过上了幸福美满的生活。而杰克、莉莉和巴克也成为了小镇上的英雄。',
            'history': None, #前端使用的Node.js，因此这里的None应该进行替换
            'user_input': '你能帮我完善一下这个故事线吗'
    }
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, data=json_data, headers=headers)
    #print(response)
    assert response.status_code == 200
    assert response.text
    print("返回的信息为：")
    print(response.text)'''
    print("以下为有消息历史的情况")
    data = {
        'action': 'get_storyline_help',
        'data': {
            'storyline': '在一个宁静的小镇上，年轻勇敢的少年杰克无意间在祖父的遗物中发现了一张藏宝图。杰克决定踏上寻宝之旅，途中结识了机智的女孩莉莉和忠诚的小狗巴克。三人克服重重困难，解开了一个又一个谜题。最终，他们找到了传说中的宝藏，并用它帮助小镇的人们过上了幸福美满的生活。而杰克、莉莉和巴克也成为了小镇上的英雄。',
            'history': [{"role": "user", "content": "你好"},{"role": "assistant", "content": "你好"}], #前端使用的Node.js，因此这里的None应该进行替换
            'user_input': '你能帮我完善一下这个故事线吗'
    }
    }
    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL+ '/get_storyline_help', data=json_data, headers=headers)
    #print(response)
    assert response.status_code == 200
    assert response.text
    print("返回的信息为：")
    print(response.text)

def test_get_saved_storyline():
    data = {
        'action': 'get_saved_storyline',
        'data': None
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/get_storyline_help', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)
def test_init_character_generation():
    data = {
        'action': 'init_character_generation',
        'data': None
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/init_character_generation', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)
def test_get_character_help():
    data = {
        'action': 'get_character_help',
        'data': {
            'history': [{"role": "user", "content": "你好"},{"role": "assistant", "content": "你好"}], #前端使用的Node.js，因此这里的None应该进行替换
            'user_input': '你能帮我再丰富一下角色信息吗'
    }
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/get_character_help', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)
def test_save_character_asset():
    data = {
        'action': 'save_character_asset',
        'data': [
    {
        "角色名字": "杰克",
        "角色介绍": "年轻勇敢的少年，因祖父的藏宝图而踏上了寻宝之旅，是故事的主人公。"
    },
    {
        "角色名字": "莉莉",
        "角色介绍": "机智聪明的女孩，与杰克在寻宝途中相遇，并成为他的伙伴，为寻宝小队带来了许多关键性的智慧。"
    },
    {
        "角色名字": "巴克",
        "角色介绍": "忠诚的小狗，陪伴杰克和莉莉共同克服困难，是寻宝途中的重要成员。"
    },
    {
        "角色名字": "祖父",
        "角色介绍": "杰克的祖父，已故，留下了一张神秘的藏宝图，引发了整个故事。"
    },
    {
        "角色名字": "小镇居民",
        "角色介绍": "小镇上的居民，在杰克、莉莉和巴克的帮助下，最终过上了幸福美满的生活。"
    }
]
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/save_character_asset', data=json_data, headers=headers)
    assert response.status_code == 200

def init_plot_generation():
    data = {
        'action': 'init_plot_generation',
        'data': None
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/init_plot_generation', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)

def update_plot():
    data = {
        'action': 'update_plot',
        'data': [
  {
    "章节名": "祖父的遗物",
    "故事阶段": "Expositon",
    "情节梗概": "杰克在整理祖父的遗物时发现了一张古老的藏宝图，激发了他的好奇心和探险欲望。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"祖父"}]
  },
  {
    "章节名": "遇见莉莉",
    "故事阶段": "Inciting Incident",
    "情节梗概": "杰克在准备寻宝时遇见了同样机智的莉莉，两人决定一起展开寻宝之旅。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"莉莉"}]
  },
  {
    "章节名": "巴克的加入",
    "故事阶段": "Conflict",
    "情节梗概": "忠诚的小狗巴克加入了杰克和莉莉的队伍，他们一起遇到了第一个难题。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"莉莉"}, {"角色名字":"巴克"}]
  },
  {
    "章节名": "谜题重重",
    "故事阶段": "Rising Action",
    "情节梗概": "寻宝小队在旅途中不断解开各种谜题，困难重重，但他们的友谊和勇气不断增强。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"莉莉"}, {"角色名字":"巴克"}]
  },
  {
    "章节名": "发现宝藏",
    "故事阶段": "Climax",
    "情节梗概": "经过一系列的冒险和挑战，杰克、莉莉和巴克终于找到了传说中的宝藏。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"莉莉"}, {"角色名字":"巴克"}]
  },
  {
    "章节名": "小镇的幸福",
    "故事阶段": "Falling Action",
    "情节梗概": "他们用宝藏帮助小镇发展，小镇居民的生活质量得到了极大的提高。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"莉莉"}, {"角色名字":"巴克"}, {"角色名字":"小镇居民"}]
  },
  {
    "章节名": "英雄归来",
    "故事阶段": "Denouement",
    "情节梗概": "杰克、莉莉和巴克被小镇居民视为英雄，他们的故事被传颂，成为了小镇的传奇。",
    "参与人物": [{"角色名字":"杰克"}, {"角色名字":"莉莉"}, {"角色名字":"巴克"}, {"角色名字":"小镇居民"}]
  }
]
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/update_plot', data=json_data, headers=headers)
    assert response.status_code == 200

def init_scene_generation():
    data = {
        'action': 'init_scene_generation',
        'data': None
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/init_scene_generation', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)

def save_scene_asset():
    data = {
        'action': 'save_scene_asset',
        'data': [
    {"场景名称": "杰克的房间",
     "场景介绍": "杰克在整理祖父的遗物时发现藏宝图，房间充满了旧时的回忆和神秘的氛围。"}
    ,
    {"场景名称": "小镇的广场",
     "场景介绍": "杰克在此与莉莉相遇，两人讨论藏宝图并决定一起寻宝，广场上人们忙碌而和谐。"}
    ,
    {"场景名称": "森林边缘",
     "场景介绍": "在这里，巴克加入了杰克和莉莉，森林神秘且充满未知，他们的寻宝之旅正式开始。"}
    ,
    {"场景名称": "古老的神庙",
     "场景介绍": "寻宝小队在此解开第一个谜题，神庙内部阴暗，充满了机关和陷阱。"}
    ,
    {"场景名称": "荒凉的沙漠",
     "场景介绍": "在穿越沙漠时，他们遇到了第二个难题，环境恶劣，但队伍的团结和智慧帮助他们继续前进。"}
    ,
    {"场景名称": "隐藏的洞穴",
     "场景介绍": "最终，杰克、莉莉和巴克在洞穴中发现了宝藏，洞穴内部宽敞且神秘，充满了古代的遗迹。"}
    ,
    {"场景名称": "小镇的庆典",
     "场景介绍": "寻宝小队回到小镇，举办庆典感谢他们的贡献，小镇焕然一新，到处都是欢声笑语。"}
    ,
    {"场景名称": "小镇的纪念碑",
     "场景介绍": "为了纪念他们的英勇，小镇树立了一座纪念碑，杰克、莉莉和巴克的名字刻在上面，成为小镇的传奇。"}
]
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/save_scene_asset', data=json_data, headers=headers)
    assert response.status_code == 200

def init_dialogue_generation():
    data = {
        'action': 'init_dialogue_generation',
        'data': {"plot_number":"1"}
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/init_dialogue_generation', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)
    print()
    print("测试写第二段")
    data = {
        'action': 'init_dialogue_generation',
        'data': {"plot_number":"2"}
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL, data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)

def test_save_dialogue_asset():
    data = {
        'action': 'save_dialogue_asset',
        'data': {"plot_number":"3","dialogue":[
    {"对话编号": "1",
    "角色名字": "杰克",
    "话语内容":"这个地图上的标记看起来是个不错的起点，但一个人寻宝似乎太孤单了。"
    },
    {"对话编号": "2",
    "角色名字": "莉莉",
    "话语内容":"孤单？哈哈，如果你愿意的话，我可以成为你的伙伴。地图上的标记我也注意到了，似乎是个有趣的谜题。"
    },
    {"对话编号": "3",
    "角色名字": "杰杰",
    "话语内容":"真的吗？那太棒了！有个聪明的伙伴总比单打独斗强。我们一起解开这个谜题，找到宝藏吧！"
    },
    {"对话编号": "4",
    "角色名字": "莉莉",
    "话语内容":"那就这么定了！不过，我们得小心，寻宝的人不止我们两个，竞争可是激烈的。"
    },
    {"对话编号": "5",
    "角色名字": "杰克",
    "话语内容":"我知道，但有了你，我相信我们能够应对任何挑战。现在，让我们开始这个冒险吧！"
    }
]
                 }
    }
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/save_dialogue_asset', data=json_data, headers=headers)
    assert response.status_code == 200

def test_create_picture():
    data = {
        'action': 'create_picture',
        'data': {"name":"古老的神庙","user_input":"神庙内部阴暗，充满了机关和陷阱。"}
    }
    headers = {'Content-Type': 'png/jpg'}
    json_data = json.dumps(data)
    response = requests.post(URL+ '/create_picture', data=json_data, headers=headers)
    assert response.status_code == 200
    print("返回的信息为：")
    print(response.text)

if __name__ == '__main__':
    #test_upload_storyline()
    test_get_storyline_help()
    #test_get_saved_storyline()
    #test_init_character_generation()
    #test_get_character_help()
    #test_save_character_asset()
    #init_plot_generation()
    #update_plot()
    #init_scene_generation()
    #save_scene_asset()
    #init_dialogue_generation()
    #test_save_dialogue_asset()
    #test_create_picture()
    pass