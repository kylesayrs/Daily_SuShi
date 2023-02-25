#!/usr/bin/python3

import os
import math
from datetime import datetime, timedelta
import json
import requests
import random
import time

# Global variables
POEMS_FILE = "poems.json" # len 2824
IMAGE_PATH = "poem.png"
POINT_SIZE = 60
LINE_MARGIN_SIZE = 5
INC = 29
START_DATE = datetime(2022, 5, 22)
SHOW_AUTHOR = False
SHOW_TAGS = True
FONT_PATH = "fonts/HanyiSentyMarshmallow.ttf"
BACKGROUND_PATH = "papyrus.jpg"
BACKGROUND_WIDTH = 1575
BACKGROUND_HEIGHT = 2362

# Pushover
raise ValueError("environment not set")
URL = None
USER_KEY = None
DEVICE = None
TOKEN = None
TITLE = None

def wrap_paragraphs(paragraphs, max_char_width):
    new_paragraphs = []
    for paragraph in paragraphs:
        for i in range(math.ceil(len(paragraph) / max_char_width)):
            p_start = i * max_char_width
            p_end = (i + 1) * max_char_width
            new_paragraphs.append(paragraph[p_start: p_end])

    return new_paragraphs

def generate_image(poem_data, image_path, point_size=POINT_SIZE):
    # Wrap paragraphs
    paragraphs = wrap_paragraphs(poem_data["paragraphs"], BACKGROUND_WIDTH // POINT_SIZE)

    # Create content
    content_lines = []
    content_lines.append(poem_data["title"])
    if SHOW_AUTHOR: content_lines.append(poem_data["author"])
    if SHOW_TAGS and ("tags" in poem_data): content_lines.append('{}'.format(' '.join(poem_data["tags"])))
    content_lines.append('        ')
    content_lines += paragraphs
    content = '\n'.join(content_lines)
    content.replace('"', '')

    # Formatting
    border_size = POINT_SIZE / 2
    max_char_width = max([len(content_line) for content_line in content_lines])
    image_width = (max_char_width - 1) * (POINT_SIZE) + border_size
    image_height = (len(content_lines) + 1) * (POINT_SIZE + LINE_MARGIN_SIZE) + border_size

    # Random offset on papyrus
    if image_width >= BACKGROUND_WIDTH or image_height >= BACKGROUND_HEIGHT:
        raise Exception("Poem too large")
    width_offset = random.randint(0, BACKGROUND_WIDTH - image_width)
    height_offset = random.randint(0, BACKGROUND_HEIGHT - image_height)

    # Construct command
    command_args = []
    command_args.append('convert')
    command_args.append(BACKGROUND_PATH)
    command_args.append(f'-crop {image_width}x{image_height}+{width_offset}+{height_offset}')
    command_args.append(f'-font "@{FONT_PATH}"')
    command_args.append(f'-pointsize {point_size}')
    command_args.append('-fill black')
    command_args.append(f'-annotate +{width_offset + border_size}+{height_offset + point_size + border_size}')
    command_args.append(f'"{content}"')
    command_args.append(image_path)

    # Execute command
    print(' '.join(command_args))
    os.system(' '.join(command_args))

def generate_message(poem_data):
    message = ''
    message += '〈{}〉\n'.format(poem_data["title"])
    if SHOW_AUTHOR: message += '{}\n'.format(poem_data["author"])
    if SHOW_TAGS and "tags" in poem_data: message += '{}\n'.format(' '.join(poem_data["tags"]))
    message += '\n'
    for paragraph in poem_data["paragraphs"]:
        message += paragraph + "\n"

    return message

def main(poems_data, poem_index, send_req=True):

    # Get poem and generate message
    num_failed_poems = 0
    while True:
        try:
            poem_data = poems_data[poem_index + num_failed_poems]
            print(poem_data)
            message = generate_message(poem_data)
            generate_image(poem_data, IMAGE_PATH)
            #generate_image(poem_data, f'poem_{i}.png')
        except Exception as e:
            print(e)
            num_failed_poems += 1
        else:
            break

    # Create payload
    payload = {"token": TOKEN,
               "user": USER_KEY,
               "device": DEVICE,
               "title": TITLE,
               "message": message}

    files = {"attachment": ("poem.png", open(IMAGE_PATH, "rb"), "image/jpeg")}

    # Send request
    if send_req:
        x = requests.post(URL, payload, files=files)
        print(payload)
        print(x)
        print(x.content)
        time.sleep(1)

if __name__ == "__main__":
    # Get poems data
    with open(POEMS_FILE, "r") as poems_file:
        poems_data = json.load(poems_file)

    #for i in range(20):
    # Get date and poem index
    today = datetime.today()
    #today = today.replace(month=5, day=25, hour=14, minute=0)
    diff = int((today - START_DATE).total_seconds() // (86400 / 2 / INC))
    poem_index = diff % len(poems_data)# + i

    main(poems_data, poem_index, send_req=True)
