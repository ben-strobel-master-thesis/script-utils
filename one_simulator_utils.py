from sys import platform
import subprocess
import os
import shutil

x_shift = 1289629.9778929972
y_shift = 6128904.62296110

simulation_center_x = 1287695.3472707325
simulation_center_y = 6098257.544913205

center_offset_x = x_shift - simulation_center_x
center_offset_y = y_shift - simulation_center_y

simulation_shift_x = 25
simulation_shift_y = -75

simulation_scale = 0.5

def setup_one_simulator():
    path_str = "./the-one/compile.sh" if platform == "linux" or platform == "darwin" else ".\\the-one\\compile.bat"
    process = subprocess.run([os.path.abspath(path_str)], cwd="./the-one")
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
    process = subprocess.run([os.path.abspath(path_str), "-b", "1", config_arg_str], cwd="./the-one")
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)

def convert_one_simulator_output_to_emercast_scenario(input_file_path, output_file_path):
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
                x = segments[1]
                y = segments[2]
                data.append(f'{cmd} {id} {x} {y}\n')
        data.append("Broadcast 0 525 300 5\n")
        data.append("EndSimulation 600\n")
        f.writelines(data)