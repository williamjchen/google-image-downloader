import os
import requests
import threading
import time
from selenium import webdriver
import argparse

counter = 0
DRIVER_PATH = "C:\Program Files (x86)\chromedriver.exe"


def download_image(image_url, name):
    global counter
    try:
        r = requests.get(image_url)
        with open(name, "wb") as f:
            f.write(r.content)
        print(f"Saved Image at:{name}, url:{image_url}")
        counter += 1
    except Exception as e:
        print("ಠ_ಠ. Could not download image", e)


def get_links(keyword, num_of_images=50):
    global DRIVER_PATH
    wd = webdriver.Chrome(DRIVER_PATH)

    url = f"https://www.google.com/search?q={keyword}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjQuNTC_pbqAhXtnuAKHVFaC84Q_AUoAXoECB4QAw&biw=1920&bih=975"
    global counter

    def scroll():
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    keyword = "+".join(keyword.split(" "))

    path = f".\{keyword}_images"

    if not os.path.exists(path):
        os.makedirs(path)

    wd.get(url)

    while counter < num_of_images:
        scroll()
        time.sleep(1)
        images = wd.find_elements_by_css_selector("img.Q4LuWd")
        for image in images:
            try:
                image.click()
            except Exception as e:
                continue
            time.sleep(0.5)
            print("made it")
            actual_images = wd.find_elements_by_css_selector("img.n3VNCb")

            for actual_image in actual_images:
                if "http" in actual_image.get_attribute("src"):
                    download_image(actual_image.get_attribute("src"), os.path.join(path, f"{keyword}{counter+1}.png"))
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
        print("hello")
        get_links(args.search_term, args.num_of_images)
        end = time.time()
        print(f"{args.num_of_images} images downloaded in {end - start} seconds.")