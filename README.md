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
    name: str = "frontend"


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
```
...run the orchestrator
```
[INFO] dealing with '/home/hunter/PycharmProjects/microstack/stack.py' as our stack description
[INFO] network 'MyBackend' exists, skipping
[INFO] network 'MyFrontend' exists, skipping
[WARNING] mount source '/path/to/my/frontend/development/repo' does not exist on host, will be created by docker
[WARNING] mount source '/path/to/my/backend/development/repo' does not exist on host, will be created by docker
[WARNING] 'alpine:latest' for 'frontend' was not found, pulling
[WARNING] 'alpine:latest' for 'frontend' was not found, pulling
[WARNING] 'nginx:latest' for 'nginx' was not found, pulling
[INFO] running 'frontend'
[INFO] running 'frontend'
[INFO] 'frontend' already exists, skipping
[INFO] running 'nginx'
```
then simply run the script!



# Design


## Input
Microstack can take inputs in one of two modes, passing them along to the parser

### Python Package
Microstack functions as a Python package, allowing developers to build more complex applications with the parser and
format. Simple pass along a list of `Service` schemas to the `parse_stack` function, and receive a list of `list[str]`,
perfect for use with Python's `subprocess` API.

### Pre-Defined Models As Python
Microstack in most scenarios will be configured to read and evaluate *'dumb'* Python files as an entire stack, similar 
to Docker Compose.


## Parser
Our parser accepts a list of `Service` schemas, written with Pydantic, allowing us to maintain reliability through
type enforcement at runtime (and write-time), along with proper IntelliSense compared to other solutions. Depending on
the configuration options defined by the stack, the parser may or may not check to ensure that the specified Networks
and Volumes already exist.


## Output
Microstack will produce an executable Python script (which can be saved to disk), which will bring up your stack. The script
will ensure that all defined networks are created & in the proper state, volumes are created & in the proper state, and
images are built/pulled.