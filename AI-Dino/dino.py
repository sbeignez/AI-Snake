# BLOGS
# - https://blog.paperspace.com/dino-run/
# - ...


# SETUP
# Selenium: pip3 install selenium
# OpenCV: pip3 install opencv-python

from PIL import ImageGrab, Image
import numpy as np
import cv2

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os
from time import sleep

def openBrowserWB():
    # using WEBBROWSER
    import webbrowser


    BROWSER_TYPE = 'chrome'
    url = 'chrome://dino/'
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    # webbrowser.get(chrome_path).open_new(url) 
    webbrowser.get(BROWSER_TYPE).open_new(url)

def openBrowser(params):

    CANVAS = "runner-canvas"


    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "bin/chromedriver")

    service=Service(DRIVER_BIN)
    browser = webdriver.Chrome(service=service)

    # browser = webdriver.Chrome(executable_path = DRIVER_BIN)
    
    browser.set_window_position(x=0,y=0)


    # Dimension dimension = new Dimension(800, 600); setSize()
    browser.set_window_size(800, 400)

    try:
        browser.get(params['url'])
    except:
        pass

    # element = browser.find_element(By.XPATH, "/html/body")
    # element = browser.find_element(By.NAME, params['name'])
    # element = browser.find_element(By.ID, params['id'])

    # for i in range(5):
    #     # inputElement.send_keys('1')
    #     element.send_keys(str(i))
    #     print(i)
    #     sleep(0.5)
    # element.send_keys(Keys.ENTER)

    return browser

def start(browser, params):
    # element = browser.find_element(By.ID, params['id'])
    element = browser.find_element(By.XPATH, "/html")
    element.send_keys(Keys.SPACE)
    sleep(1)
    element = browser.find_element(By.XPATH, params["xpath-game"])
    browser.execute_script("arguments[0].setAttribute('style', 'width: 552px; transform: scale(1) translateY(0px); height: 150px;')", element)

# <div role="application" tabindex="0" title="Dino game, play" class="runner-container"
# style="width: 394.406px; transform: scale(1.29055) translateY(70px); height: 150px;">
# <canvas class="runner-canvas" width="788" height="300" style="width: 394px; height: 150px;"></canvas>
# <span class="offline-runner-live-region" aria-live="assertive">Game started.</span></div>


def jump(browser, params):
    element = browser.find_element(By.ID, "t")
    for i in range(5):
        element.send_keys(Keys.SPACE)
        print(i)
        sleep(1)
    
def screenshot(browser, params):
    element = browser.find_element(By.XPATH, params["xpath-game"])
    img = element.screenshot_as_png
    element.screenshot("/Dino/dino.png")

    # im = Image.frombytes(img)
    # im.show()


    return img



def grabImage():
    img = ImageGrab.grab(bbox=(100,10,400,780)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    img_np = np.array(img) #this is the array obtained from conversion

    print (img_np)
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("test", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


# url = 'chrome://dino/'
params_test = { 
    "url" : 'https://www.google.com',
    "name" : 'q',
}

params = { 
    "url" : 'chrome://dino/',
    "id" : "main-content",
    "name" : 't',
    "xpath-game" : "//*[@id='main-frame-error']/div[4]"
}


browser = openBrowser(params)
start(browser, params)
jump(browser, params)
screenshot(browser, params)
browser.close()
