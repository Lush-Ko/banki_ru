import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

def calculate_data(args):

    data = pd.read_csv(args['proc_output_path'], sep='\t')
    model = BERTopic.load('cluster_model')
    clusters_name = pd.read_csv('clusters/cluster_name.csv')

    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(data['Text'], show_progress_bar=False)

    pred = model.transform(data['Text'], embeddings)
    data['cluster'] = pred[0]
    result_df = pd.merge(data, clusters_name, on='cluster')
    result_df.to_csv('data/final_data.csv', index=False)

if __name__ == "__main__":
    with open("data/config.yaml", "r", encoding='utf-8') as stream:
        args = yaml.safe_load(stream)['config_data']
    calculate_data(args)