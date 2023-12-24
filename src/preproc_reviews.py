import yaml
import warnings
from typing import Dict, Any
import pandas as pd

warnings.filterwarnings("ignore")

def preproc_reviews(args: Dict[str, Any]):
    """
    Предобработка датасета
    1) отсев по длине
    2) удаление спец символов
    3) разбиение даты на дату и время
    4) сохранение в csv
    """
    reviews = pd.read_parquet(args['preproc_file_path'])
    reviews = reviews[args['preproc_columns']]
    
    reviews['review_length'] = reviews['review_text'].map(len)
    reviews = reviews.query(f'rating_grade.isin({args["grades_to_leave"]})')
    reviews = reviews.query(f'review_length>{args["min_review_length"]}')
    reviews.drop(columns=['review_length'], inplace=True)
    
    reviews['review_text'] = reviews['review_text'].replace(
        {'\n' : '', '\t' : '', '\xa0' : ''}, regex=True
    )
    
    reviews['time'] = reviews['date'].map(lambda x: x.split(' ')[1])
    reviews['date'] = reviews['date'].map(lambda x: x.split(' ')[0])
        
    reviews.to_csv(args['preproc_output_path'], index=False)
    print(f'Данные сохранены в {args["preproc_output_path"]}')
    
if __name__ == "__main__":
    with open("data/config.yaml", "r") as stream:
        args = yaml.safe_load(stream)['config_data']
        
    preproc_reviews(args)