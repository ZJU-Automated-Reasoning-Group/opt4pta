import argparse
import os
import subprocess

IS_BUILT = True
BASE_PATH = os.getcwd()
SHELL = "bash"

# Task list
TASKS: list[dict] = [
    # {"name": "example", "bc": []},
    {"name": "memcached", "bc": ["./memcached.bc"]},
    {"name": "lua", "bc": ["./lua.bc"]},
    # {"name": "redis", "bc": ["./src/redis-benchmark.bc"]},
    {"name": "tmux", "bc": ["./tmux.bc"]},
    {"name": "vim", "bc": ["./src/vim.bc"]},
    # {"name": "cpython", "bc": ["./python.bc"]},
    # {"name": "deno", "bc": ["./target/x86_64-unknown-linux-gnu/release/deps/deno-*.bc"]}, # !problematic
    # {"name": "gdb-15.1", "bc": ["./build/gdb/gdb.bc"]}, # !problematic
    # ...
]

def is_empty_dir(directory):
    if os.listdir(directory):
        return False
    return True

def run_script(script_path, cwd, args=None):
    if not args:
        args = []
    
    result = subprocess.run([SHELL, script_path, *args], cwd=cwd)
    if result.returncode != 0:
        print(f"Script '{script_path}' failed with return code {result.returncode}")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmark tasks.")
    parser.add_argument("output_base_path", type=str, help="The base path for output files.")
    parser.add_argument("test_script_path", type=str, help="The path to the test script.")
    args = parser.parse_args()

    scripts_base_path = os.path.join(BASE_PATH, "scripts")
    repos_base_path = os.path.join(BASE_PATH, "repos")
    output_base_path = os.path.join(BASE_PATH, args.output_base_path)
    test_script = os.path.join(BASE_PATH, args.test_script_path)
    build_code = None

    for task in TASKS:
        task_name = task["name"]
        print(f"Handling: {task_name}")
        task_scripts_path = os.path.join(scripts_base_path, task_name)
        task_repos_path = os.path.join(repos_base_path, task_name)
        task_output_path = os.path.join(output_base_path, task_name)

        # These directories must be created first
        os.makedirs(task_repos_path, exist_ok=True)
        os.makedirs(task_output_path, exist_ok=True)
        
        download_script = os.path.join(task_scripts_path, "download.sh")
        build_script = os.path.join(task_scripts_path, "build.sh")
        
        # if not is_empty_dir(task_output_path):
        #     print(f"Skip task {task_name} since output folder is not empty.")
        #     continue
        
        if os.path.isfile(download_script):
            if is_empty_dir(task_repos_path):
                run_script(download_script, task_repos_path)
            else:
                print(f"Skip downloading for task {task_name}")
        else:
            print(f"Download script not found for task {task_name}")

        if not IS_BUILT:
            if os.path.isfile(build_script):
                build_code = run_script(build_script, task_repos_path)
            else:
                print(f"Compile script not found for task {task_name}")

        for i, bcfile in enumerate(task["bc"]):
            if IS_BUILT or build_code:
                run_script(test_script, task_repos_path, [task_output_path, bcfile, "_" + str(i)])
            else:
                print(f"Skip testing since building failed with code {build_code}.")

