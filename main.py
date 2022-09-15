from pytube import YouTube
import os
from pydub import AudioSegment
import requests
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.error import URLError
from soupsieve import SelectorSyntaxError

AudioSegment.converter =\
    r"C:\Users\ACER\Documents\PyCharm projects\new_no_ui_app\ffmpeg-5.1.1-essentials_build\bin\ffmpeg.exe"

username = input("What is your name? \n")
allowedUsers = {'Munir'}
allowedPassword = "1234"

if username in allowedUsers:
    password = input("Your Password \n")
    pr = [f"Welcome {username} !",
          "To the new no-ui multipurpose application.",
          "Please select an option:",
          "1. YouTube Downloader",
          "2. Convert files",
          "3. Scrape text in a blog or article on a website",
          ]

    options = [1, 2, 3]
    if password == allowedPassword:
        for i in pr:
            print(i)
        selectedOptions = int(input("Please select an option \n"))
        if selectedOptions not in options:
            for i in pr[2:]:
                print(i)
                pass
            selectedOptions = int(input("Select a valid option :( \n"))

        if selectedOptions == 1:
            try:
                yt = YouTube(str(input("Enter your YouTube link here \n")))
                path_shrt = input("Please insert a path to save your download \n")
                path_full = r'{}'.format(path_shrt)
            except (ConnectionResetError, URLError, RuntimeError):
                print("Something went wrong")
                yt = YouTube(str(input("Enter your YouTube link here \n")))
                path_shrt = input("Please insert a path to save your download \n")
                path_full = r'{}'.format(path_shrt)
            else:
                pass

            print("Audio or Video :)")
            aov = ["1. Audio", "2. Video"]
            do = [1, 2]
            for j in aov:
                print(j)
                pass
            displayOptions = int(input("Select an option \n"))
            if displayOptions not in do:
                for j in aov:
                    print(j)

                displayOptions = int(input("Select a valid option \n"))
            try:
                video = yt.streams.filter(only_audio=True).first()
                audio = video.download(output_path=path_full)
            except (ConnectionResetError, URLError, RuntimeError):
                print("Connection issues. Please check your internet and try again")

            if displayOptions == 1:
                try:
                    base, ext = os.path.splitext(audio)
                    new_audio = base + '.mp3'
                    os.rename(audio, new_audio)
                    print(yt.title + "has been downloaded :)")
                except (NameError, RuntimeError) as e:
                    print("Are you in Africa, cause this connections isn't just it")
                    pass
            elif displayOptions == 2:
                try:
                    video_hd = yt.streams.get_highest_resolution()
                    video_hd.download(path_full)
                    print(yt.title + "has been downloaded :)")
                except (NameError, RuntimeError):
                    print("You're having connection issues")
                    pass

        elif selectedOptions == 2:
            print("Available conversions:")
            conv = ["1. wav to mp3", "2. mp3 to wav"]
            conv_list = [1, 2]
            for c in conv:
                print(c)
            choice = int(input("Select an option \n"))
            if choice not in conv_list:
                for c in conv:
                    print(c)
                    pass
                choice = int(input("Select a valid option \n"))
            else:
                pass

            if choice == 1:
                source = input("Enter wav file path or file name if file in directory \n")
                destination = input("Enter destination file name \n")
                sound = AudioSegment.from_wav(source)
                sound.export(destination, format="mp3")
                print("converted successfully")
            elif choice == 2:
                source = input("Enter mp3 file path or file name if file in directory \n")
                destination = input("Enter file destination name \n")
                sound = AudioSegment.from_mp3(source)
                sound.export(destination, format="wav")
                print("converted successfully")
        elif selectedOptions == 3:
            print("Welcome to my scrapper")


            class Content:
                """
                Common base class for all articles/pages
                """

                def __init__(self, url, title, body):
                    self.url = url
                    self.title = title
                    self.body = body

                def print(self):
                    """
                    Flexible printing function controls output
                    """
                    p = ["URL: {}".format(self.url), "TITLE: {}".format(self.title), "BODY:\n{}".format(self.body)]
                    return p

            class Website:
                """
                Contains information about website structure
                """

                def __init__(self, name, url, title_tag, body_tag):
                    self.name = name
                    self.url = url
                    self.titleTag = title_tag
                    self.bodyTag = body_tag


            class Crawler:

                def get_page(self, url):
                    try:
                        req = requests.get(url)
                    except requests.exceptions.RequestException:
                        return None
                    return BeautifulSoup(req.text, 'html.parser')

                def safe_get(self, page_obj, selector):
                    """
                    Utility function used to get a content string from a Beautiful Soup object and a selector.
                    Returns an empty string if no object is found for the given selector
                    """
                    # noinspection SpellCheckingInspection
                    selected_elems = page_obj.select(selector)
                    if selected_elems is not None and len(selected_elems) > 0:
                        return '\n'.join(
                            [elem.get_text() for elem in selected_elems])
                    return ''

                def parse(self, site, url):
                    """
                    Extract content from a given page url
                    """
                    bs = self.get_page(url)
                    if bs is not None:
                        title = self.safe_get(bs, site.titleTag)
                        body = self.safe_get(bs, site.bodyTag)
                        if title != '' and body != '':
                            content = Content(url, title, body)
                            return content


            # here's the code that defines the website objects and kicks off the process:

            crawler = Crawler()
            site_data = []

            web_name = str(input("Enter the name of the website \n"))
            web_link = str(input("Enter the BASE link of the website \n"))
            t_tag = str(input("Enter the title tag of the webpage \n"))
            web_flow = str(input("Enter the tag and class that contains text to scrape \n"))
            full_link = str(input("Enter full link to webpage \n"))
            print("Save text to file in directory ?")
            save = int(input("1. Yes\n2. No \n"))
            if save == 1:
                try:
                    website = Website(web_name, web_link, t_tag, web_flow)
                    t = crawler.parse(website, full_link)
                    new = t.print()
                    f = open("Web_text.txt", "w")
                    for line in new:
                        f.write(line)
                    f.close()
                except (HTTPError, URLError, AttributeError, SelectorSyntaxError):
                    print("something went wrong :( Try again")
                    pass

            elif save == 2:
                try:
                    website = Website(web_name, web_link, t_tag, web_flow)
                    k = crawler.parse(website, full_link)
                    j = k.print()
                    for i in j:
                        print(i)
                except (HTTPError, URLError, AttributeError):
                    print("something went wrong :( Try again")
                    pass

    else:
        print("Password incorrect, please try again")
else:
    print("Name not found")
    print("Kindly change allowed name and password from script")
