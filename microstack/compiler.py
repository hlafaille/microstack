import datetime
import importlib
import logging
from textwrap import dedent

from microstack.docker.state import networks_get
from microstack.schemas import Service, Mount, Network


def parse_stack_from_file(module_path: str, module_name: str,) -> list[type[Service] | type[Network] | type[Mount]]:
    """
    Import a Python module / stack file
    :param module_path: OS style path to the stack (ex: `/home/myuser/python_projects/dev_stack`)
    :param module_name: Name of module (ex: `stack`)
    :return: list of Service, Network and Mount schema(s)
    """
    # import the module, get contents as a dict
    stack = importlib.import_module(name=module_name, package=module_path)
    stack_dict = stack.__dict__

    # iterate over the keys, filter out the ones we don't need (and convert this to a list)
    logging.info(f"dealing with '{module_path}/{module_name}.py' as our stack description")
    stack_definition: list[type[Service] | type[Network] | type[Mount]] = []
    for key in stack_dict.keys():
        if "__" in key:
            continue
        if stack_dict[key] in (Service, Network, Mount):
            continue
        stack_definition.append(stack_dict[key])
    return stack_definition