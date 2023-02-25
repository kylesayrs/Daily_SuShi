import os
import json

author_name = "蘇軾"
file_paths = ["./chinese-poetry/json/poet.song.45000.json",
              "./chinese-poetry/json/poet.song.44000.json",
              "./chinese-poetry/json/poet.song.46000.json",
              "./chinese-poetry/json/poet.song.193000.json"]

if __name__ == '__main__':
    collected_poems = []

    for file_path in file_paths:

        with open(file_path) as file:
            file_data = json.load(file)

            for poem_data in file_data:
                if poem_data["author"] == author_name:
                    collected_poems.append(poem_data)
                    if "歌头" in poem_data["title"]:
                        print(poem_data)

    #with open('poems.json', 'w') as outfile:
    #    json.dump(collected_poems, outfile)
