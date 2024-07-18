import json
str = '''{
   "action": "get_assistance",
   "data": {
     "storyline": "用户输入的故事线",
     "history": [
       {"role": "user", "content": "question"},
       {"role": "assistant", "content": "answer"}
     ],
     "user_input": "最后一次提问的内容（在输入框读取）"
   }
   }'''
json_object = json.loads(str)
print(json_object["data"]["history"])