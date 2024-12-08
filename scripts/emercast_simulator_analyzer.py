import os

import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from scipy.interpolate import interp1d, interp2d
from matplotlib.collections import EventCollection

figures_output_folder = "./figures"

def analyze_single_log(log_file, max_agents):
    metrics, ce, poor, cto, mt = parse_log_file(log_file)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    agents_with_message_value = [x[2] for x in metrics]
    agents_with_message_time = [x[0] for x in metrics]

    agents_without_message_value = [x[3] for x in metrics]
    agents_without_message_time = [x[0] for x in metrics]

    ax.plot(agents_with_message_time, agents_with_message_value, color="tab:blue")
    ax.plot(agents_without_message_time, agents_without_message_value, color="tab:orange")

    events_ce = EventCollection([x[2] for x in ce], color="purple", linelength=0.05)
    events_poor = EventCollection([x[2] for x in poor], color="yellow", linelength=0.05)
    events_cto = EventCollection([x[1] for x in cto], color="red", linelength=0.05)
    events_mt = EventCollection([x[3] for x in mt], color="green", linelength=0.05)

    ax.add_collection(events_ce)
    ax.add_collection(events_poor)
    ax.add_collection(events_cto)
    ax.add_collection(events_mt)

    ax.set_ylim([0, max_agents])

    ax.set_title(f"Emercast log analysis")
    plt.show()


def analyze_batch_log(folder_path, scenario_base_name, duration, seeds, agent_counts, outage_area_coverages):
    if not os.path.exists(figures_output_folder):
        os.makedirs(figures_output_folder)
    metric_averages, metric_timestamps = get_batch_average_metrics(folder_path, scenario_base_name, 1500, seeds, agent_counts, outage_area_coverages)
    create_enabled_disabled_plot(metric_averages, metric_timestamps)
    create_outage_area_plot(metric_averages, metric_timestamps, outage_area_coverages)
    create_agent_count_plot(metric_averages, metric_timestamps, agent_counts)
    event_averages = get_batch_event_data(folder_path, scenario_base_name, seeds, agent_counts, outage_area_coverages)
    create_message_hops_plot(event_averages, outage_area_coverages, agent_counts)
    create_connection_established_per_message_delivered_plot(event_averages, outage_area_coverages, agent_counts)


def create_message_hops_plot(event_averages, outage_area_coverages, agent_counts):
    protocol_status = "enabled"
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    num_interpolated_lines = 15

    x_orig = np.array(agent_counts)
    y_orig = np.array(outage_area_coverages)

    X_orig, Y_orig = np.meshgrid(x_orig, y_orig)
    Z_orig = np.array([([event_averages[f"{agent_value}-{outage_value}-{protocol_status}"][4] for agent_value in agent_counts]) for outage_value in outage_area_coverages])

    f = interp2d(X_orig, Y_orig, Z_orig)
    x = np.linspace(x_orig.min(), x_orig.max(), num_interpolated_lines)
    y = np.linspace(y_orig.min(), y_orig.max(), num_interpolated_lines)
    X, Y = np.meshgrid(x, y)
    Z = f(x,y)

    ax.set_xlim([0, 10000])
    ax.set_ylim([0.2, 0.8])
    ax.set_zlim([0, 10])

    norm = plt.Normalize(0, 10)
    colors = cm.jet(norm(Z))
    surface = ax.plot_surface(X, Y, Z, facecolors=colors, shade=False, norm=norm)
    surface.set_facecolor((0, 0, 0, 0))

    ax.set_xticks([1000, 5000, 10000])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_zticks([0, 2, 4, 6, 8, 10])

    sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=norm)
    sm.set_array([])

    ax.set_xlabel("Agent count")
    ax.set_ylabel("Outage area %")
    ax.set_zlabel("Average hops\nto transmit message")

    plt.colorbar(sm, ax=ax, pad=0.15, shrink=0.75)
    fig.tight_layout()
    plt.savefig(f"{figures_output_folder}/connection_hops_plot.svg")
    plt.show()

def create_connection_established_per_message_delivered_plot(event_averages, outage_area_coverages, agent_counts):
    protocol_status = "enabled"
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    num_interpolated_lines = 15

    x_orig = np.array(agent_counts)
    y_orig = np.array(outage_area_coverages)

    X_orig, Y_orig = np.meshgrid(x_orig, y_orig)
    Z_orig = np.array([([(event_averages[f"{agent_value}-{outage_value}-{protocol_status}"][3] / event_averages[f"{agent_value}-{outage_value}-{protocol_status}"][0]) for agent_value in agent_counts]) for outage_value in outage_area_coverages])

    f = interp2d(X_orig, Y_orig, Z_orig)
    x = np.linspace(x_orig.min(), x_orig.max(), num_interpolated_lines)
    y = np.linspace(y_orig.min(), y_orig.max(), num_interpolated_lines)
    X, Y = np.meshgrid(x, y)
    Z = f(x, y)

    ax.set_xlim([0, 10000])
    ax.set_ylim([0.2, 0.8])

    norm = plt.Normalize(0, 1)
    colors = cm.jet(norm(Z))
    surface = ax.plot_surface(X, Y, Z, facecolors=colors, shade=False, norm=norm)
    surface.set_facecolor((0, 0, 0, 0))

    ax.set_xticks([1000, 5000, 10000])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])

    sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=norm)
    sm.set_array([])

    ax.set_xlabel("Agent count")
    ax.set_ylabel("Outage area %")
    ax.set_zlabel("Message delivered\nby connection %", labelpad=10)

    plt.colorbar(sm, ax=ax, pad=0.15, shrink=0.75)
    fig.tight_layout()
    plt.savefig(f"{figures_output_folder}/connection_established_per_message_delivered_.svg")
    plt.show()


def create_enabled_disabled_plot(metric_averages, metric_timestamps):
    agentcount = 1000

    agents_0_2_enabled = metric_averages[f"{agentcount}-{0.2}-enabled"]
    agents_0_2_disabled = metric_averages[f"{agentcount}-{0.2}-disabled"]

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.set_ylim(0, agentcount)
    ax.set_xlim([0, 1500])
    ax.set_xticks([0, 300, 600, 900, 1200, 1500])

    ax.set_xlabel("Time in s")
    ax.set_ylabel("Agents with message", labelpad=5)

    ax.plot(metric_timestamps, agents_0_2_enabled, color="tab:blue", label="Without Emercast System")
    ax.plot(metric_timestamps, agents_0_2_disabled, color="tab:orange", label="With Emercast System")
    ax.legend(loc="lower left")
    fig.tight_layout()
    plt.savefig(f"{figures_output_folder}/enabled_disabled_by_timestamp.svg")
    plt.show()


def create_outage_area_plot(metric_averages, metric_timestamps, outage_area_coverages):
    agent_count = 10000
    protocol_status = "enabled"
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    y = np.array(outage_area_coverages)
    num_interpolated_lines = 15
    y = np.linspace(y.min(), y.max(), num_interpolated_lines)

    x = metric_timestamps
    X, Y = np.meshgrid(x, y)

    z = np.array([metric_averages[f"{agent_count}-{value}-{protocol_status}"] for value in outage_area_coverages])
    z = interp1d(
        np.linspace(0, z.shape[0] - 1, z.shape[0]), z, axis=0, kind='linear'
    )(np.linspace(0, z.shape[0] - 1, num_interpolated_lines))

    ax.set_xlim([0, 1500])
    ax.set_ylim([0.2, 0.8])

    norm = plt.Normalize(0, 10000)
    colors = cm.jet(norm(z))
    surface = ax.plot_surface(X, Y, z, facecolors=colors, shade=False, norm=norm)
    surface.set_facecolor((0, 0, 0, 0))
    ax.set_xlim(ax.get_xlim()[::-1])
    ax.set_zlim([0, 10000])

    ax.set_xlabel("Time in s")
    ax.set_ylabel("Outage area %")
    ax.set_zlabel("Agents with message", labelpad=5)

    ax.set_xticks([0, 300, 600, 900, 1200, 1500])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])

    sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=norm)
    sm.set_array([])

    plt.colorbar(sm, ax=ax, pad=0.15, shrink=0.75)
    plt.savefig(f"{figures_output_folder}/outage_area_by_timestamp.svg")
    fig.tight_layout()
    plt.show()


def create_agent_count_plot(metric_averages, metric_timestamps, agent_counts):
    outage_area_coverage = 0.8
    protocol_status = "enabled"
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    y = np.array(agent_counts)
    num_interpolated_lines = 15
    y = np.linspace(y.min(), y.max(), num_interpolated_lines)

    x = metric_timestamps
    X, Y = np.meshgrid(x, y)

    z = np.array([metric_averages[f"{value}-{outage_area_coverage}-{protocol_status}"] for value in agent_counts])
    z = interp1d(
        np.linspace(0, z.shape[0] - 1, z.shape[0]), z, axis=0, kind='linear'
    )(np.linspace(0, z.shape[0] - 1, num_interpolated_lines))

    ax.set_xlim([0, 1500])
    ax.set_ylim([0, 1000])
    ax.set_zlim([0, 10000])

    norm = plt.Normalize(0, 10000)
    colors = cm.jet(norm(z))
    surface = ax.plot_surface(X, Y, z, facecolors=colors, shade=False, norm=norm)
    surface.set_facecolor((0, 0, 0, 0))

    ax.set_xlim(ax.get_xlim()[::-1])
    ax.set_xlabel("Time in s")
    ax.set_ylabel("Agent count")
    ax.set_zlabel("Agents with message", labelpad=5)

    ax.set_xticks([0, 300, 600, 900, 1200, 1500])
    ax.set_yticks([1000, 5000, 10000])

    sm = plt.cm.ScalarMappable(cmap=cm.jet, norm=norm)
    sm.set_array([])

    plt.colorbar(sm, ax=ax, pad=0.15, shrink=0.75)
    plt.savefig(f"{figures_output_folder}/agent_count_by_timestamp.svg")
    fig.tight_layout()
    plt.show()


def get_batch_event_data(folder_path, scenario_base_name, seeds, agent_counts, outage_area_coverages):
    event_averages = {}
    status = "enabled"

    for agent_count in agent_counts:
            for outage_area_coverage in outage_area_coverages:
                count = 0
                event_sum = np.zeros(5)

                for seed in seeds:
                    _, connection_established, peer_out_of_range, connection_timed_out, message_transmitted = parse_log_file(f"{folder_path}/{scenario_base_name}-{seed}-{agent_count}-{outage_area_coverage}-{seed}-{status}.log")
                    average_hops = np.average(np.array([value[2] for value in message_transmitted]))
                    event_sum += np.array([len(connection_established), len(peer_out_of_range), len(connection_timed_out), len(message_transmitted), average_hops])
                    count += 1
                event_averages[f"{agent_count}-{outage_area_coverage}-{status}"] = np.divide(event_sum, count)
    return event_averages


def get_batch_average_metrics(folder_path, scenario_base_name, duration, seeds, agent_counts, outage_area_coverages):
    protocol_status = ["enabled", "disabled"]
    metric_timestamps = np.arange(0, duration + 1, 5)
    metric_averages = {}

    for agent_count in agent_counts:
        for status in protocol_status:
            for outage_area_coverage in outage_area_coverages:
                count = 0
                metric_sum = np.zeros_like(metric_timestamps)

                for seed in seeds:
                    metrics, _, _, _, _ = parse_log_file(f"{folder_path}/{scenario_base_name}-{seed}-{agent_count}-{outage_area_coverage}-{seed}-{status}.log")
                    timestamps = np.array([m[0] for m in metrics])
                    counts_with_message = np.array([m[2] for m in metrics])
                    interpolated_counts_with_message = np.interp(metric_timestamps, timestamps, counts_with_message)
                    metric_sum = metric_sum + interpolated_counts_with_message
                    count += 1
                metric_averages[f"{agent_count}-{outage_area_coverage}-{status}"] = np.divide(metric_sum, count)
    return metric_averages, metric_timestamps


def parse_log_file(log_file):
    metrics = []
    events_connection_established = []
    events_peer_out_of_range = []
    events_connection_timed_out = []
    events_message_transmitted = []

    with open(log_file, 'r') as f:
        for line in f:
            segments = line.split("|")
            if len(segments) < 3:
                continue
            if segments[2] == "EVENTS":
                if segments[3] == "CONNECTION_ESTABLISHED":
                    events_connection_established.append((int(segments[4]), int(segments[5]), float(segments[6])))
                elif segments[3] == "CONNECTION_OUT_OF_RANGE":
                    events_peer_out_of_range.append((int(segments[4]), int(segments[5]), float(segments[6])))
                elif segments[3] == "PROTOCOL_TIMED_OUT":
                    events_connection_timed_out.append((int(segments[4]), float(segments[5])))
                elif segments[3] == "MESSAGE_TRANSMITTED":
                    events_message_transmitted.append((int(segments[4]), int(segments[5]), int(segments[6]), float(segments[7])))
            elif segments[2] == "METRICS":
                simulated_time = float(segments[3])
                real_time = float(segments[4])
                agents_with_message = int(segments[5])
                agents_without_message = int(segments[6])
                metrics.append((simulated_time, real_time, agents_with_message, agents_without_message))

    return metrics, events_connection_established, events_peer_out_of_range, events_connection_timed_out, events_message_transmitted
