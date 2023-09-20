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

# Ideas to do this better:
# 1. Store the embeddings in vectorDB to stop having to call the API every time
# 2. Instead of dropping terms, roll them up into a list of terms, then have LLM synthesize them all into a single term
# 3. Switch to LLAMA for better results, fine tune it on accruate responses we have
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
        if len(similarities) > 0 and similarities[1][0] >= 0.85:
            similar_indices = similarities[1]

        # If there are similar values, add the first similar value to the 'Collapsed Skill' column
        if similar_indices:
            df.loc[i, 'Collapsed Skill'] = df.loc[similar_indices[1], 'Skill']
        else:
            # If there are no similar values, add the original value to the 'Collapsed Skill' column
            df.loc[i, 'Collapsed Skill'] = df.loc[i, 'Skill']

    # Loop through each row. Check if the 'Collapsed Skill' value is the same as the 'Skill' value If it's not,
    # find other 'Collapsed Skills' that are the same as the 'Skill' value and make them equal to the 'Collapsed
    # Skill' value
    for i, row in enumerate(df['Collapsed Skill']):
        if row != df.loc[i, 'Skill']:
            for j, row2 in enumerate(df['Collapsed Skill']):
                if row2 == df.loc[i, 'Skill']:
                    df.loc[j, 'Collapsed Skill'] = row

    # Drop the 'Embedding' column
    df = df.drop(columns=['Embedding'])

    return df
