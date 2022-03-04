import threading
import time
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from  selenium.webdriver.common.by import By
from pymongo import MongoClient
import re

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
            print ("Exiting " + self.key_word)

    def stop(self):
        self.browser.close()

    def Twitter(self,key_word, number):
        self.browser.get("https://twitter.com/i/flow/login")
        self.login_twitter()
        self.search(key_word)
        self.get_all_links(number)
        self.get_comment_replies(number)
        self.crawl_data_twitter(key_word, number)

    def login_twitter(self):
        try:

            click_deteth = self.browser.find_element(By.XPATH, "//html").click()
            time.sleep(5)
            email_login = self.browser.find_element(By.CLASS_NAME, "r-z2wwpe")
            # email_login = self.browser.find_element_by_name("username")
            email_login.send_keys("armi1xx11@gmail.com")
            sleep(5)
            email_login.send_keys(Keys.RETURN)
            sleep(5)


            # witter
            click_deteth = self.browser.find_element(By.XPATH, "//html").click()
            username_login = self.browser.find_element_by_name("text")
            sleep(5)
            username_login.send_keys("Quangdzvcl")
            username_login.send_keys(Keys.RETURN)
            sleep(5)


            click_deteth = self.browser.find_element(By.XPATH, "//html").click()
            password_login = self.browser.find_element(By.CLASS_NAME, "r-1ets6dv")
            # password_login = self.browser.find_element_by_name("password")
            password_login.send_keys("Quangtran12341@")
            password_login.send_keys(Keys.RETURN)
            sleep(5)
        except:
            print ("YOU code ngu")

    def search(self,key_word):

        self.browser.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]').click()
        sleep(5)
        search_keyword = self.browser.find_element(By.CLASS_NAME,"r-1dqbpge")
        search_keyword.send_keys(key_word)
        search_keyword.send_keys(Keys.RETURN)
        sleep(5)

    def get_all_links(self,number):
        all_url_post = []
        for i in range(int(number)):
            self.browser.execute_script(f'window.scrollTo(0,{i + 1}*1080)')
            sleep(5)
            page_source = BeautifulSoup(self.browser.page_source, "html.parser")
            post2 = page_source.find_all('a',
                                        class_='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-t2kpel r-1ny4l3l r-1udh08x r-ymttw5 r-1vvnge1 r-o7ynqc r-6416eg')
            post3 = page_source.find_all('a',
                                        class_='css-4rbku5 css-18t94o4 css-901oao r-9ilb82 r-1loqt21 r-1q142lx r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0')
            sleep(5)
            post_all = post2 + post3
            for url_post in post_all:
                link_url = url_post.get("href")
                link_url_full = 'https://twitter.com' + link_url
                if link_url_full not in all_url_post:
                    all_url_post.append(link_url_full)
        return all_url_post

    def get_comment_replies(self,number):
        name_replies = []
        name_list_replies = []
        comment_replies = []
        comment_list_replies = []
        name_and_comment = []
        for i in range(int(number)):
            self.browser.execute_script(f'window.scrollTo(0,{i}*1080)')
            page_source_twiter = BeautifulSoup(self.browser.page_source, "html.parser")

            info_div = page_source_twiter.find('div', class_="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l")
            info_div2 = page_source_twiter.find_all('article',
                                                    class_='css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg')

            if info_div2:            # check bài viết có cmt không nếu không có thì sang bài viết khác

                info_div3 = page_source_twiter.find_all('article',
                                                        class_='css-1dbjc4n r-1loqt21 r-18u37iz r-1ut4w64 r-1ny4l3l r-1udh08x r-1qhn6m8 r-i023vh r-o7ynqc r-6416eg')
                info_div4 = info_div2 + info_div3       # cộng 2 info div vào vì comment và replies cmt là 2 thẻ div khác nhau

                for i in info_div4:
                    try:
                        name_replies = i.find('div',
                                            class_='css-901oao css-bfa6kz r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0').get_text().strip()
                        name_list_replies.append(name_replies)
                    except:
                        name_replies = None
                    try:

                        comment_replies = i.find('div',
                                                class_='css-901oao r-1fmj7o5 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0').get_text().strip()
                        comment_list_replies.append(comment_replies)
                    except:
                        comment_replies = None
                    name_and_comment_replies = map(lambda x, y: x + str(':') + y, name_list_replies, comment_list_replies)    # map tên người cmt và nội dung cmt

                    for i in name_and_comment_replies:
                        if i not in name_and_comment:
                            name_and_comment.append(i)
                sleep(5)
            else:
                break
        return name_and_comment

    def crawl_data_twitter(self, key_word, number):
        STT = 0
        all_url_post = self.get_all_links(int(number))
        for link in all_url_post:
            STT +=1
            self.browser.get(link)
            sleep(2)
            page_source_twiter = BeautifulSoup(self.browser.page_source, "html.parser")
            info_div = page_source_twiter.find('div', class_="css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l")
            info_div2 = page_source_twiter.find('div', class_='css-1dbjc4n r-j5o65s r-qklmqi r-1adg3ll r-1ny4l3l')


            # get name
            try:
                name = info_div.find('span', class_="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0").get_text().strip()
            except:
                name = "None"
            # get content
            try:
                try:
                    post = info_div.find('div',
                                    class_='r-1s2bzr4').get_text().strip()
                except:
                    continue
            except :
                post = info_div2.find('div',
                                    class_='r-1s2bzr4').get_text().strip()
            #get device
            try:
                device = info_div2.find('a',
                                    class_='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-1loqt21 r-poiln3 r-bcqeeo r-1jeg54m r-qvutc0').get_text().strip()
            except:
                device = info_div2.find('a',
                                        class_='css-4rbku5 css-18t94o4 css-901oao css-16my406 r-9ilb82 r-1loqt21 r-poiln3 r-bcqeeo r-1jeg54m r-qvutc0').get_text().strip()
            #get time

            try:
                time_class = info_div.find('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wtj0ep')
                info_loc = time_class.find_all('span')
                time = info_loc[0].get_text()

            except:
                time_class = info_div2.find('div', class_='css-1dbjc4n r-1awozwy r-18u37iz r-1wtj0ep')
                info_loc = time_class.find_all('span')
                time = info_loc[0].get_text()

            #get comment
            try:
                name_and_comment = self.get_comment_replies()
            except:
                name_and_comment = "None"

            Number = re.findall('\d+', link)
            for i in Number:
                if len(i) >=16:
                    ID = i


            my_details = {
                'Social_Network' :'Twitter',
                'Id':ID,
                'Key_word':key_word,
                'Names': name,
                'Link_post': link,
                'post': post,
                'comment': name_and_comment,
                'device': device,
                'location': None,
                'Job_title': None,
                'time': time
            }
            print(my_details)
            # cluster = MongoClient(
            #     "103.226.248.168:27017")
            # db = cluster['123a']
            # collection = db['myapp_employee']

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
    # thread1 = myDataCrawler("ETL dev", 3)
    # thread2 = myDataCrawler("data analyst", 3)
    # thread1.start()
    # thread2.start()
    # threads = []
    # threads.append(thread1)
    # threads.append(thread2)
    # for t in threads:
    #     t.join()
    # print ("Exiting Main Thread")


if __name__ == "__main__":
    main()


