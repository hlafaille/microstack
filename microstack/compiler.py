import datetime
import importlib
import logging
from textwrap import dedent

from microstack.docker.state import networks_get
from microstack.schemas import Service, Mount, Network


def parse_stack_to_docker_commands(stack_definition: list[Service], pull: bool = False) -> list[list[str]]:
    """
    Parse a list of Service schema(s), converting into Docker commands
    :param stack_definition: list of Service schema(s)
    :param pull: Run `docker pull x` on every service
    :return: List of list[str]'s, perfect for subprocess.%
    """


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


def compile_stack(stack_definition: list[type[Service] | type[Network] | type[Mount]]) -> str:
    """
    Compile the stack into executable Python
    :param stack_definition: List of `Service`, `Network`, and `Mount` schema(s)
    :return: services: Executable Python code
    """
    logging.info(f"parsing stack definition with {len(stack_definition)} element(s)")

    def _does_network_exist(network: Network) -> bool:
        """
        Checks if the provided Network already exists on the host
        :param network: Network schema
        :return: True if it exists, False if it doesn't
        """
        docker_networks = networks_get()
        if network.name in [x.name for x in docker_networks]:
            return True
        return False

    # define our output python string
    out = ""

    # define tracking for network & mounts existence checks
    queue_network_create: list[Network] = []

    logging.info("beginning compilation")
    # iterate over the service definition, begin creating the script file
    for type_ in stack_definition:
        instantiated_type = type_()
        if issubclass(type_, Network):
            logging.info(f"got network '{type_.__name__}'")
            if not _does_network_exist(instantiated_type):
                queue_network_create.append(instantiated_type)
        elif issubclass(type_, Mount):
            logging.info(f"got mount '{type_.__name__}'")
        elif issubclass(type_, Service):
            logging.info(f"got service '{type_.__name__}'")
        else:
            logging.critical(f"unknown stack definition type: {type_.__name__}")
            quit(1)

    # begin writing our output
    out += f'"""\ngenerated by microstack @ {datetime.datetime.utcnow().isoformat()}\n"""\n'
    out += f"import subprocess\n"

    # iterate over networks, create missing ones
    for network in queue_network_create:
        logging.info(f"writing action:create_if_not_exists for '{network.name}'")
        var_name = f"cmd_create_network_{network.name}"
        out += dedent(f"""
        # action:create_if_not_exists || create network '{network.name}'
        {var_name} = subprocess.run(
            args=['docker', 'network', 'create', '{network.name}', '-d', '{network.driver.name.lower()}']
        )\n
        """)

    # iterate over stack definition, skip anything that's not a Service, create the container
    for type_ in stack_definition:
        instantiated_type = type_()
        if not issubclass(type_, Service):
            continue
        # write pull command
        logging.info(f"writing action:pull for '{instantiated_type.name}'")
        var_name = f"cmd_pull_{instantiated_type.name}"
        out += dedent(f"""
        # action:pull || pull '{instantiated_type.name}'
        {var_name} = subprocess.run(
            args=['docker', 'pull', '{instantiated_type.image}']
        )
        """)
        # write run command
        logging.info(f"writing action:run for '{instantiated_type.name}'")
        var_name = f"cmd_run_{instantiated_type.name}"
        out += dedent(f"""
                # action:run || run '{instantiated_type.name}'
                {var_name} = subprocess.run(
                    args=['docker', 'run', '-d', '{instantiated_type.name}']
                )
                """)
    return out
