import time

if __name__ == "__main__":
    with open("../browser_path.txt", "r") as f:
        browser = f.readline().split("\\")[-1]
else:
    with open("browser_path.txt", "r") as f:
        browser = f.readline().split("\\")[-1]

if browser == "chrome.exe":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager

    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
   
elif browser == "msedge.exe":    
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager

    option = webdriver.EdgeOptions()
    # option.add_argument("--headless")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])

elif browser == "brave.exe":
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as BraveService
    from webdriver_manager.chrome import ChromeDriverManager

    option = webdriver.ChromeOptions()
    # option.add_argument("--headless")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    
elif browser == "firefox.exe":
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service as FirefoxService
    from webdriver_manager.firefox import GeckoDriverManager

    option = webdriver.FirefoxOptions()
    # option.add_argument("--headless")
    option.add_experimental_option("excludeSwitches", ["enable-logging"])
    
def instantiate_driver():
        if browser == "chrome.exe":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
        elif browser == "msedge.exe": 
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=option)
        elif browser == "brave.exe":
            driver = webdriver.Chrome(service=BraveService(ChromeDriverManager().install()), options=option)
        elif browser == "firefox.exe":
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=option)
        return driver

def start(link, interval, obj):
    driver = instantiate_driver()
    try:
        driver.get(link)
        if (driver.current_url != link):
            time.sleep(3)
            driver.get(link)
            obj.process_id = driver.service.process.pid
        while True:
            time.sleep(interval)
            driver.refresh()
    except BaseException as e:
        print(e)
        driver.quit()
        obj.error_stop()