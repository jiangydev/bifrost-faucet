import clipboard

from selenium import webdriver


def generate_bnc(url):
    browser = webdriver.Chrome(executable_path='C:\迅雷下载\chromedriver_win32\chromedriver')
    browser.get(url)
    # 宽度不能太小，会影响按钮的点击
    browser.maximize_window()

    # 循环生成地址
    for i in range(50):
        # 点击'添加账户'
        add_account_ele = browser.find_element_by_css_selector(
            '#root > div.apps--Wrapper.theme--default.Apps-sc-1153uyw-0.kupRCq > div.Content-sc-1lmz432-0.kWZvYr > main > div.Accounts-mp0ofd-0.jLuSnm > div.ui--Button-Group.Group-sc-16hevwk-0.bIEgqG > button:nth-child(1)')
        add_account_ele.click()

        # 点击'助记词'
        secret_option_ele = browser.find_element_by_css_selector(
            'body > div.ui.page.modals.dimmer.transition.visible.active > div > div.content > div:nth-child(3) > div:nth-child(1) > div > div > div > div.ui.buttons > div')
        secret_option_ele.click()

        # 点击'原始种子'
        secret_seed_ele = browser.find_element_by_css_selector(
            'body > div.ui.page.modals.dimmer.transition.visible.active > div > div.content > div:nth-child(3) > div:nth-child(1) > div > div > div > div.ui.buttons > div > div.visible.menu.transition > div:nth-child(2)')
        secret_seed_ele.click()

        # 点击种子复制按钮
        secret_seed_copy_btn = browser.find_element_by_css_selector(
            'body > div.ui.page.modals.dimmer.transition.visible.active > div > div.content > div:nth-child(3) > div:nth-child(1) > div > div > div > div.CopyButton-bmxo6f-0.QRLBT.copyMoved > div > span > button')
        secret_seed_copy_btn.click()
        bnc_secret = clipboard.paste()

        # 点击bnc地址复制按钮
        bnc_address_copy_btn = browser.find_element_by_css_selector(
            'body > div.ui.page.modals.dimmer.transition.visible.active > div > div.content > div:nth-child(1) > div > div > div.ui--Row-base > div.ui--Row-icon > div')
        bnc_address_copy_btn.click()
        bnc_address = clipboard.paste()

        # 点击'取消'
        cancel_ele = browser.find_element_by_css_selector(
            'body > div.ui.page.modals.dimmer.transition.visible.active > div > div.actions > div > button:nth-child(1)')
        cancel_ele.click()

        # 追加模式写入文件
        with open('./bnc_gen.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{bnc_address},{bnc_secret}\n')



if __name__ == '__main__':
    url = 'https://dash.bifrost.finance/#/accounts'
    generate_bnc(url)
