import csv
from abc import ABC, abstractmethod


class table_handler(ABC):
    @abstractmethod
    def get_html_table(self, content=None) -> dict:
        pass

    @abstractmethod
    def append(self, row) -> None:
        pass

    @abstractmethod
    def filter_by(self, key, value):
        pass


class CSV_handler(table_handler):
    def __init__(self, filename, delimiter=';', headers=None):
        self.filename = filename
        self.delimiter = delimiter
        self.headers = headers
        self.contents = self._read_csv()

    def _read_csv(self):
        contents = {}
        with open(self.filename, 'r') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            if self.headers is not None:
                contents['headers'] = self.headers
            else:
                contents['headers'] = next(reader)
            for i, row in enumerate(reader):
                contents[i] = row

        return contents

    def get_html_table(self, content=None):
        if content is None:
            with open(self.filename) as f:
                content = f.readlines()

        rows = [x.strip() for x in content]
        table = '<table><tr>'
        if self.headers is not None:
            table += "".join(["<th>" + cell + "</th>" for cell in self.headers.split(self.delimiter)])
        else:
            table += "".join(["<th>" + cell + "</th>" for cell in rows[0].split(self.delimiter)])
            rows = rows[1:]
        table += "</tr>"

        for row in rows:
            table += "<tr>" + "".join(["<td>" + cell + "</td>" for cell in row.split(self.delimiter)]) + "</tr>" + "\n"
        table += "</table><br>"
        return table

    def append(self, row):
        with open(self.filename, 'a') as f:
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(row)
        self.contents = self._read_csv()

    def filter_by(self, key, value):
        if key not in self.contents['headers']:
            raise KeyError
        filter_index = self.contents['headers'].index(key)
        filtered_values = [';'.join(self.contents['headers'])]
        for contents_key, contents_value in self.contents.items():
            if contents_key == 'headers':
                pass
            if contents_value[filter_index] == value:
                filtered_values.append(';'.join(contents_value))
        return filtered_values


def generate_page(table, filename='static/index.html'):
    with open(filename) as f:
        html = f.read()
    html = html.replace('{{}}', table)
    return "HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n" + html


if __name__ == '__main__':
    scvhandler = CSV_handler(filename='static/data.csv')
    print(scvhandler.get_html_table(content=scvhandler.filter_by('subject', 'DB')))