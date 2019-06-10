#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/8 19:11
# @Author  : wansho
# @File    : setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="weibo-preprocess-toolkit",
    version="1.0.0",
    author="wansho",
    author_email="wanshojs@gmail.com",
    description="Weibo Preprocess Toolkit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wansho/weibo-preprocess-toolkit",
    include_package_data=True,
    packages=["weibo_preprocess_toolkit.dictionary", "weibo_preprocess_toolkit", "weibo_preprocess_toolkit.lib"],
    package_data={"weibo_preprocess_toolkit": ["dictionary/*"]},
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'jieba>=0.39'
    ],
    python_requires='>=3',
)