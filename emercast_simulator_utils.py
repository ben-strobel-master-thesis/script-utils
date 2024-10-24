from sys import platform
import os
import urllib.request
import tarfile
import subprocess

def download_emercast_simulator():
    try:
        os.mkdir("./emercast-simulator")
    except OSError:
        pass
    print("Downloading emercast simulator archive...")
    urllib.request.urlretrieve("https://benstrobel.b-cdn.net/master-thesis/emercast-simulator/latest.tar", "./emercast-simulator/emercast-simulator.tar")
    print("Download complete. Expanding archive...")
    tar = tarfile.open("./emercast-simulator/emercast-simulator.tar", "r:")
    tar.extractall("./emercast-simulator")
    tar.close()
    os.remove("./emercast-simulator/emercast-simulator.tar")
    print("Done")

def run_emercast_simulator(seed: int, scenario_name: str, scenario_file_path: str):
    try:
        os.mkdir("./emercast-simulator/logs")
    except OSError:
        pass
    if platform != "linux" and platform != "win32":
        raise ValueError("Only linux and win32 are supported")
    if platform == "linux":
        process = subprocess.run(["./emercast-simulator/EmercastSimulator.x86_64",
                        "-batchmode",
                        "-nographics",
                        "-timestamps",
                        "-logFile", f"./emercast-simulator/logs/{scenario_name}.log",
                        "-Seed", str(seed),
                        "-ScenarioFile", scenario_file_path])
    else:
        process = subprocess.run(["wsl", "--exec",
                        "./emercast-simulator/EmercastSimulator.x86_64",
                        "-batchmode",
                        "-nographics",
                        "-timestamps",
                        "-logFile", f"./emercast-simulator/logs/{scenario_name}.log",
                        "-Seed", str(seed),
                        "-ScenarioFile", scenario_file_path])
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)
