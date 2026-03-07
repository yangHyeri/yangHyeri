import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# Reproducibility
np.random.seed(42)


def gaussian(x, mu, sigma, depth):
    """Absorption-like Gaussian dip."""
    return depth * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def generate_virtual_spectra():
    """
    Generate virtual baseline/reference spectrum (R0) and altered spectrum (Rt)
    with key absorptions near 1400/1900/2400 nm and a 950 nm feature.
    """
    wl = np.linspace(900, 2500, 801)  # 2 nm step

    # Smooth baseline reflectance shape
    base = 0.53 + 0.04 * np.sin((wl - 900) / 400) + 0.015 * np.cos((wl - 900) / 110)

    # Shared absorption features (both spectra)
    common_dips = (
        gaussian(wl, 1400, 45, 0.080)
        + gaussian(wl, 1900, 60, 0.130)
        + gaussian(wl, 2400, 75, 0.095)
    )

    # W group-like 950 nm feature: stronger in Rt for explanation
    dip_950_R0 = gaussian(wl, 950, 22, 0.012)
    dip_950_Rt = gaussian(wl, 950, 22, 0.030)

    # Build spectra
    R0 = base - common_dips - dip_950_R0

    # Rt simulates hydration/carbonation change:
    # slightly deeper around 1900 and 2400, plus subtle slope change
    Rt = (
        base
        - gaussian(wl, 1400, 45, 0.085)
        - gaussian(wl, 1900, 62, 0.155)
        - gaussian(wl, 2400, 78, 0.108)
        - dip_950_Rt
        + 0.005 * (wl - wl.mean()) / (wl.max() - wl.min())
    )

    # Light measurement-like texture
    R0 += 0.0012 * np.sin(wl / 19)
    Rt += 0.0015 * np.cos(wl / 23)

    # keep in reflectance range
    R0 = np.clip(R0, 0.05, 0.9)
    Rt = np.clip(Rt, 0.05, 0.9)
    return wl, R0, Rt


def figure_rmse(wl, R0, Rt, out_path="fig1_rmse.png"):
    diff = Rt - R0
    rmse = np.sqrt(np.mean(diff**2))

    fig, axes = plt.subplots(
        2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]}
    )

    # Top panel: spectra overlap
    axes[0].plot(wl, R0, color="tab:blue", lw=2.2, label="Reference $R_0(\\lambda)$")
    axes[0].plot(wl, Rt, color="tab:orange", lw=2.2, label="Test $R_t(\\lambda)$")
    axes[0].set_ylabel("Reflectance")
    axes[0].set_title("(1) RMSE concept: spectrum overlap and residual")
    axes[0].grid(alpha=0.25)
    axes[0].legend(loc="best")
    axes[0].text(
        0.03,
        0.06,
        f"RMSE = $\\sqrt{{\\frac{{1}}{{N}}\\sum (R_t-R_0)^2}}$ = {rmse:.4f}",
        transform=axes[0].transAxes,
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="gray", alpha=0.92),
    )

    # Bottom panel: delta
    axes[1].axhline(0, color="black", lw=1)
    axes[1].plot(wl, diff, color="tab:red", lw=1.8)
    axes[1].fill_between(wl, 0, diff, color="tab:red", alpha=0.22)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel("$\\Delta R(\\lambda)$")
    axes[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=220)
    plt.close(fig)


def figure_sam(out_path="fig2_sam.png"):
    # 3-wave reduced vectors
    r0 = np.array([0.42, 0.31, 0.26])
    rt = np.array([0.39, 0.24, 0.30])

    dot = np.dot(r0, rt)
    theta = np.degrees(np.arccos(dot / (np.linalg.norm(r0) * np.linalg.norm(rt))))

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    # axis limits
    lim = 0.5
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_zlim(0, lim)

    # vectors
    ax.quiver(0, 0, 0, r0[0], r0[1], r0[2], color="tab:blue", linewidth=2.5, arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, rt[0], rt[1], rt[2], color="tab:orange", linewidth=2.5, arrow_length_ratio=0.08)

    ax.text(r0[0] + 0.015, r0[1], r0[2], "$\\mathbf{R_0}$", color="tab:blue", fontsize=12)
    ax.text(rt[0] + 0.015, rt[1], rt[2], "$\\mathbf{R_t}$", color="tab:orange", fontsize=12)

    # arc-like annotation in plane spanned by vectors
    t = np.linspace(0, 1, 70)
    u0 = r0 / np.linalg.norm(r0)
    u1 = rt / np.linalg.norm(rt)
    # spherical linear interpolation for a neat angle arc
    omega = np.arccos(np.clip(np.dot(u0, u1), -1, 1))
    if np.sin(omega) > 1e-8:
        arc = (
            np.sin((1 - t) * omega)[:, None] / np.sin(omega) * u0[None, :]
            + np.sin(t * omega)[:, None] / np.sin(omega) * u1[None, :]
        )
    else:
        arc = np.outer(np.ones_like(t), u0)
    arc *= 0.17
    ax.plot(arc[:, 0], arc[:, 1], arc[:, 2], color="crimson", lw=2)

    mid = arc[len(arc) // 2]
    ax.text(mid[0], mid[1], mid[2] + 0.02, f"$\\theta$ = {theta:.1f}°", color="crimson", fontsize=11)

    ax.set_xlabel("$\\lambda_1$")
    ax.set_ylabel("$\\lambda_2$")
    ax.set_zlabel("$\\lambda_3$")
    ax.set_title("(2) SAM concept in 3D reduced space")
    ax.view_init(elev=24, azim=42)

    fig.tight_layout()
    fig.savefig(out_path, dpi=220)
    plt.close(fig)


def figure_continuum_bd1900(wl, Rt, out_path="fig3_continuum_bd1900.png"):
    # Focus window
    mask = (wl >= 1800) & (wl <= 2000)
    w = wl[mask]
    r = Rt[mask]

    # Shoulders (example positions around band edges)
    lambda_L, lambda_R = 1810.0, 1985.0
    iL = np.argmin(np.abs(w - lambda_L))
    iR = np.argmin(np.abs(w - lambda_R))
    xL, xR = w[iL], w[iR]
    yL, yR = r[iL], r[iR]

    # Continuum line Rc(lambda)
    Rc = yL + (yR - yL) * (w - xL) / (xR - xL)

    # Continuum-removed
    cr = r / Rc

    # BD1900 index-like depth from continuum removed minimum
    idx_min = np.argmin(cr)
    w_min, cr_min = w[idx_min], cr[idx_min]
    bd1900 = 1.0 - cr_min

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8), sharex=True)

    # Panel 1: raw reflectance with shoulders
    axes[0].plot(w, r, color="tab:blue", lw=2)
    axes[0].scatter([xL, xR], [yL, yR], color="black", zorder=5)
    axes[0].annotate("$\\lambda_L$", (xL, yL), xytext=(xL - 28, yL + 0.018), arrowprops=dict(arrowstyle="->", lw=1))
    axes[0].annotate("$\\lambda_R$", (xR, yR), xytext=(xR - 30, yR + 0.018), arrowprops=dict(arrowstyle="->", lw=1))
    axes[0].set_title("Shoulders selection")
    axes[0].set_ylabel("Reflectance")
    axes[0].grid(alpha=0.25)

    # Panel 2: add continuum line
    axes[1].plot(w, r, color="tab:blue", lw=2, label="$R(\\lambda)$")
    axes[1].plot(w, Rc, color="tab:orange", lw=2, ls="--", label="$R_c(\\lambda)$")
    axes[1].scatter([xL, xR], [yL, yR], color="black", zorder=5)
    axes[1].set_title("Continuum line $R_c(\\lambda)$")
    axes[1].legend(loc="lower right")
    axes[1].grid(alpha=0.25)

    # Panel 3: continuum removed + BD depth
    axes[2].plot(w, cr, color="tab:green", lw=2.2, label="$R/R_c$")
    axes[2].axhline(1.0, color="gray", lw=1, ls=":")
    axes[2].scatter([w_min], [cr_min], color="crimson", zorder=6)
    axes[2].vlines(w_min, cr_min, 1.0, color="crimson", lw=2)
    axes[2].annotate(
        f"BD1900 = 1 - min(R/Rc)\n= {bd1900:.3f}",
        (w_min, (1 + cr_min) / 2),
        xytext=(w_min + 18, cr_min + 0.08),
        arrowprops=dict(arrowstyle="->", lw=1.2),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9),
    )
    axes[2].set_ylim(min(0.75, cr.min() - 0.02), 1.03)
    axes[2].set_title("Continuum removal and BD1900")
    axes[2].set_ylabel("Normalized reflectance")
    axes[2].grid(alpha=0.25)

    for ax in axes:
        ax.set_xlabel("Wavelength (nm)")

    fig.suptitle("(3) Continuum removal workflow (1800–2000 nm)", y=1.03, fontsize=13)
    fig.tight_layout()
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def pca_numpy(X, n_components=2):
    """Simple PCA with numpy (mean-center + SVD)."""
    Xc = X - X.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    scores = U[:, :n_components] * S[:n_components]
    loadings = Vt[:n_components, :]
    explained = (S**2) / np.sum(S**2)
    return scores, loadings, explained[:n_components]


def make_virtual_group_time_spectra():
    """
    Virtual spectra dataset: 4 groups x multiple times.
    Groups differ mainly in 950 nm and moisture-related bands.
    """
    wl = np.linspace(900, 2500, 321)  # coarser for PCA

    groups = ["Ref", "A", "B", "W"]
    times = np.array([0, 1, 3, 7, 14, 28])

    data = []
    labels = []

    for g in groups:
        for t in times:
            base = 0.52 + 0.035 * np.sin((wl - 900) / 420) + 0.012 * np.cos((wl - 900) / 140)

            # Time-driven absorption modulation (hydration evolution concept)
            f_t = 1.0 + 0.22 * np.log1p(t) / np.log(29)

            dip1400 = gaussian(wl, 1400, 46, 0.070 * f_t)
            dip1900 = gaussian(wl, 1900, 62, 0.120 * f_t)
            dip2400 = gaussian(wl, 2400, 78, 0.090 * (1 + 0.15 * np.sqrt(t / 28 if t > 0 else 0)))

            # Group-specific 950 feature (W strongest)
            d950 = {"Ref": 0.010, "A": 0.017, "B": 0.022, "W": 0.034}[g]
            dip950 = gaussian(wl, 950, 23, d950)

            # Group-specific global offset / subtle slope
            offset = {"Ref": 0.0, "A": -0.003, "B": 0.002, "W": -0.006}[g]
            slope = {"Ref": 0.0, "A": 0.004, "B": -0.002, "W": 0.006}[g] * (wl - wl.mean()) / (wl.max() - wl.min())

            spec = base - dip1400 - dip1900 - dip2400 - dip950 + offset + slope
            spec += 0.0015 * np.sin((wl + t * 17) / 27)  # deterministic tiny texture
            spec = np.clip(spec, 0.05, 0.9)

            data.append(spec)
            labels.append((g, t))

    return wl, np.array(data), labels


def figure_pca(out_path="fig4_pca_scores_loadings.png"):
    wl, X, labels = make_virtual_group_time_spectra()
    scores, loadings, exp_var = pca_numpy(X, n_components=2)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.3))

    # Left: PC1-PC2 scores
    groups = ["Ref", "A", "B", "W"]
    cmap = {"Ref": "tab:blue", "A": "tab:orange", "B": "tab:green", "W": "tab:red"}
    markers = {0: "o", 1: "s", 3: "^", 7: "D", 14: "P", 28: "X"}

    for g in groups:
        idx = [i for i, (gg, _) in enumerate(labels) if gg == g]
        for i in idx:
            t = labels[i][1]
            axes[0].scatter(
                scores[i, 0],
                scores[i, 1],
                color=cmap[g],
                marker=markers[t],
                s=65,
                alpha=0.85,
                edgecolor="black",
                linewidth=0.35,
            )
        # connect time progression within each group
        idx_sorted = sorted(idx, key=lambda k: labels[k][1])
        axes[0].plot(scores[idx_sorted, 0], scores[idx_sorted, 1], color=cmap[g], alpha=0.55, lw=1.3)

    # compact legends (group + time marker guide)
    for g in groups:
        axes[0].scatter([], [], color=cmap[g], label=f"Group {g}")
    leg1 = axes[0].legend(loc="upper left", fontsize=9, frameon=True)
    axes[0].add_artist(leg1)

    for t, mk in markers.items():
        axes[0].scatter([], [], color="gray", marker=mk, label=f"t={t} d")
    axes[0].legend(loc="lower right", fontsize=8, frameon=True, ncol=2)

    axes[0].axhline(0, color="gray", lw=0.8)
    axes[0].axvline(0, color="gray", lw=0.8)
    axes[0].set_xlabel(f"PC1 score ({exp_var[0]*100:.1f}% var)")
    axes[0].set_ylabel(f"PC2 score ({exp_var[1]*100:.1f}% var)")
    axes[0].set_title("(4) PCA score plot: 4 groups × time")
    axes[0].grid(alpha=0.25)

    # Right: loadings
    axes[1].plot(wl, loadings[0], color="tab:purple", lw=2, label="PC1 loading")
    axes[1].plot(wl, loadings[1], color="tab:brown", lw=2, label="PC2 loading")
    axes[1].axhline(0, color="black", lw=1)
    for x in [950, 1400, 1900, 2400]:
        axes[1].axvline(x, color="gray", ls=":", lw=1)
    axes[1].set_xlabel("Wavelength (nm)")
    axes[1].set_ylabel("Loading value")
    axes[1].set_title("PC1 / PC2 loading curves")
    axes[1].legend(loc="best")
    axes[1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(out_path, dpi=220)
    plt.close(fig)


def main():
    wl, R0, Rt = generate_virtual_spectra()

    figure_rmse(wl, R0, Rt, out_path="fig1_rmse.png")
    figure_sam(out_path="fig2_sam.png")
    figure_continuum_bd1900(wl, Rt, out_path="fig3_continuum_bd1900.png")
    figure_pca(out_path="fig4_pca_scores_loadings.png")

    print("Saved:")
    print(" - fig1_rmse.png")
    print(" - fig2_sam.png")
    print(" - fig3_continuum_bd1900.png")
    print(" - fig4_pca_scores_loadings.png")


if __name__ == "__main__":
    main()
