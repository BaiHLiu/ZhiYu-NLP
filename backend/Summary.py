# coding:utf-8

import jiagu
import json
import requests
from Common import Config


def summary(content, max_len):
    summarize = jiagu.summarize(content, 3)  # 摘要
    ret = {
        'ret0': summarize[0],
        'ret1': summarize[1],
        'ret2': summarize[2]
    }
    return ret


def title(content):
    # 选择GPU节点逻辑
    gpu_url = list(Config.GPU_Node.values())[0]
    req_body = {
        'content': content
    }

    resp = requests.post(url=gpu_url, data=req_body).text
    resp = json.loads(resp)

    title_ret = resp['summary']

    ret = {
        'ret0': title_ret[0],
        'ret1': title_ret[1],
        'ret2': title_ret[2]
    }

    return ret


if __name__ == "__main__":
    fin = open('input.txt', 'r')
    text = fin.read()
    fin.close()

    summarize = jiagu.summarize(text, 3)  # 摘要
    print(summarize)
    title_ret = title(text)
    print(title_ret)
