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
T_seq_rd14 = 1540
T_seq_rd16 = 2400
T_seq_rd18 = 11530

# QAPBB_SP
T_sp_rd14 = np.array([[1560, 1280, 1080, 940, 840],
                      [1320, 1070, 910, 770, 700],
                      [1240, 990, 820, 730, 670],
                      [1220, 960, 810, 730, 710]])

T_sp_rd16 = np.array([[2430, 1980, 1650, 1430, 1240],
                      [2030, 1650, 1390, 1200, 1050],
                      [1910, 1530, 1270, 1150, 1030],
                      [1870, 1480, 1260, 1140, 1050]])

T_sp_rd18 = np.array([[11760, 9500, 7950, 6940, 6100],
                      [9680, 7940, 6730, 5910, 5180],
                      [9020, 7330, 6140, 5490, 5030],
                      [9610, 7110, 6190, 5340, 5130]])

S_sp_rd14 = T_seq_rd14 / T_sp_rd14
S_sp_rd16 = T_seq_rd16 / T_sp_rd16
S_sp_rd18 = T_seq_rd18 / T_sp_rd18


# QAPBB_MP

T_mp_rd14 = np.array([[1360, 1160, 960, 770, 590],
                      [1330, 1030, 760, 500, 350],
                      [1370, 920, 560, 390, 240],
                      [1400, 840, 540, 330, 250]])

T_mp_rd16 = np.array([[1970, 1720, 1420, 1180, 871],
                      [1960, 1580, 1160, 780, 460],
                      [2090, 1350, 810, 530, 320],
                      [2020, 1190, 740, 460, 330]])

T_mp_rd18 = np.array([[10310, 8720, 7405, 5540, 3990],
                      [10170, 7940, 5900, 3580, 2250],
                      [10190, 6490, 4040, 2420, 1520],
                      [9620, 5890, 3580, 2110, 1330]])

S_mp_rd14 = T_seq_rd14 / T_mp_rd14
S_mp_rd16 = T_seq_rd16 / T_mp_rd16
S_mp_rd18 = T_seq_rd18 / T_mp_rd18


##--------------- QAPBB_SP ---------------##

## rd_14 ##
fig1, ax1 = plt.subplots(figsize=fig_size)
fig1.suptitle("QAPBB_SP  rd_14", weight="bold")

for i in range(nk):

    offset = width * i
    ax1.bar(x + offset, S_sp_rd14[i], width, color=colors_sp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

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


## rd_16 ##
fig2, ax2 = plt.subplots(figsize=fig_size)
fig2.suptitle("QAPBB_SP  rd_16", weight="bold")

for i in range(nk):

    offset = width * i
    ax2.bar(x + offset, S_sp_rd16[i], width, color=colors_sp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

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

## rd_18 ##
fig3, ax3 = plt.subplots(figsize=fig_size)
fig3.suptitle("QAPBB_SP  rd_18", weight="bold")

for i in range(nk):

    offset = width * i
    ax3.bar(x + offset, S_sp_rd18[i], width, color=colors_sp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax3.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax3.set_ylim(0, 3)

ax3.set_xticks(x + width, x_labels)
ax3.tick_params(axis="both", labelsize=fs0)

ax3.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax3.set_ylabel("speedup", fontsize=fs0)
ax3.legend(fontsize=fs1)

ax3.set_axisbelow(True)
ax3.grid()


##--------------- QAPBB_MP ---------------##

## rd_14 ##
fig4, ax4 = plt.subplots(figsize=fig_size)
fig4.suptitle("QAPBB_MP  rd_14", weight="bold")

for i in range(nk):

    offset = width * i
    ax4.bar(x + offset, S_mp_rd14[i], width, color=colors_mp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax4.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax4.set_ylim(0, 7)

ax4.set_xticks(x + width, x_labels)
ax4.tick_params(axis="both", labelsize=fs0)

ax4.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax4.set_ylabel("speedup", fontsize=fs0)

ax4.legend(fontsize=fs1)

ax4.set_axisbelow(True)
ax4.grid()

## rd_16
fig5, ax5 = plt.subplots(figsize=fig_size)
fig5.suptitle("QAPBB_MP  rd_16")

for i in range(nk):

    offset = width * i
    ax5.bar(x + offset, S_mp_rd16[i], width, color=colors_mp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax5.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax5.set_ylim(0, 8)

ax5.set_xticks(x + width, x_labels)
ax5.tick_params(axis="both", labelsize=fs0)

ax5.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax5.set_ylabel("speedup", fontsize=fs0)

ax5.legend(fontsize=fs1)

ax5.set_axisbelow(True)
ax5.grid()

## rd_18
fig6, ax6 = plt.subplots(figsize=fig_size)
fig6.suptitle("QAPBB_MP  rd_18")

for i in range(nk):

    offset = width * i
    ax6.bar(x + offset, S_mp_rd18[i], width, color=colors_mp[i], edgecolor="k", linewidth=lw0, hatch=textures[i], label=y_labels[i])

x_pad = 0.5
ax6.set_xlim(x[0] - x_pad, x[-1] + 3*width + x_pad)
ax6.set_ylim(0, 10)

ax6.set_xticks(x + width, x_labels)
ax6.tick_params(axis="both", labelsize=fs0)

ax6.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax6.set_ylabel("speedup", fontsize=fs0)

ax6.legend(fontsize=fs1)

ax6.set_axisbelow(True)
ax6.grid()

plt.show()
