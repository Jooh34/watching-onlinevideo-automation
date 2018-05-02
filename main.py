# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# var
DRIVER_PATH = 'C:/Users/mnh51/workspace/selenium/chromedriver.exe';
user_id = '';
user_pw = '';

# close alert if it exists
def handle_alert():
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")

# See all video in the subject
def see_Subject():

    listeningList = driver.find_element_by_css_selector("ul[class='listeningList']");
    lis = listeningList.find_elements_by_tag_name("li");
    list_size = len(lis);

    for i in range(list_size) :
        listeningList = driver.find_element_by_css_selector("ul[class='listeningList']");
        lis = listeningList.find_elements_by_tag_name("li");
        study_complete = lis[i].find_element_by_css_selector("p");

        if(study_complete.text.strip() != "학습완료"):
            lis[i].find_element_by_css_selector("a[class='titleA']").click();
            time.sleep(2);
            see_Num();

    driver.find_element_by_css_selector("a[title='다른과목보기']").click();
    time.sleep(1);
    return;

#See all video in that number
def see_Num():
    handle_alert();
    time.sleep(1);

    listeningList = driver.find_element_by_css_selector("ul[class='learningList']");
    lis = listeningList.find_elements_by_tag_name("li");
    list_size = len(lis)
    for i in range(list_size) :
        listeningList = driver.find_element_by_css_selector("ul[class='learningList']");
        lis = listeningList.find_elements_by_tag_name("li");
        timeclock = lis[i].find_elements_by_css_selector("span");
        learning_complete = lis[i].find_element_by_css_selector("p[class='second']");
        text = learning_complete.text[:3];

        if len(timeclock) and text != "학습완" : # if it is video and isn't watched yet
            minute_str = timeclock[0].text[:-1];
            minute = int(minute_str);
            lis[i].click();
            time.sleep(60*minute);
            handle_alert();

    driver.find_element_by_css_selector("a[title='전체회차보기']").click();
    time.sleep(1);
    return;


driver = webdriver.Chrome(DRIVER_PATH)

driver.get("https://www.cyber.hs.kr/user/login.do")
time.sleep(0.5)

driver.find_element_by_id('userId').send_keys(user_id);
driver.find_element_by_id('password').send_keys(user_pw);
driver.find_element_by_id('login_btn').click();
time.sleep(3)

driver.get("http://www.cyber.hs.kr/myclassNew/myclassMain.do")
time.sleep(1)

driver.find_element_by_css_selector("img[alt='닫기']").click();
time.sleep(1)

for i in range(10):
    ul = driver.find_element_by_css_selector("ul[class='all_subject']");
    lis = ul.find_elements_by_tag_name("li");
    lis[i].find_element_by_css_selector("a[class='layer']").click();
    time.sleep(1);
    see_Subject();
