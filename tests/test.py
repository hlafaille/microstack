import importlib
import json

from microstack.compiler import parse_stack_from_file, compile_stack
from microstack.orchestrator import orchestrator_up

if __name__ == "__main__":
    # parse stack from file
    stack_definition = parse_stack_from_file(
        module_path="/home/hunter/PycharmProjects/microstack",
        module_name="stack"
    )

    # compile the stack
    #out = compile_stack(
    #    stack_definition=stack_definition
    #)
    #print("\n\noutput:\n" + out)'

    orchestrator_up(stack_definition)