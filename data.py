import os

user_id = 3

os.makedirs(f'./{user_id}', exist_ok=True)
os.makedirs(f'./{user_id}/wav', exist_ok=True)
os.makedirs(f'./{user_id}/character_image', exist_ok=True)
os.makedirs(f'./{user_id}/scene_image', exist_ok=True)
os.makedirs(f'./back-end/程序/history', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/character', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/dialog', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/outline', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/scene', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/storyline', exist_ok=True)
os.makedirs(f'./back-end/程序/opera_info/audio', exist_ok=True)

wav_path = './back-end/程序/opera_info/audio'
wav_files = os.listdir(wav_path)
wav_files = [f for f in wav_files if f.endswith('.wav')]
for f in wav_files:
    os.rename(f'{wav_path}/{f}', f'./{user_id}/wav/{f}')

audio_path = "./back-end/程序/opera_info/audio"
audio_files = os.listdir(audio_path)
# 删除所有文件
for f in audio_files:
    os.remove(f'{audio_path}/{f}')

history_path = "./back-end/程序/history"
history_files = os.listdir(history_path)
history_files = [f for f in history_files if f.endswith('.jsonl')]
for f in history_files:
    os.rename(f'{history_path}/{f}', f'./{user_id}/{f}')

character_path = "./back-end/程序/opera_info/character"
character_files = os.listdir(character_path)
character_image_files = [f for f in character_files if f.endswith('.jpeg') or f.endswith('.png')]

character_files = [f for f in character_files if f.endswith('.json')]
for f in character_files:
    os.rename(f'{character_path}/{f}', f'./{user_id}/{f}')

for f in character_image_files:
    os.rename(f'{character_path}/{f}', f'./{user_id}/character_image/{f}')

dialogue_path = "./back-end/程序/opera_info/dialog"
dialogue_files = os.listdir(dialogue_path)
dialogue_files = [f for f in dialogue_files if f.endswith('.json')]
for f in dialogue_files:
    os.rename(f'{dialogue_path}/{f}', f'./{user_id}/{f}')

outline_path = "./back-end/程序/opera_info/outline"
outline_files = os.listdir(outline_path)
outline_files = [f for f in outline_files if f.endswith('.json')]
for f in outline_files:
    os.rename(f'{outline_path}/{f}', f'./{user_id}/{f}')

scene_path = "./back-end/程序/opera_info/scene"
scene_files = os.listdir(scene_path)
scene_image_files = [f for f in scene_files if f.endswith('.jpeg') or f.endswith('.png')]
scene_files = [f for f in scene_files if f.endswith('.json')]
for f in scene_files:
    os.rename(f'{scene_path}/{f}', f'./{user_id}/{f}')

for f in scene_image_files:
    os.rename(f'{scene_path}/{f}', f'./{user_id}/scene_image/{f}')

storyline_path = "./back-end/程序/opera_info/storyline"
storyline_files = os.listdir(storyline_path)
for f in storyline_files:
    os.rename(f'{storyline_path}/{f}', f'./{user_id}/{f}')



