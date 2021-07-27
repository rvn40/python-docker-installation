import subprocess

def pre_tasks():  
  dep_packages = ["apt-transport-https", "ca-certificates", "curl", "gnupg", "lsb-release"]
  old_packages = ["docker-engine", "docker.io", "containerd", "runc"]

  try:

    for old_package in old_packages:
      subprocess.run(["sudo", "apt", "remove", "-y", old_package], capture_output=True, check=True)

    gpg_key = subprocess.Popen(["sudo", "gpg", "--dearmor", "--batch", "--yes", "-o", "/usr/share/keyrings/docker-archive-keyring.gpg"], stdin=subprocess.Popen(["sudo", "curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg"], stdout=subprocess.PIPE).stdout, stdout=subprocess.PIPE)

    dist = str(subprocess.check_output(["lsb_release", "-cs"]).decode("utf-8").replace("\n", ""))

    add_repo = subprocess.Popen(["sudo", "echo", "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu "+ dist + " stable"], stdout=subprocess.PIPE)

    subprocess.Popen(["sudo", "tee", "/etc/apt/sources.list.d/docker.list", ">", "/dev/null"], stdin=add_repo.stdout, stdout=subprocess.PIPE)
    
    subprocess.run(["sudo", "apt", "update", "-y"], capture_output=True, check=True) 

    for dep_package in dep_packages:
      subprocess.run(["sudo", "apt", "install", "-y", dep_package], capture_output=True, check=True)

    gpg_key.stdout.close()
    add_repo.stdout.close()

  except subprocess.CalledProcessError as e:
    print(e.output)


def docker_version_list():
  try:
    docker_cache = subprocess.run(["sudo", "apt-cache", "madison", "docker-ce"], capture_output=True, check=True)
    print(str(docker_cache.stdout.decode("utf-8")))
    
  except subprocess.CalledProcessError as e:
    print(e.output)


def install_docker(packages_version):
  try:
    for package_version in packages_version:
      subprocess.run(["sudo", "apt", "install", "-y", package_version], capture_output=True, check=True)
  except subprocess.CalledProcessError as e:
    print(e.output)

if __name__ == "__main__":
  print("Select what you need here: \n")
  print("1. Get list of docker version \n")
  print("2. Install docker \n")
  selection = input("Enter your choice: ") 

  if selection == "1":
    pre_tasks()
    docker_version_list()
  elif selection == "2":
    print("Let it blank to install the latest version !!\n")
    input_packages_version = input("Enter your docker version: ")

    matches = input_packages_version.endswith("-focal")
    pre_tasks()

    if input_packages_version == None and input_packages_version == "":
      packages_version = ["docker-ce", "containerd.io"]
      print(packages_version)
      install_docker(packages_version)
    elif matches:
      packages_version = ["docker-ce="+input_packages_version, "containerd.io"]
      print(packages_version)
      install_docker(packages_version)
    else:
      print("Unrecognize docker version!!")

  else:
    print("Unrecognize options!!")