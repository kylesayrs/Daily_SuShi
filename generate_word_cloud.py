import jieba
import json
from imageio import imread
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, ImageColorGenerator

font_path = "/Library/Fonts/HanyiSentyMarshmallow.ttf"

# Read the whole text.
text = ""
with open('poems.json', 'r') as poems_file:
    poems_data = json.load(poems_file)
    for poem_data in poems_data:
        for paragraph in poem_data["paragraphs"]:
            paragraph = paragraph.replace("。", " ")
            paragraph = paragraph.replace("，", " ")
            paragraph = paragraph.replace("：", " ")
            text += paragraph + " "

# The function for processing text with Jieba
def jieba_processing_txt(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)

    f_stop_seg_list = ["詩題"]

    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ' '.join(mywordlist)

# Generate word cloud
wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=None,
               max_font_size=100, random_state=42, width=1000, height=860, margin=2,)
wc.generate(jieba_processing_txt(text))

# save wordcloud
wc.to_file('word_cloud.png')
