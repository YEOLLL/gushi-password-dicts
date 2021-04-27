from rule import *
from pypinyin import pinyin, Style


def main():
    s = '秦时明月汉时关，万里长征人未还。'
    sentence_pinyin = pinyin(
        s,
        style=Style.TONE3,
        errors='ignore',  # 忽略汉字外的字符
        heteronym=True,  # 开启多音字
        neutral_tone_with_five=True  # 开启轻声标记，防止字符串切片错误
    )
    for index, word_pinyin_list in enumerate(sentence_pinyin):
        for word_pinyin in word_pinyin_list:
            print(word_pinyin)


if __name__ == '__main__':
    main()
