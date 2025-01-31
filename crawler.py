import os
import time
import logging
import argparse
import random
import json
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Parse arguments
parser = argparse.ArgumentParser(description="Dynamic Selenium Crawler.")
parser.add_argument("-c", "--config", type=str, help="Path to the JSON configuration file.")
parser.add_argument("-u", "--url", type=str, help="URL of product to test credit card on.")
args = parser.parse_args()

# Persons Dict that have more than 1 user data
persons = {
    "John Doe": {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": "1234567890",
        "street": "10 Main St",
        "city": "New York",
        "state": "NY",
        "postal": "10001"
    },
    "Jane Doe": {
        "name": "Jane Doe",
        "email": "janedoe@icloud.com",
        "phone": "0987654321",
        "street": "11 Main St",
        "city": "New York",
        "state": "NY",
        "postal": "15041"
    }
}


def setup_driver():
    try:
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=socks4://127.0.0.1:9050')
        # block images loading
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(service=service, options=options)
        logging.info("ChromeDriver setup successfully with Tor proxy.")
        return driver
    except WebDriverException as e:
        logging.error(f"Error setting up ChromeDriver: {e}")
        return None


def load_data():
    with open("data.txt", "r") as f:
        return f.read().splitlines()


def load_cc_data():
    with open("cc.txt", "r") as f:
        return f.read().splitlines()


def get_by_type(target_type):
    if target_type == "id":
        return By.ID
    elif target_type == "name":
        return By.NAME
    elif target_type == "class":
        return By.CLASS_NAME
    elif target_type == "css":
        return By.CSS_SELECTOR
    elif target_type == "xpath":
        return By.XPATH
    else:
        raise ValueError(f"Unsupported target type: {target_type}")


def get_wait_condition(wait_condition):
    if wait_condition == "presence_of_element_located":
        return EC.presence_of_element_located
    elif wait_condition == "element_to_be_clickable":
        return EC.element_to_be_clickable
    elif wait_condition == "presence_of_all_elements_located":
        return EC.presence_of_all_elements_located
    else:
        raise ValueError(f"Unsupported wait condition: {wait_condition}")


def execute_step(driver, step, persons, cc_data):
    action = step.get("action")
    target_type = step.get("target_type")
    target = step.get("target")
    input_data = step.get("input_data")
    wait_condition = step.get("wait_condition")
    frame_id = step.get("frame_id")
    wait_time = step.get("wait_time", 10)  # set default wait time to 10 secs if not provided

    if wait_condition:
        wait_condition_func = get_wait_condition(wait_condition)
        by_type = get_by_type(target_type)

    if frame_id:
        try:
            frame_element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((get_by_type(target_type), frame_id))
            )
            driver.switch_to.frame(frame_element)
            logging.info(f"Switched to frame: {frame_id}")
        except Exception as e:
            logging.error(f"Error while switching to frame {frame_id} : {e}")
            return

    try:

        if action == "navigate":
            driver.get(target)
            logging.info(f"Navigated to: {target}")

        elif action == "click":
            if wait_condition:
                element = WebDriverWait(driver, wait_time).until(
                    wait_condition_func((by_type, target))
                )
                element.click()
                logging.info(f"Clicked element: {target}")
            else:
                element = driver.find_element(get_by_type(target_type), target)
                element.click()
                logging.info(f"Clicked element: {target}")

        elif action == "input":

            if wait_condition:
                element = WebDriverWait(driver, wait_time).until(
                    wait_condition_func((by_type, target))
                )
                if isinstance(input_data, str) and input_data.startswith("person."):
                    data_key = input_data.split(".")[1]
                    person = random.choice(list(persons.values()))
                    element.send_keys(person.get(data_key, ""))
                    logging.info(f"Input: {data_key} from person data into element: {target}")
                elif isinstance(input_data, str) and input_data.startswith("cc."):
                    cc = random.choice(cc_data).split("|")
                    data_key = input_data.split(".")[1]
                    if data_key == "number":
                        element.send_keys(cc[0])
                    elif data_key == "exp":
                        element.send_keys(cc[1] + cc[2])
                    elif data_key == "cvc":
                        element.send_keys(cc[3])
                    else:
                        element.send_keys(input_data)
                    logging.info(f"Input {data_key} from credit card data into element: {target}")
                elif input_data:
                    element.send_keys(input_data)
                    logging.info(f"Input '{input_data}' into element: {target}")
            else:
                element = driver.find_element(get_by_type(target_type), target)
                if isinstance(input_data, str) and input_data.startswith("person."):
                    data_key = input_data.split(".")[1]
                    person = random.choice(list(persons.values()))
                    element.send_keys(person.get(data_key, ""))
                    logging.info(f"Input: {data_key} from person data into element: {target}")
                elif isinstance(input_data, str) and input_data.startswith("cc."):
                    cc = random.choice(cc_data).split("|")
                    data_key = input_data.split(".")[1]
                    if data_key == "number":
                        element.send_keys(cc[0])
                    elif data_key == "exp":
                        element.send_keys(cc[1] + cc[2])
                        logging.info(f"Input {cc[2]} into element: {target}")
                    elif data_key == "cvc":
                        element.send_keys(cc[3])
                    else:
                        element.send_keys(input_data)

                    logging.info(f"Input {cc[2]} from credit card ")
                    logging.info(f"Input {data_key} from credit card data into element: {target}")
                elif input_data:
                    element.send_keys(input_data)
                    logging.info(f"Input '{input_data}' into element: {target}")

        elif action == "switch_frame":
            try:
                driver.switch_to.default_content()
                iframe_element = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((get_by_type(target_type), target))
                )
                driver.switch_to.frame(iframe_element)
                logging.info(f"Switched to frame: {target}")
            except Exception as e:
                logging.error(f"Error while switching to frame {target} : {e}")

        elif action == "switch_to_default":
            driver.switch_to.default_content()
            logging.info("Switched to default content")

        elif action == "get_elements_and_click":
            if wait_condition:
                elements = WebDriverWait(driver, wait_time).until(
                    wait_condition_func((by_type, target))
                )
                if elements:
                    elements[0].click()
                    logging.info(f"Clicked element: {target}")
            else:
                elements = driver.find_elements(get_by_type(target_type), target)
                if elements:
                    elements[0].click()
                    logging.info(f"Clicked element: {target}")
    except WebDriverException as e:
        logging.error(f"Error executing action '{action}' on target '{target}': {e}")

    if frame_id:
        driver.switch_to.default_content()


def main():
    driver = setup_driver()
    if not driver:
        return

    if not args.config:
        logging.error("Please provide a configuration file.")
        return

    if not args.url:
        logging.error("Please provide a URL to navigate to.")
        url = "https://startselect.com/fr-fr/e-carte-google-play-euro25/32659"
    else:
        url = args.url

    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {args.config}")
        return
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {args.config}")
        return

    cc_data = load_cc_data()
    try:
        while True:
            try:
                for cc in cc_data:
                    driver.get(url)
                    for step in config["steps"]:
                        execute_step(driver, step, persons, cc_data)
                    try:
                        iframe_close = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '[name="NuveiIrame"]'))
                        )
                        driver.switch_to.frame(iframe_close)
                        try:
                            cancel_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="cancelButton"]'))
                            )
                            if cancel_button:
                                logging.info("Credit card is working.")
                        except:
                            logging.info("Error during payment.")

                        try:

                            close_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="closeButton"]'))
                            )
                            if close_button:
                                logging.info("Credit card is not working.")
                        except:
                            logging.info("Error during payment.")
                        driver.switch_to.default_content()
                    except:
                        logging.info("Error during payment verification iframe")
                    time.sleep(10)
                    driver.delete_all_cookies()
                logging.info("All credit cards tested.")
                exit(0)
            except WebDriverException as e:
                logging.error(f"Error during navigation: {e}")
                break
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    finally:
        driver.quit()
        logging.info("ChromeDriver closed.")


if __name__ == "__main__":
    main()