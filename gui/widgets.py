import customtkinter as ctk
import os
import psutil
import threading
import time

class Header(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.grid_propagate(False)
            self.grid_columnconfigure(0, weight=1)
            
            self.title = ctk.CTkLabel(self, text="Webpage Autorefresh", text_color="white", font=ctk.CTkFont(family="Roboto", size=40), anchor="center")
            self.title.grid(pady=20)

            self.description = ctk.CTkLabel(self, text="Input a link and set the interval timer", text_color="white", font=ctk.CTkFont(family="Arial", size=24), anchor="center")
            self.description.grid()

class LinkItem(ctk.CTkFrame):
    def __init__(self, master, link, interval, height=45, width=480, **kwargs):
        super().__init__(master, height=height, width=width, **kwargs)
        self.grid_propagate(False)
        self.grid_columnconfigure((0,5), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.delete_button = ctk.CTkButton(self, text="X", fg_color="transparent", hover_color="gray", width=5, corner_radius=10, command=self.delete_link)
        self.delete_button.grid(column=1, row=0, padx=3)
        
        self.default_color = self.cget("fg_color")

        self.process_id = 0

        self.timer_value = 30
        self.interval_values = ["5 secs", "10 secs", "20 secs", "30 secs", "40 secs", "50 secs", 
                                "1 min", "5 mins", "10 mins", "30 mins", "45 mins", 
                                "1 hr", "2 hrs", "3 hrs"]
        self.interval_variable = ctk.StringVar()
        
        self.interval_menu = ctk.CTkOptionMenu(self, values=self.interval_values, variable=self.interval_variable, command=self.set_timer_interval, width=90)
        self.interval_menu.set(interval)
        self.interval_menu.grid(column=3, row=0, padx=3)
        self.prev_int_var = self.interval_variable.get()
        self.interval_variable.trace('w', self.update_interval)

        vcmd_link_text = (self.register(self.update_link), r'%P', r'%s')

        self.link_text = ctk.CTkEntry(self, width=280)
        self.link_text.grid(column=2, row=0, padx=3)
        
        self.start_btn = ctk.CTkButton(self, text="Go", width=45, command=self.set_running)
        self.start_btn.grid(column=4, row=0, padx=3)

        self.stop_btn = ctk.CTkButton(self, text="Stop", width=45, command=self.set_stop, fg_color="maroon")

        self.link_text.insert(0, "")
        self.link_text.insert(0, link)
        self.set_timer_interval(interval=interval)
        self.link_text.configure(validate='all', validatecommand=vcmd_link_text)

    def set_timer_interval(self, interval):
        interval = interval.split(" ")
        multiplier = interval[1]
        value = int(interval[0])
        if ("hr" in multiplier):
            value = value * 60 * 60
        elif ("min" in multiplier):
            value = value * 60

        self.timer_value = value
    
    def set_running(self):
        def start(self):
            self.configure(fg_color="green")
            self.start_btn.grid_forget()
            self.stop_btn.grid(column=4, row=0, padx=3)
            self.link_text.configure(state="readonly")
            self.interval_menu.configure(state="disabled")
            functions.main.start(self.link_text.get(), self.timer_value, self)
        thread = threading.Thread(target=lambda x=self:start(x), daemon=True)
        thread.start()
    
    def set_stop(self):
        def stop(self):
            self.configure(fg_color=self.default_color)
            self.stop_btn.grid_forget()
            self.start_btn.grid(column=4, row=0, padx=3)
            self.link_text.configure(state="normal")
            self.interval_menu.configure(state="normal")
            if (self.process_id != 0):
                parent = psutil.Process(self.process_id)
                for child in parent.children(recursive=True):
                    child.kill()
                parent.kill()
        thread = threading.Thread(target=lambda x=self:stop(x), daemon=True)
        thread.start()
    
    def error_stop(self):
        self.configure(fg_color="red")
        self.link_text.configure(state="readonly")
        self.interval_menu.configure(state="disabled")
        self.start_btn.grid_forget()
        self.stop_btn.grid(column=4, row=0, padx=3)

    def delete_link(self):
        to_delete = "@!@!@".join([self.link_text.get(), self.interval_variable.get()])
        with open("links.txt", "r") as read:
            links = [i.rstrip() for i in read.readlines()]
            links.remove(to_delete)
            with open("links.txt", "w") as write:
                write.writelines(link + "\n" for link in links)
        self.set_stop()
        self.destroy()

    def update_link(self, P, s):
        with open("links.txt", "r") as read:
            links = [i.rstrip() for i in read.readlines()]
        prev = "@!@!@".join([s, self.interval_variable.get()])
        links[links.index(prev)] = "@!@!@".join([P, self.interval_variable.get()])
        with open("links.txt", "w") as write:
            write.writelines(link + "\n" for link in links)
        return True
    
    def update_interval(self, *args):
        link = self.link_text.get()
        interval = self.interval_variable.get()
        with open("links.txt", "r") as read:
            links = [i.rstrip() for i in read.readlines()]
            prev = "@!@!@".join([link, self.prev_int_var])
            links[links.index(prev)] = "@!@!@".join([link, interval])
            with open("links.txt", "w") as write:
                write.writelines(link + "\n" for link in links)
        self.prev_int_var = interval


class LinksContainer(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.grid_propagate(False)
            self.grid_columnconfigure((0), weight=1)
            self.grid_rowconfigure((500), weight=1)

            self.container_body = ctk.CTkScrollableFrame(self, width=500, height=330)
            self.container_body.propagate(False)
            self.container_body.grid_columnconfigure((0), weight=1)
            self.container_body.grid(column=0, pady=10)

            self.add_btn = ctk.CTkButton(self, text="Add New Link", width=120, command=self.add_link)
            self.add_btn.grid(sticky='s', pady=7, row=500)
            
            self.init_links()
        
        def add_link(self):
            content = ["", "30 secs"]
            link_item = LinkItem(self.container_body, content[0], content[1])
            link_item.grid(pady=3)
            
            with open("links.txt", "a+") as f:
                f.write("@!@!@".join(content) + "\n")
        
        def init_links(self):
            with open("links.txt", "r") as f:
                items = [line.split(sep="@!@!@") for line in f.readlines()]
                for i in items:
                    link_item = LinkItem(self.container_body, i[0], i[1].rstrip())
                    link_item.grid(pady=3)
                # for item in self.container_body.winfo_children():
                #     item.set_running()
                #     time.sleep(10)

class GetBrowserWindow(ctk.CTkToplevel):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.title("Set Browser")
            self.screen_width = self.winfo_screenwidth()
            self.screen_height = self.winfo_screenheight()
            self.window_width = 300
            self.window_height = 150
            self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
            self.y_coordinate = int((self.screen_height/2) - (self.window_height/1.9))
            self.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
            self.grab_set()
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.bg_frame = ctk.CTkFrame(self, width=250, height=120)
            self.bg_frame.grid_propagate(False)
            self.bg_frame.grid_columnconfigure((0,3), weight=1)
            self.bg_frame.grid_rowconfigure((0,4), weight=1)
            self.bg_frame.grid()

            self.label = ctk.CTkLabel(self.bg_frame, text="Set your browser:")
            self.label.grid(columnspan=2, column=1, row=1, padx=3, pady=2)

            self.browser_var = ctk.StringVar()
            self.browser_exes = {"Chrome":"chrome.exe", 
                             "Brave":"brave.exe", 
                             "Edge":"msedge.exe", 
                             "Firefox":"firefox.exe"}
            self.browsers = list(self.browser_exes.keys())
            self.browser_menu = ctk.CTkOptionMenu(self.bg_frame, values=self.browsers, variable=self.browser_var, width=90)
            self.browser_menu.grid(column = 1, row=2, padx=4, pady=2)
            self.browser_var.set("Chrome")

            self.find_btn = ctk.CTkButton(self.bg_frame, text="Find", width=45, command=self.set_browser)
            self.find_btn.grid(column = 2, row=2, padx=4, pady=2)

            self.status_label = ctk.CTkLabel(self.bg_frame, text="")
            self.text_color = self.status_label.cget("text_color")
            self.status_label.grid(column = 1, columnspan=2, padx=4, pady=5)
        
        def set_browser(self):
            browser = self.browser_exes[self.browser_var.get()]
            tmp = self.find_files(browser, 'C:\\Program Files')
            if os.path.isfile(tmp):
                with open("browser_path.txt", 'w+') as browser_tmp:
                    browser_tmp.write(tmp)
                    self.status_label.configure(text=browser + " found!", text_color=self.text_color)
            else:
                tmp = self.find_files(browser, 'C:\\Program Files (x86)')
                if os.path.isfile(tmp):
                    with open("browser_path.txt", 'w+') as browser_tmp:
                        browser_tmp.write(tmp)
                        self.status_label.configure(text=browser + " found!", text_color=self.text_color)
                else:
                    with open("browser_path.txt", 'w+') as browser_tmp:
                        browser_tmp.write("")
                    self.status_label.configure(text=browser + " not found!\nTry with other browsers.", text_color="red")
        
        @staticmethod
        def find_files(filename, search_path):
            result = ''
            for root, dir, files in os.walk(search_path):
                if filename in files:
                    temp = os.path.join(root, filename)
                    if filename in temp.split('\\')[-1]:
                        result = temp
            return result

import functions.main
                     
                
