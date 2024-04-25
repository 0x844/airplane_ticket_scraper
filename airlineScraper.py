from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import smtplib
from email.message import EmailMessage
import selenium.common.exceptions # for exception handling
import undetected_chromedriver as webdriver


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--use_subprocess")

browser = webdriver.Chrome(options=chrome_options)

# Enter airport inputs as the 3 letter abbrev. ex: "IAD", "NAN", etc.
departure_inputs = {'Departing Airport':'ENTER HERE', 
                    'Arriving Airport': 'ENTER HERE',
                    'Date of Departure': 'January 1, 2024'}

returning_inputs = {'Departing Airport': 'ENTER HERE',
                    'Arriving Airport': 'ENTER HERE',
                    'Date of Departure': 'January 1, 2024'}

def cheap_flight_scrape(flight):
    PATH = r'ENTER CHROMEDRIVER PATH HERE'
    
    driver = webdriver.Chrome()

    departing_from = flight['Departing Airport']
    departure_month_and_year = flight['Date of Departure'].split()[0] + ' ' + flight['Date of Departure'].split()[-1]
    arriving_at = flight['Arriving Airport']

    # Website
    driver.get("https://www.travelocity.com/Flights")

    time.sleep(1)
    # Clicks 'One Way' button
    one_way_elem = driver.find_element(By.XPATH, '//*[@aria-controls="FlightSearchForm_ONE_WAY"]')
    one_way_elem.click()
    time.sleep(2)

    # Selects 'Leaving from' box 
    where_from_elem = driver.find_element(By.XPATH, '//*[@aria-label="Leaving from"]')
    where_from_elem.click()
    fill_out = driver.find_element(By.XPATH, '//*[@placeholder="Leaving from"]')

    # Fills out 'Leaving from' box
    fill_out.send_keys(departing_from)
    fill_out.send_keys(Keys.ENTER)
    time.sleep(1)

    # Selects 'Going to' box
    where_to_elem = driver.find_element(By.XPATH, '//*[@aria-label="Going to"]')
    where_to_elem.click()
    going_to = driver.find_element(By.XPATH, '//*[@placeholder="Going to"]')

    # Fills out 'Going to' box
    going_to.send_keys(arriving_at)
    going_to.send_keys(Keys.ENTER)

    # Selects 'Dates' to open calender menu
    dates_box_elem = driver.find_element(By.XPATH, '//*[@id="date_form_field-btn"]')
    dates_box_elem.click()
    time.sleep(1)
    
    month = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/form/div/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/h2').text
    
    # Scroll through calendar to find desired month
    while month != departure_month_and_year:
        next_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'uitk-button-paging')))
        if len(next_buttons) >= 2:
            second_button = next_buttons[1]
            second_button.click()
            # Update month after clicking the arrow button
            month_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div/div/form/div/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/h2')
            month = month_element.text
    time.sleep(2)
    
    # Formatted Date
    extracted_date = flight['Date of Departure']
    date = extracted_date.split()
    month_abrev = date[0][:3]
    day = date[1]
    year = date[2]
    
    # Find 'day' on calendar
    day_xpath = f"//*[@aria-label[starts-with(., '{month_abrev} {day} {year}')]]"

    # Clicks departing date 'day' button
    driver.find_element(By.XPATH, day_xpath).click()
    time.sleep(2)
    
    # Clicks 'Done' button
    driver.find_element(By.XPATH, '//*[@aria-label="Save changes and close the date picker."]').click()
    time.sleep(2)
    
    # Clicks 'Search' button
    driver.find_element(By.XPATH, '//*[@id="search_button"]').click()
    time.sleep(5)
    
    # Dropdown to select 'Sort by: Lowest to Highest'
    driver.find_element(By.XPATH, '//*[@id="sort-filter-dropdown-SORT"]').click()
    price_button = driver.find_element(By.XPATH, '//*[@value="PRICE_INCREASING"]').click()
    time.sleep(1)

    # Deselect dropdown menu
    driver.find_element(By.XPATH, '//*[@style="--uitk-layoutgrid-auto-columns:minmax(var(--uitk-layoutgrid-egds-size__0x), 1fr);--uitk-layoutgrid-column-start:span 8;--uitk-layoutgrid-column-start-medium:span 2;--uitk-layoutgrid-column-start-extra_large:span 2"]').click()
    time.sleep(3)

    # Scroll down the page to load more flights
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(20)
    
    flight_list = []

    # Formatted flight data, with initialized headings for email format
    formatted_flight_info = [['Departure Time:', 'Arrival Time:', 'Price:', 'Total Travel Time:']]
    
    n = 0

    # Finds the first 10 cheapest flights, adds them to flight_info list
    for i in range(1,11):
        flight_xpath = f"//*[@stid='FLIGHTS_DETAILS_AND_FARES-index-{i}-leg-0-fsr-FlightsActionButton']"
        flight_list.append([driver.find_element(By.XPATH, flight_xpath).text])
    
    print(flight_list)
    
    # Formats the data from flight_info
    for i in range(1, len(flight_list)):
        departing_time = flight_list[i][0].split(",")[1][13:]
        arriving_time = flight_list[i][0].split(",")[2][12:]
        
        total_travel_time = [] 

        # Since flight data isn't consistent for all flights, 
        # we must search for the "total travel time" string and 
        # take the data from there on out
        for list in flight_list:
            for flight_info in list:
                data = flight_info.split(".")
                for time in data:
                    if "total travel time" in part:
                # Find index of "total travel time"
                        index = part.index("total travel time")
                # Get the substring from the index minus 20 characters to the index
                        time_str = part[max(index - 20, 0):index]
                        total_travel_time.append(time_str.strip())

    
        for flight_info in flight_list[i]:  
            parts = flight_info.split()  
            for part in parts:
                if part.startswith("$"): 
                    price = part.strip()  
                    
                     
        formatted_flight_info.append([departing_time, arriving_time, price, total_travel_time[n]])
        n+=1

    # Closes browser
    driver.quit()

    return formatted_flight_info
    

def email():
    data = pd.DataFrame(cheap_flight_scrape(departure_inputs))
    print(data)
    email = open('email.txt').read()
    password = open('pass.txt').read()
    msg = EmailMessage()
    msg['Subject'] = "Flight Info: {} -> {}, Departing: {}".format(departure_inputs['Departing Airport'], departure_inputs['Arriving Airport'], departure_inputs['Date of Departure'])
    msg['From'] = email
    msg['To'] = email   
    msg.add_alternative('''\
            <!DOCTYPE html>
            <html>
                <body>
                    {}
                </body>
            </html>'''.format(data.to_html()), subtype="html")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email,password)
            smtp.send_message(msg)
email()
