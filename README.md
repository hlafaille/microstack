# Microstack
Define your containerized stack in Python.


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