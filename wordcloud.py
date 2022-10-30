# 5号词云：乡村振兴战略中央文件（词云）
# B站专栏：同济子豪兄 2019-5-23




import pandas as pd
import re
import jieba.posseg as pseg
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from sklearn import metrics
import imageio
# # 导入词云制作库wordcloud和中文分词库jieba
# import jieba
import wordcloud
#
# # 构建并配置词云对象w
# w = wordcloud.WordCloud(width=1000,
#                         height=700,
#                         background_color='white',
#                         font_path='msyh.ttc')
#
# # 对来自外部文件的文本进行中文分词，得到string
# f = open('关于实施乡村振兴战略的意见.txt',encoding='utf-8')
# txt = f.read()
# txtlist = jieba.lcut(txt)
# string = " ".join(txtlist)
#
# # 将string变量传入w的generate()方法，给词云输入文字
# w.generate(string)
#
# # 将词云图片导出到当前文件夹
# w.to_file('output5-village.png')


def flat(l):
    for k in l:
        if not isinstance(k, (list, tuple)):
            yield k
        else:
            yield from flat(k)


def clean_text(text, name=False, ):
    if text == '':
        return ''
    if name:
        for i in range(len(text)):
            if text[i] == ':' or text[i] == '：':
                text = text[i + 1:-1]
                break

    zh_puncts1 = "，；、。！？（）《》【】"
    URL_REGEX = re.compile(
        r'(?i)((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>' + zh_puncts1 + ']+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’' + zh_puncts1 + ']))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)

    EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
    text = re.sub(EMAIL_REGEX, "", text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    lb, rb = 1, 6
    text = re.sub(r"\[\S{" + str(lb) + r"," + str(rb) + r"}?\]", "", text)
    emoji_pattern = re.compile("["u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0" "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r"#\S+#", "", text)
    text = text.replace("\n", " ")

    text = re.sub(r"(\s)+", r"\1", text)
    stop_terms = ['展开', '全文', '展开全文', '一个', '网页', '链接', '?【', 'ue627', 'c【', '10', '一下', '一直', 'u3000', '24', '12',
                  '30', '?我', '15', '11', '17', '?\\', '显示地图', '原图']
    for x in stop_terms:
        text = text.replace(x, "")
    allpuncs = re.compile(
        r"[，\_《。》、？；：‘’＂“”【「】」·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#\$\%\^\&\*\(\)\-\=\+]")
    text = re.sub(allpuncs, "", text)

    return text.strip()


def get_words_by_flags(words, flags=None):
    flags = ['n.*', 'v.*'] if flags is None else flags
    words = [w for w, f in words if w != ' ' and re.match('|'.join(['(%s$)' % flag for flag in flags]), f)]
    return words


def stop_words_cut(words, stop_words_path):
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
        stopwords.append(' ')
        words = [word for word in words if word not in stopwords]
    return words


def pseg_cut(x):
    return pseg.lcut(x, HMM=True)


def preProcess(df):
    df['content'] = df['微博正文'].map(lambda x: clean_text(x))
    df['content_cut'] = df['content'].map(lambda x: pseg_cut(x))
    df['content_cut'] = df['content_cut'].map(lambda x: get_words_by_flags(
        x, flags=['n.*', 'v.*', 'eng', 't', 's', 'j', 'l', 'i']))
    df['content_cut'] = df['content_cut'].map(lambda x: stop_words_cut(
        x, 'stop_words.txt'))
    df['content_'] = df['content_cut'].map(lambda x: ' '.join(x))


def fun():
    filepath = '热门微博.csv'
    df = pd.read_csv(filepath, index_col=0, )
    preProcess(df)
    word_library_list = list(flat((df['content_cut'])))
    # print(word_library_list)

    str = ""

    for s in word_library_list:
        str += s
        str += ' '

    mk = imageio.imread("./sina.png")

    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path='msyh.ttc',
                            mask=mk)

    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(str)
    from wordcloud import ImageColorGenerator

    image_colors = ImageColorGenerator(mk)
    w.recolor(color_func=image_colors)

    # 将词云图片导出到当前文件夹
    w.to_file('output5.png')



fun()
