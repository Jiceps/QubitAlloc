import matplotlib.pyplot as plt

# Set Times New Roman
plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
})

# parameters
fs0 = 16
fs1 = fs0 - 2

lw0 = 1.25

col = "g"
marker = "o"
marker_size = 5
linestyles = [':', '--', '-']


# data
it_max = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

rt_rd_14 = [10150, 6320, 5830, 5870, 5980, 6010, 6060, 6080, 6080, 6080]
rt_rd_16 = [15290, 9620, 8880, 8940, 9130, 9380, 9550, 9610, 9630, 9650]
rt_rd_18 = [73630, 45910, 41550, 41050, 42200, 43280, 44140, 44520, 44650, 44680]

nodes_rd_14 = [7.65e6, 3.65e6, 2.89e6, 2.65e6, 2.55e6, 2.51e6, 2.51e6, 2.51e6, 2.51e6, 2.51e6]
nodes_rd_16 = [1.18e7, 5.72e6, 4.54e6, 4.10e6, 3.88e6, 3.81e6, 3.79e6, 3.78e6, 3.77e6, 3.77e6]
nodes_rd_18 = [6.30e7, 3.12e7, 2.45e7, 2.17e7, 2.08e7, 2.04e7, 2.03e7, 2.03e7, 2.03e7, 2.03e7]

# runtime
fig1, ax1 = plt.subplots(figsize=(6.6, 5.2))

ax1.plot(it_max, rt_rd_14, col, marker=marker, markersize=marker_size, linestyle=linestyles[0], lw=lw0, label="rd_14")
ax1.plot(it_max, rt_rd_16, col, marker=marker, markersize=marker_size, linestyle=linestyles[1], lw=lw0, label="rd_16")
ax1.plot(it_max, rt_rd_18, col, marker=marker, markersize=marker_size, linestyle=linestyles[2], lw=lw0, label="rd_18")

ax1.legend(fontsize=fs1)
ax1.set_xlabel(r"$it\_max$", fontsize=fs0)
ax1.set_ylabel("execution time (s)", fontsize=fs0)
ax1.set_xticks(it_max)
ax1.tick_params(axis='both', labelsize=fs0)
ax1.set(yscale="log", ylim=[3e3,1e5])

# visited nodes
fig2, ax2 = plt.subplots(figsize=(6.6, 5.2))

ax2.plot(it_max, nodes_rd_14, col, marker=marker, markersize=marker_size, linestyle=linestyles[0], lw=lw0, label="rd_14")
ax2.plot(it_max, nodes_rd_16, col, marker=marker, markersize=marker_size, linestyle=linestyles[1], lw=lw0, label="rd_16")
ax2.plot(it_max, nodes_rd_18, col, marker=marker, markersize=marker_size, linestyle=linestyles[2], lw=lw0, label="rd_18")

ax2.legend(fontsize=fs1)
ax2.set_xlabel(r"$it\_max$", fontsize=fs0)
ax2.set_ylabel("visited nodes", fontsize=fs0)
ax2.set_xticks(it_max)
ax2.tick_params(axis='both', labelsize=fs0)

# save
#fig1.savefig("../calib_it_max_runtime.pdf", bbox_inches='tight', pad_inches=0.02)
#fig2.savefig("../calib_it_max_nodes.pdf", bbox_inches='tight', pad_inches=0.02)

plt.show()
