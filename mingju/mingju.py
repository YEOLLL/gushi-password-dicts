import requests
from pypinyin import pinyin, Style
import click


def get_response(page, category):
    headers = {
        'Accept-Encoding': 'json',
    }

    params = (
        ('xstr', category),
        ('page', page),
        ('token', 'gswapi'),
    )

    response = requests.get('https://app.gushiwen.cn/api/mingju/Default12.aspx',
                            headers=headers,
                            params=params
                            ).json()

    return response


@click.command()
@click.option('-c', '--category',
              type=int,
              required=True,
              help='要爬取的分类: 1.诗文 2.古籍 3.谚语 4.对联')
def main(category):
    original_file_name = ''
    first_letter_file_name = ''
    initials_file_name = ''

    if category == 1:
        print('正在爬取诗文名言')
        original_file_name = 'mingju/shiwen/mingju_shiwen_original.txt'
        first_letter_file_name = 'mingju/shiwen/mingju_shiwen_first_letter.txt'
        initials_file_name = 'mingju/shiwen/mingju_shiwen_initials.txt'

    elif category == 2:
        print('正在爬取古籍名言')
        original_file_name = 'mingju/guji/mingju_guji_original.txt'
        first_letter_file_name = 'mingju/guji/mingju_guji_first_letter.txt'
        initials_file_name = 'mingju/guji/mingju_guji_initials.txt'

    elif category == 3:
        print('正在爬取谚语名言')
        original_file_name = 'mingju/yanyu/mingju_yanyu_original.txt'
        first_letter_file_name = 'mingju/yanyu/mingju_yanyu_first_letter.txt'
        initials_file_name = 'mingju/yanyu/mingju_yanyu_initials.txt'

    elif category == 4:
        print('正在爬取对联名言')
        original_file_name = 'mingju/duilian/mingju_duilian_original.txt'
        first_letter_file_name = 'mingju/duilian/mingju_duilian_first_letter.txt'
        initials_file_name = 'mingju/duilian/mingju_duilian_initials.txt'

    else:
        click.echo('请输入正确的分类')
        exit()

    original_file = open(original_file_name, 'w')
    first_letter_file = open(first_letter_file_name, 'w')
    initials_file = open(initials_file_name, 'w')

    # 截至2021.04.18，名句接口返回共500条，均分为十页
    # sum_page = get_response(1, '诗文')['sumPage']  # 10
    # sum_count = get_response(1)["sumCount"]  # 500
    for page in range(1, 11):

        mingjus = get_response(page, category)['mingjus']
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

            original_file.write(name_str + '\n')
            first_letter_file.write(first_letter + '\n')
            initials_file.write(initials + '\n')
            # print('{}\t{}\t{}'.format(name_str, first_letter, initials))


if __name__ == '__main__':
    main()
