import pathlib
from sys import platform
import subprocess
import os
import shutil

emercast_sim_lower_corner = (689943.8, 5333949.88)
emercast_sim_upper_corner = (692065.86, 5336041.33)
emercast_sim_center = (691004.83, 5334995.605)

emercast_sim_shift = (0, 258)
emercast_sim_simulation_scale = 0.5

def setup_one_simulator():
    path_str = "./the-one/compile.sh" if platform == "linux" or platform == "darwin" else ".\\the-one\\compile.bat"
    process = subprocess.run(([] if platform == "win32" else ["sh"]) + [os.path.abspath(path_str)], cwd="./the-one")
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)

def run_one_simulator(seed: int, end_time_secs: int, agents_count: int, scenario_name: str, base_settings_file_path: str):
    try:
        os.remove("./scenarios/settings.txt")
    except OSError:
        pass
    shutil.copyfile(base_settings_file_path, "./scenarios/settings.txt")
    with open("./scenarios/settings.txt", "a") as f:
        f.write(f"MovementModel.rngSeed = {seed}\n")
        f.write(f"Scenario.endTime = {end_time_secs}\n")
        f.write(f"Group.nrofHosts = {agents_count}\n")
        f.write(f"Scenario.name = {scenario_name}\n")

    path_str = "./the-one/one.sh" if platform == "linux" or platform == "darwin" else ".\\the-one\\one.bat"
    config_arg_str = "../scenarios/settings.txt" if platform == "linux" or platform == "darwin" else "..\\scenarios\\settings.txt"
    process = subprocess.run(([] if platform == "win32" else ["sh"]) + [os.path.abspath(path_str), "-b", "1", config_arg_str], cwd="./the-one")
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)
    os.remove("./scenarios/settings.txt")

def convert_one_simulator_output_to_emercast_scenario(input_file_path, output_file_path, wkt_min_bounds = (0,0), end_time = 100):
    pathlib.Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(input_file_path, "r") as f:
        read_data = f.readlines()
    with open(output_file_path, "w") as f:
        data = []
        current_timestamp = -10
        first_timestamp = -1
        for line in read_data:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                line = line.replace("[", "").replace("]", "")
                current_timestamp = int(line)
                if first_timestamp == -1:
                    first_timestamp = current_timestamp
            elif line.startswith("p"):
                segments = line.split(" ")
                cmd = "Spawn" if current_timestamp == first_timestamp else "AddDestination"
                id = int(segments[0].replace("p", ""))+1
                x = float(segments[1])
                y = float(segments[2])
                x = (x - (emercast_sim_center[0] - wkt_min_bounds[0])) * emercast_sim_simulation_scale + emercast_sim_shift[0]
                y = (y - (emercast_sim_center[1] - wkt_min_bounds[1])) * emercast_sim_simulation_scale + emercast_sim_shift[1]
                y = -(y - emercast_sim_shift[1]) + emercast_sim_shift[1]
                if x < -500 or 500 < x:
                    continue
                if y < -500 or 500 < y:
                    continue
                data.append(f'{cmd} {id} {x} {y}\n')
        data.append("Broadcast 0 525 300 5\n")
        data.append(f"EndSimulation {end_time}\n")
        f.writelines(data)