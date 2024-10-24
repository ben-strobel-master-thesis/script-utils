import emercast_simulator_scenario_utils
import emercast_simulator_utils
import one_simulator_utils
import wkt_file_utils

# wkt_file_utils.remove_unreachable_multilines("./scenarios/intermediate_walkable_lines.wkt", "./scenarios/emercast_city_model.wkt", 1)
# one_simulator_utils.setup_one_simulator()
# emercast_simulator_utils.download_emercast_simulator()
one_simulator_utils.run_one_simulator(1, 1000, 500, "random-city-1", "./scenarios/one-simulator-settings-baseline-random-city-scenario.txt")
one_simulator_utils.convert_one_simulator_output_to_emercast_scenario("./scenarios/one-simulator-output/random-city-1_LocationSnapshotReport.txt", "./scenarios/emercast-simulator-input/random-city-1.emerscenario")
emercast_simulator_utils.run_emercast_simulator(1, "random-city-1", "./emercast-simulator/default.emerscenario")
#emercast_simulator_utils.run_emercast_simulator(1, "random-city-1", "./scenarios/emercast-simulator-input/random-city-1.emerscenario")