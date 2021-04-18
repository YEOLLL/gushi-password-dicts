import requests
from pypinyin import pinyin, Style


def get_response(page):
    headers = {
        'Accept-Encoding': 'json',
    }

    params = (
        ('xstr', '诗文'),
        ('page', page),
        ('token', 'gswapi'),
    )

    response = requests.get('https://app.gushiwen.cn/api/mingju/Default12.aspx',
                            headers=headers,
                            params=params
                            ).json()
    return response


def main():
    # 截至2021.04.18，名句接口返回共500条，均分为十页
    sum_page = get_response(1)['sumPage']  # 10
    # sum_count = get_response(1)["sumCount"]  # 500
    first_letter_file = open('./mingju_first_letter.txt', 'w')
    initials_file = open('mingju_intials.txt', 'w')

    for page in range(1, sum_page + 1):

        mingjus = get_response(page)['mingjus']
        for mingju in mingjus:

            first_letter = ''
            initials = ''
            name_str = mingju['nameStr']

            letters = pinyin(name_str, style=Style.FIRST_LETTER, errors='ignore')
            letters2 = pinyin(name_str, style=Style.INITIALS, strict=False, errors='ignore')

            for letter in letters:
                first_letter = first_letter + letter[0]
            for letter2 in letters2:
                initials = initials + letter2[0]

            first_letter_file.write(first_letter + '\n')
            initials_file.write(initials + '\n')
            print('{}\t{}\t{}'.format(name_str, first_letter, initials))


if __name__ == '__main__':
    main()
