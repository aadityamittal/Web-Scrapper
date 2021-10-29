import tkinter as tk                # python 3
from tkinter import font as tkfont

from selenium import webdriver

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("678x987")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage,  PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome To The App", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

       
        button2 = tk.Button(self, text="Linked In",
                            command=lambda: controller.show_frame("PageTwo"), padx=22)
        
        button2.pack(pady=23)




class PageTwo(tk.Frame):
# Main function 
    def getUser(self, ok):
        loginuser = self.textfield0.get()
        passd = self.textfield1.get()
        driver = webdriver.Chrome("<Chrome Driver Extension>>")
        user = self.textfield.get() 
        driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')
        username = driver.find_element_by_id('username')
        username.send_keys(loginuser)
        password = driver.find_element_by_id('password')
        password.send_keys(passd)
        sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
        sign_in_button.click()
        driver.get(f'https://www.linkedin.com/in/{user}/') #change profile_url here.
        try:
            name = driver.find_element_by_class_name('text-heading-xlarge').text
            abot = driver.find_element_by_xpath('//*[@id="ember44"]/div[2]/div[2]/div/div[2]').text
            self.mylist.delete ( 0, last=tk.END )
            self.mylist.insert(tk.END, f"Name:{name}")
            self.mylist.insert(tk.END, f"About:{abot}")
            driver.close()
        except Exception as e:
            self.mylist.insert("Try Again")
            driver.close()



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Type User Name", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        # Font
        t = ("Times", "24", "normal")
        #login using webdriver
        self.textfield0 = tk.Entry(self, justify = 'center',font = t)
        self.textfield0.pack(pady = 20)
        self.textfield0.focus()

        self.textfield1 = tk.Entry(self, justify = 'center',font = t)
        self.textfield1.pack(pady = 20)
        self.textfield1.focus()
        # For taking city input
        self.textfield = tk.Entry(self, justify = 'center',font = t)
        self.textfield.pack(pady = 20)
        self.textfield.focus()
        self.textfield.bind('<Return>', self.getUser)
        button1 = tk.Button(self, text="Check User")
        button1.bind('<Button-1>', self.getUser)
        button1.pack()
  
      # creating labels to display data

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        
        self.mylist = tk.Listbox(self, yscrollcommand = scrollbar.set)
        self.mylist.pack(expand=tk.TRUE,fill=tk.BOTH)
        scrollbar.config( command = self.mylist.yview ) 
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack() 


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
