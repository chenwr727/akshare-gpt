import inspect
import traceback
from copy import deepcopy
from pprint import pformat
from types import GenericAlias
from typing import Annotated, get_args, get_origin

from utils.log import logger

_TOOL_HOOKS = {}
_TOOL_DESCRIPTIONS = []


def parse_param_annotation(param_name: str, param_annotation):
    """
    解析函数参数的注解信息。

    本函数旨在处理函数参数的注解，提取参数的类型、描述信息以及是否必填等信息。
    它支持处理不同类型的参数注解，如字符串、整数、浮点数和布尔值等。

    参数:
    - param_name: 字符串类型，表示待解析参数的名称。
    - param_annotation: 参数的注解，应包含类型信息及元数据。

    返回:
    - param_info: 字典类型，包含解析后的参数信息，如描述、类型及是否必填等。
    - required: 布尔类型，指示参数是否为必填项。
    """
    typ, (description, required) = (
        param_annotation.__origin__,
        param_annotation.__metadata__,
    )
    typ_str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__

    if not isinstance(description, str):
        raise ValueError(f"Description for `{param_name}` must be a string")
    if not isinstance(required, bool):
        raise ValueError(f"Required for `{param_name}` must be a bool")

    param_info = {"description": description}
    if typ_str == "Literal":
        enum_values = list(get_args(typ))
        first_value_type = type(enum_values[0])
        typ_str = (
            str(first_value_type)
            if isinstance(first_value_type, GenericAlias)
            else first_value_type.__name__
        )
        param_info["enum"] = enum_values
    if typ_str == "str":
        typ_str = "string"
    elif typ_str == "int":
        typ_str = "integer"
    elif typ_str == "float":
        typ_str = "number"
    elif typ_str == "bool":
        typ_str = "boolean"
    param_info["type"] = typ_str

    return param_info, required


def register_tool(func: callable):
    """
    参数:
    - func: callable类型，一个工具函数。

    返回:
    - 注册后的工具函数。

    该函数首先获取工具函数的名称和描述，然后检查每个参数的类型注解，
    确保它们是使用typing.Annotated注解的。随后解析参数注解，并构建工具定义字典，
    包括工具的类型、名称、描述和参数信息。最后将工具函数和描述存储到全局变量中。
    """
    tool_name = func.__name__
    tool_description = inspect.getdoc(func).strip()
    python_params = inspect.signature(func).parameters
    tool_params = {}
    tool_required = []

    for param_name, param_obj in python_params.items():
        param_annotation = param_obj.annotation
        if param_annotation is inspect.Parameter.empty:
            raise TypeError(f"Parameter `{param_name}` missing type annotation")
        if get_origin(param_annotation) != Annotated:
            raise TypeError(
                f"Annotation type for `{param_name}` must be typing.Annotated"
            )

        param_info, required = parse_param_annotation(param_name, param_annotation)

        tool_params[param_name] = param_info

        if required:
            tool_required.append(param_name)

    tool_def = {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": tool_description,
            "parameters": {
                "type": "object",
                "properties": tool_params,
                "required": tool_required,
            },
        },
    }

    logger.info("[registered tool] " + tool_name)
    logger.debug("[registered tool] " + pformat(tool_def))
    _TOOL_HOOKS[tool_name] = func
    _TOOL_DESCRIPTIONS.append(tool_def)

    return func


def dispatch_tool(tool_name: str, tool_params: dict) -> str:
    """
    根据提供的工具名称和参数调用相应的工具函数。

    参数:
    - tool_name (str): 需要调用的工具名称。
    - tool_params (dict): 工具的参数字典。

    返回:
    - str: 工具执行的结果字符串，如果工具未找到或执行出错，则返回相应的错误信息。
    """
    if tool_name not in _TOOL_HOOKS:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = _TOOL_HOOKS[tool_name]
    try:
        ret = tool_call(**tool_params)
    except:
        ret = traceback.format_exc()
    return str(ret)


def get_tools() -> dict:
    return deepcopy(_TOOL_DESCRIPTIONS)
