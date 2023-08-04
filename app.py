import customtkinter as ctk
from gui.widgets import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Webpage Autorefresh")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 700
        self.window_height = 600
        self.x_coordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_coordinate = int((self.screen_height/2) - (self.window_height/1.9))
        self.geometry(f"{self.window_width}x{self.window_height}+{self.x_coordinate}+{self.y_coordinate}")
        self.grid_columnconfigure(0, weight=1)

        self.header = Header(master=self, width = 550, height = 150)
        self.header.grid(pady=(10, 5))
        self.links_container = LinksContainer(self, width = 550, height = 400)
        self.links_container.grid(pady=5)
        self.get_browser()
        
    def get_browser(self):
        with open("browser_path.txt", "r") as f:
            if not os.path.isfile(f.readline()):
                    GetBrowserWindow(self)



if __name__ == "__main__":
    app = App()
    app.mainloop()
