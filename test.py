# -*- coding: utf-8 -*-

from natto import MeCab

mc = MeCab()

# テキストは cookbiz.jp より
text = "お仕事については基本的には店舗に配属してからのOJTが中心となりますが、先輩スタッフがしっかりとサポートしてくれるので、どなたも安心してお仕事していただけます。2013年には本社内に開発室を設置。店舗配属前にもトレーニングを行なってから実際の店舗に配属されるなど、サポート体制がしっかりと整っているのも当社の魅力。実際、経験が浅い方や未経験スタートのスタッフも多数活躍中！"

print ('Input text:\n'+text)

print('====================================================')

# -F / --node-format オプションでノードの出力フォーマットを指定する
#
# %m    ... 形態素の表層文
# %f[0] ... 品詞
# %h    ... 品詞 ID (IPADIC)
# %f[8] ... 発音
#
words = []
with MeCab('-F%m,%f[0],%h') as nm:
    for n in nm.parse(text, as_nodes=True):
        node = n.feature.split(',');
        if len(node) != 3:
            continue
        if node[1] == '名詞':
            # if True:
            words.append(node[0])
print(words)
