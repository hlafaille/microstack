from pydantic import BaseModel

from microstack.docker.enums import DockerCliNetworkDrivers


class DockerCliNetwork(BaseModel):
    id_: str
    name: str
    driver: DockerCliNetworkDrivers
    scope: str  # todo update this with an enum
