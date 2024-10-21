x_shift = 1289629.9778929972
y_shift = 6128904.62296110

simulation_center_x = 1287695.3472707325
simulation_center_y = 6098257.544913205

center_offset_x = x_shift - simulation_center_x
center_offset_y = y_shift - simulation_center_y

simulation_shift_x = 25
simulation_shift_y = -75

simulation_scale = 0.5

def convert_one_simulator_output_scenario(input_file_path, output_file_path):
    with open(input_file_path, "r") as f:
        read_data = f.readlines()
    with open(output_file_path, "w") as f:
        data = []
        current_timestamp = -10
        for line in read_data:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                line = line.replace("[", "").replace("]", "")
                current_timestamp = int(line)
            elif line.startswith("p"):
                segments = line.split(" ")
                cmd = "Spawn" if current_timestamp == 1 else "AddDestination"
                id = int(segments[0].replace("p", ""))+1
                x = segments[1]
                y = segments[2]
                data.append(f'{cmd} {id} {x} {y}\n')
        data.append("Broadcast 0 525 300 5\n")
        data.append("EndSimulation 600\n")
        f.writelines(data)