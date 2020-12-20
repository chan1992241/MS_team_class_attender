from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import mysql.connector
import datetime
import time
import os

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="testdatabase"
)

mycursor = db.cursor()

timeTable = []

email = ""
password = ""

def navigate_main_page():
    global driver
    driver = webdriver.Chrome(chrome_options=opt, executable_path='C:\\Users\\Chan Jin Yee\\Documents\\udemy course\\python\MS_automation\\webDriver\\chromedriver')
    url = 'https://teams.microsoft.com'
    driver.get(url)
    driver.maximize_window()
    email_field = driver.find_element(By.XPATH, '//*[@id="i0116"]')
    email_field.click()
    email_field.send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
    WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="i0118"]')))
    password_field = driver.find_element(By.XPATH, '//*[@id="i0118"]')
    password_field.click()
    password_field.send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="idSIButton9"]').click()
    time.sleep(2)
    WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    driver.find_element(By.CSS_SELECTOR, '#download-desktop-page > div > a').click()
    WebDriverWait(driver,10000).until(EC.title_is('Microsoft Teams'))

timeTable = []
def join_class():
    global driver
    while True:
        day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        today = datetime.date.today().weekday() #get 0-6 monday - sunday 0 is monday 6 is sunday
        today = day_name[today]
        now = datetime.datetime.now().time() #get current time
        now = now.strftime('%H %M %S') #we want hour and minute only (https://stackoverflow.com/questions/25363966/find-and-click-element-by-title-python-selenium)
        for course in timeTable:
            info = 0
            current_course = ''
            for key in course:
                current_course = key
                info = course[key]
            if info['day'] == today and info['time'] == now:
                loc = '#favorite-teams-panel > div > div.stv-items-container > div:nth-child(' + str(course[key]['location'][1] + 1) + ') > div:nth-child(' + str(course[key]['location'][0] + 1) + ') > div > ng-include > div'
                driver.find_element(By.CSS_SELECTOR, loc).click()
                time.sleep(5)
                while True:
                    wait = 0
                    try:
                        joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
                        joinbtn.click()
                    except:
                        print("Havent start yet")
                        time.sleep(60)
                        wait+=1
                        if wait == 15:
                            print("Do not have course")
                            break
                    else:
                        break
                try:
                    driver.find_element(By.CSS_SELECTOR, '#preJoinAudioButton > div > button > span[title="Mute microphone"]').click()
                except:
                    print("Muted already")
                try:
                    driver.find_element(By.CSS_SELECTOR, '#page-content-wrapper > div.flex-fill > div > calling-pre-join-screen > div > div > div.ts-calling-pre-join-content > div.central-section > div.video-and-name-input > div > div > section > div.buttons-container > toggle-button:nth-child(1) > div > button > span[title="Turn camera off"]').click()
                except:
                    print("Camera off already")
                driver.find_element(By.CSS_SELECTOR, '#page-content-wrapper > div.flex-fill > div > calling-pre-join-screen > div > div > div.ts-calling-pre-join-content > div.central-section > div.video-and-name-input > div > div > section > div.flex-fill.input-section > div > div > button').click()
                time.sleep(float(info['duration'])*60*60)
                driver.find_element(By.CSS_SELECTOR, '#hangup-button > ng-include > svg').click()
                time.sleep(2)
                try:
                    driver.find_element(By.CSS_SELECTOR, '#hangup-button > ng-include > svg').click()
                except:
                    print("cannot click")
                time.sleep(2)
                try:
                    driver.find_element(By.XPATH, '//*[@id="page-content-wrapper"]/div[1]/div/calling-screen/div/div[2]/calling-quality-feedback/div/div[2]/button[2]').click()
                except:
                    print("Feedback already")
                driver.find_element(By.CSS_SELECTOR, '#wrapper > div.app-left-wrapper.pull-left > div > left-rail > div > div > school-app-left-rail > single-team-channel-list > div > school-app-back-button > button > ng-include > svg').click()
                os.system('cls')
                print("Press < CTR + C > to terminate")
            else: 
                print("Haven't reach time yet, now is: {}".format(now))
                os.system('cls')


def add_timeTable():
    course_name = input("What is the course name: ")
    course_day = input("What is the day of the course (Monday - Friday): ")
    course_time = input("What is the time of the course (hh mm ss): ")
    course_duration = input("What is the duration of the course (hour): ")
    course_location_x = int(input("Where is the course locate (x-axes): "))
    course_location_y = int(input("Where is the course locate (y-axes): "))
    sql = "insert into timetable (courseName, day, time, duration, location_x, location_y) values (%s, %s, %s, %s, %s, %s)"
    mycursor.execute(sql, (course_name, course_day, course_time,course_duration,course_location_x,course_location_y))
    db.commit()
    
def confirmation(email, password, timeTable):
    print("Confirm your information")
    print("Your email is: {}".format(email))
    print("Your password is: {}".format(password))
    print("Your timetable is: ")
    mycursor.execute("select * from timetable")
    for data in mycursor:
        timeTable.append({data[1]: {"day": data[2], "time": data[3], "duration": data[4], "location": [data[5], data[6]]}})
    print("{:<15} {:<12} {:<10} {:<10} {:<10} {:<10}".format('course', 'day', 'time', 'duration', 'location x', 'location y'))
    for course in timeTable:
        info = 0
        current_course = ''
        for key in course:
            current_course = key
            info = course[key]
        print ("{:<15} {:<12} {:<10} {:<10} {:<10} {:<10}".format(current_course, info['day'], info['time'], info['duration'], info['location'][0], info['location'][1]))
    timeTable = []
    print("Press 1 for correct \nPress 2 for reenter again")
    confirm_ans = int(input()) 
    if confirm_ans == 2:
        return False
    else:
        return True
    #timeTable = [{"Chan Jin Yee": {"day": "Sunday", "time": now, "duration": '0.001', 'location': [4, 2] }}]



if __name__ == "__main__":
    while True:
        print("What action you want to do \n\t 1 - initialize program \n\t 2 - execute the program \n\t 3 - terminate program ")
        action = int(input())
        if action == 1:
            email = input("What is your microsoft team email: ")
            password = input("What is your microsoft team password: ")
            print("How many course you want to add")
            noOfCourse = int(input())
            for i in range(noOfCourse):
                print(f'{i+1} course')
                add_timeTable()
            os.system("cls")
            print("Please confirm your information before proceeding")
            if confirmation(email, password, timeTable) == False:
                timeTable = []
                mycursor.execute("truncate table timetable")
                db.commit()
            else:
                timeTable = []
            
        elif action == 2:
            mycursor.execute("select * from timetable")
            for data in mycursor:
                timeTable.append({data[1]: {"day": data[2], "time": data[3], "duration": data[4], "location": [data[5], data[6]]}})
            mycursor.execute("truncate table timetable")
            db.commit()
            navigate_main_page()
            join_class()
            driver.quit()
        else: 
            break
"""
1. need to use mysql to stor timetable data
2. reconfigure timetable dictionary

"""
    
    