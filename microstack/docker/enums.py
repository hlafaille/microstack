from enum import Enum


class DockerCliNetworkDrivers(Enum):
    BRIDGE = "bridge"
    HOST = "host"
    NULL = "null"


class DockerCliMountTypes(Enum):
    MOUNT = "mount"
    BIND = "bind"




