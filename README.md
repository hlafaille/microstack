# Microstack
Define your containerized stack in Python.

# Planned
* Implement an abstract syntax tree as compiler 
  output, instead of generating raw Python. This 
  will allow us to implement multiple outputs.


# Usage
Create `stack.py`, describe your stack using familiar names as Python types.
```python
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
    name: str = "backend"
    networks: list[Network] = [MyBackend()]
    mounts: list[Mount] = [Mount(source="/path/to/my/backend/development/repo", target="/app")]


class Nginx(Service):
    image: str = "nginx:latest"
    name: str = "nginx"
    networks: list[Network] = [MyBackend()]
```
...run the orchestrator
```
[INFO] dealing with '/home/hunter/PycharmProjects/microstack/stack.py' as our stack description
[INFO] creating network 'MyBackend'
[INFO] creating network 'MyFrontend'
[WARNING] mount source '/path/to/my/frontend/development/repo' does not exist on host, will be created by docker
[WARNING] mount source '/path/to/my/backend/development/repo' does not exist on host, will be created by docker
[WARNING] 'alpine:latest' for 'frontend' was not found, pulling
[WARNING] 'alpine:latest' for 'backend' was not found, pulling
[WARNING] 'nginx:latest' for 'nginx' was not found, pulling
[INFO] running 'frontend'
[INFO] running 'backend'
[INFO] running 'nginx'
```