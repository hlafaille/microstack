from microstack.schemas import Network, Service


# Networks
class MyBackend(Network):
    """My backend network!"""
    name: str = "backend"


class MyFrontend(Network):
    """My frontend network!"""
    name: str = "frontend"


# Services
class MySQL(Service):
    image: str = "mysql:latest"
    name: str = "mysql"  # not required, leaving None will make this name lowercase
    networks: list[Network] = [MyBackend()]


class Nginx(Service):
    image: str = "nginx:latest"
    name: str = "nginx"  # not required, leaving None will make this name lowercase
    networks: list[Network] = [MyBackend()]