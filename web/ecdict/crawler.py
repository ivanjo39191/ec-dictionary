import requests
from bs4 import BeautifulSoup



def crawler(vocabulary):
    
    en_dict = None
    
    html = get_html(vocabulary)
    try:
        en_dict = get_ecdict(html)
    except:
        try:
            origin_vocabulary_explanation = html.find('div', class_='dictionaryExplanation').text
            origin_vocabulary = origin_vocabulary_explanation.split('的')[0]
            html = get_html(origin_vocabulary)
            en_dict = get_ecdict(html)
        except:
            pass
    return en_dict

def get_html(vocabulary):
    print(vocabulary)
    url = f"https://tw.dictionary.search.yahoo.com/search?p={vocabulary}&fr2=dict"
    response = requests.get(url)
    html = BeautifulSoup(response.text, "html.parser")
    return html

def get_ecdict(html):
    # 例外待處理 bandanas healthcare
    origin_vocabulary = None
    other_keywords = ['過去式', '動詞過去式', '過去分詞', '動詞過去分詞', '動詞現在分詞', '現在進行式', '動詞現在進行式', '名詞複數', '形容詞比較級']
    title = html.find('div', class_='compTitle mt-25 mb-10').find('h3', class_='title').find('span').text
    try:
        kk = " ".join([k.text for k in html.find('div', class_='compList d-ib').find('ul').find_all('li')])
    except:
        kk = ""
    part_of_speech_result_list = []
    part_of_speech_list = html.find('div', class_='compList mb-25 p-rel').find('ul').find_all('li')
    for part_of_speech in part_of_speech_list:
        # 可能沒有詞性
        try:
            pos_button = part_of_speech.find('div', class_='pos_button').text
            dictionary_explanation = part_of_speech.find('div', class_='dictionaryExplanation').text
            part_of_speech_result_list.append([pos_button, dictionary_explanation])
        except:
            dictionary_explanation = part_of_speech.find('div', class_='dictionaryExplanation').text
            part_of_speech_result_list.append(['', dictionary_explanation])
        # 如果有原始單字
        for other_keyword in other_keywords:
            if other_keyword in dictionary_explanation:
                dictionary_explanation_part = dictionary_explanation.split('；')
                for part in dictionary_explanation_part:
                    if other_keyword in part:
                        try:
                            origin_vocabulary_split = part.split(f'的{other_keyword}')
                            # 切開之後要有至少兩個段落才代表有找到值
                            if len(origin_vocabulary_split) > 1:
                                origin_vocabulary = origin_vocabulary_split[0]
                        except:
                            pass
                        if origin_vocabulary:
                            break
            if origin_vocabulary:
                break
        if origin_vocabulary:
                break
    if origin_vocabulary:
        html = get_html(origin_vocabulary)
        en_dict = get_ecdict(html)
    else:
        en_dict = {
            'name_en': title,
            'kk': kk,
            'part_of_speech': part_of_speech_result_list
        }
    return en_dict