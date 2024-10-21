import emercast_simulator_scenario_utils
import one_simulator_utils
import wkt_file_utils

# emercast_simulator_scenario_utils.generate_crossing_scenario("C:\\Users\\bened\\Desktop\\default.emerscenario")
# one_simulator_utils.convert_one_simulator_output_scenario("C:\\Users\\bened\\Desktop\\munich_scenario_LocationSnapshotReport.txt", "C:\\Users\\bened\\Desktop\\test.emerscenario")
wkt_file_utils.remove_unreachable_multilines("C:\\Users\\bened\\Desktop\\munich_roads_squares_walkways.wkt", "C:\\Users\\bened\\Desktop\\processed_walkable_lines.wkt", 1)