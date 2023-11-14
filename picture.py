import requests

image_url = "https://i0.hdslb.com/bfs/archive/2931060b97fa7e51d2a49d69de47a66494e9ffe4.jpg@672w_378h_1c_!web-home-common-cover"
response = requests.get(image_url)

if response.status_code == 200:
    with open("downloaded_image.jpg", "wb") as file:
        file.write(response.content)
    print("Image downloaded successfully.")
else:
    print(f"Failed to download image. Status code: {response.status_code}")
