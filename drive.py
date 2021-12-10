from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ffmpeg
import logging
import os
import sys

logging.getLogger().setLevel(logging.INFO)

if len(sys.argv) < 3:
    logging.fatal('Please supply a .wav and .json files on the command line')
    sys.exit(1)

script_directory = os.path.dirname(__file__)

options = webdriver.ChromeOptions()
options.add_argument("--allow-insecure-localhost")
options.add_experimental_option("excludeSwitches", [
    "ignore-certificate-errors",
    "enable-automation"
])
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-web-security")
options.add_argument("--autoplay-policy=no-user-gesture-required")
options.add_argument("--headless")
options.add_argument("--nogpu")
options.add_argument("--disablegpu")
options.add_argument("--window-size=1280,1280")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("prefs", {
    "download.default_directory" : script_directory,
    'profile.default_content_setting_values.automatic_downloads': 2,
    })
options.add_argument("--mute-audio")

if os.path.exists('myvid.webm'):
    os.unlink('myvid.webm')
if os.path.exists('myvid.mp4'):
    os.unlink('myvid.mp4')

logging.info('Create environment')
driver = webdriver.Chrome(options=options)
driver.get(f'file://{script_directory}/index.html')
driver.execute_script(f'window.transcriptionFile = \'{script_directory}/{sys.argv[2]}\';')
driver.execute_script(f'window.audioFile = \'{script_directory}/{sys.argv[1]}\';')
driver.execute_script('window.startVideo();')
logging.info('Creating video...')
case_status = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'downloadlink')))
logging.info('Done.')
driver.close()
driver.quit()

logging.info('Converting...')
(
    ffmpeg
    .input('myvid.webm')
    .output('myvid.mp4', **{'qscale:v': 3})
    .global_args('-loglevel', 'error')
    .global_args('-y')
    .run()
)
os.unlink('myvid.webm')
logging.info('Video is ready.')
