import requests
from urllib.parse import urlparse

def download_image(url, save_path="downloaded_image.jpg"):
    try:
        # 定义自定义的请求头，包括用户代理（User-Agent）和cookie
        headers = {
            'User-Agent': 'Your_Custom_User_Agent',
            'Cookie': 'your_cookie_key=your_cookie_value',
        }

        # 创建一个会话（session）以在多个请求之间保持cookie
        with requests.Session() as session:
            # 发送初始请求以获取cookie
            response = session.get(url, headers=headers)
            response.raise_for_status()

            # 发送实际请求以下载图片
            response = session.get(url, headers=headers)
            response.raise_for_status()

            # 写入文件
            with open(save_path, "wb") as file:
                file.write(response.content)

            print(f"图片下载成功。保存在：{save_path}")
    except requests.exceptions.RequestException as e:
        print(f"图片下载失败。错误信息：{e}")

if __name__ == "__main__":
    image_url = "https://i0.hdslb.com/bfs/archive/2931060b97fa7e51d2a49d69de47a66494e9ffe4.jpg@672w_378h_1c_!web-home-common-cover"
    filename = urlparse(image_url).path.split("/")[-1]  # 从URL中提取文件名
    download_image(image_url, filename+".jpg")
