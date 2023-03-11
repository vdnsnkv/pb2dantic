import argparse
import importlib.util
from pathlib import Path

from .pydantic_gen import pydantic_module

parser = argparse.ArgumentParser(
    description="Generate pydantic model definitions from proto file"
)
parser.add_argument(
    "input_proto",
    type=str,
    nargs=1,
    help="input proto file",
)


def _import_module_from_file_path(file_path: Path):
    spec = importlib.util.spec_from_file_location(
        "module_name",
        file_path.absolute(),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    args = parser.parse_args()

    input_file_path = Path(args.input_proto[0])

    pb2_module = _import_module_from_file_path(input_file_path)

    print(f"Generating pydantic models for proto: {input_file_path.absolute()}")

    module_contents = pydantic_module(pb2_module.DESCRIPTOR, input_file_path.name)

    print("\n" + module_contents + "\n")

    output_file_name = (
        str(input_file_path.absolute()).replace("_pb2", "").replace(".py", "_output.py")
    )

    print(f"Saving result to: {output_file_name}")

    with open(output_file_name, "w") as f:
        f.write(module_contents)
