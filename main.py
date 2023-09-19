# This is a sample Python script.
import pandas as pd

from SupportingFunction.CollapseRows import collapse_rows
from SupportingFunction.ParseData import parse_scraped_data


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def driver():
    # Use a breakpoint in the code line below to debug your script.
    parse_scraped_data()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # driver()
    # Read csv from /Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/SkillOutputv2.csv
    df = pd.read_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/SkillOutputv2.csv')
    test = collapse_rows(df)
    test.to_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/SkillOutputUpdated.csv',
                       index=False)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
