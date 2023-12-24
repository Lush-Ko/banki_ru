from gigachat import GigaChat
from langchain.prompts import PromptTemplate
from typing import Dict, Any
import pandas as pd
import yaml
import warnings

warnings.filterwarnings("ignore")

def add_answer(msg):
    splits = msg.split('\n')
    answer_dict = {'Problem': [],
                   'Solve': [],
                   'Short problem': [],
                   'Tag': []}
    keys = list(answer_dict.keys())
    for i in range(len(keys)):
        pos = splits[i].find(':')
        if i < 3:
            answer_dict[keys[i]].append(splits[i][pos + 2 : -1])
        if i == 3:
            answer = splits[i][pos + 2 :].split(' ')
            answer_dict[keys[i]].append(answer)
    return answer_dict

def gigachat_process(args: Dict[str, Any]):

    prompt_template = PromptTemplate.from_template(args['prompt_template'])
    result_gigachat = pd.DataFrame(columns=args['proc_columns'])
    data = pd.read_csv(args['proc_file_path'], encoding='utf-8')

    for row in data.iterrows():
        with GigaChat(credentials=args['credit'], verify_ssl_certs=False) as giga:
            review = row[1]['review_text']
            text = prompt_template.format(content=review)
            response = giga.chat(text)
            try:
                result_dict = add_answer(msg=response.choices[0].message.content)
            except IndexError as e:
                print(f'Ошибка в строке: {row[1].name}')
                pass
            result_dict['Text'] = review
            result_dict['Date'] = row[1]['date']
            result_gigachat = pd.concat([result_gigachat, pd.DataFrame.from_dict(result_dict)], ignore_index=True)

    result_gigachat.to_csv(args['proc_output_path'], encoding='utf-8', sep='\t', index=False)
    print(f'Данные сохранены в {args["proc_output_path"]}')
 
if __name__ == "__main__":
    with open("data/config.yaml", "r", encoding='utf-8') as stream:
        args = yaml.safe_load(stream)['config_data']
    gigachat_process(args)
