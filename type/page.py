from typing import List
import time
from pydantic import BaseModel, Field, validator, constr, ConfigDict, BaseConfig
from datetime import datetime
from typing import get_type_hints


def dealDataList(data, model_class, popKeys=None):  # 参数：查询结果list,basemodel类，移除属性
    dicts = []
    for d in data:
        base_model = model_class.model_validate(d)
        dicts.append(base_model.model_dump(exclude=popKeys))
    return dicts


class page(BaseModel):  # 定义的分页类
    pageSize: int = Field(..., gt=0)
    pageNow: int = Field(..., gt=0)

    def offset(self):
        return (max(1, self.pageNow) - 1) * self.pageSize

    def limit(self):
        return self.pageSize


class pageResult(BaseModel):  # 分页结果类
    totalNum: int
    totalPage: int
    rows: List
