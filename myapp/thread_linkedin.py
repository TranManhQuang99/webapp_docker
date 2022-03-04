from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from random import randint
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from  selenium.webdriver.common.by import By

from pymongo import MongoClient, collation
import re
import threading
import time
class myDataCrawler(threading.Thread):
    
    def set_key_word(self, kw):
        self.key_word = kw

    def set_number(self, nb):
        self.number = nb

    def get_current_att(self):
        print(f"key: {self.key_word}, number: {self.number}")
        
    def __init__(self):

        threading.Thread.__init__(self)
        self.service = Service("/home/nguyen/Downloads/chromedriver")  
        self.key_word = ""
        self.number = 0
        self.browser = webdriver.Chrome(service=self.service)
        pass
        
    def run(self):
        if (self.key_word == "" or self.number == 0):
            pass
        else:
            print ("Starting " + self.key_word)
            self.Twitter(self.key_word, self.number)

            self.linkedin(self.key_word, self.number)
            print ("Exiting " + self.key_word)
        
    def stop(self):
        self.browser.close()
        
    def Twitter(self,key_word, number):
        self.browser.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        self.login_linkdin()
        self.search_linkdin(key_word)

    def linkedin(self,key_word, number):
        self.browser.get("https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        self.login_linkedin()
        self.search_linkedin(key_word)
        self.get_url_profile()
        self.get_url_all_page(number)
        self.crawl_data_json(key_word, number)
        

    def login_linkedin(self):
        try:
            credential = open('/home/nguyen/Minh/Python/webapp/login.txt')
            line = credential.readlines()
            username = line[0]
            password = line[1]
            # import user name
            email_field = self.browser.find_element(By.ID,'username')
            email_field.send_keys(username)
            sleep(randint(1,3))
            # import password
            password_login = self.browser.find_element(By.ID,'password')
            password_login.send_keys(password)
            sleep(randint(1,3))
            #key in ueser name
            login_field = self.browser.find_element(By.XPATH,"/html/body/div/main/div[2]/div[1]/form/div[3]/button")
            login_field.click()
            sleep(2)
        except:
            print("ban code ngu")

    def search_linkedin(self,key_word):
        x= self.browser.find_element(By.CLASS_NAME,'global-nav__content')
        x.click()
        sleep(2)
        click_findkey = self.browser.find_element(By.XPATH,'//*[@id="global-nav-search"]/div/button')
        click_findkey.click()
        sleep(3)
        search_line =self.browser.find_element(By.XPATH,'//*[@id="global-nav-typeahead"]/input')
        sleep(2)
        search_line.send_keys(key_word)
        sleep(3)
        search_line.send_keys(Keys.RETURN)
        sleep(4)
        jobs = self.browser.find_element(By.CLASS_NAME,'artdeco-pill')
        jobs.click()
        sleep(2)

    def get_url_profile(self):
        page_source = BeautifulSoup(self.browser.page_source, "html.parser")
        profiles_company = page_source.find_all('a',
                                                class_='disabled ember-view job-card-container__link job-card-list__title')
        all_profiles_company = []
        for profiles in profiles_company:
            profiles_company_id = profiles.get('href')
            Number = re.findall('\d+', profiles_company_id)
            ID = Number[0]
            profiles_url = 'https://www.linkedin.com/jobs/view/' + ID
            if profiles_url not in all_profiles_company:
                all_profiles_company.append(profiles_url)
        return all_profiles_company

    def get_url_all_page(self,number):
        url_all_page = []
        for i in range(int(number)):
            url_one_page =  self.get_url_profile()
            self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(2)
            try:
                next_button = self.browser.find_element(By.XPATH,f'//*[@aria-label="Page {i+1}"]')
                next_button.click()
                sleep(3)
            except:
                pass
            for i in url_one_page:
                if i not in url_all_page:
                    url_all_page.append(i)

            sleep(2)

        return url_all_page

    def crawl_data_json(self,key_word,number):
        STT = 0
        url_all_page = self.get_url_all_page(int(number))
        for linkdin_url in url_all_page:
            STT += 1
            self.browser.get(linkdin_url)

        for linkedin_url in url_all_page:
            STT += 1
            self.browser.get(linkedin_url)
            sleep(1)
            try:
                see_more = self.browser.find_element(By.CLASS_NAME, 'artdeco-card__action')
                sleep(1)
            except:
                continue
            see_more.click()
            sleep(2)
            page_source_company = BeautifulSoup(self.browser.page_source, "html.parser")
            info_div = page_source_company.find('div', class_="p5")
            try:
                name_job = info_div.find('h1').get_text().strip()
            except:
                name_job = '////'



            name_company = info_div.find('div', class_="mt2")
            try:
                company = name_company.find('a').get_text().strip()
            except:
                info_loc = name_company.find_all('span')
                company = info_loc[0].find('span').get_text().strip()

            try:
                location = name_company.find('span', class_='jobs-unified-top-card__bullet').get_text().strip()
            except:
                location = '////'
            try:
                content = page_source_company.find('div', class_='jobs-box__html-content').get_text().strip()
            except:
                continue

            Number = re.findall('\d+', linkdin_url)
            Number = re.findall('\d+', linkedin_url)
            ID = Number[0]



            my_details = {
                'Social_Network':'Linkedin',
                'Id': ID,
                'Key_word': key_word,
                'Names': company,
                'Link_post': linkdin_url,
                'Link_post': linkedin_url,
                'post': content,
                'comment': None,
                'device': None,
                'location': location,
                'Job_title': name_job,
                'time': None


            }
            print(my_details)
            cluster = MongoClient(
                "mongodb+srv://minh15599:123456asdf@cluster0.wkj8v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = cluster['123a']
            collection = db['myapp_employee']

            collection.insert_one(my_details)

def main():
    
    cluster = MongoClient(
    "mongodb+srv://minh15599:123456asdf@cluster0.wkj8v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = cluster['123a']
    collection = db['data']
    Kv = list(collection.find({},{ "Data":1,"_id":0}))
    Kv1 = list(collection.find({},{ "Number":1,"_id":0}))
    cs = []
    ts = []
    while (1):
        for i in range(3):
            cs.append(myDataCrawler())
            ts.append(threading.Thread(target=cs[i].run))
            for v in Kv:
                print(v["Data"])
            input_Data = v["Data"]
            cs[i].set_key_word(input_Data)
            for n in Kv1:
                print(n["Number"])
            input_Number = int(n["Number"])
            cs[i].set_number(input_Number)

            print("Du lieu cua ban: ")
            cs[i].get_current_att()

            for j in ts: 
                j.start()
        
        for c in cs:
            c.stop()
        for t in ts:
            t.join()
        pass

if __name__ == "__main__":
    main()

            # cluster = MongoClient(
            #     "mongodb+srv://minh15599:123456asdf@cluster0.wkj8v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            # db = cluster['123a']
            # collection = db['data']

            # collection.insert_one(my_details)

def main():
    cs = []
    ts = []
    while (1):
        command = str(input("Nhap lenh bat dau: "))
        if command == "start":
            for i in range(4):
                cs.append(myDataCrawler())
                ts.append(threading.Thread(target=cs[i].run))

                command = str(input("Nhap data muon crawl: "))
                cs[i].set_key_word(command)

                command = str(input("Nhap number muon crawl: "))
                cs[i].set_number(command)

                print("Du lieu cua ban: ")
                cs[i].get_current_att()

                command = str(input("START?"))
                if command == "y":
                    for i in ts:
                        if not i.is_alive():
                            i.start()
                else:
                    pass
                pass

        elif command == "stop":
            print("Ket thuc chuong trinh")
            for c in cs:
                c.stop()
            for t in ts:
                t.join()
            pass

        elif command == "pause":
            print("Tam dung chuong trinh")
            for t in ts:
                time.sleep(10)
        # Create new threads
    # thread1 = myDataCrawler("ETL dev",   3)
    # thread2 = myDataCrawler("data analyst",  3)
    # thread3 = myDataCrawler("BI dev",  3) 
    # thread4 = myDataCrawler("deep learning",  3)
    # thread1.start()
    # thread2.start()
    # thread3.start()
    # thread4.start()
    # threads = []
    # threads.append(thread1)
    # threads.append(thread2)
    # threads.append(thread3)
    # threads.append(thread4)
    # for t in threads:
    #     t.join()
    # print ("Exiting Main Thread")
    
if __name__ == '__main__':
    main()
    













































