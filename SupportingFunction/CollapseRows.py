import numpy as np
import openai
from dotenv import dotenv_values
from openai.embeddings_utils import cosine_similarity, get_embedding
from pandas import DataFrame
import pandas as pd


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
def collapse_rows(df: DataFrame, school) -> DataFrame:
    config = dotenv_values("/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/.env")
    openai.api_key = config.get("SECRET_KEY")
    # Get embeddings for each value in the 'Skill' column
    embeddings = get_embeddings(df['Skill'].tolist())
    df['Embedding'] = embeddings

    # Add a column to the df called 'Collapsed Skill'
    df['Collapsed Skill'] = ''

    # Iterate through the similarity matrix
    for i, row in enumerate(df['Embedding']):
        if df.loc[i, 'Collapsed Skill'] != "":
            continue
        similarities = []
        for j, row2 in enumerate(df['Embedding']):
            # Get skill name from the 'Skill' column
            skill_name = df.loc[j, 'Skill']
            if row is not None and row2 is not None:
                # Calculate the cosine similarity between the two rows
                similarities.append([cosine_similarity(row, row2), skill_name, j])

        # Filter similarities to only include values that are greater than 0.8
        similarities = [x for x in similarities if x[0] >= 0.9]

        count = 0
        if len(similarities) > 0:
            word = similarities[0][1]
            for similarity in similarities:
                if similarity[1] == word:
                    count += 1

        if count > 0 and count == len(similarities):
            df.loc[i, 'Collapsed Skill'] = df.loc[i, 'Skill']
            continue

        # Create a string that concats similarities
        similar_skills = df.loc[i, 'Skill'] + ", "
        for similarity in similarities:
            similar_skills += similarity[1] + ", "
        # Create prompt that asks OpenAI for a label that summarizes the similar skills
        course_description = f"""
            Review the following terms, seperated by commas, and summarize them with one label. 
            
            Follow the format as per example below:
            The terms are: Bowling, Skiing and Surfing, Vibing
            
            Label: Sporting Activities
            
            The terms are: {similar_skills}
        """

        prompt_message = [{
            "role": "user",
            "content": course_description
        }]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt_message,
            temperature=0
        )

        response_message = response.choices[0].message.content
        print(similar_skills)
        print(response_message)
        # Get the label from the response
        label = response_message.split("Label: ")[1].strip()
        # If there are similar values, add the first similar value to the 'Collapsed Skill' column
        df.loc[i, 'Collapsed Skill'] = label
        for similarity in similarities:
            if df.loc[similarity[2], 'Related Course'] != df.loc[i, 'Related Course']:
                df.loc[similarity[2], 'Collapsed Skill'] = label
            else:
                df.loc[similarity[2], 'Collapsed Skill'] = None

    # Drop the 'Embedding' column
    df = df.drop(columns=['Embedding'])

    # Merge original column with df
    orig_df = pd.read_csv(f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/Data - Sheet1.csv')
    # Drop credits and syllabus from orig_df
    orig_df = orig_df.drop(columns=['Credits', 'Syllabus'])
    df = pd.merge(df, orig_df, left_on=['Related Course', 'Semester'], right_on=['Title', 'Semester'])

    return df
