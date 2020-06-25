import os
import requests
import threading
import time
from selenium import webdriver
import base64
import argparse

counter = 0
DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"


def download_image(image_url, name):
    global counter
    try:
        r = requests.get(image_url)
        with open(name, "wb") as f:
            f.write(r.content)
        print(f"Saved Image as:{name}, url:{image_url}")
        counter += 1
    except ValueError as e:
        try:
            image_url = image_url.strip("data:image/jpeg")
            img = base64.b64decode(image_url)
            with open(name, "wb") as f:
                f.write(img)
            print(f"Saved Image as:{name}, base64:{image_url}")
            counter += 1
        except:
            print(e, "ಠ_ಠ. Could not download image")

    except Exception as e:
        print(e, "ಠ_ಠ. Could not download image")


def get_links(keyword, num_of_images=50):
    global DRIVER_PATH
    wd = webdriver.Chrome(DRIVER_PATH)

    url = f"https://www.google.com/search?q={keyword}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjQuNTC_pbqAhXtnuAKHVFaC84Q_AUoAXoECB4QAw&biw=1920&bih=975"
    global counter

    def scroll():
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    keyword = "+".join(keyword.split(" "))

    path = f"./{keyword}_images"

    if not os.path.exists(path):
        os.makedirs(path)

    wd.get(url)

    while counter < num_of_images:
        scroll()
        images = wd.find_elements_by_css_selector("img.Q4LuWd")
        for image in images:
            download_image(image.get_attribute("src"), os.path.join(path, f"{keyword}{counter}.png"))
            if counter == num_of_images:
                break

    wd.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Images from Google for your dataset")
    parser.add_argument("-k", "--search_term", type=str, required=True, help="What you want images of")
    parser.add_argument("-N", "--num_of_images", type=int, help="How many images you want")
    args = parser.parse_args()

    if not args.search_term:
        parser.error("Please provide a search term")
    else:
        start = time.time()
        get_links(args.search_term, args.num_of_images)
        end = time.time()
        print(f"{args.num_of_images} images downloaded in {end - start} seconds.")