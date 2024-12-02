from scripts import emercast_simulator_utils, emercast_simulator_analyzer, one_simulator_utils

min_bound = (689016.97, 5333281.47)

# Random city scenario runs
scenario_name = "random-city"
duration = 800
agent_count = 1000
outage_cover_percentage = 0.5
protocol_enabled = True

seed = 1
file_name = f"{scenario_name}-{seed}"
one_simulator_utils.run_one_simulator(seed, duration, agent_count, file_name, "./scenarios/one-simulator-settings-baseline-random-city-scenario.txt")
one_simulator_utils.convert_one_simulator_output_to_emercast_scenario(f"./scenarios/one-simulator-output/{file_name}_LocationSnapshotReport.txt", f"./scenarios/emercast-simulator-input/{file_name}.emerscenario", outage_cover_percentage, min_bound, duration)
emercast_simulator_utils.run_emercast_simulator(seed, file_name, f"./scenarios/emercast-simulator-input/{file_name}.emerscenario", protocol_enabled)
emercast_simulator_analyzer.analyze_single_log(f"./scenarios/emercast-simulator-output/{file_name}.log", agent_count)