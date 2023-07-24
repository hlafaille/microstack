from microstack.compiler import parse_stack_from_file
from microstack.orchestrator import orchestrator_up

if __name__ == "__main__":
    # parse stack from file
    stack_definition = parse_stack_from_file(
        module_path="/home/hunter/PycharmProjects/microstack",
        module_name="stack"
    )

    # or, we could orchestrate the stack directly
    orchestrator_up(stack_definition)