import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection


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
                    events_peer_out_of_range.append((int(segments[4]), int(segments[5]), int(segments[6]), float(segments[7])))
            elif segments[2] == "METRICS":
                simulated_time = float(segments[3])
                real_time = float(segments[4])
                agents_with_message = int(segments[5])
                agents_without_message = int(segments[6])
                metrics.append((simulated_time, real_time, agents_with_message, agents_without_message))

    return metrics, events_connection_established, events_peer_out_of_range, events_connection_timed_out, events_message_transmitted
