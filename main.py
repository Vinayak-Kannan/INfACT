# This is a sample Python script.
import pandas as pd
import math
from SupportingFunction.CollapseRows import collapse_rows, collapse_rows_pinecone
from SupportingFunction.CreateLexicon import create_lexicon
from SupportingFunction.ParseData import parse_scraped_data
from SupportingFunction.CompareSkills import compare_skills


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def driver():
    school = "Columbia_Fall2023_v1"
    # Use a breakpoint in the code line below to debug your script.
    # parse_scraped_data(school)
    skill_df = pd.read_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/SkillOutputv2.csv')
    skill_cleaned = collapse_rows_pinecone(skill_df)
    skill_cleaned.to_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/SkillOutputUpdated.csv',
        index=False)

    abilities_df = pd.read_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/AbilitiesOutputv2.csv')
    abilities_cleaned = collapse_rows_pinecone(abilities_df)
    abilities_cleaned.to_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/AbilitiesOutputUpdated.csv',
        index=False)

    knowledge_df = pd.read_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/KnowledgeOutputv2.csv')
    knowledge_cleaned = collapse_rows_pinecone(knowledge_df)
    knowledge_cleaned.to_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/KnowledgeOutputUpdated.csv',
        index=False)

    columbia = pd.read_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Columbia_Fall2023_v1/SkillOutputUpdated.csv')
    mit = pd.read_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/MIT_Fall2023_v1/SkillOutputUpdated.csv')

    # Drop rows from columbia where course and collapsed skill columns are duplicates
    columbia = columbia.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])
    mit = mit.drop_duplicates(subset=['Related Course', 'Collapsed Skill'])

    # Join columbia and mit by 'Collapsed Skill' by outer join
    joined = pd.merge(columbia, mit, on='Collapsed Skill', how='outer', suffixes=('_columbia', '_mit'))
    # Save joined to csv in Columba_MIT_Comparison
    joined.to_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Columbia_MIT_Comparison/comparison.csv', index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver()
    # print_hi('PyCharm')
    # compare_skills()
    # create_lexicon(True)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
