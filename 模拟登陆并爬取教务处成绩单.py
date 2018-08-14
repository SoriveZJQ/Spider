import xlrd
from selenium import webdriver
from pyquery import PyQuery as pq
import pymongo


# 导入学生信息
data = xlrd.open_workbook('学生信息表.xls')
table = data.sheets()[1]
names = table.col_values(0)
names.pop(0)
names.pop(0)
n = len(names)
accounts = table.col_values(1)
accounts.pop(0)
accounts.pop(0)
passwords = table.col_values(5)
passwords.pop(0)
passwords.pop(0)


login_url = 'http://202.115.133.173:805/Default.aspx'
score_url = 'http://202.115.133.173:805/SearchInfo/Score/ScoreList.aspx'
TERM_INIT = '201702'


# 采用headless模式
options = webdriver.FirefoxOptions()
options.add_argument('--headless')


# 遍历每个学生，爬取成绩
def get_score():
    for i in range(n):
        driver = webdriver.Firefox(firefox_options=options)
        account = accounts[i]
        password = passwords[i]
        driver.get(login_url)
        input_account = driver.find_element_by_name('txtUser')
        input_password = driver.find_element_by_name('txtPWD')
        button = driver.find_element_by_class_name('btn_login')
        input_account.send_keys(account)
        input_password.send_keys(password)
        button.click()
        driver.get(score_url)
        html = driver.page_source
        doc = pq(html)
        score = {}
        score['姓名'] = names[i]
        courses = doc('.score_right_infor_list.listUl')
        courses = courses.children()
        for item in courses.items():
            term = item.children('.floatDiv20').text().strip()
            if term == TERM_INIT:
                title = item.find('div:nth-child(3)').text().strip()
                cj = item.find('div:nth-child(6)').text().strip()
                score[title] = cj
        driver.close()
        yield score


# 保存到MongoDB
MONGO_URL = 'localhost'
MONGO_DB = 'score'
MONGO_COLLECTION = 'xinguan2017_2'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def save_to_mongo(score):
    try:
        if db[MONGO_COLLECTION].insert(score):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')



if __name__ == '__main__':
    for item in get_score():
        save_to_mongo(item)
