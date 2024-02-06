import os
import requests
import tarfile
import zipfile
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from browsermobproxy import Server

from os.path import join

import os
import stat

# Specify versions and paths
geckodriver_version = 'v0.31.0'  # Example version
firefox_version = '121.0'  # Example version
geckodriver_download_url = f'https://github.com/mozilla/geckodriver/releases/download/{geckodriver_version}/geckodriver-{geckodriver_version}-linux64.tar.gz'
firefox_download_url = f'https://ftp.mozilla.org/pub/firefox/releases/{firefox_version}/linux-x86_64/en-US/firefox-{firefox_version}.tar.bz2'  # Example URL
geckodriver_path = './geckodriver'
firefox_path = './firefox'

browsermob_proxy_version = '2.1.4'  # Example version, adjust as needed
bmp_download_url = f'https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-{browsermob_proxy_version}/browsermob-proxy-{browsermob_proxy_version}-bin.zip'
bmp_path = join('browsermob-proxy',f'browsermob-proxy-{browsermob_proxy_version}','bin','browsermob-proxy') # Adjust your BrowserMob Proxy path

# with open(bmp_path) as f:
#     print(f.read())

def get_firefox(options):
    # Setup Selenium to use the downloaded Geckodriver and Firefox binary
    firefox_binary = f'{firefox_path}/firefox/firefox'
    service = Service(executable_path=geckodriver_path)
    options.binary_location = firefox_binary
    return webdriver.Firefox(options=options, service=service)

def get_proxied_firefox(options, log_file_path='logs'):
    server = Server(bmp_path)
    server.start()
    proxy = server.create_proxy()
    # Start the proxy and create a new HAR file for logging
    proxy.new_har("test", options={'captureHeaders': True, 'captureContent': True})

    # Configure Selenium to use the proxy
    selenium_proxy = proxy.selenium_proxy()
    options.proxy = selenium_proxy

    # Use the existing get_firefox function to initialize the browser with these options
    driver = get_firefox(options)

    # Save the proxy HAR to a file
    with open(log_file_path, 'w') as logfile:
        import json
        logfile.write(json.dumps(proxy.har, ensure_ascii=False))

    return driver


# Function to download and extract geckodriver
def download_geckodriver():
    if not os.path.exists(geckodriver_path):
        print(f"Downloading geckodriver version {geckodriver_version}...")
        response = requests.get(geckodriver_download_url)
        open(f'geckodriver-{geckodriver_version}-linux64.tar.gz', 'wb').write(response.content)
        print("Extracting geckodriver...")
        with tarfile.open(f'geckodriver-{geckodriver_version}-linux64.tar.gz', 'r:gz') as tar:
            tar.extractall()
        os.rename(f'geckodriver', geckodriver_path)
        os.remove(f'geckodriver-{geckodriver_version}-linux64.tar.gz')
    else:
        print("Geckodriver is already downloaded.")

# Function to download and extract Firefox
def download_firefox():
    if not os.path.exists(f'{firefox_path}/firefox'):
        print(f"Downloading Firefox version {firefox_version}...")
        response = requests.get(firefox_download_url)
        open(f'firefox-{firefox_version}.tar.bz2', 'wb').write(response.content)
        print("Extracting Firefox...")
        tar = tarfile.open(f'firefox-{firefox_version}.tar.bz2', 'r:bz2')
        tar.extractall(firefox_path)
        tar.close()
        os.remove(f'firefox-{firefox_version}.tar.bz2')
    else:
        print("Firefox is already downloaded.")

def download_browsermob_proxy():
    if not os.path.exists(bmp_path):
        print(f"Downloading BrowserMob Proxy version {browsermob_proxy_version}...")
        response = requests.get(bmp_download_url)
        zip_path = f'browsermob-proxy-{browsermob_proxy_version}-bin.zip'
        open(zip_path, 'wb').write(response.content)
        print("Extracting BrowserMob Proxy...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(bmp_path)
        os.remove(zip_path)
    else:
        print("BrowserMob Proxy is already downloaded.")

    os.chmod(bmp_path, os.stat(bmp_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

if __name__=="__main__":
    download_geckodriver()
    download_firefox()
    download_browsermob_proxy()


    options = Options()
    driver = get_proxied_firefox(options)
    # Now you can use driver to navigate
    driver.get("https://github.com/nevakrien/")
    print(driver.title)

    driver.quit()
