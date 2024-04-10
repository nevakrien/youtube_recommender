from browsermobproxy import Server
from env_setup import get_firefox,get_proxied_firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

from selenium.webdriver.remote.webelement import WebElement

def find_parent_with_aria_label(element):
    """
    Recursively traverses up the DOM tree from the given element
    until an element with an 'aria-label' attribute is found.
    :param element: The starting WebElement to search from.
    :return: WebElement with 'aria-label' or None if not found.
    """
    while element and isinstance(element, WebElement):
        aria_label = element.get_attribute('aria-label')
        if aria_label:
            return element
        else:
            # Move to the parent element using XPath's parent axis
            element = element.find_element(By.XPATH, '..')
    return None

# Setup WebDriver with Proxy
options = webdriver.FirefoxOptions()
#options.add_argument("--headless")
driver,proxy = get_proxied_firefox(options)
print('yay')
# Start capturing traffic
#proxy.new_har("https://github.com/nevakrien/")



# Wait for a few seconds to capture all requests
# You might need to adjust this sleep time or use more sophisticated waiting methods
import time

# Open a website
driver.get("https://www.youtube.com/watch?v=p60L-TOecik")

time.sleep(3)

# # Dump captured data to files
with open('network_traffic.json', 'w') as traffic_file:
    json.dump(proxy.har, traffic_file)

with open('page_source.html', 'w') as html_file:
    html_file.write(driver.page_source)

#elements_containing_like = driver.find_elements(By.XPATH, "//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'like')]")
#elements_containing_like = driver.find_elements(By.XPATH, '/.[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "like")]')

# Use find_elements with By.XPATH to find the smallest elements that contain the text "like"
#elements_containing_like = driver.find_elements(By.XPATH, "//text()[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'like')]/parent::*[not(./*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'like')])]")

#GOOD
#elements_containing_like = driver.find_elements(By.XPATH, '//*[@title="I like this"]')

#less good but worth checking
elements_containing_like = driver.find_elements(By.XPATH, '//*[contains(translate(@title, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "like")]')




print(len(elements_containing_like))
for element in elements_containing_like:
    print(10*"!")
    print(element.tag_name)
    print(element.text)

    parent_with_aria_label = find_parent_with_aria_label(element)
    if parent_with_aria_label:
        print("Found an element with aria-label:", parent_with_aria_label.get_attribute('aria-label'))
    else:
        print("No parent element with aria-label found.")
        #print(element.aria-label)


print(3*"\n")

#info_elements = driver.find_elements(By.ID, "info")
info_elements = driver.find_elements( By.XPATH, "//*[contains(@id, 'info')]//*[contains(@class, 'yt-formatted-string') and contains(., 'views')]")
#info_element = driver.find_element(By.XPATH, "//g[contains(@id, 'info')]//*[contains(@class, 'yt-formatted-string') and contains(text(), 'views')]")

for e in info_elements:
    print(10*"!")
    print(e.text)#e.get_attribute('outerHTML'))
#views_element = info_element.find_element(By.XPATH, ".//*[contains(text(), 'views')]")
#views_element = info_element.find_element(By.XPATH, ".//span[contains(@class, 'yt-formatted-string') and contains(text(), 'views')]")



# Stop the proxy and close the browser
# server.stop()
driver.quit()
