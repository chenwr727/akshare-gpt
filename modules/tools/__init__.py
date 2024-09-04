import importlib.util
import os

from modules.tools.tool_register import _TOOL_DESCRIPTIONS, dispatch_tool, get_tools


def scan_current_directory():
    """
    扫描当前目录及子目录下的所有Python文件，并动态导入这些模块。

    本函数跳过当前目录，仅处理子目录中的`.py`文件，通过构建模块路径并使用`importlib`进行动态导入。
    """
    current_dir = os.path.dirname(__file__)
    for root, _, files in os.walk(current_dir):
        if root == current_dir:
            continue
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.relpath(
                    os.path.join(root, file), current_dir
                ).replace(os.sep, ".")[:-3]
                module_name = f"{os.path.basename(current_dir)}.{module_path}"
                spec = importlib.util.spec_from_file_location(
                    module_name, os.path.join(root, file)
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)


scan_current_directory()
