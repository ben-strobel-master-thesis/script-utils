def remove_unreachable_multilines(input_file_path, output_file_path, root_multi_line_string_index = 0):
    with open(input_file_path, "r") as f:
        read_data = f.readlines()
    vertices_sets = list()
    vertices_lists = list()
    connected_vertices = set()
    connected_multi_line_indexes = set()

    # Parsing wkt file
    i = 0
    for fileline in read_data:
        fileline = fileline.upper().replace("MULTILINESTRING", "").replace("LINESTRING", "").strip()
        linestrings = fileline.split("),(")
        for linestring in linestrings:
            linestring = linestring.replace("(", "").replace(")", "").strip()
            segments = linestring.split(", ")
            vertices_set = set()
            vertices_list = list()
            for segment in segments:
                coords = segment.split(" ")
                if len(coords) != 2:
                    continue
                vertices_set.add((coords[0], coords[1]))
                vertices_list.append((coords[0], coords[1]))
                if i == root_multi_line_string_index:
                    connected_vertices.add((coords[0], coords[1]))
            vertices_sets.append(vertices_set)
            vertices_lists.append(vertices_list)
            i += 1

    # Expanding known connected graph (contains first multi line as root), until an expansion iteration doesn't yield any new vertices
    found_new_in_last_iteration = True
    iteration_number = 0
    while found_new_in_last_iteration:
        iteration_number += 1
        found_new_in_last_iteration = False
        print(f"Iteration {iteration_number} Connected Vertices: {len(connected_vertices)}")
        for i in range(len(vertices_sets)):
            group = vertices_sets[i]
            intersection = group.intersection(connected_vertices)
            if len(intersection) > 0:
                connected_vertices_len_before_add = len(connected_vertices)
                for vertex in group:
                    connected_vertices.add(vertex)
                if len(connected_vertices) > connected_vertices_len_before_add:
                    found_new_in_last_iteration = True
                    connected_multi_line_indexes.add(i)

    print(f"Total vertices: {sum([len(x) for x in vertices_sets])} connected vertices: {len(connected_vertices)}")
    print(f"Total linestrings: {len(read_data)} connected linestrings: {len(connected_multi_line_indexes)}")

    min_x = float("inf")
    min_y = float("inf")

    # Writing filtered wkt file
    with open(output_file_path, "w") as f:
        for i in range(len(vertices_lists)):
            if i in connected_multi_line_indexes:
                for v in vertices_lists[i]:
                    if float(v[0]) < min_x:
                        min_x = float(v[0])
                    if float(v[1]) < min_y:
                        min_y = float(v[1])
                f.write(f"LINESTRING ({', '.join([t[0] + ' ' + t[1] for t in vertices_lists[i]])})\n\n")
    return min_x, min_y