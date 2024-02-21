import numpy as np
from langchain_openai import OpenAIEmbeddings
import pandas as pd
import faiss


def get_closest(question, k=5, lang=None):
    embeddings = OpenAIEmbeddings(openai_api_key='OPENAI_API_KEY', model="text-embedding-3-large", dimensions=1536)

    if lang == None:
        df = pd.read_csv('FAQ.csv')
        df = df[['question', 'answer']]
        index = faiss.read_index("mohirdev_index.index")

    else:
        df = pd.read_csv('uzbek_question.csv', index_col=[0])
        index = faiss.read_index("mohirdev_uzb_index.index")

    question_vector = embeddings.embed_query(question)
    question_vector = np.array([question_vector]).astype('float32')

    distances, indices = index.search(question_vector, k)
    closest = [(df['question'].iloc[x].values, df['answer'].iloc[x].values) for x in indices[::-1]]

    return closest
