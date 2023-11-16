import requests
import pprint
import os

file = '快手视频\\'
if not os.path.exists(file):
    os.mkdir(file)

ID = input("请输入用户ID")

# 递归函数
# 我自己调用我自己
# 找出口 本身无限循环 1000 报错 可以 解决底层  no_more
# 当我执行到最后一个数据包的时候 就跳出循环
def get_page(pcursor):
    """
    def 定义一个函数的关键字
    :param pcursor: 函数要传递参数 形参
    :return: 函数返回值
    """
    url = 'https://www.kuaishou.com/graphql'
    # 手动构建请求参数 字典
    # data 关键字传递参数 提交的字典
    # json 关键字传递参数 提交的字符串
    json = {
        'operationName': "visionProfilePhotoList",
        'query': "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
        'variables': {'userId': ID, 'pcursor': pcursor, 'page': "detail", 'webPageArea': "profilexxnull"}
    }

    # 反爬 服务器识别了我们身份 爬虫程序 不给数据
    # 伪装 python代码 伪装 成浏览器用户
    headers = {
        # 用户身份 异步 要携带cookie 不会给你重复的数据
        'Cookie': 'kpf=PC_WEB; clientid=3; did=web_c94bf90320cc5c566243d36fe8eb9936; userId=3073169111; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABM10rpYrIOVlreE6WHqqr81UCB-gy7OFYmZU5K_3iZnmtghDmIZitYYnr1FNhPA7Ptr5O4bg9nrMS5L5cEGwY0xNaV09M_lXbp0OwGPmdizlHHkVErDp37QDiU9Vxt7o__rzc4G4oyIldD9Dsn3zfuanL47OoGgPXf64cTwd6rQyZCGtaJsuMFbLu6Lwh1XKU7EfHjx8-dH_WP7BKFj_8QBoSBmjJ_SI5Snf4O3WXJiYJKm0lIiCPIkfKn3zRdIwiHFoVhQRZsrz_nDExwcF5q7DAwwdYRigFMAE; kuaishou.server.web_ph=e50c2f7d30510100fd230baff67fce6fc63b; kpn=KUAISHOU_VISION',
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Pragma': 'no-cache',
        'Referer': 'https://www.kuaishou.com/short-video/3x8f9bryquyewck?authorId=3xbr4c2b9mfy8f6&streamSource=profile&area=profilexxnull',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    response = requests.post(url=url, json=json, headers=headers)
    # <Response [200]>  响应体对象
    # print(response.text)
    json_data = response.json()
    # pprint.pprint(json_data['data']['visionProfilePhotoList']['feeds'])
    feeds = json_data['data']['visionProfilePhotoList']['feeds']
    # pprint.pprint(json_data)
    pcursor = json_data['data']['visionProfilePhotoList']['pcursor']
    # print(pcursor)
    # 遍历列表 通过循环方式 把列表里面数据 一条一条的拿出来
    num = 1
    for feed in feeds:
        # pprint.pprint(feed)
        caption = feed['photo']['caption']
        photoUrl = feed['photo']['photoUrl']
        # print(caption, photoUrl)

        video = requests.get(url=photoUrl).content
        with open(file + str(num) + '_' + caption + '.mp4', mode='wb') as f:
            f.write(video)
            print(caption, '-->已保存')
        num += 1
    # 先指定函数的出口
    if pcursor == 'no_more':
        return None  # 返回的是空值 可写可不写
    # 自己调用自己
    get_page(pcursor)


# 运行代码
get_page("")
