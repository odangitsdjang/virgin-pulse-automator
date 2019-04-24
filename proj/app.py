import time
import os
from selenium import webdriver

import virgin_pulse.actions
import email_sender

try:
    VIRGIN_PULSE_EMAIL = os.environ['VIRGIN_PULSE_EMAIL']
    VIRGIN_PULSE_PASSWORD = os.environ['VIRGIN_PULSE_PASSWORD']
except KeyError as keyError:
    print('KeyError occurred while trying to access environment variables. If on local, did you run source ./set_env_secrets.sh?')
    raise keyError

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=800,600")


# MAIN SCRIPT
def main():
    step = 'FETCH_LOGIN_PAGE'
    print('Fetching virgin pulse login page...')
    driver.get("https://app.member.virginpulse.com/#/home")
    print('Fetched.')
    step = 'LOGIN'
    virgin_pulse.actions.login(driver, VIRGIN_PULSE_EMAIL, VIRGIN_PULSE_PASSWORD)
    step = 'DAILY CARDS'
    virgin_pulse.actions.click_daily_cards(driver)
    time.sleep(2)
    step = 'HEALTHY_HABITS'
    virgin_pulse.actions.click_healthy_habits(driver)
    print('CLOSING IN 10 SECONDS...')
    step = 'SHUTDOWN'
    time.sleep(10)
    driver.close()

def handle_exception(exception, step, attempts, retry_limit, driver):
    print(exception)

    try:
        if driver:
            driver.close()
    except Exception:
        print('Handle exception: unable to close driver. Skipping.')

    FAILURE_MESSAGES.append(get_fail_message(exception, step, attempts))
    if attempts > retry_limit:
        fail_text = "\n".join([x[0] for x in FAILURE_MESSAGES])
        fail_html = "".join(x[1] for x in FAILURE_MESSAGES)
        email_sender.vp_auto_failure(fail_text, fail_html)
        raise exception
    else:
        print('Exception of type {} occurred. Trying again...'.format(type(exception)))

def get_fail_message(exception, step, attempt_number):
    message =  "Attempt #{} | Failed at step {}| Exception of type {} occurred:| {} |".format(
        attempt_number,
        step,
        type(exception),
        exception
    )
    message_plaintext = message.replace('|','\n')
    message_html = "".join(["<p>"+line+"</p>" for line in message.split('|')])
    return message_plaintext, message_html

if __name__ == "__main__":
    retry_limit = 3
    attempts = 1
    driver = None
    step = 'SETUP'
    FAILURE_MESSAGES = []
    while attempts <= retry_limit:
        print('Attempt #{}'.format(attempts))
        try:
            driver = webdriver.Chrome(options=chrome_options)
            print('Driver UP')
            main()
            break
        except Exception as exception:
            attempts += 1
            handle_exception(exception, step, attempts-1, retry_limit, driver)
    print('Success!')
    email_sender.vp_auto_success()
