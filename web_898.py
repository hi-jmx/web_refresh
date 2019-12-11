from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import re
import time
from playsound import playsound
from configparser import ConfigParser
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from selenium.common.exceptions import NoSuchElementException


class My_driver:
    """
    Parse web and fill info
    """
    def __init__(self, web_driver):
        self.web_driver = web_driver
        self.targetUrl = ''
        self.s_role = ''
        self.value = 1
        self.startIndex = -1
        self.endIndex = -1

    def login(self, url, user_name, pswd):
        self.web_driver.get(url)
        self.web_driver.find_element_by_xpath('/html/body/form/div[3]/div[1]/div[1]/div/ul[1]/li/p/span[1]/a').click()
        self.web_driver.find_element_by_name('UserName').send_keys(user_name)
        self.web_driver.find_element_by_name('PassWord').send_keys(pswd)
        self.web_driver.find_element_by_id('btn_login').click()
        time.sleep(2)

    def find_item(self, url, number):
        # self.web_driver.send_keys(Keys.ESCAPE)
        handles = self.web_driver.window_handles
        self.web_driver.switch_to.window(handles[0])
        self.web_driver.get(url)
        # / html / body / div[4] / div[2] / div[4] / div[3] / div[2] / div / a[1]
        # /html/body/div[4]/div[2]/div[4]/div[3]/div[2]/div/a[4]/span
        # /html/body/div[4]/div[2]/div[4]/div[3]/div[2]/div/a[4]
        # s = WebDriverWait(self.web_driver, 10).until(lambda x: x.find_element_by_name("divCommodityLst"))
        web_string = self.web_driver.page_source
        self.startInde = web_string.find('【拍卖交易】')
        print('start:{}'.format(web_string[0:self.startInde+200]))
        if -1 == self.startInde:
            print('startIndex:{}'.format(self.startInde))
            self.startInde = web_string.find('【拍卖交易】')
        self.endIndex = web_string.find('立即购买</a>', self.startInde)
        print('start:{} end:{}'.format(self.startInde, self.endIndex))
        self.targetUrl = web_string[self.startInde:self.endIndex]

        print(self.targetUrl)
        try:
            money_m = re.search('<span>1元=(.*?)万金</span>', self.targetUrl).group(1)
        except:
            print('find money or url may error!')
            print(web_string)

            return

        print('price:{}'.format(money_m))
        print('number:{}'.format(number))
        if float(money_m) > float(number):
            print('money_m > number')
            # /html/body/form/div[3]/div[2]/div[5]/div[4]/div[15]/div[4]/div[4]/div[5]/ul[2]/li[4]/a
            # self.web_driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div[5]/div[4]/div[15]/div[4]/div[4]/div[5]/ul[1]/li[4]/a').click()
            self.web_driver.find_element_by_css_selector('.sp_li1 > a').click()

            return True
        else:
            print('money_m <= number')
            return False

    def check(self):
        # self.web_driver.get(target_url)
        try:
            # self.web_driver.switch_to_alert().accept()
            pass
            return False
        except:
            pass
        try:
            self.web_driver.find_element_by_id('divNotBuy')
            print('can not bug')
            return True
        # except NoSuchElementException:
        #     self.web_driver.find_element_by_id('linkCreateOrder').click
        #     return False
        except NoSuchElementException:
            return False

    def fill_area(self, area):
        # 切换界面
        handles = self.web_driver.window_handles
        print(handles)
        self.web_driver.switch_to.window(handles[1])
        s = WebDriverWait(self.web_driver, 10).until(lambda x: x.find_element_by_name("ddlRoleArea"))
        if s:
            Select(s).select_by_visible_text(area)
            print('area s is find')
            return True
        else:
            print('area s is not find ')
            return False

    def fill_server(self, server):
        try:
            s_S = self.web_driver.find_element_by_name('selRoleServer')
        except:
            # s_S = self.web_driver.find_element_by_name('SelectedServerId')
            pass
        if s_S:
            Select(s_S).select_by_visible_text(server)
            return True
        else:
            return False

    def fill_name(self, name):
        try:
            s_name = self.web_driver.find_element_by_name('txtGameAccount').send_keys(name)
        except:
            # s_name = self.web_driver.find_element_by_name('yReNewRole')
            pass
        # if s_name:
        #     self.web_driver.send_keys(name)
        #     return True
        # else:
        #     return False

    def fill_name2(self, name):
        try:
            s_name2 = self.web_driver.find_element_by_name('txtGameAccountR').send_keys(name)
        except:
            # s_name2 = self.web_driver.find_element_by_name('txtReOldRole')
            pass

    def fill_qq(self, qq):
        try:
            s_qq = self.web_driver.find_element_by_id('PurchaseOrderNew1_txtBuyerQQ')
        except:
            print('qq:may something error!')
            s_qq = self.web_driver.find_element_by_id('txtQQ')
        if s_qq:
            s_qq.send_keys(qq)
            return True
        else:
            return False

    def fill_role(self):
        try:
            self.web_driver.find_element_by_name('PurchaseOrderNew1$txtRoleGrade').send_keys('1')
        except:
            self.web_driver.find_element_by_name('txtReceivingRole').send_keys('1')

    def find_role(self):
        # /html/body/form/div[2]/div[2]/div[3]/div[2]/div[1]/div[7]/div/p[1]/input
        try:
            s_role = self.web_driver.find_element_by_xpath('/html/body/form/div[2]/div[2]/div[3]/div[2]/div[1]/div[7]/div/p[1]/input')
        except:
            # / html / body / form / div[3] / div[2] / div[2] / div[1] / div[5] / div / p[1] / input
            s_role = self.web_driver.find_element_by_id('rdNewGameId0')
        if s_role:
            self.s_role = s_role
            return True
        return False


    def fill_info(self, area, server, name, qq):
        if self.check():
            return False

        self.fill_area(area)
        self.fill_server(server)
        self.fill_name(name)
        self.fill_name2(name)
                # self.fill_role()


        # except:
        #     #driver.find_element_by_id('BuyerGameRoleInfo_rbExistGameRole_0').click()
        #     print('try find BuyerGameRoleInfo_rbExistGameRole_0!')
        #     # s_role = self.web_driver.find_element_by_id('BuyerGameRoleInfo_rbExistGameRole_0')
        #     if self.find_role():
        #         self.s_role.click

                #assert(True)
                # print('may some error!')
                # return False
        # try:
        #     self.fill_role()
        # except:
        #     pass
        # 选择客服
        # self.web_driver.find_element_by_xpath('(//*[@id="kf_list"]/li)[last()]').click()
        # try:
        #     self.web_driver.find_element_by_id('PurchaseOrderNew1_rdNoPostSale').click()
        # except:
        #     self.web_driver.find_element_by_id('rdbtnOffPostSaleIndemnity').click()
        self.fill_qq(qq)
        try:
            self.web_driver.find_element_by_id('btnSubmit').click()
        except:
            self.web_driver.find_element_by_id('linkOk').click()
        return True

    def handle(self, url, number, area, server, name, qq):
        handles = self.web_driver.window_handles
        print(handles)
        if len(handles) == 3:
            self.web_driver.switch_to.window(handles[2])
            self.web_driver.close()
            self.web_driver.switch_to.window(handles[1])
            self.web_driver.close()
        elif len(handles) == 2:
            self.web_driver.close()
        while True:
            if self.find_item(url, number):
                print('find it!')
                if self.fill_info(area, server, name, qq):
                    # 提醒
                    self.web_driver.find_element_by_xpath('/html/body/form/div[13]/li/button').click()
                    playsound('1.mp3')
                    self.targetUrl = ''
                    self.s_role = ''
                    self.value = 2
                    self.startIndex = -1
                    self.endIndex = -1
                    break

    def handler_adaptor(self, fun, my_url, number, area, server, name, qq):
        return lambda event: fun(my_url, number, area, server, name, qq)

CONFIGFILL = 'cfg.txt'
config = ConfigParser()
config.read(CONFIGFILL, encoding='utf-8')

my_url = config['config'].get('my_url')
my_user = config['config'].get('my_user')
my_pswd = config['config'].get('my_pswd')
number = config['config'].get('number')
area = config['config'].get('area')
server = config['config'].get('server')
name = config['config'].get('name')
qq = config['config'].get('qq')

driver = webdriver.Chrome()
parser = My_driver(driver)

top = Tk()
contents = ScrolledText()
contents.pack(side=BOTTOM, expand=True, fill=BOTH)
btn = Button(text='Go on')
btn.pack(side=RIGHT)

btn.bind('<Button-1>', func=parser.handler_adaptor(parser.handle, my_url, number, area, server, name, qq))
parser.login(my_url, my_user, my_pswd)
#开始
#my_string = input('input url:')




    # parser.find_item(my_url, number)
    #
    # if parser.tag_url:
    #     print('find it!')
    #     if parser.fill_info(parser.tag_url, area, server, name, qq):
    #         #提醒
    #         playsound('1.mp3')
    #         my_string = input('input url:')
    #         #继续

mainloop()
