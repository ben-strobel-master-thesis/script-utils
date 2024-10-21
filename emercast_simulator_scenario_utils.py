def generate_crossing_scenario(output_file_path):
    with open(output_file_path, "w") as f:
        data = []
        x = -125
        for i in range(1, 51):
            data.append("Spawn " + str(i) + " " + str(x) + " " + "525\n")
            x += 5
        x = -125
        for i in range(1, 51):
            data.append("Spawn " + str(50+i) + " " + str(x) + " " + "-525\n")
            x += 5
        x = -125
        for i in range(1, 51):
            data.append("AddDestination " + str(i) + " " + str(x) + " " + "-525\n")
            x += 5
        x = -125
        for i in range(1, 51):
            data.append("AddDestination " + str(50+i) + " " + str(x) + " " + "525\n")
            x += 5
        data.append("Broadcast 0 525 300 5\n")
        data.append("EndSimulation 600\n")
        f.writelines(data)