import os
import json

author_name = "蘇軾"
author_id = "55c7bfff-55e8-4334-9290-787c1b2189aa"

data_dir = "./chinese-poetry/json"

if __name__ == '__main__':
    for file_name in os.listdir(data_dir):
        if file_name[0] == '.': continue
        if file_name[:9] != 'poet.song': continue

        file_path = os.path.join(data_dir, file_name)

        with open(file_path) as file:
            file_data = json.load(file)

            found = False
            for poem_data in file_data:
                if poem_data["author"] == author_name:
                    found = True
                    print(file_path)
                    break
