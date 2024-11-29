import matplotlib.pyplot as plt
import numpy as np


means = [3.286, 1.861, 0.522]
std_dev = [0.447, 1.303, 0.242]
x_pos = np.arange(len(means))

fig, ax = plt.subplots()
ax.bar(x_pos, means, yerr=std_dev, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Time in seconds')
ax.set_xticks(x_pos)
ax.set_xticklabels(["Backend to device \nwith internet", "First advertisement to \nconnection request", "Connection requested\nuntil teardown"])
ax.set_title('Phases of the Emercast prototype')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
plt.savefig('bar_plot_with_error_bars.svg')
plt.show()