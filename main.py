import tkinter as tk                # python 3
from tkinter import font as tkfont
from tkinter.constants import LEFT, TOP  # python 3
import requests
import time
from bs4 import BeautifulSoup as bs

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
        for F in (StartPage, PageOne, PageTwo):
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

        button1 = tk.Button(self, text="Check Weather",
                            command=lambda: controller.show_frame("PageOne"), padx=11)
        button2 = tk.Button(self, text="Check News",
                            command=lambda: controller.show_frame("PageTwo"), padx=22)
        button1.pack(pady=23)
        button2.pack(pady=23)


class PageOne(tk.Frame):
    def getWeather(self, ok):
        city = self.textfield.get() 
        api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=bbbb83567a6bf30776f041d977987f19"
        json_data = requests.get(api).json()

        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise'] - 21600))
        sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset'] - 21600))
        
        final_info = condition + "\n" + str(temp)+"C"
        final_data = "\n"+  "Max Temp: "+ str(max_temp)+"\n" + "Min temp: "+ str(min_temp)+"\n"+"Pressure: "+str(pressure)+"\n"+ "Humidity: "+ str(humidity)+"\n"+"Wind Speed: "+str(wind)+"\nSunrise: "+str(sunrise)+"\nSunset: "+str(sunset)

        self.label1.config(text = final_info)
        self.label2.config(text = final_data)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Enter any city", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        # Font
        f = ("poppins", 15, "bold")
        t = ("poppins", 35, "bold")

        # For taking city input
        self.textfield = tk.Entry(self, justify = 'center',font = t)
        self.textfield.pack(pady = 20)
        self.textfield.focus()

        self.textfield.bind('<Return>', self.getWeather)
        button = tk.Button(self, text="Check Weather")
        button.bind('<Button-1>', self.getWeather)
        
        button.pack()
        # creating labels to display data
        self.label1 = tk.Label(self, font = t)
        self.label1.pack()
        self.label2 = tk.Label(self, font = f)
        self.label2.pack()
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        
        button.pack(pady=28)


class PageTwo(tk.Frame):
# Main function 
    def getNews(self,canvas):
        self.mylist.delete ( 0, last=tk.END )
        city = self.textfield.get() 
        city += '-news'
        api = 'https://www.ndtv.com/' + city
        page = requests.get(api)
        if page.status_code == 404:
            page = requests.get('https://www.ndtv.com/others-news')
        soup = bs(page.content, 'html.parser')
        items = soup.find_all('div', class_='news_Itm')
        output = ""
        i = 0
        for news in items:
            heading = news.find('h2', class_='newsHdng')
            if heading != None:
                heading = heading.find('a').text
                output = "Heading: "+heading.strip()+"\n"
                self.mylist.insert(tk.END, output)

            postedBy = news.find('span', class_='posted-by')
            if postedBy != None:
                postedBy = postedBy.text
                output = "Posted by: "+postedBy.strip()+"\n"
                self.mylist.insert(tk.END, output)

            content = news.find('p', class_='newsCont')
            if content != None:
                content = content.text
                output = "About: " + content.strip() + "\n\n\n"
                self.mylist.insert(tk.END, output)
                self.mylist.insert(tk.END, "\n")
                self.mylist.insert(tk.END, "\n")
                self.mylist.insert(tk.END, "\n")

            i = i+1;
            if(i > 100):
                break;
            

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Type City Name(Used Web Scrapping Here)", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        # Font
        f = ("poppins", 15, "bold")
        t = ("poppins", 35, "bold")

        # For taking city input
        self.textfield = tk.Entry(self, justify = 'center',font = t)
        self.textfield.pack(pady = 20)
        self.textfield.focus()
        self.textfield.bind('<Return>', self.getNews)
        button1 = tk.Button(self, text="Check News")
        button1.bind('<Button-1>', self.getNews)
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