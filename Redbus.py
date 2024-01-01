
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import re


cs = webdriver.ChromeService(service_args=['--disable-build-check'])
co = Options()
co.add_argument('--disable-notifications')
driver = webdriver.Chrome(service=cs)

# Navigate to https://www.redbus.in/
driver.get('https://www.redbus.in/')
driver.maximize_window()
sleep(2)

# Book bus ticket
# In From text field type "Mumbai" and capture all the values in a list that is being populated
driver.find_element('id', 'src').send_keys('Mumbai')
sleep(2)
# From that list select "Borivali East"
options = driver.find_elements('css selector', 'li.sc-iwsKbI')
drop_down_list = [option.text for option in options]
from_places = []
for mitem in drop_down_list:
    if mitem.endswith('\nMumbai'):
        res = mitem[:-len('\nMumbai')]
        from_places.append(res)
for place in from_places:
    if place == 'Borivali East':
        driver.find_element('xpath', '//text[text()= "Borivali East"]').click()
sleep(5)
# driver.find_element('xpath', '//text[text()= "Borivali East"]').click()
# sleep(2)

# In To text field type "Banglore" and select Indiranagar from the list populated
driver.find_element('id', 'dest').send_keys('Bangalore')
sleep(2)
to_options = driver.find_elements('xpath', "//div[@class='sc-gZMcBi grvhsy']")
to_list = [option.text for option in to_options]
to_places = []
for item in to_list:
    if item.endswith('\nBangalore'):
        res = item[:-len('\nBangalore')]
        to_places.append(res)
action = ActionChains(driver)
for place in to_places:
    if place == 'Indiranagar':
        element = driver.find_element('xpath', "//text[text()='Indiranagar']")
        action.move_to_element(element).perform()
        driver.find_element('xpath', "//text[text()='Indiranagar']").click()
sleep(5)
# In the date section book on a date which is 2 days after current date
current_date = datetime(year=2023,month=12,day=31) + timedelta(days=2)
formatted_date = current_date.strftime("%d")
if formatted_date.startswith('0'):
    res = re.findall(r'[\d]$',formatted_date)
    for d in res:
        date_ = d
else:
    date_ = formatted_date
day = f"//hr[@class='divider']/..//span[text()='{date_}']"
driver.find_element('xpath', day).click()

# Click on search  buses
sleep(5)
driver.find_element('id', 'search_button').click()
sleep(5)

# Then when the search results appear filter them by Seater and AC
driver.find_element('xpath', "//label[text()='SEATER']").click()
sleep(5)
driver.find_element('xpath', "//label[text()='AC']").click()
buses = driver.find_elements('xpath', "//div[@class='travels lh-24 f-bold d-color']")

# Capture all the bus names in the list
bus_lst = [bus.text for bus in buses]
prices = driver.find_elements('xpath', "//div[@class='travels lh-24 f-bold d-color']/../..//div[@class='fare d-block']/child::span")
price_lst = [price.text for price in prices]

# And capture detail of the the bus which have lowest fare
d = {bus_lst[index]: price_lst[index] for index in range(len(bus_lst))}
sort_d = sorted(d.items(), key=lambda x:x[-1])
convert_d = dict(sort_d)
sort_list = [[key, value] for key, value in convert_d.items()]
Bus = sort_list[0][0]
price = sort_list[0][1]
print(Bus+" has the lowest fair of "+"Rs " +price+"/-")