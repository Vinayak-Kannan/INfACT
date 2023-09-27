# This is a sample Python script.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv
from selenium.webdriver.chrome.options import Options

from SupportingFunction.CollapseRows import collapse_rows
from SupportingFunction.ParseData import parse_scraped_data


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def driver_function():
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-data-dir=/Users/vinayakkannan/Library/Application Support/Google/Chrome/Profile 4")  # e.g. C:\Users\You\AppData\Local\Google\Chrome\User Data
    # Set up the webdriver
    driver = webdriver.Chrome(options=options)
    driver.get("https://vergil.registrar.columbia.edu/#/courses/*")

    # Open a new tab
    driver.execute_script("window.open();")
    driver.switch_to.window(driver.window_handles[-1])

    # Navigate to the desired URL
    driver.get("https://vergil.registrar.columbia.edu/#/courses/*")

    # 1. Select 'More Search Criteria'
    more_search_criteria = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'More Search Criteria')]"))
    )
    more_search_criteria.click()

    # 2. Select 'Fall 2023' from the 'Semester' dropdown
    semester_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='search-semester']"))
    )
    Select(semester_dropdown).select_by_visible_text("Fall 2023")

    # 3. Type 'Computer Science' in the 'Subject' dropdown
    subject_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='subject']"))
    )
    Select(subject_dropdown).select_by_visible_text("Computer Science")

    # 4. Click the 'Search' button
    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Search')]"))
    )
    search_button.click()

    # 5. Click the 'Expand All' button
    expand_all_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Expand All')]"))
    )
    expand_all_button.click()

    # Scrape course information and save it to a CSV file
    courses = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='class-description']"))
    )

    with open("courses.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["course_name", "credits", "course_description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for course in courses:
            course_name = course.find_element_by_xpath(".//h3").text
            credits = course.find_element_by_xpath(".//span[@class='credits']").text
            course_description = course.find_element_by_xpath(".//div[@class='description']").text

            writer.writerow({"course_name": course_name, "credits": credits, "course_description": course_description})

    driver.quit()
    print("hello")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver_function()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
