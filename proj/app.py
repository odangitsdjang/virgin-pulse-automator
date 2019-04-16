import time
import os
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

VIRGIN_PULSE_EMAIL = os.environ['VIRGIN_PULSE_EMAIL']
VIRGIN_PULSE_PASSWORD = os.environ['VIRGIN_PULSE_PASSWORD']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=800,600")

def is_home_page_loaded(driver):
    tips = driver.find_elements_by_class_name("dialy-tips-wrapper")
    return len(tips) >= 4

def wait_for_homepage_load():
    print('--Wait for Home to Load---')
    WebDriverWait(driver, 30).until(
        is_home_page_loaded
    )
    print('Home page loaded')

def click_daily_cards():
    print('---Daily Cards---')
    # Make sure daily cards are shown on page, if not, get them to appear
    print('Get cards displayed on page')
    daily_tips = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "dialy-tips-wrapper"))
    )
    daily_tips_active = (daily_tips.get_attribute('aria-pressed') == 'true')
    if daily_tips_active:
        print('Daily cards already displayed')
    else:
        print('Clicking button to display cards')
        daily_tips.click()

     # Click the first daily card
    print('Get first daily card button')
    got_it_button_one = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "triggerCloseCurtain"))
    )
    button_completed = 'completed-button' in got_it_button_one.get_attribute('class')
    if button_completed:
        print('Card 1: Already complete')
    else:
        print('Card 1: Clicking "GOT IT" button')
        got_it_button_one.click()

    # Wait for Virgin Pulse to automatically present the next button
    print('Wait for Virgin Pulse to automatically present the next card')
    try:
        got_it_button_changed = WebDriverWait(driver, 5).until(
            EC.staleness_of(got_it_button_one)
        )
        print('Card was switched automatically. Sleeping 3 seconds')
        time.sleep(3)
    except TimeoutException:
        print('Timeout. Manually switching cards')
        # Button didn't change, go to the next/prev card manually
        try:
            print('Looking for "next" arrow button')
            switch_card_button = driver.find_element_by_class_name('next-card-btn')
        except NoSuchElementException:
            print('"Next" not found. Looking for "Prev" arrow button')
            switch_card_button = driver.find_element_by_class_name('prev-card-btn')
        print("Button to switch cards found. Clicking...")
        switch_card_button.click()

    print('Second daily card button')
    got_it_button_two = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "triggerCloseCurtain"))
    )
    button_completed = 'completed-button' in got_it_button_two.get_attribute('class')
    if button_completed:
        print('Card 2: Already complete')
    else:
        print('Card 2: Clicking "GOT IT" button')
        got_it_button_two.click()

def click_healthy_habits():
    print('---Healthy Habits---')
    print('Navigating to healthy habits page')
    side_nav_buttons = driver.find_elements_by_class_name("dialy-tips-wrapper")
    habits_page_button = side_nav_buttons[1]
    habits_page_active = (habits_page_button.get_attribute('aria-pressed') == 'true')
    if habits_page_active:
        print('Healthy habits page already displayed')
    else:
        print('Clicking button to display healthy habits')
        habits_page_button.click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "home-healthy-habit-main"))
    )
    print('Healthy habits page loaded')
    healthy_habits = driver.find_elements_by_class_name('home-healthy-habit-main')
    print('Found {} habits on screen'.format(len(healthy_habits)))
    habits_confirmed = 0
    for habit in healthy_habits:
        if habits_confirmed >= 6:
            break

        try:
            habit_title = habit.find_element_by_tag_name('h2').text
        except WebDriverException as webDriverException:
            print('Unable to find habit title, skipping...')
            print(webDriverException)
            continue

        try:
            print('Habit: {}'.format(habit_title))
            hover = ActionChains(driver)
            hover.move_to_element(habit)
            hover.pause(1)
            hover.move_to_element(habit.find_element_by_class_name('yes-btn'))
            hover.pause(1)
            hover.click()

            hover.perform()
            print('Habit clicked')
            habits_confirmed += 1
        except WebDriverException as webDriverException:
            print('Unable to perform action chain on habit successfully')
            print(webDriverException)


def login(username, password):
    print('--Login--')
    print('User: {} Pass Length: {}'.format(username, len(password)))
    print('Waiting for login form')

    try:
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
    except TimeoutException:
        print('Page took too long to load')
        raise
    except WebDriverException:
        print('Selenium encountered an error')
        raise

    print('Login form loaded.')
    print('Entering credentials...')
    username_input.clear()
    username_input.send_keys(username)
    password_input = driver.find_element_by_id("password")
    password_input.clear()
    password_input.send_keys(password)
    print('Entered.')
    print('Signing in...')
    sign_in = driver.find_element_by_id("kc-login")
    sign_in.click()
    print('Sign in clicked.')
    try:
        wait_for_homepage_load()
    except WebDriverException as webDriverException:
        print(webDriverException)
        print('Did login fail?')
        raise webDriverException


# MAIN SCRIPT
def main():
    print('Fetching virgin pulse login page...')
    driver.get("https://app.member.virginpulse.com/#/home")
    print('Fetched.')
    login(VIRGIN_PULSE_EMAIL, VIRGIN_PULSE_PASSWORD)
    click_daily_cards()
    time.sleep(2)
    click_healthy_habits()
    print('CLOSING IN 10 SECONDS...')
    time.sleep(10)
    driver.close()

if __name__ == "__main__":
    retry_limit = 3
    attempts = 1
    while attempts <= retry_limit:
        print('Attempt #{}'.format(attempts))

        try:
            driver = webdriver.Chrome(options=chrome_options)
            print('Driver UP')
            main()
            break
        except urllib3.exceptions.ProtocolError as urlLibException:
            attempts+= 1
            print(urlLibException)
            if attempts > retry_limit:
                raise urlLibException
            else:
                print('MAIN: Urllib ProtocolError exception occurred. Trying again...')
        except WebDriverException as webDriverException:
            driver.close()
            attempts += 1
            print(webDriverException)
            if attempts > retry_limit:
                raise webDriverException
            else:
                print('MAIN: Web driver exception occurred. Trying again...')
    print('Success!')