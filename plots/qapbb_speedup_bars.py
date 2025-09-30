import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
}) 


## parameters
fs0 = 16
fs1 = fs0 - 0
fig_size = (7.6, 5)
width = 0.15
lw0 = 1.25

k_val = [1, 3, 9, 18]

nk = len(k_val)

colors_sp0 = ["limegreen", "darkolivegreen", "palegreen", "forestgreen"]
colors_sp = ["lightcoral", "maroon", "pink", "firebrick"]
colors_mp = ["mediumturquoise", "darkslategray", "aquamarine", "darkcyan"]
textures = ['', '', '//', '\\']
x_labels = [2, 4, 8, 16, 32]
y_labels = [r"$k = 1$", r"$k = 3$", r"$k = 9$", r"$k = 18$"]

x = np.arange(len(x_labels))


##----- data -----##

## K in [2, 4, 8, 16, 32]

# QABB_PB (baseline)
T_seq_rd16 = 277
T_seq_rd20 = 2850

# QAPBB_SP
T_sp_rd16 = np.array([[281, 234, 198, 173, 153],
                      [265, 212, 173, 143, 125],
                      [270, 202, 159, 136, 128],
                      [272, 205, 161, 143, 131]])

T_sp_rd20 = np.array([[2780, 2310, 1940, 1700, 1490],
                      [2570, 2050, 1690, 1440, 1260],
                      [2530, 1950, 1570, 1360, 1230],
                      [2550, 1960, 1610, 1390, 1260]])

S_sp_rd16 = T_seq_rd16 / T_sp_rd16
S_sp_rd20 = T_seq_rd20 / T_sp_rd20

print("\nSpeedups QAPBB_SP rd_20:\n", S_sp_rd20)


# QAPBB_MP

T_mp_rd16 = np.array([[254, 235, 199, 156, 112],
                      [301, 223, 163, 102, 71],
                      [320, 190, 123, 93, 57],
                      [309, 196, 138, 82, 65]])

T_mp_rd20 = np.array([[2570, 2270, 1790, 1390, 1010],
                      [2680, 2010, 1400, 909, 575],
                      [2770, 1740, 1050, 659, 433],
                      [2840, 1680, 1010, 632, 382]])

S_mp_rd16 = T_seq_rd16 / T_mp_rd16
S_mp_rd20 = T_seq_rd20 / T_mp_rd20

print("\nSpeedups QAPBB_MP rd_20:\n", S_mp_rd20, "\n")


##--------------- QAPBB_SP ---------------##

## rd_16 ##
fig1, ax1 = plt.subplots(figsize=fig_size)
#fig1.suptitle("QAPBB_SP  rd_16", weight="bold")

for i in range(nk):

    offset = width * i
    ax1.bar(x + offset, S_sp_rd16[i], width, color=colors_sp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax1.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax1.set_ylim(0, 3)

ax1.set_xticks(x + width, x_labels)
ax1.tick_params(axis="both", labelsize=fs0)

ax1.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax1.set_ylabel("speedup", fontsize=fs0)

ax1.legend(fontsize=fs1)

ax1.set_axisbelow(True)
ax1.grid()

## rd_20 ##
fig2, ax2 = plt.subplots(figsize=fig_size)
#fig2.suptitle("QAPBB_SP  rd_20", weight="bold")

for i in range(nk):

    offset = width * i
    ax2.bar(x + offset, S_sp_rd20[i], width, color=colors_sp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax2.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax2.set_ylim(0, 3)

ax2.set_xticks(x + width, x_labels)
ax2.tick_params(axis="both", labelsize=fs0)

ax2.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax2.set_ylabel("speedup", fontsize=fs0)
ax2.legend(fontsize=fs1)

ax2.set_axisbelow(True)
ax2.grid()


##--------------- QAPBB_MP ---------------##

## rd_16 ##
fig3, ax3 = plt.subplots(figsize=fig_size)
#fig3.suptitle("QAPBB_MP  rd_16", weight="bold")

for i in range(nk):

    offset = width * i
    ax3.bar(x + offset, S_mp_rd16[i], width, color=colors_mp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax3.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax3.set_ylim(0, 6)

ax3.set_xticks(x + width, x_labels)
ax3.tick_params(axis="both", labelsize=fs0)

ax3.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax3.set_ylabel("speedup", fontsize=fs0)

ax3.legend(fontsize=fs1)

ax3.set_axisbelow(True)
ax3.grid()

## rd_20
fig4, ax4 = plt.subplots(figsize=fig_size)
#fig4.suptitle("QAPBB_MP  rd_20", weight="bold")

for i in range(nk):

    offset = width * i
    ax4.bar(x + offset, S_mp_rd20[i], width, color=colors_mp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax4.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax4.set_ylim(0, 9)

ax4.set_xticks(x + width, x_labels)
ax4.tick_params(axis="both", labelsize=fs0)

ax4.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax4.set_ylabel("speedup", fontsize=fs0)

ax4.legend(fontsize=fs1)

ax4.set_axisbelow(True)
ax4.grid()


fig1.savefig("QAPBB_SP_bars_rd16.pdf", bbox_inches='tight', pad_inches=0.02)
fig2.savefig("QAPBB_SP_bars_rd20.pdf", bbox_inches='tight', pad_inches=0.02)
fig3.savefig("QAPBB_MP_bars_rd16.pdf", bbox_inches='tight', pad_inches=0.02)
fig4.savefig("QAPBB_MP_bars_rd20.pdf", bbox_inches='tight', pad_inches=0.02)


plt.show()
