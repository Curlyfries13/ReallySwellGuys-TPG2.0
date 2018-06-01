import csv
import pandas as pd

_MAP_FILE_NAME = "../data/map.csv"

class Mapper():


    def __init__(self):
        self._entries = dict()
        with open(_MAP_FILE_NAME) as data:
            reader =  csv.reader(data)
            for entry in reader:
                print(entry)
                if len(entry) == 0:
                    continue
                key = entry[0]
                self._entries[key] = {}
                self._entries[key]['filename'] = entry[1]
                self._entries[key]['format'] = entry[2]
                self._entries[key]['loaded'] = False
                self._entries[key]['dl'] = None

    def __getattr__(self, attr):
        if attr in self._entries:
            return self.get_dataframe(self._entries[attr])
        else:
            raise(AttributeError("Attribute does not exist: {}".format(attr)))

    def get_dataframe(self, file_entry):
        if file_entry['loaded']:
            return file_entry['dl']
        else:
            data = None
            filename = file_entry['filename']

            if file_entry['format'] == 'xls':
                data = pd.read_excel(filename)
            if file_entry['format'] == 'html':
                # html puts out a list of datasets, but these are expected to
                # be simple single-element lists
                data = pd.read_html(filename)[0]
            elif file_entry['format'] == 'parquet':
                data = pd.read_parquet(filename)
            else:
                raise ValueError('bad parser type: {}'.format(filename))
            file_entry['dl'] = data
            file_entry['loaded'] = True

    def list_data_names(self):
        outstring = ""
        for key, value in self._entries.items():
            outstring += "{}: {}".format(key, value['filename'])
        return outstring



