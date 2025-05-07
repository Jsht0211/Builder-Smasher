import time
import json
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from openai import OpenAI

def chatAI(bot, content, url=""):
    global token
    if bot == "ds":
        deepseek = OpenAI(
            base_url="https://router.huggingface.co/novita/v3/openai",
            api_key=token,
        )

        completion = deepseek.chat.completions.create(
            model="deepseek/deepseek-prover-v2-671b",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            max_tokens=10,
        )
    else:
        gemma = OpenAI(
            base_url="https://router.huggingface.co/nebius/v1",
            api_key=token,
        )

        completion = gemma.chat.completions.create(
            model="google/gemma-3-27b-it-fast",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": content
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ]
                }
            ],
            max_tokens=400,
        )

    return completion.choices[0].message.content.replace("`","").replace("plaintext","").replace("\n","")



from bs4 import BeautifulSoup

def browse(url):
    global browser
    browser.get(url)
    soupPage()

def soupPage():
    global soup
    soup = BeautifulSoup(browser.page_source, "html.parser")

useGemma = False
dsRule = "请严格按照只说出答案/选项的格式回答问题，再说一遍，请严格按照只说出答案/选项的格式回答问题,如果有选项就不用说选项代表的答案了，直接说选项，如果没有那就只说答案，不要有多余的话。例如：'Passage:He is the King of the world.------- Question:Is he the king?---Choices:1:Yes, 2:No, 3:Not given',你就要回答1；又或者'Passage:He is the King of the world.------- Question:He is the king of the ___,while he is the ___ of the world.'，你就要回答'world,king'(如果有多个答案必须用英文逗号隔开，不要对文字做特殊处理，比如'plaintext\nans\n'是不对的，只说ans就可以了)。下面是问题:"
allowedTypes = ["reading","speaking","writing"]
blackList = []
try:
    with open("blacklist.json","r") as fi:
        blackList = json.load(fi)
except:
    with open("blacklist.json", "w") as fi:
        json.dump(blackList, fi)

while True:
    token = input("Please enter your hugging face token\n(If you don't have one, enter 1):")
    if token == "1":
        print("\nHow to get a token:\nGo to:'huggingface.co' and create a new account.\nAfter you have confirmed your email, click on 'Access Tokens' on the setting page.\nClick 'create new token', fill in the name of the token and tick all the boxes of 'User permissions'.Other things are not required.\nThen click 'Create token' and copy the token.\n")
    else:
        try:
           chatAI("ds", "reply 1 if you see this message,dont say an other things")
           break

        except:
          print("\nInvalid token\n")

while True:
    exercise = input("\n\n\nDo how many exercises:")
    try:
        exercise = int(exercise)
        if exercise > 0:
            break
        else:
            print("Invalid input")
    except:
        print("invalid input")

if input("\n\n\nEnable image-type reading passage scanning? 1: Yes , 2: No\n(Not suggested,this will use a lot of your tokens):") == "1":
    print("Image-type reading passage scanning is enabled now")
    useGemma = True
else:
    print("Image-type reading passage scanning is disabled now")

name = input("\n\n\nYour username:")
psw = input("\nYour password:")


def get_chromedriver_path():
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "chromedriver.exe")


driver_path = get_chromedriver_path()
service = Service(executable_path=driver_path)

browser = webdriver.Chrome(service=service)


browse("https://2025.wiseman.com.hk/en/")

#login
username = browser.find_element(By.ID,'username')
password = browser.find_element(By.ID,'password')
submit = browser.find_element(By.CLASS_NAME,"btn-submit")

username.send_keys(name)
password.send_keys(psw)

submit.click()

time.sleep(1)

excCount = 0
while excCount < exercise:
    excCount += 1
    browse("https://lms1.wiseman.com.hk/lms/user/secure/course/eb/select_lesson/")

    lessons = soup.find_all('tr')
    lesson_link = "https://lms1.wiseman.com.hk/lms/course/eb/lessons/"
    theme = ""
    title = ""
    type = ""

    #https://lms1.wiseman.com.hk/lms/course/eb/lessons/the_korean_wave/eb04_korea_the_place_to_visit_reading/
    #The Korean Wave
    #Korea – The Place to Visit - Reading
    count = 0
    for i in lessons:

        tds = i.find_all('td')

        if len(tds) > 3:
            if tds[3].find("i")["title"] != "Completed":

                theme = str(i.find_all('span')[3].text).replace(" ","_").lower()

                wholeTitle = i.find('a').text.split('-')

                #replace special characters
                title = "eb04_" + wholeTitle[0].replace(" – ","_").lower()
                title = title.replace(": ","_")
                title = title.replace("? ", "_")
                title = title.replace("?", "")
                title = title.replace(", ", "_")
                title = title.replace(" ", "_")

                type = wholeTitle[1].replace(" ","").lower()

                if(type in allowedTypes and not(title in blackList)):
                    lesson_link += theme + "/" + title + "_" + type
                    browser.find_element(By.LINK_TEXT,i.find("a").text).click()
                    break

        count += 1


    print("Finished searching lesson")

    time.sleep(5)

    browser.switch_to.frame(browser.find_element(By.XPATH,"//body//iframe"))

    browser.switch_to.frame(browser.find_element(By.XPATH,"//body//iframe"))

    if type == "reading":

        if len(browser.find_elements(By.XPATH,"(//body//label)[2]")) > 0:
            challengingBtn = browser.find_element(By.XPATH,"(//body//label)[2]")
            challengingBtn.click()

            startBtn = browser.find_element(By.XPATH,"//body//button")
            startBtn.click()

        #answering questions
        #scan text
        soupPage()
        passage = ""

        if len(soup.find_all("resource-vocabulary")) > 0:
            if useGemma:
                passageImg = soup.find("img",class_="c_entry-image ng-star-inserted")["src"]
                passage = chatAI("gemma","Find all the text contents in this picture, and compress it, making the text able to express all the important ideas in the passage with minimum words.Ignore stuffs that doesn't seem to belong to the passage(such as links of sources).It will be better if the result is less than 200 words.Don't say anything else unrelated to the passage, just tell me the compressed content.",passageImg)
            else:
                blackList.append(title)
                with open("blacklist.json", "w") as fi:
                    json.dump(blackList, fi)
                excCount -= 1
                continue
        else:
            for i in soup.find("resource-reading").find_all("entry"):
                passage += i.text + "   "
        print("Passage: " + passage)

        totalQ = len(soup.find("group-pagination").find_all("label", class_="c_pager c_pager-active ng-star-inserted") + soup.find("group-pagination").find_all("label", class_="c_pager ng-star-inserted"))
        while len(browser.find_elements(By.XPATH, "//*[@btn-text='Next Question']")) > 0:
            browser.find_element(By.XPATH, "//*[@btn-text='Next Question']").click()
            time.sleep(1)

        for i in range(totalQ):
            soupPage()

            isMc = len(browser.find_elements(By.XPATH,"//question-smc")) > 0
            isFillin = len(browser.find_elements(By.XPATH,"//question-fillin")) > 0

            mcIndex = 1
            fillinTexts = []

            if isMc:
                choices = soup.find("question-smc").find_all("div",class_="c_entry-text ng-star-inserted")
                questions = choices[0].text + "---Choices:"
                for i in range(1,len(choices)):
                    questions += str(i) + ":" + choices[i].text + ", "

                try:
                    mcIndex = int(chatAI("ds", dsRule + "Passage: " + passage + "------- Question:" + questions))
                except:
                    mcIndex = 1
                browser.find_element(By.XPATH,'(//question-smc//*[@class="c_entry-field ng-star-inserted"])[' + str(mcIndex) + "]").click()
            elif isFillin:
                fillins = soup.find("question-fillin").find_all("div", class_="c_entry-text ng-star-inserted")
                questions = fillins[0].text
                for j in range(1,len(fillins)):
                    questions += fillins[j].text.replace("&nbsp;", " ")
                    if j < len(fillins)-1:
                         questions += "___"

                fillinTexts = chatAI("ds", dsRule + "Passage: " + passage + "------- Question:" + questions).split(",")
                inputs = browser.find_elements(By.TAG_NAME,"input")

                while len(fillinTexts) < len(inputs):
                    fillinTexts.append("fuck")
                for j in range(len(inputs)):
                    inputs[j].send_keys(fillinTexts[j])
            '''
            else:
                if len(browser.find_elements(By.XPATH,'//question-polling')) > 0:
                    time.sleep(5000)
                    browser.find_element(By.XPATH,'//question-polling//*[@class="c_entry-field ng-star-inserted"]').click()
                else:
                    browser.find_element(By.XPATH, '//picture-polling//*[@class="c_entry-field ng-star-inserted"]').click()
            '''

            browser.find_element(By.XPATH, "//*[@btn-text='Submit']").click()
            if len(browser.find_elements(By.XPATH, "//*[@btn-text='Results']")) > 0:
                browser.find_element(By.XPATH, "//*[@btn-text='Results']").click()
            else:
                browser.find_element(By.XPATH, "//*[@btn-text='Next Question']").click()
    elif type == "writing" or type == "speaking":

        passage = ""

        soupPage()

        for i in soup.find("resource-reading").find_all("entry"):
            passage += i.text + "   "
        print("Passage: " + passage)

        totalQ = len(soup.find("group-pagination").find_all("label", class_="c_pager c_pager-active ng-star-inserted") + soup.find("group-pagination").find_all("label", class_="c_pager ng-star-inserted"))
        while len(browser.find_elements(By.XPATH, "//*[@btn-text='Next Question']")) > 0:
            browser.find_element(By.XPATH, "//*[@btn-text='Next Question']").click()
            time.sleep(1)

        for i in range(totalQ):
            soupPage()

            fillins = soup.find_all("div", class_="c_entry-text ng-star-inserted")
            questions = fillins[0].text
            for j in range(1,len(fillins)):
                questions += fillins[j].text.replace("&nbsp;", " ")
                if j < len(fillins)-1:
                     questions += "___"

            fillinTexts = chatAI("ds", dsRule + "Passage: " + passage + "------- Question:" + questions).split(",")
            inputs = browser.find_elements(By.TAG_NAME,"input")

            while len(fillinTexts) < len(inputs):
                fillinTexts.append("fuck")
            for j in range(len(inputs)):
                inputs[j].send_keys(fillinTexts[j])

            browser.find_element(By.XPATH, "//*[@btn-text='Submit']").click()
            if len(browser.find_elements(By.XPATH, "//*[@btn-text='Results']")) > 0:
                browser.find_element(By.XPATH, "//*[@btn-text='Results']").click()
            else:
                browser.find_element(By.XPATH, "//*[@btn-text='Next Question']").click()

    browser.switch_to.default_content()
    time.sleep(2)