"""
import necessary libraries
load data defination
load user's units:import unimported libraries
init task manager
register unit to service
parse defined task template from user
verfiy the template avaliable
execute tasks according to template
abroting task;restart task; restart task in abroting point
"""
from asyncio import gather
from dataclasses import Field, dataclass
import json
from typing import Dict

from fastapi import FastAPI


class DataMixin:
    @classmethod
    def encoder(cls, dict_obj: Dict) -> str:
        return json.dumps(dict_obj, ensure_ascii=False)

    @classmethod
    def decoder(cls, str_obj: str) -> Dict:
        return json.loads(str_obj)


@dataclass
class Data(DataMixin):
    params: Dict[str, str] = Field(default_factory=Dict)
    meta: Dict[str, any] = Field(default_factory=Dict)
    content: str = ""


fas_management = {}


def fas(fas_id: str):
    # register fas
    def decorator(func):
        def wrapper(*args, **kwargs):
            if fas_id in fas_management:
                print("same unit has been register, try another name")
            else:
                fas_management[fas_id] = (func, args, kwargs)
        return wrapper
    return decorator


app = FastAPI()


@app.post("/fas/{fas_id}")
async def service(fas_id: str):
    func, args, kwargs = fas_management[fas_id]
    return await func(args, kwargs)


@app.post("/fas/task/{template}")
async def task(template: str):
    task_flow = parse(template)
    return gather(task_flow)


@fas("political_word_remove_plugin")
async def political_word_remove_plugin(data: Data):
    return data


def parse(template):
    return ""
