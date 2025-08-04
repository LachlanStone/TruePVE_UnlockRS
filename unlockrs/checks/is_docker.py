import os
def is_docker(PROJECT_ROOT):
    result = (
        os.path.exists("/.dockerenv")
        or os.path.isfile("/proc/1/cgroup")
        and any("docker" in line for line in open("/proc/1/cgroup"))
    )
    if result == True:
        dir_path = "$HOME/config"
        return dir_path
    else:
        dir_path = PROJECT_ROOT
        return dir_path
