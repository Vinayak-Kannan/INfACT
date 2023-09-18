import openai
import pandas as pd


def parse_scraped_data():
    baseDF = create_dataframe()
    skillDF = pd.DataFrame(columns=['Skill', 'Explanation', 'Related Course', 'Credits'])
    knowledgeDF = pd.DataFrame(columns=['Skill', 'Explanation', 'Related Course', 'Credits'])
    abilitiesDF = pd.DataFrame(columns=['Skill', 'Explanation', 'Related Course', 'Credits'])

    newDFs = get_skills(baseDF, baseDF, skillDF, knowledgeDF, abilitiesDF)
    skillDF = newDFs[0]
    knowledgeDF = newDFs[1]
    abilitiesDF = newDFs[2]

    skillDF.to_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/SkillOutputv2.csv', index=False)
    knowledgeDF.to_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/KnowledgeOutputv2.csv', index=False)
    abilitiesDF.to_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/AbilitiesOutputv2.csv', index=False)


def create_dataframe():
    data = pd.read_csv('/Users/vinayakkannan/Desktop/INfACT/Script/SupportingFunction/RawData/Data - Sheet1.csv')
    data['Syllabus'].fillna('', inplace=True)
    data["combined"] = (
            "Title: " + data.Title.str.strip() + "; Description: " + data.Description.str.strip() + "Syllabus: " + data.Syllabus.str.strip()
    )
    model = "text-embedding-ada-002"
    data['Skills'] = ""
    data['Knowledge'] = ""
    data['Abilities'] = ""
    data['SkillsAndExplanation'] = ""
    data['KnowledgeAndExplanation'] = ""
    data['AbilitiesAndExplanation'] = ""

    return data


def get_course_label(course_description):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=course_description,
        temperature=0
    )
    return response


def get_skills(df, baseDF, skillDF, knowledgeDF, abilitiesDF):
    prompt = """
    Review the course title and description below and give me a list of at most 5 'skills' and at most 5 'knowledge' and at most 5 'abilities' students who take this course are going to learn. The definition for 'skill' and 'competency' are below:
    A 'skill' refers to something taught in a course that is quantifiable and is measured as handling or manipulating things, data or people, either verbally, manually or mentally to accomplish an objective. Skills can be developed with practice or appropriate training. Examples of skills include carpentry, computer repair, leadership, public speaking.

    A 'knowledge' is defined as the body of information that you have that can be applied in helping you to do the job. Knowledge can be quantified. Examples of knowledge are federal regulations, document preperation practices, engineering practices

    A 'ability' is the capacity to express a skill. Typically, abilities are the tasks completed on the job. Skills and abilities are often used interchangeably, but there are subtle differences. Ability is the capacity to perform, where a skill is the actual performing. Examples of abilities are the ability to organize, the ability to analyze issues, the ability to communicate verbally, the ability to communicate in writing

    Provide the skills, knowledge, and abilities as a list separated by commas with an explanation of why this skill, knowledge, or ability was selected, following the format of the example below:

    Skills:
    SQL: Students will gain proficiency in SQL
    XML: Students will learn about XML (eXtensible Markup Language) and its use in databases

    Knowledge:
    Database design: Students will learn how to design a database

    Abilities:
    Problem-solving: Students will develop the ability of problem-solving as they work on programming projects
    Communication: Students will enhance their communication skills.


    The course description and title are as follows:
    """

    for i, row in enumerate(df.index):
        response = get_course_label([{
            "role": "user",
            "content": prompt + df.combined[i]
        }])
        newDFs = parse_response(response.choices[0].message.content, i, baseDF, df.Title[i], df.Credits[i], skillDF,
                                knowledgeDF, abilitiesDF)
        skillDF = newDFs[0]
        knowledgeDF = newDFs[1]
        abilitiesDF = newDFs[2]
    return [skillDF, knowledgeDF, abilitiesDF]


def parse_response(response, index, df, courseName, credits, skillDF, knowledgeDF, abilitiesDF):
    print(response)
    # Split the response into lines and remove empty lines
    lines = [line.strip() for line in response.split('\n') if line.strip()]

    # Initialize lists for skills and competencies
    skills = []
    knowledge = []
    abilities = []

    # Parse the response and populate the lists
    current_section = None
    for line in lines:
        if line == "Skills:":
            current_section = "skills"
        elif line == "Knowledge:":
            current_section = "knowledge"
        elif line == "Abilities:":
            current_section = "abilities"
        else:
            name, explanation = line.split(': ', 1)
            if current_section == "skills":
                skills.append({"Name": name[3:], "Explanation": explanation})
                new_row = pd.DataFrame(
                    {'Skill': name[3:], 'Explanation': explanation, 'Related Course': courseName, 'Credits': credits},
                    index=[0])
                skillDF = pd.concat([skillDF, new_row], ignore_index=True)
            elif current_section == "knowledge":
                knowledge.append({"Name": name[3:], "Explanation": explanation})
                new_row = pd.DataFrame(
                    {'Skill': name[3:], 'Explanation': explanation, 'Related Course': courseName, 'Credits': credits},
                    index=[0])
                knowledgeDF = pd.concat([knowledgeDF, new_row], ignore_index=True)
            elif current_section == "abilities":
                abilities.append({"Name": name[3:], "Explanation": explanation})
                new_row = pd.DataFrame(
                    {'Skill': name[3:], 'Explanation': explanation, 'Related Course': courseName, 'Credits': credits},
                    index=[0])
                abilitiesDF = pd.concat([abilitiesDF, new_row], ignore_index=True)

    # Convert the lists to DataFrames
    skills_df = pd.DataFrame(skills)
    knowledge_df = pd.DataFrame(knowledge)
    abilities_df = pd.DataFrame(abilities)

    # Merge the DataFrames with the existing DataFrame, df
    df.at[index, 'Skills'] = skills_df['Name'].str.cat(sep=', ')
    df.at[index, 'Knowledge'] = knowledge_df['Name'].str.cat(sep=', ')
    df.at[index, 'Abilities'] = abilities_df['Name'].str.cat(sep=', ')
    df.at[index, 'SkillsAndExplanation'] = skills_df['Name'] + ': ' + skills_df['Explanation']
    df.at[index, 'KnowledgeAndExplanation'] = knowledge_df['Name'] + ': ' + knowledge_df['Explanation']
    df.at[index, 'AbilitiesAndExplanation'] = abilities_df['Name'] + ': ' + abilities_df['Explanation']
    df.at[index, 'SkillsAndExplanation'] = df.at[index, 'SkillsAndExplanation'].str.cat(sep=', ')
    df.at[index, 'KnowledgeAndExplanation'] = df.at[index, 'KnowledgeAndExplanation'].str.cat(sep=', ')
    df.at[index, 'AbilitiesAndExplanation'] = df.at[index, 'AbilitiesAndExplanation'].str.cat(sep=', ')

    return [skillDF, knowledgeDF, abilitiesDF]
