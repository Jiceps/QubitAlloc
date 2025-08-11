import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "Times New Roman",
    "mathtext.fontset": "stix",
}) 

## parameters
fs0 = 16
fs_leg = fs0 - 1

lw0 = 1.5
lw_ideal = 1.25

fig_size = (6.2, 5.2)

col_sp = "firebrick"
col_mp = "darkblue"
marker_sp = "d"
marker_mp = "o"
marker_size = 4


##--------------- data ---------------##

# params
K_val = [1, 4, 8, 16, 32]

# QABB_PB (baseline)
T_seq_rd14 = 1540
T_seq_rd16 = 2400
T_seq_rd18 = 11530

# QAPBB_SP (k = 9)
T_sp_rd14 = np.array([T_seq_rd14, 990, 820, 730, 670])
T_sp_rd16 = np.array([T_seq_rd16, 1530, 1270, 1150, 1030])
T_sp_rd18 = np.array([T_seq_rd18, 7330, 6140, 5490, 5030])

S_sp_rd14 = T_seq_rd14 / T_sp_rd14
S_sp_rd16 = T_seq_rd16 / T_sp_rd16
S_sp_rd18 = T_seq_rd18 / T_sp_rd18


# QAPBB_MP (k = 9)
#T_mp_rd14 = np.array([T_seq_rd14, 920, 560, 390, 230])
#T_mp_rd16 = np.array([T_seq_rd16, 1350, 810, 530, 320])
#T_mp_rd18 = np.array([T_seq_rd18, 6490, 4040, 2420, 1510])
# QAPBB_MP (k = 18)
T_mp_rd14 = np.array([T_seq_rd14, 840, 540, 330, 250])
T_mp_rd16 = np.array([T_seq_rd16, 1190, 740, 460, 330])
T_mp_rd18 = np.array([T_seq_rd18, 5890, 3580, 2110, 1330])

S_mp_rd14 = T_seq_rd14 / T_mp_rd14
S_mp_rd16 = T_seq_rd16 / T_mp_rd16
S_mp_rd18 = T_seq_rd18 / T_mp_rd18


##--------------- speedups ---------------##

## rd_14 ##
fig1, ax1 = plt.subplots(figsize = fig_size)
fig1.suptitle("rd_14")

ax1.plot(K_val, K_val, "k", lw=lw_ideal, label="ideal")

ax1.plot(K_val, S_sp_rd14, col_sp, marker=marker_sp, markersize=marker_size, lw=lw0, label="QAPBB_SP")
ax1.plot(K_val, S_mp_rd14, col_mp, marker=marker_mp, markersize=marker_size, lw=lw0, label="QAPBB_MP")

ax1.set_xticks(K_val)
ax1.tick_params(axis="both", labelsize=fs0)
ax1.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax1.set_ylabel("speedup", fontsize=fs0)
ax1.legend(fontsize=fs_leg)
ax1.grid()

## rd_16 ##
fig2, ax2 = plt.subplots(figsize = fig_size)
fig2.suptitle("rd_16")

ax2.plot(K_val, K_val, "k", lw=lw_ideal, label="ideal")

ax2.plot(K_val, S_sp_rd16, col_sp, marker=marker_sp, markersize=marker_size, lw=lw0, label="QAPBB_SP")
ax2.plot(K_val, S_mp_rd16, col_mp, marker=marker_mp, markersize=marker_size, lw=lw0, label="QAPBB_MP")

ax2.set_xticks(K_val)
ax2.tick_params(axis="both", labelsize=fs0)
ax2.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax2.set_ylabel("speedup", fontsize=fs0)
ax2.legend(fontsize=fs_leg)
ax2.grid()

## rd_18 ##
fig3, ax3 = plt.subplots(figsize = fig_size)
fig3.suptitle("rd_18")

ax3.plot(K_val, K_val, "k", lw=lw_ideal, label="ideal")

ax3.plot(K_val, S_sp_rd18, col_sp, marker=marker_sp, markersize=marker_size, lw=lw0, label="QAPBB_SP")
ax3.plot(K_val, S_mp_rd18, col_mp, marker=marker_mp, markersize=marker_size, lw=lw0, label="QAPBB_MP")

ax3.set_xticks(K_val)
ax3.tick_params(axis="both", labelsize=fs0)
ax3.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax3.set_ylabel("speedup", fontsize=fs0)
ax3.legend(fontsize=fs_leg)
ax3.grid()

## bonus (MP for all circuits) ##
linestyles = [':', '--', '-']

fig4, ax4 = plt.subplots(figsize = fig_size)
fig4.suptitle("QAPBB_MP")

ax4.plot(K_val, K_val, "k", lw=lw_ideal, label="ideal")

ax4.plot(K_val, S_mp_rd14, col_mp, marker=marker_mp, markersize=marker_size, linestyle=linestyles[0], lw=lw0, label="rd_14")
ax4.plot(K_val, S_mp_rd16, col_mp, marker=marker_mp, markersize=marker_size, linestyle=linestyles[1], lw=lw0, label="rd_16")
ax4.plot(K_val, S_mp_rd18, col_mp, marker=marker_mp, markersize=marker_size, linestyle=linestyles[2], lw=lw0, label="rd_18")

ax4.set_xticks(K_val)
ax4.tick_params(axis="both", labelsize=fs0)
ax4.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax4.set_ylabel("speedup", fontsize=fs0)
ax4.legend(fontsize=fs_leg)
ax4.grid()


plt.show()
