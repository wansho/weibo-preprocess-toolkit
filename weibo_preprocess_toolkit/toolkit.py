#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 19:59
# @Author  : wansho
# @File    : toolkit.py

import re
import os
import sys
import csv
import codecs
import pkg_resources

import jieba
from weibo_preprocess_toolkit.lib.langconv import Converter

sys.path.append("../")


class WeiboPreprocess:

    __newline_space_regex = r'(\n)+|( )+'
    __num_regex = "\d+"

    def __init__(self):
        """
        init lib and load dictionary
        """
        self.__init_jieba()
        # load lib for coverting traditional chinese to simplified chinese
        self.tradition2simplified_converter = Converter("zh-hans")
        # load weibo stop word
        stop_words_regex_before_special_chars = self.__load_weibo_stop_word(should_before_special_chars=True)
        self.stop_words_regex1 = "|".join(stop_words_regex_before_special_chars)
        # load special chars
        special_chars = self.__load_special_chars()
        self.special_chars_regex = '[' + "".join(special_chars) + ']'
        # load weibo stop word
        stop_words_regex_after_special_chars = self.__load_weibo_stop_word(should_before_special_chars=False)
        self.stop_words_regex2 = "|".join(stop_words_regex_after_special_chars)
        # load stop words
        self.stop_words = self.__load_stop_words()
        pass

    def __load_weibo_stop_word(self, should_before_special_chars):
        """
        load weibo stop-words regex
        :param should_before_special_chars:
        :return:
        """
        if should_before_special_chars:
            path = "dictionary/weibo_stopwords1_regex.csv"
        else:
            path = "dictionary/weibo_stopwords2_regex.csv"
        utf8_reader = codecs.getreader("utf-8")
        with pkg_resources.resource_stream(__name__, os.path.join(path)) as fr:
            result = csv.reader(utf8_reader(fr), delimiter=',')
            stop_words_regex = [record[0] for record in result]
        return stop_words_regex

    def __load_stop_words(self):
        """
        load stop words
        :return:
        """
        path = "dictionary/stop_words.txt"
        with pkg_resources.resource_stream(__name__, os.path.join(path)) as fr:
            stop_words = [word.decode("utf-8").strip() for word in fr if word.strip()]
        stop_words = set(stop_words)
        return stop_words

    def __load_special_chars(self):
        """
        load special char
        :return:
        """
        path = "dictionary/special_chars.csv"
        utf8_reader = codecs.getreader("utf-8")
        with pkg_resources.resource_stream(__name__, os.path.join(path)) as fr:
            result = csv.reader(utf8_reader(fr))
            special_chars = [record[0] for record in result]
        return special_chars

    def __init_jieba(self):
        """
        init jieba seg tool
        :return:
        """
        path = "dictionary/jieba_expanded_dict.txt"
        jieba.load_userdict(pkg_resources.resource_stream(__name__, os.path.join(path)))

    def cut(self, weibo, keep_stop_word=True):
        """
        seg weibo into word list
        :param weibo: weibo text
        :param keep_stop_word: default keep stop word
        :return seged_words: word list
        """
        seged_words = [word for word in jieba.lcut(weibo) if word != " "]
        # fix negative prefix
        end_index = len(seged_words) - 1
        index = 0
        reconstructed_seged_words = []
        while (index <= end_index):
            word = seged_words[index]
            if word not in ["不", "没"]:
                index += 1
            else:
                next_word_index = index + 1
                if next_word_index <= end_index:
                    word += seged_words[next_word_index]
                    index = next_word_index + 1
                else:
                    index += 1
            reconstructed_seged_words.append(word)
        if not keep_stop_word:
            reconstructed_seged_words = [word for word in reconstructed_seged_words if word not in self.stop_words]
        return reconstructed_seged_words

    def traditional2simplified(self, weibo):
        """
        traditional Chinese to simplified Chinese
        :param weibo:
        :return:
        """
        return self.tradition2simplified_converter.convert(weibo)


    def clean(self, weibo, simplified=True):
        """
        weibo clean
        :param weibo: weibo text
        :param simplified: default simplified Chinese
        :return cleaned_weibo: cleaned weibo
        """
        weibo = weibo.lower().strip()
        if simplified:
            weibo = self.traditional2simplified(weibo)
        weibo = re.sub(self.stop_words_regex1, ' ', weibo)
        weibo = re.sub(self.special_chars_regex, ' ', weibo)
        weibo = re.sub(self.stop_words_regex2, ' ', weibo)
        weibo = re.sub(self.__num_regex, ' ', weibo)
        weibo = re.sub(self.__newline_space_regex, ' ', weibo)
        return weibo

    def preprocess(self, weibo, simplified=True, keep_stop_word=True):
        """
        clean and seg weibo
        :param weibo: weibo text
        :param simplified: default simplified Chinese
        :param keep_stop_word: default keep stop word
        :return cleaned_seged_weibo: cleaned and seged weibo
        """
        cleaned_weibo = self.clean(weibo, simplified=simplified)
        cleaned_seged_weibo = " ".join(self.cut(cleaned_weibo, keep_stop_word=keep_stop_word))
        return cleaned_seged_weibo
