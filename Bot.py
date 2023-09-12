from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pyttsx3
import sounddevice as sd

def login():
    username= "harrypotterpork"
    password= "HemeraNyx123"

    # Set up the Chrome driver
    service = Service("chromedriver.exe")  # Replace with the path to your chromedriver executable
    driver = webdriver.Chrome(service=service)

    # Navigate to the login page
    driver.get("https://steamcommunity.com/login/home/?goto=%2Fchat%2F")
   
    time.sleep(6)
    username_field = driver.find_element("css selector", "input[type='text']")
    username_field.send_keys(username)

    password_field = driver.find_element("css selector", "input[type='password']")
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)


    # Define the maximum number of retries
    max_retries = 200  # Adjust this value as needed

    # Define the timeout for form submission
    form_submit_timeout = 200  # Adjust this value as needed

    # Initialize the number of retries
    num_retries = 0

    while num_retries < max_retries:
        try:
            # Submit the login form
            password_field.send_keys(Keys.RETURN)

            # Wait until the chat page URL is matched or until the form submit timeout is reached
            WebDriverWait(driver, form_submit_timeout).until(EC.url_to_be("https://steamcommunity.com/chat/"))

            # If the chat page loads successfully, break out of the loop
            break

        except TimeoutException:
            print("Timeout occurred while waiting for the chat page to load after form submission.")
            # Handle the timeout scenario here
            
            # Increment the number of retries
            num_retries += 1

        # Check if the maximum number of retries is reached
        if num_retries == max_retries:
            print("Maximum number of retries reached. Exiting.")
            # Handle the maximum retries scenario here
            break
        # Wait for the chat page to load
    # Check if the login was successful
    if driver.current_url == "https://steamcommunity.com/chat/":
        # Successfully logged in
        print("Successfully logged in and navigated to the chat page.")
    else:
        # Failed to log in
        print("Failed to log in and navigate to the chat page.")
        driver.quit()
        return

    # Stay on the chat page and interact continuously
    time.sleep(10)
    temptext=""
    while True:
        # Perform your desired actions on the chat page here
        # For example, get the text in the textarea
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        text = textarea.get_attribute("value")
        if text!=temptext:
            temptext=text
            print("Text in the textarea:", text)
            text_to_speech(text, output_device="CABLE Output (VB-Audio Virtual Cable)")
            time.sleep(1)

def main():
    login()
def text_to_speech(text, output_device=None):
    engine = pyttsx3.init()
    
    if output_device:
        # Get the available sound devices and find the ID of the desired output device
        devices = sd.query_devices()
        for device in devices:
            print(device)
            if device['name'] == output_device:
                output_device_id = device['index']    
                break
        else:
            #print(f"Output device '{output_device}' not found.")
            return

        # Set the output device for sound playback
        sd.default.device[0] = output_device_id
    voice = engine.getProperty('voices') #get the available voices
    
    # eng.setProperty('voice', voice[0].id) #set the voice to index 0 for male voice
    engine.setProperty('voice', voice[0].id)
    engine.say(text)
    engine.runAndWait()
if __name__ == "__main__":
    main()
