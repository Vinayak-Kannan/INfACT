import pandas as pd
from pandas import DataFrame


def merge_files(df1: DataFrame, df2: DataFrame, df1_name: str, df2_name: str) -> DataFrame:
    # Drop rows from columbia where course and collapsed skill columns are duplicates
    # Check if Related Course and Collapsed Skill are in the dataframe
    if 'Related Course' in df1.columns and 'Collapsed Skill' in df1.columns:
        df1 = df1.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])
    if 'Related Course' in df2.columns and 'Collapsed Skill' in df2.columns:
        df2 = df2.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])

    # Print number of rows in df1 and df2 that share the same 'Collapsed Skill'
    # Remove trailing and leading white space from 'Collapsed Skill' column
    df1['Collapsed Skill'] = df1['Collapsed Skill'].str.strip()
    df2['Collapsed Skill'] = df2['Collapsed Skill'].str.strip()

    # Drop columns that contain the string 'Embedding'
    df1 = df1.loc[:, ~df1.columns.str.contains('Embedding')]
    df2 = df2.loc[:, ~df2.columns.str.contains('Embedding')]


    # Join columbia and mit by 'Collapsed Skill' by outer join
    joined = pd.merge(df1, df2, on='Collapsed Skill', how='outer', suffixes=(f"_{df1_name}", f"_{df2_name}"))
    return joined

def create_skills_df():
    columbia = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Columbia_Fall2023_v1/SkillOutputUpdated11012023.csv')
    mit = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/MIT_Fall2023_v1/SkillOutputUpdated11012023.csv')

    # Drop rows from columbia where course and collapsed skill columns are duplicates
    columbia = columbia.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])
    mit = mit.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])

    # Join columbia and mit by 'Collapsed Skill' by outer join
    joined = pd.merge(columbia, mit, on='Collapsed Skill', how='outer', suffixes=('_columbia', '_mit'))

    # Read df1 from csv
    df1 = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Amazon Skills Collapsed.csv')


    output = merge_files(df1, joined, "Amazon", "Schools_Fall_2023")
    output.to_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Amazon_Columbia_MIT_Comparison_Fall_2023_Skills.csv',
        index=False)

    # Read df1 from csv
    df1 = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Industry/Collapsed Skills11012023.csv')

    # Rename 'Job Title' column in df1 to 'Unique Job ID'
    df1 = df1.rename(columns={'Job Title': 'Unique Job ID'})

    output = merge_files(df1, joined, "Industry", "Schools_Fall_2023")
    output.to_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Industry/Industry_Columbia_MIT_Comparison_Fall_2023_Skills.csv',
        index=False)


def create_knowledge_df():
    columbia = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Columbia_Fall2023_v1/KnowledgeOutputUpdated11012023.csv')
    mit = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/MIT_Fall2023_v1/KnowledgeOutputUpdated11012023.csv')

    columbia_amazon = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Columbia_Fall2023_v1/KnowledgeOutputUpdatedAmazon11012023.csv')
    mit_amazon = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/MIT_Fall2023_v1/KnowledgeOutputUpdatedAmazon11012023.csv')

    # Drop rows from columbia where course and collapsed skill columns are duplicates
    columbia = columbia.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])
    mit = mit.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])

    columbia_amazon = columbia_amazon.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])
    mit_amazon = mit_amazon.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])

    # Join columbia and mit by 'Collapsed Skill' by outer join
    joined = pd.merge(columbia, mit, on='Collapsed Skill', how='outer', suffixes=('_columbia', '_mit'))
    joined_amazon = pd.merge(columbia_amazon, mit_amazon, on='Collapsed Skill', how='outer', suffixes=('_columbia', '_mit'))


    # Read df1 from csv
    df1 = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Collapsed Knowledge11012023.csv')


    output = merge_files(df1, joined_amazon, "Amazon", "Schools_Fall_2023")
    output.to_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Amazon_Columbia_MIT_Comparison_Fall_2023_Knowledge.csv',
        index=False)

    # Read df1 from csv
    df1 = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Collapsed Skills11012023.csv')

    output = merge_files(df1, joined, "Industry", "Schools_Fall_2023")
    output.to_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Industry/Industry_Columbia_MIT_Comparison_Fall_2023_Knowledge.csv',
        index=False)


def create_abilities_df():
    columbia = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Columbia_Fall2023_v1/AbilitiesOutputUpdated.csv')
    mit = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/MIT_Fall2023_v1/AbilitiesOutputUpdated.csv')

    # Drop rows from columbia where course and collapsed skill columns are duplicates
    columbia = columbia.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])
    mit = mit.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])

    # Join columbia and mit by 'Collapsed Skill' by outer join
    joined = pd.merge(columbia, mit, on='Collapsed Skill', how='outer', suffixes=('_columbia', '_mit'))

    # Read df1 from csv
    df1 = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Amazon_Ability Collapsed.csv')

    output = merge_files(df1, joined, "Amazon", "Schools_Fall_2023")
    output.to_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Amazon/Amazon_Columbia_MIT_Comparison_Fall_2023_Abilities.csv',
        index=False)

    # Read df1 from csv
    df1 = pd.read_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Industry/Collapsed_Abilities.csv')

    output = merge_files(df1, joined, "Industry", "Schools_Fall_2023")
    output.to_csv(
        '/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Industry/Industry_Columbia_MIT_Comparison_Fall_2023_Abilities.csv',
        index=False)


create_skills_df()
create_knowledge_df()
create_abilities_df()