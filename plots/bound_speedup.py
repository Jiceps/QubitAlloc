import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
}) 

# parameters
fs0 = 16
fs1 = fs0 - 0

lw0 = 1.5

col = "darkblue"
marker = "o"
marker_size = 4
linestyles = [':', '--', '-']

P = [1, 4, 8, 16, 32]

su_10 = [1, 2.7, 4.2, 4.6, 4.6]
su_15 = [1, 2.9, 5.1, 7.0, 7.2]
su_25 = [1, 3.0, 5.6, 7.9, 9.5]



fig, ax = plt.subplots(figsize = (6.2, 5.2))
#fig.suptitle("speedup", weight="bold")

ax.plot(P, P, "k", lw = 1.25, label="ideal")

ax.plot(P, su_10, col, marker=marker, markersize=marker_size, linestyle=linestyles[0], lw=lw0, label=r"$N = 15$")
ax.plot(P, su_15, col, marker=marker, markersize=marker_size, linestyle=linestyles[1], lw=lw0, label=r"$N = 20$")
ax.plot(P, su_25, col, marker=marker, markersize=marker_size, linestyle=linestyles[2], lw=lw0, label=r"$N = 25$")

ax.legend(fontsize=fs1)
ax.set_xlabel("number of threads", fontsize=fs0)
ax.set_ylabel("speedup", fontsize=fs0)
ax.set_xticks(P)
ax.tick_params(axis='both', labelsize=fs0)
ax.grid()
#ax.set_aspect('equal', 'box')

fig.savefig("bound_speedup.pdf", bbox_inches='tight', pad_inches=0.02)

plt.show()
