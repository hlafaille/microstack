from microstack.schemas import Network, Service, Mount


# Networks
class MyBackend(Network):
    """My backend network!"""


class MyFrontend(Network):
    """My frontend network!"""


# Services
class Frontend(Service):
    image: str = "alpine:latest"
    name: str = "frontend"
    networks: list[Network] = [MyBackend()]
    mounts: list[Mount] = [Mount(source="/path/to/my/frontend/development/repo", target="/app")]


class Backend(Service):
    image: str = "alpine:latest"
    name: str = "frontend"
    networks: list[Network] = [MyBackend()]
    mounts: list[Mount] = [Mount(source="/path/to/my/backend/development/repo", target="/app")]


class Nginx(Service):
    image: str = "nginx:latest"
    name: str = "nginx"
    networks: list[Network] = [MyBackend()]