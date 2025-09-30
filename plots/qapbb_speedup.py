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
T_seq_rd16 = 277
T_seq_rd18 = 1450
T_seq_rd20 = 2850

# QAPBB_SP (k = 9)
T_sp_rd20 = np.array([T_seq_rd20, 1950, 1570, 1360, 1230])

S_sp_rd20 = T_seq_rd20 / T_sp_rd20

# QAPBB_MP (k = 18)
T_mp_rd16 = np.array([T_seq_rd16, 196, 138, 82, 65])
T_mp_rd18 = np.array([T_seq_rd18, 964, 591, 363, 256])
T_mp_rd20 = np.array([T_seq_rd20, 1680, 1010, 632, 382])

S_mp_rd16 = T_seq_rd16 / T_mp_rd16
S_mp_rd18 = T_seq_rd18 / T_mp_rd18
S_mp_rd20 = T_seq_rd20 / T_mp_rd20


##--------------- speedups ---------------##

## rd_20 ##
fig1, ax1 = plt.subplots(figsize = fig_size)
#fig1.suptitle("rd_20")

ax1.plot(K_val, K_val, "k", lw=lw_ideal, label="ideal")

#ax1.plot(K_val, S_sp_rd20, col_sp, marker=marker_sp, markersize=marker_size, lw=lw0, label="QAPBB_SP")
#ax1.plot(K_val, S_mp_rd20, col_mp, marker=marker_mp, markersize=marker_size, lw=lw0, label="QAPBB_MP")
ax1.plot(K_val, S_sp_rd20, col_sp, marker=marker_sp, markersize=marker_size, lw=lw0, label="PBB_SP")
ax1.plot(K_val, S_mp_rd20, col_mp, marker=marker_mp, markersize=marker_size, lw=lw0, label="PBB_MP")

ax1.set_xticks(K_val)
ax1.tick_params(axis="both", labelsize=fs0)
#ax1.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax1.set_xlabel("number of computing nodes", fontsize=fs0)
ax1.set_ylabel("speedup", fontsize=fs0)
ax1.legend(fontsize=fs_leg)
ax1.grid()

## bonus (MP for all circuits) ##
linestyles = [':', '--', '-']

fig2, ax2 = plt.subplots(figsize = fig_size)
#fig2.suptitle("QAPBB_MP")

ax2.plot(K_val, K_val, "k", lw=lw_ideal, label="ideal")

ax2.plot(K_val, S_mp_rd16, col_mp, marker=marker_mp, markersize=marker_size, linestyle=linestyles[0], lw=lw0, label="rd_16")
ax2.plot(K_val, S_mp_rd18, col_mp, marker=marker_mp, markersize=marker_size, linestyle=linestyles[1], lw=lw0, label="rd_18")
ax2.plot(K_val, S_mp_rd20, col_mp, marker=marker_mp, markersize=marker_size, linestyle=linestyles[2], lw=lw0, label="rd_20")

ax2.set_xticks(K_val)
ax2.tick_params(axis="both", labelsize=fs0)
#ax2.set_xlabel(r"number of nodes ($K$)", fontsize=fs0)
ax2.set_xlabel("number of computing nodes", fontsize=fs0)
ax2.set_ylabel("speedup", fontsize=fs0)
ax2.legend(fontsize=fs_leg)
ax2.grid()


fig1.savefig("QAPBB_SPvsMP_rd20.pdf", bbox_inches='tight', pad_inches=0.02)
fig2.savefig("QAPBB_MP_rd16rd18rd20.pdf", bbox_inches='tight', pad_inches=0.02)


plt.show()
