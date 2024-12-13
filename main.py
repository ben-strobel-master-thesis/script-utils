from scripts import emercast_simulator_utils, emercast_simulator_analyzer, one_simulator_utils, wkt_file_utils

min_bound = (689016.97, 5333281.47)
wkt_file_utils.remove_unreachable_multilines("./scenarios/intermediate_walkable_lines.wkt", "./scenarios/emercast_city_model.wkt", 0)
wkt_file_utils.create_skeleton_with_fingers("./scenarios/emercast_city_model.wkt", "./scenarios/emercast_city_model_skeleton.wkt")
one_simulator_utils.setup_one_simulator()
emercast_simulator_utils.download_emercast_simulator()

def run_experiment_with_analysis(seed, scenario_name, duration, agent_count, outage_cover_percentage):
    file_name = f"{scenario_name}-{seed}"
    run_experiment(seed, scenario_name, duration, agent_count, outage_cover_percentage)
    emercast_simulator_analyzer.analyze_single_log(f"./scenarios/emercast-simulator-output/{file_name}-enabled.log", agent_count)
    emercast_simulator_analyzer.analyze_single_log(f"./scenarios/emercast-simulator-output/{file_name}-disabled.log", agent_count)

def run_experiment(seed, scenario_name, duration, agent_count, outage_cover_percentage):
    file_name = f"{scenario_name}-{seed}"
    one_simulator_utils.run_one_simulator(seed, duration, agent_count, file_name, "./scenarios/one-simulator-settings-baseline-random-city-scenario.txt")
    one_simulator_utils.convert_one_simulator_output_to_emercast_scenario(f"./scenarios/one-simulator-output/{file_name}_LocationSnapshotReport.txt", f"./scenarios/emercast-simulator-input/{file_name}-enabled.emerscenario", outage_cover_percentage, min_bound, duration)
    one_simulator_utils.convert_one_simulator_output_to_emercast_scenario(f"./scenarios/one-simulator-output/{file_name}_LocationSnapshotReport.txt", f"./scenarios/emercast-simulator-input/{file_name}-disabled.emerscenario", outage_cover_percentage, min_bound, duration)
    emercast_simulator_utils.run_emercast_simulator(seed, f"{file_name}-enabled", f"./scenarios/emercast-simulator-input/{file_name}-enabled.emerscenario", True)
    emercast_simulator_utils.run_emercast_simulator(seed, f"{file_name}-disabled", f"./scenarios/emercast-simulator-input/{file_name}-disabled.emerscenario", False)

seeds = [1,2,3,4,5]
agent_counts = [1000, 5000, 10000]
outage_area_coverages = [0.2, 0.4, 0.6, 0.8]
duration = 1500

for seed in seeds:
    for agent_count in agent_counts:
        for outage_area_coverage in outage_area_coverages:
            run_experiment(seed, f"random-city-{seed}-{agent_count}-{outage_area_coverage}", duration, agent_count, outage_area_coverage)

emercast_simulator_analyzer.analyze_batch_log("./scenarios/emercast-simulator-output", "random-city", duration, seeds, agent_counts, outage_area_coverages)