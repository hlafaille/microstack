from enum import Enum


class NetworkDrivers(Enum):
    BRIDGE = "bridge"
    HOST = "host"
    NULL = "null"


class MountTypes(Enum):
    MOUNT = "mount"
    BIND = "bind"




