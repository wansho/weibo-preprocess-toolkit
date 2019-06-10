# weibo-preprocess-toolkit
Weibo Preprocess Toolkit

## Getting Started

### Installation

```shell
pip install weibo-preprocess-toolkit
```

### Tutorial

```Python
from weibo_preprocess_toolkit import WeiboPreprocess

test_weibo = "所以我都不喝蒙 #南京·大行宫[地点]#牛，一直不喜欢蒙牛。謝駿毅 赞[122]转发[11] [超话] 收藏09月11日 18:57 "

# clean weibo
print(preprocess.clean(test_weibo))
# 所以我都不喝蒙 牛 一直不喜欢蒙牛 谢骏毅

# seg weibo
print(preprocess.seg(test_weibo))
# 所以 我 都 不喝 蒙 # 南京 · 大行宫 [ 地点 ] # 牛 ， 一直 不喜欢 蒙牛 。 謝駿毅 赞 [ 122 ] 转发 [ 11 ] [ 超话 ] 收藏 09 月 11 日 18 : 57

# clean and seg weibo
print(preprocess.clean_and_seg(test_weibo))
# 所以 我 都 不喝 蒙 牛 一直 不喜欢 蒙牛 谢骏毅
```


## Introduction
该工具用于微博文本的预处理：清洗 + 分词。

### Inspiration
在中文 NLP 领域，文本清洗和分词对于模型的性能有着很大的影响，如果语料库和测试集/**线上环境**的文本清洗规则和分词工具不同，就会导致在语料库上训练出来的模型在测试集上效果很差。举例来说，语料库采用了清洗规则 Clean-A 和 分词工具 Seg-A 来清洗和分词微博，而用户在线上环境采用了另一种清洗规则 Clean-B 和另一种分词工具 Seg-B，那么线上环境就会产生很多不在语料库词典中的**未登陆词（Unknown Words）**，这些未登陆词会导致预先训练好的模型，面对线上环境的另一种规则时，性能变差。

本人在对微博进行情感分析的过程中，总结了较多的微博清洗技巧和分词规则，并总结了一份微博情感分析词典用于优化 jieba 分词。所以我在这里尝试对微博的清洗和分词规则进行整理，同时也是为了保持语料库和线上环境的规则同步，为其他研究者和使用我的模型的人，提供一个和语料库匹配的清洗和分词规则。

### Weibo Cleaning

本人对微博文本的清洗规则进行了整理，主要涉及到如下的规则：

1. 中文繁体转简体
2. [微博停用词规则1(正则表达式)](weibo_preprocess_toolkit/dictionary/weibo_stopwords1_regex.csv)，包括 url, email, @某人, 地点，…… 等停用词规则
3. [微博停用词规则2(正则表达式)](weibo_preprocess_toolkit/dictionary/weibo_stopwords2_regex.csv)，包括 时间，数字和微博中常出现的无意义的词等停用词规则
4. [微博特殊字符](weibo_preprocess_toolkit/dictionary/special_chars.csv)
5. 其他细节处理

注意：考虑到停用词在词向量训练中衔接上下文的作用，本工具并没有对微博的停用词进行清洗

### Weibo Seg

基于 jieba 分词对微博文本进行分词优化，优化的地方主要有两点：

1. 扩种 jieba 分词词典，构建情感词典，优化情感分析的分词结果
2. 对否定前缀词进行特殊处理

## Dependencies
```bash
pip install jieba
```

## Acknowledgment
[jieba 结巴中文分词](https://github.com/fxsjy/jieba)

[nstools 中文繁体转简体](https://github.com/skydark/nstools)

[NTUSD 情感词典](https://www.aaai.org/Papers/Symposia/Spring/2006/SS-06-03/SS06-03-020.pdf)

## License

MIT