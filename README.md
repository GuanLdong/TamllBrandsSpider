

# 天猫网络爬虫\IP池\更改浏览器webdriver参数

本项目通过解析天猫超市首页JSON文件，获取天猫上所有产品的一二级类目（天猫首页左侧菜单栏以及其弹框菜单）。之后通过selenium控制浏览器爬取二级类目下所有推荐品牌（通过搜索获得），最后抓取所有推荐品牌的详情（包括品牌店铺数推荐产品等），也即如下步骤：

- 获取首页JSON解析得到一二级目录
- 获取二级目录下的推荐品牌
- 抓取推荐品牌的相关店铺、推荐商品

第一至第三个ipynb文件表示了以上所述三步。

使用前晴运行0.*开头的文件以初始化环境。

## 包依赖

- selenium
- webdriver
- mitmproxy
- urllib3
- redis

其中redis是用来实现 IP池，mitmproxy是用来实现天猫登录操作的；但IP池+账号登录的方法在最后使用的过程中没有用到，所以这两个包不安装也可以。