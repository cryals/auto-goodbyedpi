import psutil
import pygetwindow as gw
import time
import subprocess
import os
import json
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# Загрузка конфигурации из config.json
with open('config.json', 'r') as f:
    config = json.load(f)

goodbyedpi_path = config["goodbyedpi_path"]

goodbyedpi_process = None
delay_before_closing = 30  # задержка перед закрытием в секундах
youtube_last_seen = 0

# Создаем иконки для трея
def create_image(color):
    image = Image.new('RGB', (64, 64), color)
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill=color)
    return image

icon_active = create_image("green")
icon_inactive = create_image("red")

def is_youtube_open():
    windows = gw.getAllWindows()
    youtube_keywords = ['youtube', 'youtube.com', 'YouTube']

    for window in windows:
        title = window.title.lower()
        if any(keyword in title for keyword in youtube_keywords):
            return True
    return False

def start_goodbyedpi():
    global goodbyedpi_process
    if goodbyedpi_process is None:
        goodbyedpi_process = subprocess.Popen([goodbyedpi_path])
        icon.icon = icon_active
        print("goodbyedpi.exe запущен")

def stop_goodbyedpi():
    global goodbyedpi_process
    if goodbyedpi_process:
        goodbyedpi_process.terminate()
        goodbyedpi_process = None
        icon.icon = icon_inactive
        print("goodbyedpi.exe закрыт")

def on_quit(icon, item):
    stop_goodbyedpi()
    icon.stop()

icon = Icon("GoodbyeDPI", icon_inactive, menu=Menu(MenuItem("Quit", on_quit)))

def run():
    try:
        icon.run_detached()
        while True:
            if is_youtube_open():
                start_goodbyedpi()
                youtube_last_seen = time.time()
            else:
                if goodbyedpi_process and (time.time() - youtube_last_seen > delay_before_closing):
                    stop_goodbyedpi()
            time.sleep(1)
    except KeyboardInterrupt:
        stop_goodbyedpi()

if __name__ == "__main__":
    run()
