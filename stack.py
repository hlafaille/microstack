from microstack.schemas import Network, Service, Mount


# Networks
class MyBackend(Network):
    """My backend network!"""


class MyFrontend(Network):
    """My frontend network!"""
    name: str = "frontend"


# Services
class Ubuntu(Service):
    image: str = "ubuntu:latest"
    name: str = "ubuntu"
    networks: list[Network] = [MyBackend()]
    mounts: list[Mount] = [Mount(source="/home/hunter/Downloas", target="/downloads")]


class Nginx(Service):
    image: str = "nginx:latest"
    name: str = "nginx"
    networks: list[Network] = [MyBackend()]