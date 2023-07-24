from typing import Any

from pydantic import BaseModel, Field

from microstack.docker.enums import DockerCliNetworkDrivers, DockerCliMountTypes


class PublishedPort(BaseModel):
    """Represents a host <-> container published port"""
    host: int = Field(title="Host port", le=65_535)
    container: int = Field(title="Container port", le=65_535)


class Network(BaseModel):
    """Represents a network that can be shared with multiple containers"""
    driver: DockerCliNetworkDrivers = Field(title="Which network driver to use", default=DockerCliNetworkDrivers.BRIDGE)


class Mount(BaseModel):
    """Represents a verbose mount that can be shared with multiple containers"""
    source: str = Field(title="Host filesystem path")
    target: str = Field(title="Remote filesystem path")
    type_: DockerCliMountTypes = Field(title="Which type should the mount be", default=DockerCliMountTypes.BIND)


class Service(BaseModel):
    """A service in your backend"""
    image: str = Field(title="Base image for the container")
    name: str | None = Field(title="Name of this container", default=None)
    mounts: list[Mount] = Field(title="Mounts for this container", default=[])
    networks: list[Network] = Field(title="Networks for this container. Note: recent versions of Docker have had issues with containers & more than one network.", default=[])
    published_ports: list[PublishedPort] = Field(title="Published Ports for this container", default=[])

    def __init__(self, **data: Any):
        super().__init__(**data)

