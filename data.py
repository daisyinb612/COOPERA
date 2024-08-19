import os

user_id = '1'

user_file_name = f'./experiment_data/{user_id}'
os.makedirs(user_file_name, exist_ok=True)
os.makedirs(user_file_name + '/wav', exist_ok=True)
os.makedirs(user_file_name + '/character_image', exist_ok=True)
os.makedirs(user_file_name + '/scene_image', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/history', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/character', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/dialog', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/outline', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/scene', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/change', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/storyline', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/audio', exist_ok=True)


history_path = "./back-end/程序/opera_info/history"
history_files = os.listdir(history_path)
history_files = [f for f in history_files if f.endswith('.json')]
for f in history_files:
    os.rename(f'{history_path}/{f}', user_file_name + f'/{f}')

change_path = "./back-end/程序/opera_info/change"
change_files = os.listdir(change_path)
change_files = [f for f in change_files if f.endswith('.json')]
for f in change_files:
    os.rename(f'{change_path}/{f}', user_file_name + f'/{f}')



wav_path = './back-end/程序/opera_info/audio'
wav_files = os.listdir(wav_path)
wav_files = [f for f in wav_files if f.endswith('.wav')]
for f in wav_files:
    os.rename(f'{wav_path}/{f}', user_file_name + f'/wav/{f}')

# audio_path = "./back-end/程序/opera_info/audio"
# audio_files = os.listdir(audio_path)
# # 删除所有文件
# for f in audio_files:
#     os.remove(f'{audio_path}/{f}')

character_path = "./back-end/程序/opera_info/character"
character_files = os.listdir(character_path)
character_image_files = [f for f in character_files if f.endswith('.jpeg') or f.endswith('.png')]

character_files = [f for f in character_files if f.endswith('.json')]
for f in character_files:
    os.rename(f'{character_path}/{f}', user_file_name + f'/{f}')

for f in character_image_files:
    os.rename(f'{character_path}/{f}', user_file_name + f'/character_image/{f}')

dialogue_path = "./back-end/程序/opera_info/dialog"
dialogue_files = os.listdir(dialogue_path)
dialogue_files = [f for f in dialogue_files if f.endswith('.json')]
for f in dialogue_files:
    os.rename(f'{dialogue_path}/{f}', user_file_name + f'/{f}')

outline_path = "./back-end/程序/opera_info/outline"
outline_files = os.listdir(outline_path)
outline_files = [f for f in outline_files if f.endswith('.json')]
for f in outline_files:
    os.rename(f'{outline_path}/{f}', user_file_name + f'/{f}')

scene_path = "./back-end/程序/opera_info/scene"
scene_files = os.listdir(scene_path)
scene_image_files = [f for f in scene_files if f.endswith('.jpeg') or f.endswith('.png')]
scene_files = [f for f in scene_files if f.endswith('.json')]
for f in scene_files:
    os.rename(f'{scene_path}/{f}', user_file_name + f'/{f}')

for f in scene_image_files:
    os.rename(f'{scene_path}/{f}', user_file_name + f'/{f}')

storyline_path = "./back-end/程序/opera_info/storyline"
storyline_files = os.listdir(storyline_path)
storyline_files = [f for f in storyline_files if f.endswith('.txt')]
for f in storyline_files:
    os.rename(f'{storyline_path}/{f}', user_file_name + f'/{f}')



