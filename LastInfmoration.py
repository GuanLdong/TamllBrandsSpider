from selenium import webdriver
import urllib.parse
import time
import datetime
import random
import time

#程序说明
print("-"*30,"*"*4,"-"*30)
print('程序说明'.center(61))
print(r'''【1】程序用来获取一个品牌在天猫中搜索的店铺信息
【2】建一个文本，在里面存放品牌名称，每行放一个
【3】按要求输入文本的名称，信息表格会保存在同层文件夹中''')
print("-"*30,"*"*4,"-"*30)

class Brands(object):
    def __init__(self,filename):
        # self.driver = webdriver.PhantomJS()
        self.Time = datetime.datetime.now()
        self.savename = "".join(list(map(str,[self.Time.year,self.Time.month,self.Time.day,self.Time.hour,self.Time.minute])))+".csv"
        with open(self.savename,"w") as f:
            f.write(",".join(["品牌","相关商品总数","相关店铺总数","店铺名称","店铺链接","店铺相关商品数"])+"\n")
        self.filename = filename

    
    def InitChrome():
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
    #    options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        prefs = {
            'profile.default_content_setting_values': {
            'images': 2
            }
        }
    #    options.add_argument('--headless') 
    #    options.add_argument('--proxy-server='+ip)

        options.add_experimental_option('prefs',prefs)
        browser = webdriver.Chrome(chrome_options=options)
        js =r"Object.defineProperty(navigator, 'webdriver', {get: () => undefined,});"

        browser.execute_script(js)
        return browser

    def getbrands(self):
        brandlist = []
        with open(self.filename,"r") as f:
            lines = f.readlines()
        for each in lines:
            if len(each.strip()) > 1:
                brandlist.append(each.strip())
        print("成功读取{}个品牌,开始爬取天猫搜索信息...".format(len(brandlist)))
        return brandlist

    def getstores(driver,brand):
        # 将品牌转码成url格式
        str_p = urllib.parse.quote(brand,encoding="utf-8")
        url = "https://list.tmall.com/search_product.htm?q={}&sort=s&style=g#J_Filter".format(str_p)
        time.sleep(random.randint(5,10))
        driver.get(url)
        time.sleep(random.randint(4,8))
        driver.implicitly_wait(10)
        # 获取相关商品总数
        product_num = self.driver.find_element_by_css_selector(".j_ResultsNumber > span").text.strip()
        # 点击店铺按钮，切换到店铺信息展示页面
        driver.find_element_by_css_selector("#J_Filter > a.fType-w").click()
        time.sleep(random.randint(4,8))
        driver.implicitly_wait(10)
        # 获取店铺总数
        store_num = driver.find_element_by_css_selector(".j_ResultsNumber > span").text
        # 获取总页数
        pages = int(driver.find_element_by_class_name("ui-page-s-len").text.strip().split("/")[-1])
        while pages:
            time.sleep(random.randint(4,8))
            self.driver.implicitly_wait(10)
            try:
                stores = driver.find_elements_by_class_name("j_ShopBox")
                for each in stores:
                    # 店铺名称
                    storename = each.find_element_by_css_selector("div.shopHeader > div.shopHeader-info > a").text
                    # 店铺链接
                    storelink = each.find_element_by_css_selector("div.shopHeader > div.shopHeader-enter > a.sHe-shop").get_attribute("href")
                    # 相关商品数
                    products = each.find_element_by_css_selector("a.sHe-product.j_MoreProduct > em").text
                    the_list = list(map(str,[brand,product_num,store_num,storename,storelink,products]))
                    print("品牌：{} \t店铺总数{} \t相关商品数{} \t店铺名称:{}".format(brand,store_num,products,storename))
                    with open(self.savename,"a") as f:
                        f.write(",".join(the_list)+"\n")
            except Exception as e:
                print(e)
            # 点击下一页
            time.sleep(random.randint(4,8))
            driver.find_element_by_class_name("ui-page-next").click()
            pages -= 1
        
    
        
    def main(self):
        brandlist = self.getbrands()
        for i in brandlist:
            driver = self.InitChrome()
            try:
                self.getstores(driver,i)
                time.sleep(random.randint(4,8))
            except:
                print("品牌【{}】无法搜索到信息".format(i))
            driver.close()

if __name__ == '__main__':
    filename = input("请输入品牌文件名称（含后缀）：")
    start = time.time()
    brands = Brands(filename)
    brands.main()
    end = time.time()
    print("运行结束，耗时%0.2f秒" %(float(end-start)))
    k = input("按任意键退出程序")
