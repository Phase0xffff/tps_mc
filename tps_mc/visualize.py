# thomson_mc/visualize.py
import matplotlib.pyplot as plt
import numpy as np
import itertools

COLORS = itertools.cycle([
    "tab:blue", "tab:orange", "tab:green",
    "tab:red", "tab:purple", "tab:brown"
])


def plot_coords(coords_list, labels=None, mode="scatter"):
    plt.figure()

    if mode in ("heatmap", "both"):
        all_coords = np.vstack(coords_list)
        x_all, y_all = all_coords[:, 0], all_coords[:, 1]
        heatmap, xedges, yedges = np.histogram2d(x_all, y_all, bins=100)
        plt.imshow(
            heatmap.T, origin='lower', aspect='auto',
            extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
            alpha=0.5, cmap="inferno"
        )

    if mode in ("scatter", "both"):
        if labels is None:
            labels = [f"species {i}" for i in range(len(coords_list))]
        for coords, label, color in zip(coords_list, labels, COLORS):
            x, y = coords[:, 0], coords[:, 1]
            plt.scatter(x, y, s=2, alpha=0.6, label=label, c=color)

    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.axis("equal")
    plt.legend()
    plt.title("Thomson Spectrometer Projection")
    plt.show()
