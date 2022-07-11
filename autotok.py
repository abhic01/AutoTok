from selenium.webdriver import Firefox, FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from markdown import markdown
from time import sleep
from moviepy.editor import *
import pyttsx3, praw, random, os

# DECLARING VARIABLES
timeout = 10
text = {}

# MARKDOWN TO TEXT
def markdown_to_text(md):
    html = markdown(md)
    #return ''.join(BeautifulSoup(html,features='html.parser').findAll(text=True))
    return BeautifulSoup(html,features='html.parser').get_text()

# REDDIT INSTANCE FOR PRAW TO HELP US SCRAPE
r = praw.Reddit(username="abhigotbars",
                     password="abhiMANI123",
                     client_id="****",
                     client_secret="****",
                     user_agent="tokbot"
                     )

# FIREFOX DRIVER
opts = FirefoxOptions()
opts.add_argument("--headless")
opts.set_preference("dom.push.enabled", False)  # kill notification popup
drv = Firefox(executable_path='D:/Downloads/example data/geckodriver.exe', options=opts)

# LOGGING INTO REDDIT
def login():
    drv.get("https://www.reddit.com/login")
    user = drv.find_element(By.ID, "loginUsername")
    user.send_keys("abhigotbars")
    pwd = drv.find_element(By.ID, "loginPassword")
    pwd.send_keys("abhiMANI123")
    btn = drv.find_element(By.CSS_SELECTOR, "button[type='submit']")
    btn.click()
    sleep(timeout)
login()

# SCRAPING THROUGH POST
for post in r.subreddit("AskReddit").top(time_filter="hour", limit=1):
    cmts = "https://www.reddit.com" + post.permalink
    drv.get(cmts)

    # SCRAPING ACTUAL POST
    text[0] = post.title

    try:
        cmt = WebDriverWait(drv, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Post')))
    except TimeoutException:
        print("Page load timed out...")
    else:
        cmt.screenshot("D:/Downloads/example data/ss/screenshots/comment#0.png")

    # SCRAPING TOP 10 COMMENTS FROM THE POST
    count = 1
    for comment in post.comments:
        id = f"t1_{comment.id}"
        try:
            cmt = WebDriverWait(drv, timeout).until(
                    lambda x: x.find_element(By.ID, id))
        except TimeoutException:
            print("Page load timed out...")
        else:
            if count > 10:
                break
            text[count] = markdown_to_text(comment.body_html)
            cmt.screenshot(f"D:/Downloads/example data/ss/screenshots/comment#{count}.png")
            count += 1

# TTS
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)
#engine.setProperty('rate', 180)
for i in range(11):
    engine.save_to_file(text[i], f"D:/Downloads/example data/ss/tts/comment#{i}.mp3")
    engine.runAndWait()

# CREATING THE FINAL VIDEO
resolution = (1080,1920)

def render(name):
    # Create clip 'flow'
    flow = []
    for i in range(11):
        if os.path.exists(f'D:/Downloads/example data/ss/tts/comment#{i}.mp3'):
            flow.append(str(i))

    # Load all the clips
    image_clips = []
    sound_clips = []
    duration = 0
    for part in flow:
        sound_clips.append(AudioFileClip(f"D:/Downloads/example data/ss/tts/comment#{part}.mp3"))
        if sound_clips[-1].duration > 20:
            sound_clips.pop()
            continue
        image_clips.append(ImageClip(f"D:/Downloads/example data/ss/screenshots/comment#{part}.png",duration=sound_clips[-1].duration).fx(vfx.resize,width=resolution[0]*0.9).set_position(("center","center")))
        duration += sound_clips[-1].duration
        # Ensure length of video
        if duration > 60:
            break

    # Combine all the clips into one
    image_clips = concatenate_videoclips(image_clips).set_position(("center","center"))
    sound_clips = concatenate_audioclips(sound_clips)

    # 3 minute limit
    if sound_clips.duration > 60*2.9:
        return False

    #Loading background
    background_clip = f"D:/Downloads/example data/ss/background/#{random.randint(1, 4)}.mp4"
    background = VideoFileClip(background_clip).fx(vfx.resize, height=resolution[1]).fx(vfx.loop, duration=image_clips.duration).set_position(("center","center"))
    
    # Composite all the components
    composite = CompositeVideoClip([background,image_clips],resolution)
    composite.audio = sound_clips
    composite.duration = sound_clips.duration

    # Render
    composite.write_videofile(f'D:/Downloads/example data/ss/render/{name}.mp4',threads=4,fps=30)
    return True

render("test")
