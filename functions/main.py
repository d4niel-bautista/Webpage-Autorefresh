import time
from selenium import webdriver
from datetime import datetime

class RefreshBotInstance():
    def __init__(self):
        self.running = False
        self.set_stop = False
    
    def get_browser(self):
        with open("browser_path.txt", "r") as f:
            browser = f.readline().split("\\")[-1]
            return browser
    
    def set_service(self, browser):
        if browser == "chrome.exe":
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager

            option = webdriver.ChromeOptions()
            option.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.service = ChromeService(ChromeDriverManager.install())
            self.option = option
        elif browser == "msedge.exe":
            from selenium.webdriver.edge.service import Service as EdgeService
            from webdriver_manager.microsoft import EdgeChromiumDriverManager

            option = webdriver.EdgeOptions()
            option.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.service = EdgeService(EdgeChromiumDriverManager().install())
            self.option = option
        elif browser == "brave.exe":
            from selenium.webdriver.chrome.service import Service as BraveService
            from webdriver_manager.chrome import ChromeDriverManager

            option = webdriver.ChromeOptions()
            option.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.service = BraveService(ChromeDriverManager().install())
            self.option = option
        elif browser == "firefox.exe":
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager

            option = webdriver.FirefoxOptions()
            option.add_experimental_option("excludeSwitches", ["enable-logging"])
            self.service = FirefoxService(GeckoDriverManager().install())
            self.option = option
    
    def instantiate_driver(self):
        browser = self.get_browser()
        self.set_service(browser=browser)
        if browser == "chrome.exe":
            driver = webdriver.Chrome(service=self.service, options=self.option)
        elif browser == "msedge.exe": 
            driver = webdriver.Edge(service=self.service, options=self.option)
        elif browser == "brave.exe":
            driver = webdriver.Chrome(service=self.service, options=self.option)
        elif browser == "firefox.exe":
            driver = webdriver.Firefox(service=self.service, options=self.option)
        return driver

    def start(self, link, interval, obj):
        try:
            self.running = True
            self.set_stop = False
            driver = self.instantiate_driver()
        
            driver.get(link)
            if (driver.current_url != link):
                time.sleep(3)
                try:
                    with open("creds.txt") as f:
                        creds = [i.rstrip() for i in f.readlines()]
                    id = driver.find_element("xpath", "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input")
                    id.send_keys(creds[0])
                    pwd = driver.find_element("xpath", "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input")
                    pwd.send_keys(creds[1])
                    login = driver.find_element("xpath", "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[3]/input")
                    login.click()
                    driver.get(link)
                except Exception as e:
                    print(e)
                    driver.get(link)
                obj.process_id = driver.service.process.pid
            while not self.set_stop:
                time.sleep(interval)
                driver.refresh()
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                with open('logs.txt', 'a+') as f:
                    f.write('RELOADED AT ' + dt_string + '\n' + link + " @" + str(interval) + " seconds" + '\n\n')
            try:
                driver.quit()
                obj.set_stop()
                self.running = False
                obj.start_btn.configure(state='normal')
            except:
                obj.set_stop()
                self.running = False
                obj.start_btn.configure(state='normal')
        except Exception as e:
            print("error here", e)
            driver.quit()
            self.running = False
            obj.error_stop()
            obj.start_btn.configure(state='normal')

# if __name__ == "__main__":
#     with open("../browser_path.txt", "r") as f:
#         browser = f.readline().split("\\")[-1]
# else:
#     with open("browser_path.txt", "r") as f:
#         browser = f.readline().split("\\")[-1]

# if browser == "chrome.exe":
#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service as ChromeService
#     from webdriver_manager.chrome import ChromeDriverManager

#     option = webdriver.ChromeOptions()
#     # option.add_argument("--headless")
#     option.add_experimental_option("excludeSwitches", ["enable-logging"])
   
# elif browser == "msedge.exe":    
#     from selenium import webdriver
#     from selenium.webdriver.edge.service import Service as EdgeService
#     from webdriver_manager.microsoft import EdgeChromiumDriverManager

#     option = webdriver.EdgeOptions()
#     # option.add_argument("--headless")
#     option.add_experimental_option("excludeSwitches", ["enable-logging"])

# elif browser == "brave.exe":
#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service as BraveService
#     from webdriver_manager.chrome import ChromeDriverManager

#     option = webdriver.ChromeOptions()
#     # option.add_argument("--headless")
#     option.add_experimental_option("excludeSwitches", ["enable-logging"])
    
# elif browser == "firefox.exe":
#     from selenium import webdriver
#     from selenium.webdriver.firefox.service import Service as FirefoxService
#     from webdriver_manager.firefox import GeckoDriverManager

#     option = webdriver.FirefoxOptions()
#     # option.add_argument("--headless")
#     option.add_experimental_option("excludeSwitches", ["enable-logging"])
    
# def instantiate_driver():
#         if browser == "chrome.exe":
#             driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=option)
#         elif browser == "msedge.exe": 
#             driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=option)
#         elif browser == "brave.exe":
#             driver = webdriver.Chrome(service=BraveService(ChromeDriverManager().install()), options=option)
#         elif browser == "firefox.exe":
#             driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=option)
#         return driver

# def start(link, interval, obj):
#     driver = instantiate_driver()
#     try:
#         driver.get(link)
#         if (driver.current_url != link):
#             time.sleep(3)
#             try:
#                 with open("creds.txt") as f:
#                     creds = [i.rstrip() for i in f.readlines()]
#                 id = driver.find_element("xpath", "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[2]/input")
#                 id.send_keys(creds[0])
#                 pwd = driver.find_element("xpath", "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input")
#                 pwd.send_keys(creds[1])
#                 login = driver.find_element("xpath", "/html/body/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[1]/td[3]/input")
#                 login.click()
#                 driver.get(link)
#             except Exception as e:
#                 print(e)
#                 driver.get(link)
#             obj.process_id = driver.service.process.pid
#         while True:
#             time.sleep(interval)
#             driver.refresh()
#     except Exception as e:
#         print(e)
#         driver.quit()
#         obj.error_stop()