#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import random
from abc import ABC
from functools import partial
import pandas as pd
import requests
import re

from graph.component.base import ComponentBase, ComponentParamBase


class BaiduParam(ComponentParamBase):
    """
    Define the Baidu component parameters.
    """

    def __init__(self):
        super().__init__()
        self.top_n = 10

    def check(self):
        self.check_positive_integer(self.top_n, "Top N")


class Baidu(ComponentBase, ABC):
    component_name = "Baidu"

    def _run(self, history, **kwargs):
        ans = self.get_input()
        ans = " - ".join(ans["content"]) if "content" in ans else ""
        if not ans:
            return Baidu.be_output(self._param.no)

        url = 'https://www.baidu.com/s?wd=' + ans + '&rn=' + str(self._param.top_n)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'}
        response = requests.get(url=url, headers=headers)

        baidu_res = re.findall(r'"contentText":"(.*?)"', response.text)
        url_res = re.findall(r"'url': \\\"(.*?)\\\"}", response.text)
        for i in range(min(len(baidu_res), len(url_res))):
            baidu_res[i] += '<a>' + url_res[i] + '</a>'

        del url_res

        br = pd.DataFrame(baidu_res, columns=['content'])
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>\n", br)
        return br