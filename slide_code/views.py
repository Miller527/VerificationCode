#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Miller"
# Date: 2019/1/2

import os

import jwt
import random

from sanic.response import json as JsonResponse

from config import URL_PREFIX
from wtf import TokenWtf


def file_name(file_dir):
    li = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            li.append(file)
    return li


def verify_bearer_token(token):
    #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
    try:
        header = jwt.api_jws.get_unverified_header(token)
        jwt.decode(token, 'V5mafzMTLGGJaDNQKCqw', issuer=URL_PREFIX + "/login",
                   audience=URL_PREFIX + "/slide_code", algorithms=[header.get("alg")])
    except Exception as e:
        print(e)
        return False
    return True


async def slide_code(request):
    """请求验证码数据"""

    wtf = TokenWtf(request)
    print(wtf.token)
    status = verify_bearer_token(wtf.token.data)
    if not status:
        return JsonResponse({"status": 403, "msg": "登录验证码授权token校验失效"})

    width = 360
    height = 176
    img = file_name("static")
    img_src = random.choice(img)

    pl_size = 48
    padding = 20
    _min_x = pl_size + padding
    _max_x = width - padding - pl_size - pl_size // 6
    _min_y = height - padding - pl_size - pl_size // 6
    _max_y = padding
    deviation = 4  # 滑动偏移量

    x = await random_num(_min_x, _max_x)
    y = await random_num(_min_y, _max_y)
    request["session"]["coords"] = [x - deviation, x + deviation]
    request["session"]["coordY"] = y

    print("code------>", x, y)

    return JsonResponse({"status":200, "msg":"SUCCESS","data":{ "img_src": img_src, "x": x, "y": y}})
    # width = 360
    # height = 176
    # img = file_name("static")
    # img_src = random.choice(img)
    #
    # pl_size = 48
    # padding = 20
    # _min_x = pl_size + padding
    # _max_x = width - padding - pl_size - pl_size // 6
    # _min_y = height - padding - pl_size - pl_size // 6
    # _max_y = padding
    # deviation = 4  # 滑动偏移量
    #
    # x = await random_num(_min_x, _max_x)
    # y = await random_num(_min_y, _max_y)
    # request["session"]["coords"] = [x - 10 - deviation, x - 10 + deviation]
    # request["session"]["coordY"] = y
    # return JsonResponse({"width": width, "height": height,
    #                      "img_src": img_src, "pl_size": pl_size,
    #                      "padding": padding, "x": x, "y": y,
    #                      })


async def random_num(mi, ma):
    rang = ma - mi
    rand = random.random()
    if round(rand * rang) == 0:
        return mi + 1
    elif round(rand * ma) == ma:
        return ma - 1
    else:
        return mi + round(rand * rang) - 1
