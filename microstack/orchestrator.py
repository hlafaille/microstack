import logging

import docker

from microstack.schemas import Mount, Network, Service


def orchestrator_up(stack_definition: list[type[Service] | type[Network] | type[Mount]]):
    """
    Bring up the defined stack.
    :param stack_definition: List of `Service`, `Network`, and `Mount` schema(s)
    """
    client = docker.from_env()

    # get our networks
    docker_networks = client.networks.list()

    # iterate over the stack definition, if type is Network, check if it exists
    for type_ in stack_definition:
        instantiated_type = type_()
        if not issubclass(type_, Network):
            continue

        # check if this network exists
        match_found = False
        for network in docker_networks:
            if network.attrs["Name"] == f"microstack-{instantiated_type.__class__.__name__}":
                logging.info(f"network '{instantiated_type.__name__}' exists, skipping")
                match_found = True
                break
        if not match_found:
            client.networks.create(f"microstack-{instantiated_type.__class__.__name__}")
            logging.info(f"creating network '{instantiated_type.__class__.__name__}'")