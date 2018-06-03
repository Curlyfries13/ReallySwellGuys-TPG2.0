import csv
import pandas as pd

_MAP_FILE_NAME = "../data/map.csv"

class Mapper():


    def __init__(self):
        self._entries = dict()
        with open(_MAP_FILE_NAME) as data:
            reader =  csv.reader(data)
            for entry in reader:
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
            file_format = file_entry['format']

            if file_format == 'xls':
                data = pd.read_excel(filename)
            elif file_format == 'html':
                # html puts out a list of datasets, but these are expected to
                # be simple single-element lists
                data = pd.read_html(filename)[0]
                old_label = data.columns.values.tolist()
                new_label = data.iloc[0].values.tolist()

                relabel = dict(zip(old_label, new_label))
                data = data.rename(index=str, columns=relabel)
                data = data.iloc[1:]
            elif file_format == 'parquet':
                data = pd.read_parquet(filename)
            elif file_format == 'csv':
                data = pd.read_csv(filename)
            else:
                raise ValueError('bad parser type: {}'.format(file_format))
            print('Data Loaded')
            file_entry['dl'] = data
            file_entry['loaded'] = True
            return data

    def list_data_names(self):
        outstring = ""
        for key, value in self._entries.items():
            outstring += "{}: {}".format(key, value['filename'])
        return outstring


    def get_entry(self, name):
        entry = self._entries[name]
        return self.get_dataframe(entry)

    def update_entry(self, dataframe, name):
        entry = self._entries[name]
        filename = entry['filename']
        file_format = entry['format']
        if file_format == 'xls':
            data = dataframe.to_excel(filename)
        elif file_format == 'html':
            # html puts out a list of datasets, but these are expected to
            # be simple single-element lists
            data = dataframe.to_html(filename)
        elif file_format == 'parquet':
            data = dataframe.to_parquet(filename)
        elif file_format == 'csv':
            data = dataframe.to_csv(filename)

    def add_entry(self, dataframe, name, filename, fmt):
        """
        add an entry to the map.csv file: note this will add a name even if
        the subsequent save to disk doesn't work (bad filenames, bad formats)
        """
        if name in self._entries:
            print('mapping for "{}" already exists.'.format(name))
            return
        with open(_MAP_FILE_NAME, 'a') as data:
            self._entries[name] = {}
            self._entries[name]['filename'] = filename
            self._entries[name]['format'] = fmt
            self._entries[name]['loaded'] = True
            self._entries[name]['dl'] = dataframe

            self.update_entry(dataframe, name)
            writer = csv.writer(data)
            writer.writerow([name, filename, fmt])
