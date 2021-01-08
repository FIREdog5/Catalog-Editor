import json
import os

class Data_manager():

    PICTURES = []

    def __init__(self):
        self.database = []
        self.got_skipped = []
        self.index = 0

    def load_data(self):
        #errors with FileNotFoundError if savestate.txt does not exist. Wrap with try except for all uses where save may not have been first called.
        f = open("savestate.json", "r")
        json_str = f.read()
        data_dict = json.loads(json_str)
        self.database = data_dict["database"]
        self.index = data_dict["index"]
        self.got_skipped = data_dict["got_skipped"]

    def collect_data(self, data):
        if data["name"] and data["number"] and data["description"] and data["picture"]:
            self.database.append(data)
            self.index += 1

    def get_entry_index(self, number):
        for i in range(len(self.database)):
            if self.database[i]["number"] == number:
                return i

    def get_entry(self, number):
        return self.database[self.get_entry_index(number)]

    def modify_data(self, number, data):
        self.database[self.get_entry_index(number)]=data

    def save_data(self):
        json_str = json.dumps(self.__dict__)
        f = open("savestate.json", "w")
        f.write(json_str)
        f.close()

    def get_next_picture(self):
        return self.get_picture(self.index)

    def sorted_data(self):
        return self.database.sort(key = lambda x: x["number"])

    def set_skipped(self, skipped):
        self.got_skipped = skipped

    def get_picture(self, index):
        if not Data_manager.PICTURES:
            load_pictures()
        if len(Data_manager.PICTURES) <= index:
            if not self.got_skipped:
                raise EOFError
            else:
                return self.got_skipped.pop()
        return Data_manager.PICTURES[index]

def load_pictures():
    Data_manager.PICTURES = []
    for file in os.listdir("pictures"):
        Data_manager.PICTURES.append(file)
    Data_manager.PICTURES.sort()
