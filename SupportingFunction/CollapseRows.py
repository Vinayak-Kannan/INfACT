import numpy as np
import openai
from dotenv import dotenv_values
from openai.embeddings_utils import cosine_similarity, get_embedding
from pandas import DataFrame


def get_embeddings(texts):
    embeddings = []
    for text in texts:
        embedding_model = "text-embedding-ada-002"
        value = get_embedding(text, engine=embedding_model)
        embeddings.append(value)
    return embeddings


def collapse_rows(df: DataFrame) -> DataFrame:
    config = dotenv_values("/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/.env")
    openai.api_key = config.get("SECRET_KEY")
    # Get embeddings for each value in the 'Skill' column
    embeddings = get_embeddings(df['Skill'].tolist())
    df['Embedding'] = embeddings

    # Add a column to the df called 'Collapsed Skill'
    df['Collapsed Skill'] = ''

    # Iterate through the similarity matrix
    for i, row in enumerate(df['Embedding']):
        similarities = []
        for j, row2 in enumerate(df['Embedding']):
            if row is not None and row2 is not None:
                # Calculate the cosine similarity between the two rows
                similarities.append([cosine_similarity(row, row2), j])

        # Sort similarities by the first value in the list (the cosine similarity)
        similarities.sort(key=lambda x: x[0], reverse=True)

        similar_indices = None
        # If similarity is less than 0.8, make similar_index == None
        if len(similarities) > 0 and similarities[1][0] >= 0.9:
            similar_indices = similarities[1]
            df.loc[i, 'Embedding'] = None

        # If there are similar values, add the first similar value to the 'Collapsed Skill' column
        if similar_indices:
            df.loc[i, 'Collapsed Skill'] = df.loc[similar_indices[1], 'Skill']
        else:
            # If there are no similar values, add the original value to the 'Collapsed Skill' column
            df.loc[i, 'Collapsed Skill'] = df.loc[i, 'Skill']

    # Drop the 'Embedding' column
    df = df.drop(columns=['Embedding'])

    return df
