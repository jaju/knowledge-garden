from utils import script_main, run_script

@script_main
def main():
    print("Hello from llm-from-scratch!")


@script_main
def main2(name):
    print(f"Hello from llm-from-scratch, {name}!")


if __name__ == "__main__":
    run_script()
