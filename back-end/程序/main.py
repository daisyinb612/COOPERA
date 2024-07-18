from llm import LLM
from db import DB
from excel import ExcelOp

def test_rag():
    d = DB()
    d.creat_db_empty(savepath="./向量数据库/已完成的语料")
    d.add_file(filepath="./剧本信息/世界观设定/1.txt",savepath="./向量数据库/已完成的语料")
    d.search_from_db(savepath="./向量数据库/已完成的语料",question="地球遭受了名为什么的灾难")

def create_world_setting(world_setting_path):
    apikey = "e4ab8bb5cc7cc6eb620f9cde3093b8b4.FauytagDuxsJpEuD"
    a = LLM(apikey=apikey)
    print("请输入世界观的主题关键词(用“，”隔开)")
    question = "###主题关键词###："
    question += input()
    world_setting = a.ask(question=question,prompt=a.setting_world_create)
    with open(world_setting_path,"w",encoding="utf-8") as f:
        f.write(world_setting)
    f.close()

def create_characters_setting(world_setting_path,characters_path = './剧本信息/角色设定/characters.xlsx'):
    apikey = "e4ab8bb5cc7cc6eb620f9cde3093b8b4.FauytagDuxsJpEuD"
    a = LLM(apikey=apikey)
    d = DB()
    question = d.get_world_setting(filepath=world_setting_path)
    answer= a.ask(prompt=a.setting_role_create,question=question)
    characters = a.analyze_answer(answer)
    print(characters)
    a.save_json_to_excel(json_object=characters,filepath=characters_path)

def create_ouline_setting(world_setting_path,characters_setting_path,outline_path = './剧本信息/故事大纲/outline.xlsx'):
    apikey = "e4ab8bb5cc7cc6eb620f9cde3093b8b4.FauytagDuxsJpEuD"
    a = LLM(apikey=apikey)
    d = DB() 
    c = ExcelOp(characters_setting_path)
    question = d.get_world_setting(filepath=world_setting_path)
    question += "\n###角色设定###："+c.get_json_all()
    answer= a.ask(prompt=a.setting_outline_create,question=question)
    outline = a.analyze_answer(answer)
    print(outline)
    a.save_json_to_excel(json_object=outline,filepath=outline_path)

def create_detail(world_setting_path,characters_setting_path,outline_path,detail_path,chapter_nunmber):
    apikey = "e4ab8bb5cc7cc6eb620f9cde3093b8b4.FauytagDuxsJpEuD"
    a = LLM(apikey=apikey)
    d = DB() 
    c = ExcelOp(characters_setting_path)
    e = ExcelOp(outline_path)
    question = d.get_world_setting(filepath=world_setting_path)
    question += "\n###角色设定###："+c.get_json_all()
    question += "\n###本章大纲###："+e.get_json_by_row(chapter_nunmber)
    question += "\n###前情提要###:"+"无" #后续将修改为从已完成的情节中总结
    answer= a.ask(prompt=a.setting_dialogue_create,question=question)
    #detail = a.analyze_answer(answer)
    #print(detail)

if __name__ == "__main__":
    world_setting_path = "./剧本信息/世界观设定/2.txt"
    characters_path = './剧本信息/角色设定/characters.xlsx'
    outline_path = './剧本信息/故事大纲/outline.xlsx'
    #create_world_setting(world_setting_path)
    #create_characters_setting(world_setting_path)
    #create_ouline_setting(world_setting_path=world_setting_path,characters_setting_path=characters_path)
    create_detail(world_setting_path,characters_path,outline_path,detail_path="",chapter_nunmber=2)
    #test_rag()