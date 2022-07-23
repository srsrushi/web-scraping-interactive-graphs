import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime as dt
import pandas as pd

# Opening the connection and grabbing the page
my_url = 'https://www.google.com/webhp?hl=en'
option = Options()
option.headless = False
driver = Chrome(options=option)
driver.get(my_url)
driver.maximize_window()

action = selenium.webdriver.ActionChains(driver)
search_bar = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Search"]')))
search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
    (By.XPATH, '//form[@role="search"]/div/div/div/center/input[@aria-label="Google Search"]')))

search_bar.send_keys('inr euro')
search_button.click()

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,
                                                                          '//div[@id="knowledge-currency__updatable-chart-column"]/div/div[2]/div[@data-async-type="wholepage_currency_v2_chart"]')))
loc = element.location
size = element.size

print(loc)
print(size)

action.move_to_element_with_offset(element, 316, 0).perform()

value = driver.find_element_by_xpath(
    '//div[@data-async-type="wholepage_currency_v2_chart"]/div/div/span[@class="knowledge-finance-wholepage-chart__hover-card-value"]').text
date = driver.find_element_by_xpath(
    '//div[@data-async-type="wholepage_currency_v2_chart"]/div/div/span[@class="knowledge-finance-wholepage-chart__hover-card-time"]').text

date_lst = []
value_lst = []

limit = dt.datetime.strptime('06/28', '%m/%d')
pace = -5

while True:
    action.move_by_offset(pace, 0).perform()
    date = driver.find_element_by_xpath(
        '//div[@data-async-type="wholepage_currency_v2_chart"]/div/div/span[@class="knowledge-finance-wholepage-chart__hover-card-time"]').text
    value = driver.find_element_by_xpath(
        '//div[@data-async-type="wholepage_currency_v2_chart"]/div/div/span[@class="knowledge-finance-wholepage-chart__hover-card-value"]').text

    if dt.datetime.strptime(date, '%a, %d %b') < limit:
        break

    if date in date_lst:
        pass
    else:
        date_lst.append(date)
        value_lst.append(value)

driver.quit()

df = pd.DataFrame({"Currency_Value":value_lst, "Date": date_lst})
print(df)
df.to_csv("INR_Euro_Currency_Data.csv", index=False)
