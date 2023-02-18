#!/usr/bin/env python3
from json import dump, load
from json.decoder import JSONDecodeError
from os import mkdir
from os.path import isfile, isdir
from sys import stdout

import gspread
from readchar import readchar
from unidecode import unidecode

import textfield

CREDENTIAL_PATH = './secret/credential.json'
ZASOSPIKA_DICTIONARY = '1QSqIbmShJiUiJWNB0x8dQzGbb6W1dqEz_LBlP363e_E'


def normalise(string: str) -> str:
    """
    소문자화, 다이어크리틱 제거 등을 진행한다.
    """

    return unidecode(string).lower()


class Dictionary:
    def __init__(self):
        self.path = './.dict_cache/zasospika.json'
        self.data = None

        if self.is_local_available():
            try:
                self.load()
            except JSONDecodeError:
                self.synchronize()
        else:
            self.synchronize()

    def __str__(self):
        return f'<Dictionary len(data)={len(self.data)}>'

    def synchronize(self, fileout: bool = True):
        """
        구글 스프레드이시트에서 자소크어 사전을 불러온다.

        그 후, ``self.data``를 동기화한다.
        """
        credential = gspread.service_account(filename=CREDENTIAL_PATH)
        sheet = credential.open_by_key(ZASOSPIKA_DICTIONARY).get_worksheet(0)

        self.data = sheet.get_all_values()[1:]

        if fileout:
            if not isdir('./.dict_cache'):
                mkdir('./.dict_cache')
            with open(self.path, 'w', encoding='utf-8') as file:
                dump(self.data, file)

    def is_local_available(self) -> bool:
        """
        ``load()`` 함수를 통해 불러올 수 있는 로컬 사전 저장 파일이 존재하는지 확인한다.
        """
        return isfile(self.path)

    def load(self):
        """
        ``syncronize()`` 함수를 통해 로컬에 저장되어있는 함수를 불러온다.
        """
        with open(self.path, 'r', encoding='utf-8') as file:
            self.data = load(file)

    def query(self, query: str, limit: int = 10) -> list[int]:
        """
        단어의 ``self.data`` 상 인덱스 목록을 출력한다.
        """
        query = normalise(query)

        result = list()
        for i, row in enumerate(self.data):
            if any(query in normalise(datum) for datum in row):
                result.append(i)
        return result

    def get(self, index: int) -> list:
        return self.data[index]


def main():
    dictionary = Dictionary()

    buffer = ''

    textfield.clear()

    while True:
        try:
            c = readchar()
        except KeyboardInterrupt:
            break

        if c == '\x7f':
            buffer = buffer[:-1]
        elif c == '\x15':
            buffer = ''
        elif c == '\n':
            pass
        else:
            buffer += c

        textfield.clear()

        textfield.clear_line(1)
        stdout.write('\r' + buffer)

        if not buffer:
            continue

        indexes = dictionary.query(buffer)
        print(buffer)
        for i, index in enumerate(indexes):
            textfield.move(i+2)
            data = dictionary.get(index)

            stdout.write(data[0])


if __name__ == '__main__':
    main()
