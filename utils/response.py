import functools
from datetime import datetime
from typing import Callable, List

from starlette.responses import JSONResponse
from type.page import page, pageResult
from utils.times import getMsTime


def standard_response(func: Callable):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)
        return JSONResponse({
            "code": 0,
            "message": "OK",
            "data": result,
            "timestamp": getMsTime(datetime.now())
        }, status_code=200)

    return decorator


def makePageResult(pg: page, tn: int, data: List):  # 处理分页数据
    return pageResult(
        totalNum=tn,
        totalPage=(tn + pg.pageSize - 1) // pg.pageSize,
        rows=data
    ).model_dump()


def user_standard_response(func: Callable):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)
        response = JSONResponse({
            "code": result['code'],
            "message": result['message'],
            "data": result['data'],
            "timestamp": getMsTime(datetime.now())
        }, status_code=200)
        if 'token_header' in result:
            if result['token_header'] == '-1':
                response.delete_cookie(key="TOKEN")  # 删除cookie
            else:
                response.set_cookie(key="TOKEN", value=str(result['token_header']))  # 添加cookie
        if 'token' in result:  # 判断是否有token项，如果有且不为-1就把它添加到cookie里
            if result['token'] == '-1':
                response.delete_cookie(key="SESSION")  # 删除cookie
            else:
                response.set_cookie(key="SESSION", value=str(result['token']))  # 添加cookie
        return response

    return decorator


def page_response(func: Callable):
    @functools.wraps(func)
    async def decorator(*args, **kwargs):
        result = await func(*args, **kwargs)
        response = JSONResponse({
            "message": result['message'],
            "data": result['data'],
            "code":result['code'],
            "timestamp": getMsTime(datetime.now())
        }, status_code=200)
        return response

    return decorator