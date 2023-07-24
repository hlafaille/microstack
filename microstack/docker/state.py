import logging
import subprocess

from microstack.docker.enums import DockerCliNetworkDrivers
from microstack.docker.schemas import DockerCliNetwork


def networks_get() -> list[DockerCliNetwork]:
    """
    Get a list of Network(s) currently configured on the host
    :return: list of Network schema(s)
    """
    networks_cmd = subprocess.run(
        args=["docker", "network", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if networks_cmd.returncode != 0:
        logging.error("failed to get networks from docker cli")
        print(networks_cmd.stderr.decode())
        quit(1)

    # parse the networks command output
    networks_cmd_output = networks_cmd.stdout.decode().split("\n")
    payload: list[DockerCliNetwork] = []
    for elem, line in enumerate(networks_cmd_output):
        if elem == 0 or len(line) == 0:
            continue
        line = line.split(" ")
        line = [x for x in line if x != '']
        payload.append(
            DockerCliNetwork(
                id_=line[0],
                name=line[1],
                driver=NetworkDrivers(line[2]),
                scope=line[3]
            )
        )
    return payload