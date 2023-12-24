import pandas as pd
import yaml

from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic

from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer

from gigachat import GigaChat
from langchain.prompts import PromptTemplate


def get_cluster_name(args, data):
  credit = args['credit']
  prompt_template = PromptTemplate.from_template(args['collect_cluster_prompt'])
  result_df = pd.DataFrame(columns=['cluster', 'cluster_name'])
  for label in data['cluster'].unique():
      if label >= 0:
          list_samp = data[data['cluster'] == label].sample(5)['Problem'].values.tolist()
          with GigaChat(credentials=credit, verify_ssl_certs=False) as giga:
              response = giga.chat(prompt_template.format(content=list_samp))
              cluster_name = response.choices[0].message.content
          result_df = result_df.append({'cluster': label, 'cluster_name': cluster_name}, ignore_index=True)

  result_df = result_df.append({'cluster': -1, 'cluster_name': 'Нет явной проблемы'}, ignore_index=True)

  return result_df

def make_clusters(args):

    data = pd.read_csv(args['proc_output_path'], sep='\t')
    
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
    vectorizer_model = CountVectorizer()
    ctfidf_model = ClassTfidfTransformer()
    representation_model = KeyBERTInspired()

    topic_model_1 = BERTopic(
      embedding_model=embedding_model,
      hdbscan_model=hdbscan_model,
      vectorizer_model=vectorizer_model,
      ctfidf_model=ctfidf_model,
      representation_model=representation_model,
      language="russian",
    )

    topics, _ = topic_model_1.fit_transform(data['Text'])
    data['cluster'] = topics
    cluster_names_df = get_cluster_name(args, data)
    cluster_names_df.to_csv('clusters/cluster_name.csv', index=False)
    topic_model_1.save('cluster_model')

if __name__ == "__main__":
    with open("data/config.yaml", "r", encoding='utf-8') as stream:
        args = yaml.safe_load(stream)['config_data']
    make_clusters(args)
    