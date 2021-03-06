from selenium import webdriver
from selenium.webdriver.support.select import Select
import re
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
        self.tag_url = ''
        self.s_role = ''

    def login(self, url, user_name, pswd):
        self.web_driver.get(url)
        self.web_driver.find_element_by_id('J_GlobalTop').click()
        self.web_driver.find_element_by_name('userName').send_keys(user_name)
        self.web_driver.find_element_by_name('password').send_keys(pswd)

    def find_item(self, url, number):
        self.web_driver.get(url)
        # / html / body / div[4] / div[2] / div[4] / div[3] / div[2] / div / a[1]
        # /html/body/div[4]/div[2]/div[4]/div[3]/div[2]/div/a[4]/span
        # /html/body/div[4]/div[2]/div[4]/div[3]/div[2]/div/a[4]
        startIndex = self.web_driver.page_source.find('拍卖交易')
        if -1 == startIndex:
            print('go the next page')
            self.web_driver.get(url.replace('0.shtml', '2.shtml'))
            startIndex = self.web_driver.page_source.find('拍卖交易')
        endIndex = self.web_driver.page_source.find('</div>', startIndex)
        targetUrl = self.web_driver.page_source[startIndex:endIndex]

        print(targetUrl)
        try:
            money_m = re.search('<li><b>1元=(.*?)</b>', targetUrl).group(1)
            url_m = re.search('<li class="btn_box"><a class="btnlink_o_s_small" href="(.*?)" ', targetUrl).group(1)
        except:
            print('find money or url may error!')

            return

        print('price:{}'.format(money_m))
        print('url:{}'.format(url_m))
        print('number:{}'.format(number))
        if float(money_m) > float(number):
            self.tag_url = url_m.replace('&amp;', '&')
        else:
            self.tag_url = ''

    def check(self, target_url):
        self.web_driver.get(target_url)
        try:
            self.web_driver.switch_to_alert().accept()
            return True
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
        try:
            s = self.web_driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$ddlGameArea')
        except:
            s = self.web_driver.find_element_by_name('SelectedAreaId')
        if s:
            Select(s).select_by_visible_text(area)
            print('area s is find')
            return True
        else:
            print('area s is not find ')
            return False

    def fill_server(self, server):
        try:
            s_S = self.web_driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$ddlGameServer')
        except:
            s_S = self.web_driver.find_element_by_name('SelectedServerId')
        if s_S:
            Select(s_S).select_by_visible_text(server)
            return True
        else:
            return False

    def fill_name(self, name):
        try:
            s_name = self.web_driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$txtGameRole')
        except:
            s_name = self.web_driver.find_element_by_name('yReNewRole')
        if s_name:
            self.web_driver.send_keys(name)
            return True
        else:
            return False

    def fill_name2(self, name):
        try:
            s_name2 = self.web_driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$txtGameRoleValidate')
        except:
            s_name2 = self.web_driver.find_element_by_name('txtReOldRole')
        if s_name2:
            s_name2.send_keys(name)
            return True
        else:
            return False

    def fill_qq(self, qq):
        try:
            s_qq = self.web_driver.find_element_by_id('PurchaseOrderNew1_txtBuyerQQ')
        except:
            print('qq:may something error!')
            s_qq = self.web_driver.find_element_by_id('txtQq')
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


    def fill_info(self, target_url, area, server, name, qq):
        if self.check(target_url):
            return False
        # try:
        #     if self.fill_area(area):
        #         self.fill_server(server)
        #         self.fill_name(name)
        #         self.fill_name2(name)
        #         self.fill_role()
        #
        #
        # except:
        #     #driver.find_element_by_id('BuyerGameRoleInfo_rbExistGameRole_0').click()
        #     print('try find BuyerGameRoleInfo_rbExistGameRole_0!')
        #     # s_role = self.web_driver.find_element_by_id('BuyerGameRoleInfo_rbExistGameRole_0')
        #     if self.find_role():
        #         self.s_role.click
        #
        #         #assert(True)
        #         # print('may some error!')
        #         # return False
        try:
            self.fill_role()
        except:
            pass
        # 选择客服
        self.web_driver.find_element_by_xpath('(//*[@id="kf_list"]/li)[last()]').click()
        try:
            self.web_driver.find_element_by_id('PurchaseOrderNew1_rdNoPostSale').click()
        except:
            self.web_driver.find_element_by_id('rdbtnOffPostSaleIndemnity').click()
        self.fill_qq(qq)
        try:
            self.web_driver.find_element_by_id('lbtnCreateOrder').click()
        except:
            self.web_driver.find_element_by_id('linkOk').click()
        return True

    def handle(self, url, number, area, server, name, qq):
        while True:
            self.find_item(url, number)
            if self.tag_url:
                print('find it!')
                if self.fill_info(parser.tag_url, area, server, name, qq):
                    # 提醒
                    playsound('1.mp3')
                    self.tag_url = ''
                    self.s_role = ''
                    break
                else:
                    continue


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
#parser.handle(my_url, number, area, server, name, qq)




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
