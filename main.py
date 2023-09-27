# This is a sample Python script.
import pandas as pd

from SupportingFunction.CollapseRows import collapse_rows
from SupportingFunction.ParseData import parse_scraped_data


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def driver():
    school = "Columbia_Updated"
    # Use a breakpoint in the code line below to debug your script.
    # parse_scraped_data(school)
    skill_df = pd.read_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/SkillOutputv2.csv')
    skill_cleaned = collapse_rows(skill_df, school)
    skill_cleaned.to_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/SkillOutputUpdated.csv',
        index=False)

    abilities_df = pd.read_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/AbilitiesOutputv2.csv')
    abilities_cleaned = collapse_rows(abilities_df, school)
    abilities_cleaned.to_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/AbilitiesOutputUpdated.csv',
        index=False)

    knowledge_df = pd.read_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/KnowledgeOutputv2.csv')
    knowledge_cleaned = collapse_rows(knowledge_df, school)
    knowledge_cleaned.to_csv(
        f'/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/{school}/KnowledgeOutputUpdated.csv',
        index=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
