import requests
def do_tts(text,id_speaker,path):
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
        "per": id_speaker, #1为男声，0为女声
        "aue": 6
    }
    response = requests.post(url, headers=header, data=body)
    print('Status Code:', response.status_code)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            file.write(response.content)
        return response.content
    else:
        print(f'Failed to retrieve the file. Status code: {response.status_code}')
        print(response.text)