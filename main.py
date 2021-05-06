import requests
import json

file_patch_read = 'countries.json'
file_patch_write = 'output'


def get_country_list(file_patch):
    with open(file_patch_read, encoding='utf8') as file:
        json_data = json.load(file)

    return [country['name']['common'] for country in json_data]


def get_link(search_string, session):
    params = {'action': 'opensearch',
              'search': search_string,
              'limit': '1'}

    response = session.get('https://commons.wikimedia.org/w/api.php', params=params)
    try:
        if response.json()[3]:
            return response.json()[3][0]
    except json.decoder.JSONDecodeError:
        return None


def write_country(country_data, file_patch_write):
    with open(file_patch_write, 'a', newline='\n', encoding='utf8') as write_file:
        write_file.writelines(country_data + '\n')


class Wiki_parser:
    def __init__(self, file_patch_read, file_patch_write):
        self.country_list = get_country_list(file_patch_read)
        self.session = requests.Session()

    def __iter__(self):
        return self

    def __next__(self):
        if self.country_list:
            country = self.country_list.pop(0)
            country_data = f'{country}: {get_link(country, self.session)}'
            write_country(country_data, file_patch_write)
            return country_data
        else:
            raise StopIteration


from hashlib import md5


def json_read_hash(file_patch):
    with open(file_patch, encoding='utf8') as file:
        for line in file:
            yield md5(bytearray(line, encoding='utf8'))


if __name__ == '__main__':

    for data in Wiki_parser(file_patch_read, file_patch_write):
        print(data)

    for hash in json_read_hash('output'):
        print(hash)