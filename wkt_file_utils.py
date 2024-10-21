def remove_unreachable_multilines(input_file_path, output_file_path, root_multi_line_string_index = 1):
    with open(input_file_path, "r") as f:
        read_data = f.readlines()
    vertices_groups = list()
    connected_vertices = set()
    connected_multi_line_indexes = set()

    # Parsing wkt file
    for i in range(len(read_data)):
        line = read_data[i]
        line = line.replace("MultiLineString ((", "").replace("))", "")
        segments = line.split(", ")
        vertices = set()
        for segment in segments:
            coords = segment.split(" ")
            vertices.add((coords[0], coords[1]))
            if i == root_multi_line_string_index:
                connected_vertices.add((coords[0], coords[1]))
        vertices_groups.append(vertices)

    # Expanding known connected graph (contains first multi line as root), until an expansion iteration doesn't yield any new vertices
    found_new_in_last_iteration = True
    iteration_number = 0
    while found_new_in_last_iteration:
        iteration_number += 1
        found_new_in_last_iteration = False
        print(f"Iteration {iteration_number} Connected Vertices: {len(connected_vertices)}")
        for i in range(len(vertices_groups)):
            group = vertices_groups[i]
            intersection = group.intersection(connected_vertices)
            if len(intersection) > 0:
                connected_vertices_len_before_add = len(connected_vertices)
                for vertex in group:
                    connected_vertices.add(vertex)
                if len(connected_vertices) > connected_vertices_len_before_add:
                    found_new_in_last_iteration = True
                    connected_multi_line_indexes.add(i)

    print(f"Total vertices: {sum([len(x) for x in vertices_groups])} connected vertices: {len(connected_vertices)}")
    print(f"Total multi lines: {len(read_data)} connected multi lines: {len(connected_multi_line_indexes)}")

    # Writing filtered wkt file
    with open(output_file_path, "w") as f:
        for i in range(len(read_data)):
            if i in connected_multi_line_indexes:
                f.write(read_data[i])