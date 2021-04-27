import rule
from pypinyin import pinyin, Style
import re


def convert(old_string):
    punctuation = ['，', '﹑', '：', '；', '。', '！', '？', '-', '──']

    # 去除标点
    for i in punctuation:
        old_string = old_string.replace(i, '')

    # 先转为List
    new_string = list(old_string)

    # 谐音替换
    sentence_pinyin = pinyin(
        old_string,
        style=Style.TONE3,
        # errors='ignore',  # 忽略汉字外的字符
        heteronym=True,  # 开启多音字
        neutral_tone_with_five=True  # 开启轻声标记，防止字符串切片错误
    )
    for index, word_pinyin_list in enumerate(sentence_pinyin):
        for word_pinyin in word_pinyin_list:
            if word_pinyin[:-1] in rule.number['homonymic']:
                new_string[index] = rule.number['homonymic'][word_pinyin[:-1]]
            if word_pinyin[:-1] in rule.character['homonymic']:
                new_string[index] = rule.character['homonymic'][word_pinyin[:-1]]

    # 形象替换
    # 放在谐音替换之后，会覆盖谐音替换结果（如果有）
    # 比谐音优先级更高，因为形象字可以精确到某个字
    for index, word in enumerate(old_string):
        if word in rule.number['image_word']:
            new_string[index] = rule.number['image_word'][word]
        if word in rule.character['image_word']:
            new_string[index] = rule.character['image_word'][word]

    # 首字母替换
    new_string = pinyin(
        new_string,
        style=Style.FIRST_LETTER,
        # heteronym=True,  # 开启多音字
    )

    # 转换为字符串
    new_string = ''.join([i[0] for i in new_string])

    # 缺少数字补末尾字音调
    if not bool(re.search(r'\d', new_string)):
        last_word_pinyin = pinyin(
            old_string[-2:-1],
            style=Style.TONE3,
            neutral_tone_with_five=True
        )[0][0]
        new_string += last_word_pinyin[-1:]

    # 缺少特殊字符补刀($)
    if not bool(re.search(r'\D', new_string)):
        new_string += '$'

    # 长度不足使用填充规则
    if len(new_string) < 8:
        length = len(new_string)
        add_length = 8 - length
        new_string += str(add_length) * add_length

    # # 第一个字母大写
    # # 不能保证一定有大写字母
    # new_string = new_string.capitalize()

    return new_string


def main():
    with open('mingju/shiwen/mingju_shiwen_original.txt', 'r') as fp1,\
            open('converted/mingju_shiwen_converted.txt', 'w') as fp2:
        for line in fp1.readlines():
            print(line.replace('\n', ''))
            password = convert(line.replace('\n', ''))
            fp2.write(password+'\n')


if __name__ == '__main__':
    main()
