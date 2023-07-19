# Microstack
Define your containerized stack in Python.

# Usage
Create `stack.py`, describe your stack using familiar names as Python types.
```python
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
```
...run the compiler
```python
"""
generated by microstack @ 2023-07-19T03:21:24.493209
"""
import subprocess

# action:create_if_not_exists || create network 'backend'
cmd_create_network_backend = subprocess.run(
    args=['docker', 'network', 'create', 'backend', '-d', 'bridge']
)


# action:create_if_not_exists || create network 'frontend'
cmd_create_network_frontend = subprocess.run(
    args=['docker', 'network', 'create', 'frontend', '-d', 'bridge']
)


# action:pull || pull 'mysql'
cmd_pull_mysql = subprocess.run(
    args=['docker', 'pull', 'mysql:latest']
)

# action:run || run 'mysql'
cmd_run_mysql = subprocess.run(
    args=['docker', 'run', 'mysql']
)

# action:pull || pull 'nginx'
cmd_pull_nginx = subprocess.run(
    args=['docker', 'pull', 'nginx:latest']
)

# action:run || run 'nginx'
cmd_run_nginx = subprocess.run(
    args=['docker', 'run', 'nginx']
)

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