import addressparser
from typing import List
from collections import Counter
import Levenshtein

import re
from typing import List
import addressparser

class AddressProcessor:
    # 可配置的特殊区域列表
    SPECIAL_AREAS = ['开发区', '高新区']

    @staticmethod
    def preprocess(address: str) -> str:
        """
        去除地址字符串的首尾空格。
        """
        return address.strip()

    @staticmethod
    def normalize_brackets(address: str) -> str:
        """
        将英文括号转换为中文括号。
        """
        return address.replace('(', '（').replace(')', '）')

    @staticmethod
    def remove_brackets_content(address: str) -> str:
        """
        移除括号及括号内的内容。
        """
        address = AddressProcessor.normalize_brackets(address)
        return re.sub(r'（[^）]+）', '', address)

    @staticmethod
    def retain_alphanumeric_and_chinese(address: str) -> str:
        """
        保留字母、数字和中文字符，移除其他字符。
        """
        address = AddressProcessor.remove_brackets_content(address)
        return re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5]', '', address)

    @staticmethod
    def parse(address: str) -> str:
        """
        使用 addressparser 解析地址，提取地名。
        """
        processed_address = AddressProcessor.retain_alphanumeric_and_chinese(address)
        if not processed_address.strip():
            return ''
        else:
            return addressparser.transform([processed_address])['地名'][0]

    @classmethod
    def remove_special_areas(cls, place_name: str) -> str:
        """
        移除地名中的特殊区域（如开发区、高新区）。
        """
        for area in cls.SPECIAL_AREAS:
            if area in place_name:
                return place_name.split(area)[1]
        return place_name

    @classmethod
    def process(cls, address: str) -> str:
        """
        处理地址字符串，返回标准化后的地名。
        """
        # 预处理地址
        preprocessed = cls.preprocess(address)
        # 解析地址
        parsed = cls.parse(preprocessed)
        # 移除特殊区域
        return cls.remove_special_areas(parsed)


def calculate_similarity_score(addr1: str, addr2: str) -> str:
    processed_addr1 = AddressProcessor.process(addr1)
    processed_addr2 = AddressProcessor.process(addr2)
    
    if 'nan' in (processed_addr1, processed_addr2):
        return 0
    
    min_len = min(len(processed_addr1), len(processed_addr2))
    if min_len >= 4 and (processed_addr1 in processed_addr2 or processed_addr2 in processed_addr1):
        return '相同' if processed_addr1 == processed_addr2 else '包含'
    
    # return Levenshtein.ratio(processed_addr1, processed_addr2)
    return 1 - Levenshtein.distance(processed_addr1, processed_addr2) / (len(processed_addr1) + len(processed_addr2))

def compare_shipping_addresses(addr1: str, addr2: str, addr3: str, addr4: str) -> str:
    comparisons = [
        (addr1, addr3), (addr1, addr4),
        (addr2, addr3), (addr2, addr4)
    ]
    scores = [calculate_similarity_score(a, b) for a, b in comparisons]
    
    if '相同' in scores:
        return '相同'
    if '包含' in scores:
        return '包含'
    # print(scores)
    return max((score for score in scores if isinstance(score, float)), default=0)