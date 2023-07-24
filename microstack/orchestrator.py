import logging
import os

import docker
from docker.errors import APIError
from docker.models.containers import Container

from microstack.schemas import Mount, Network, Service


def orchestrator_up(stack_definition: list[type[Service] | type[Network] | type[Mount]]):
    """
    Bring up the defined stack.
    :param stack_definition: List of `Service`, `Network`, and `Mount` schema(s)
    """
    client = docker.from_env()

    # get our current docker state
    docker_networks = client.networks.list()
    docker_images = client.images.list()

    # iterate over the stack definition, if type is Network, check if it exists
    for type_ in stack_definition:
        instantiated_type = type_()
        if not issubclass(type_, Network):
            continue

        # check if this network exists
        match_found = False
        for network in docker_networks:
            if network.attrs["Name"] == f"microstack-{instantiated_type.__class__.__name__}":
                logging.info(f"network '{instantiated_type.__class__.__name__}' exists, skipping")
                match_found = True
                break
        if not match_found:
            client.networks.create(f"microstack-{instantiated_type.__class__.__name__}")
            logging.info(f"creating network '{instantiated_type.__class__.__name__}'")

    # iterate over the stack definition, if type is Service, iterate over each Mount & warn if source does not exist
    for type_ in stack_definition:
        instantiated_type = type_()
        if not issubclass(type_, Service):
            continue
        for mount in instantiated_type.mounts:
            if not os.path.exists(mount.source):
                logging.warning(f"mount source'{mount.source}' does not exist on host, will be created by docker")

    # iterate over stack definitions, pull images if it doesn't exist
    for type_ in stack_definition:
        instantiated_type = type_()
        if not issubclass(type_, Service):
            continue

        # check if we have a matching image
        match_found = False
        for image in docker_images:
            if len(image.tags) == 0:
                continue
            if image.tags[0] == instantiated_type.image:
                match_found = True
                break

        # exit out of this loop if a match was found
        if match_found:
            break

        # no matching image found, pull it
        logging.warning(f"'{instantiated_type.image}' for '{instantiated_type.name}' was not found, pulling")
        client.images.pull(instantiated_type.image)

    # iterate over stack definitions, create containers
    for type_ in stack_definition:
        instantiated_type = type_()
        if not issubclass(type_, Service):
            continue

        # create the container
        started_containers: list[Container] = []
        logging.info(f"running '{instantiated_type.name}'")
        try:
            started_containers.append(
                client.containers.run(
                    image=instantiated_type.image,
                    name=f"microstack-{instantiated_type.name}",
                    detach=True
                )
            )
        except APIError as e:
            if e.status_code != 409:
                pass
            logging.info(f"'{instantiated_type.name}' already exists, skipping")
