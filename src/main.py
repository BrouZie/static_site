# import shutil
# import os
#
# def copy_from_static():
#     os.mkdir("dick")
#     
    # shutil.rmtree()

# def main():
#     print(dest_dir)
#     print(os.listdir("static"))
#
# if __name__ == "__main__":
#     main()

import os, sys
from pathlib import Path

print("Python:", sys.version)
print("Platform os.name:", os.name)         # 'posix' on Linux
print("Current user id:", os.geteuid() if hasattr(os, "geteuid") else "n/a")

# 1) Where am I?
print("CWD:", os.getcwd())

# 2) Make a directory you definitely can write to
test_dir = Path("/tmp/os_test_dir")         # /tmp is writable on Linux
try:
    os.mkdir(test_dir)                      # will fail if it already exists
    print("Created:", test_dir)
except FileExistsError:
    print("Already exists:", test_dir)
except PermissionError as e:
    print("PermissionError:", e)
except OSError as e:
    print("OSError:", e)

# 3) Prefer this if parents may not exist or you want 'exist_ok'
Path("/tmp/nested/a/b").mkdir(parents=True, exist_ok=True)
print("Ensured:", "/tmp/nested/a/b")
