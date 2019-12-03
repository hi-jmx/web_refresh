
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
import time
import re
driver = webdriver.Chrome()
"""

web.visit('http://10.1.1.133')
print(browser.title)
browser.find_by_name('loginName').fill('jmx')
browser.find_by_name('password').fill('admin123')

browser.find_by_id('goHome').click()

print(browser.title + browser.url)

"""

#browser.visit('http://s.5173.com/dnf-xptjnl-4qsi30-xk1ly2-0-bx1xiv-0-0-0-a-a-a-a-a-0-0-0-0.shtml')
driver.get('http://s.5173.com/dnf-0-4qsi30-xk1ly2-0-bx1xiv-0-0-0-a-a-a-a-a-0-0-0-0.shtml')
driver.maximize_window()
#头部登录
driver.find_element_by_id('J_GlobalTop').click()

print(driver.title)

driver.find_element_by_name('userName').send_keys('18560021760')
driver.find_element_by_name('password').send_keys('gyshjmx')

myUrl = input('input url:')


driver.get(myUrl.strip())
startIndex = driver.page_source.find('拍卖交易')
endIndex = driver.page_source.find('</div>', startIndex)
targetUrl = driver.page_source[startIndex:endIndex]

money_m = re.search('<li><b>1元=(.*?)</b>', targetUrl)
print(money_m.group(1))

url_m = re.search('<li class="btn_box"><a class="btnlink_o_s_small" href="(.*?)" ', targetUrl)
print(url_m.group(1)),

if url_m.group(1).count('&amp;'):
    driver.get(url_m.group(1).replace('&amp;', '&'))
else:
    driver.get(url_m.group(1))

try:
    try:
        s = driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$ddlGameArea')
    except:
        s = driver.find_element_by_name('SelectedAreaId')
    if s:
        Select(s).select_by_visible_text('山东区')

    try:
        s_S = driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$ddlGameServer')
    except:
        s_S = driver.find_element_by_name('SelectedServerId')
    if s_S:
        Select(s_S).select_by_visible_text('山东1区')

    try:
        driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$txtGameRole').send_keys('jmx')
    except:
        driver.find_element_by_name('yReNewRole').send_keys('jmx')

    try:
        driver.find_element_by_name('PurchaseOrderNew1$BuyerGameRoleInfo1$txtGameRoleValidate').send_keys('jmx')
    except:
        driver.find_element_by_name('txtReOldRole').send_keys('jmx')
except:
    print('----------------------++-------------------------')
    driver.find_element_by_id('BuyerGameRoleInfo_rbExistGameRole_0').click()

print('------------------------------------------------')
try:
    driver.find_element_by_name('PurchaseOrderNew1$txtRoleGrade').send_keys('1')
except:
    driver.find_element_by_name('txtReceivingRole').send_keys('1')
# 选择客服
driver.find_element_by_xpath('(//*[@id="kf_list"]/li)[last()]').click()

driver.find_element_by_id('PurchaseOrderNew1_rdNoPostSale').click()
driver.find_element_by_id('PurchaseOrderNew1_txtBuyerQQ').send_keys('908768892')

# driver.find_element_by_id('PurchaseOrderNew1_btnCreateOrder').submit()
driver.find_element_by_id('lbtnCreateOrder').click()



