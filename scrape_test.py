from browsermobproxy import Server
from env_setup import get_firefox
from selenium import webdriver
import json

# Path to BrowserMob Proxy binary
bmp_path = 'path/to/browsermob-proxy'

#Start BrowserMob Proxy
server = Server(bmp_path)
server.start()
proxy = server.create_proxy()

# Setup WebDriver with Proxy
options = webdriver.FirefoxOptions()
driver = get_firefox(options)
print('yay')
# Start capturing traffic
#proxy.new_har("https://github.com/nevakrien/")



# Wait for a few seconds to capture all requests
# You might need to adjust this sleep time or use more sophisticated waiting methods
import time

# Open a website
driver.get("https://github.com/nevakrien/")

time.sleep(5)

# Dump captured data to files
with open('network_traffic.json', 'w') as traffic_file:
    json.dump(proxy.har, traffic_file)

with open('page_source.html', 'w') as html_file:
    html_file.write(driver.page_source)

# Stop the proxy and close the browser
server.stop()
driver.quit()
