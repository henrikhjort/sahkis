from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from PIL import Image
import pytesseract
import io
import time

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def setup_driver():
    options = FirefoxOptions()
    options.add_argument('--headless')

    service = FirefoxService(executable_path='/usr/local/bin/geckodriver')
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def get_fullpage_screenshot(driver, url):
    driver.get(url)
    
    # Wait for the page to load
    time.sleep(5)
    
    total_height = driver.execute_script("return document.body.scrollHeight")
    
    driver.set_window_size(1920, total_height)
    
    # Take the screenshot of the entire page
    screenshot = driver.get_screenshot_as_png()
    
    # Open the screenshot with PIL
    image = Image.open(io.BytesIO(screenshot))
    
    return image

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def number_of_evs(text):
    # Split the text into words
    words = text.split()
    # Search for 'Myydaan' and 'sahk' in the text
    for i in range(len(words)):
        if words[i] == 'Myydaan' and words[i+1].startswith('sahk'):
            # Grab next word (ev count)
            ev_count = words[i+2]
            # Check if numeric
            if ev_count.isnumeric():
                return int(ev_count)
            else:
                return 0

if __name__ == '__main__':
    url = 'https://www.nettiauto.com/vaihtoautot/sahkoautot'
    driver = setup_driver()
    
    # Take a screenshot of the entire page
    image = get_fullpage_screenshot(driver, url)
    
    # Extract text from the image
    text = extract_text_from_image(image)

    # Number of EVs
    result = number_of_evs(text)
    print("Number of EVs: ", result)
    
    driver.quit()

