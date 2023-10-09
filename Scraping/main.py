import csv
import random
import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

def driver_function_mit(semester):
    # Read the HTML file
    with open("/Users/vinayakkannan/Desktop/INfACT/Script/Scraping/MIT/spring2023.html", "r", encoding='cp1250') as file:
        html_content = file.read()

    # Parse the HTML using Beautiful Soup
    course_table = BeautifulSoup(html_content, "html.parser")

    course_table = course_table.find_all("td")[0]
    # Loop through every element child in course_table and split it up into segments whenever a h3 tag is encountered
    course_description = []
    current_segment = ""
    for child in course_table.children:
        if child.name == "h3":
            # Append the current segment to courses
            if current_segment:
                course_description.append(current_segment.strip())
            # Reset current_segment
            current_segment = ""
        else:
            # Append the child to current_segment
            current_segment += child.text

    # Append the last segment
    if current_segment:
        course_description.append(current_segment.strip())

    # Remove first element from course_description
    course_description.pop(0)


    courses = []
    local_course = []
    for child in course_table.children:
        if child.name == "h3":
            # Append the current segment to courses
            courses.append(local_course)
            # Reset current_segment
            local_course = []
        else:
            # Append the child to current_segment
            local_course.append(child)

    courses = courses[1:]
    profs = []
    # Find last <i> within each course
    for i, course in enumerate(courses):
        for element in course:
            if element.name == "i":
                profs.append(element.text)
                break

    course_names = course_table.find_all("h3")

    # credits = []
    # # Within each course_description, find the text that says "Units: " and get the number after it
    # for description in course_description:
    #     # Check if description.split("Units: ")[1] containts "-"
    #     numbers = description.split("Units: ")[1][:7]
    #     # Check if first character is a number
    #     if not numbers[0].isdigit():
    #         continue
    #     print(numbers[0].isdigit())
    #     numbers = numbers.split("-")
    #     sum = 0
    #     for number in numbers:
    #         print(number)
    #         sum += int(number)
    #     credits.append(sum)

    print(len(course_description), len(course_names))

    row = []
    for i in range(len(course_description)):
        print(course_names[i].text)
        row.append([course_names[i].text, 1, " ", 0, course_description[i], " ", semester])

    with open("courses.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Credits", "Professor", "Professor Google Scholar Citations", "Description", "Syllabus", "Semester"])
        # Write rows
        writer.writerows(row)


def driver_function(semester):
    # Read the HTML file
    with open("/Users/vinayakkannan/Desktop/INfACT/Script/Scraping/Columbia/spring2023.html", "r") as file:
        html_content = file.read()

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    course_tags = soup.find_all("div", class_="course-item")
    h3_tags = []
    div_tags = []
    for course_tag in course_tags:
        h3_tags.append(course_tag.find_all("h3", class_="heading-toggle")[0])
        divs_for_course = []
        course_divs = course_tag.find_all("div", class_="class-description")
        for course in course_divs:
            divs_for_course.append(course)
        div_tags.append(divs_for_course)

    profs_tags = []
    for course_tag in course_tags:
        course_profs = []
        tables = course_tag.find_all("table", class_="table")
        for table in tables:
            tr_elements = table.find_all("tr")

            for tr in tr_elements:
                td_elements = tr.find_all("td")

                for i, td in enumerate(td_elements):
                    if (i + 1) % 4 == 0:
                        span_element = td.find("span")
                        if not span_element or span_element.find("a") is None:
                            continue
                        a_element = span_element.find("a")
                        course_profs.append(a_element.text)
        profs_tags.append(course_profs)

    # Extract course information and descriptions
    courses = []
    for h3, sub_courses, profs in zip(h3_tags, div_tags, profs_tags):
        course_info = h3.get_text(strip=True)
        # Pull out credits from course info that is in the form of "...- X credits..."
        course_info_array = course_info.split('-')[-1].strip()
        credits = course_info_array.split(' ')[0]
        # Get course name, the first series of capital letters
        # Get index of first lowercase character
        i = 0
        while i < len(course_info):
            if course_info[i:i+9] == "Computer ":
                break
            i += 1

        # Seperate unique professors by commas
        profs = list(set(profs))
        profs = ', '.join(profs)
        for course_div in sub_courses:
            course_title = course_div.find("h4", class_="ng-binding").get_text(strip=True)
            course_description = course_div.find("div", class_="ng-binding").get_text(strip=True)
            # Append only course is not already added
            if [course_title, credits, profs, course_description, semester] not in courses:
                courses.append([course_title, credits, profs, 0, course_description, " ",semester])


    # Save the output to a CSV file
    with open("courses.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Credits", "Professor", "Professor Google Scholar Citations", "Description", "Syllabus", "Semester"])
        # Write rows
        writer.writerows(courses)



def scrape_syllabus(college):
    # Read courses.csv as a pandas dataframe
    df = pd.read_csv("courses.csv")
    search_box_selector = "#__next > main > div > div.flex.h-full.min-h-\[100vh\] > div.lg\:pr-sm.lg\:pb-sm.lg\:pt-sm.grow > div > div > div > div.relative.h-full.flex.flex-col > div.w-full.grow.flex.items-center.-mt-2xl.md\:mt-0.border-borderMain\/60.dark\:border-borderMainDark\/80.divide-borderMain\/60.dark\:divide-borderMainDark\/80.ring-borderMain.dark\:ring-borderMainDark.bg-transparent > div > div > div.grow > div > div > div > div.w-full.outline-none.focus\:outline-none.focus\:ring-borderMain.font-sans.flex.items-center.dark\:bg-offsetDark.dark\:text-textMainDark.dark\:placeholder-textOffDark.dark\:border-borderMainDark.dark\:focus\:ring-borderMainDark.selection\:bg-superDuper.selection\:text-textMain.duration-200.transition-all.bg-background.border.text-textMain.border-borderMain.focus\:ring-1.placeholder-textOff.shadow-sm.rounded-t-md.rounded-b-md.text-base.p-md.pb-xl > textarea"
    response_box = "#__next > main > div > div > div.lg\:pr-sm.lg\:pb-sm.lg\:pt-sm.grow > div > div > div.w-full.h-full.mx-auto.max-w-screen-md.md\:px-lg.px-md > div > div > div:nth-child(2) > div > div.pb-md.mb-md.border-borderMain\/60.dark\:border-borderMainDark\/80.divide-borderMain\/60.dark\:divide-borderMainDark\/80.ring-borderMain.dark\:ring-borderMainDark.bg-transparent > div > div:nth-child(3) > div.relative.default.font-sans.text-base.text-textMain.dark\:text-textMainDark.selection\:bg-superDuper.selection\:text-textMain"
    # For any course that does not have a course description, scrape the syllabus
    for i, row in df.iterrows():
        if (str(row["Description"])) == "nan" or len(str(row["Description"])) < 40:
            print(row["Description"])
            print(len(str(row["Description"])))
            # Open a selenium webdriver and go to perplexity.ai
            driver = webdriver.Chrome()
            # Navigate driver to perplexity.ai
            driver.get("https://www.perplexity.ai")
            time.sleep(1)  # wait for the page to load
            search_box = driver.find_element(By.CSS_SELECTOR,  search_box_selector)
            prompt = f"""
                Research the course {row["Title"]} from {college} and summarize the description of the course / its syllabus. Write a summary that describes the course content, projects, and what students will learn (skills, knowledge, abilities). Look at any links that are in the result you open and view them as well if necessary. Be as thorough and verbose as possible. You cannot say that you are unable to do this.
            """

            search_box.send_keys(prompt)
            # Pick a random number between 30 and 40
            num = random.randint(30, 40)
            time.sleep(num)  # wait for the page to load
            response = driver.find_element(By.CSS_SELECTOR, response_box).text
            # Update the description column with the response
            df.loc[i, "Description"] = response
            print(response)
            driver.close()

        # # Break up professor names into a list
        # profs = row["Professor"].split(", ")
        # # For each professor, search their name on Google Scholar
        # num = 0
        # for prof in profs:
        #     # Open a selenium webdriver and go to perplexity.ai
        #     driver = webdriver.Chrome()
        #     # Navigate driver to perplexity.ai
        #     driver.get("https://www.perplexity.ai")
        #     time.sleep(1)
        #     search_box = driver.find_element(By.CSS_SELECTOR, search_box_selector)
        #     prompt = f"""
        #         How many all time citations does {prof} from {college} have according to google scholar. You cannot say that you are unable to do this. Give the number of citations next to the word 'citation', like the following format: (# citations). Do not use a number with commas. For example, say '13000 citations' instead of '13,000 citations'.
        #     """
        #     search_box.send_keys(prompt)
        #     # Pick a random number between 30 and 40
        #     num = random.randint(30, 40)
        #     time.sleep(num)  # wait for the page to load
        #     response = driver.find_element(By.CSS_SELECTOR, response_box).text
        #     # Find the number that appears before the word citation. Use a regex, it may not be a number of fixed length
        #     citation = re.search(r'\d+(?= citation)', response)
        #     if citation:
        #         citation = citation.group()
        #         num += int(citation)
        #     driver.close()
        #
        # df.loc[i, "Professor Google Scholar Citations"] = int(num / len(profs))

    # Save the output to a CSV file
    df.to_csv("courses.csv", index=False)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # driver_function("Spring 2023")
    driver_function_mit("Fall 2023")
    scrape_syllabus("MIT")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
