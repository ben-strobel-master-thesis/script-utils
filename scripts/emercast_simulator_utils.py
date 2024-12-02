from sys import platform
import os
import urllib.request
import tarfile
import subprocess

def download_emercast_simulator():
    try:
        os.mkdir("../emercast-simulator")
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

def run_emercast_simulator(seed: int, scenario_name: str, scenario_file_path: str, protocol_enabled: bool):
    try:
        os.mkdir("./scenarios./emercast-simulator-output")
    except OSError:
        pass
    if platform != "linux" and platform != "win32":
        raise ValueError("Only linux and win32 are supported")
    if platform == "linux":
        process = subprocess.run(["./emercast-simulator/EmercastSimulator.x86_64",
                        "-batchmode",
                        "-nographics",
                        "-timestamps",
                        "-logFile", f"./scenarios/emercast-simulator-output/{scenario_name}.log",
                        "-Seed", str(seed),
                        "-ScenarioFile", scenario_file_path,
                        "-Protocol-Enabled", str(protocol_enabled)])
    else:
        process = subprocess.run(["wsl",
                        "./emercast-simulator/EmercastSimulator.x86_64",
                        "-batchmode",
                        "-nographics",
                        "-timestamps",
                        "-logFile", f"./scenarios/emercast-simulator-output/{scenario_name}.log",
                        "-Seed", str(seed),
                        "-ScenarioFile", scenario_file_path,
                        "-Protocol-Enabled", str(protocol_enabled)])
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)
