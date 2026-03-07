import numpy as np
import matplotlib.pyplot as plt


# ---------- 공통: 가상 스펙트럼 생성 ----------
def gaussian_absorption(wl, center, width, depth):
    """흡수대(reflectance 감소)를 가우시안 형태로 생성."""
    return depth * np.exp(-0.5 * ((wl - center) / width) ** 2)


def synthesize_spectrum(wl, group_idx=0, time_idx=0, rng=None):
    """석회 모르타르의 SWIR 특징을 반영한 가상 reflectance 스펙트럼.

    반영 피처:
    - 950 nm (특히 W군에서 강하게)
    - 1400, 1900, 2400 nm 흡수대
    """
    if rng is None:
        rng = np.random.default_rng(0)

    # 완만한 배경 연속선 (전체 경향)
    baseline = 0.58 + 0.00006 * (wl - 900)

    # 그룹/시간에 따른 강도 조절 (가상의 열화/양생 차이)
    group_factor = [0.75, 0.9, 1.05, 1.2][group_idx]
    time_factor = 0.85 + 0.08 * time_idx

    # 950 nm 피처: W군(group_idx==3)에서 강화
    depth_950 = 0.010 * group_factor * time_factor
    if group_idx == 3:  # W군 강조
        depth_950 *= 2.2

    depth_1400 = 0.060 * group_factor * (0.9 + 0.04 * time_idx)
    depth_1900 = 0.090 * group_factor * (0.95 + 0.06 * time_idx)
    depth_2400 = 0.070 * group_factor * (1.0 + 0.03 * time_idx)

    spectrum = baseline.copy()
    spectrum -= gaussian_absorption(wl, 950, 20, depth_950)
    spectrum -= gaussian_absorption(wl, 1400, 45, depth_1400)
    spectrum -= gaussian_absorption(wl, 1900, 55, depth_1900)
    spectrum -= gaussian_absorption(wl, 2400, 65, depth_2400)

    # 미세 잡음
    spectrum += rng.normal(0, 0.0018, size=wl.shape)

    return np.clip(spectrum, 0.02, 0.95)


# ---------- (1) RMSE ----------
def make_rmse_figure(out_path="fig1_rmse.png"):
    wl = np.linspace(900, 2500, 801)
    rng = np.random.default_rng(4)

    # 기준 스펙트럼 R0와 시간 t 스펙트럼 Rt
    r0 = synthesize_spectrum(wl, group_idx=1, time_idx=1, rng=rng)
    rt = synthesize_spectrum(wl, group_idx=1, time_idx=4, rng=rng)

    delta = rt - r0
    rmse = np.sqrt(np.mean(delta ** 2))

    fig, axes = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [2.2, 1.2]}
    )

    ax0, ax1 = axes
    ax0.plot(wl, r0, label="R0 (reference)", lw=2)
    ax0.plot(wl, rt, label="Rt (time t)", lw=2)
    ax0.set_ylabel("Reflectance")
    ax0.set_title("(1) RMSE visualization: spectral difference and error magnitude")
    ax0.grid(alpha=0.25)
    ax0.legend(loc="best")

    ax0.text(
        0.02,
        0.92,
        f"RMSE = sqrt(mean((Rt-R0)^2)) = {rmse:.4f}",
        transform=ax0.transAxes,
        fontsize=11,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"),
    )

    ax1.plot(wl, delta, color="tab:red", lw=1.8, label="ΔR(λ)=Rt-R0")
    ax1.axhline(0, color="black", lw=1)
    ax1.set_xlabel("Wavelength (nm)")
    ax1.set_ylabel("ΔR")
    ax1.grid(alpha=0.25)
    ax1.legend(loc="best")

    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


# ---------- (2) SAM ----------
def make_sam_figure(out_path="fig2_sam.png"):
    # 3개 파장 성분으로 축소한 벡터
    lam_labels = ["λ1", "λ2", "λ3"]
    v1 = np.array([0.56, 0.42, 0.34])
    v2 = np.array([0.51, 0.31, 0.46])

    # SAM 각도
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta_rad = np.arccos(cos_theta)
    theta_deg = np.degrees(theta_rad)

    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    # 축
    ax.quiver(0, 0, 0, v1[0], v1[1], v1[2], color="tab:blue", linewidth=3, arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color="tab:orange", linewidth=3, arrow_length_ratio=0.08)

    ax.text(v1[0], v1[1], v1[2], "  s1", color="tab:blue", fontsize=11)
    ax.text(v2[0], v2[1], v2[2], "  s2", color="tab:orange", fontsize=11)

    # 각도 아크(두 벡터가 놓인 평면 내부의 보간 벡터)
    u1 = v1 / np.linalg.norm(v1)
    u2 = v2 / np.linalg.norm(v2)
    t = np.linspace(0, 1, 60)
    # 구면 선형 보간(slerp) 간략식
    sin_total = np.sin(theta_rad) if theta_rad > 1e-8 else 1.0
    arc = (
        np.sin((1 - t) * theta_rad)[:, None] / sin_total * u1[None, :]
        + np.sin(t * theta_rad)[:, None] / sin_total * u2[None, :]
    )
    arc *= 0.45
    ax.plot(arc[:, 0], arc[:, 1], arc[:, 2], "k--", lw=1.6)
    mid = arc[len(arc) // 2]
    ax.text(mid[0], mid[1], mid[2], f" θ={theta_deg:.1f}°", fontsize=11)

    ax.set_xlim(0, 0.7)
    ax.set_ylim(0, 0.7)
    ax.set_zlim(0, 0.7)
    ax.set_xlabel(f"{lam_labels[0]} reflectance")
    ax.set_ylabel(f"{lam_labels[1]} reflectance")
    ax.set_zlabel(f"{lam_labels[2]} reflectance")
    ax.set_title("(2) SAM visualization: angle between two spectral vectors")

    # 보기 각도
    ax.view_init(elev=22, azim=38)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180)
    plt.close(fig)


# ---------- (3) Continuum / BD1900 ----------
def make_continuum_bd1900_figure(out_path="fig3_continuum_bd1900.png"):
    wl = np.linspace(1700, 2100, 401)
    rng = np.random.default_rng(7)

    # 1900 nm 흡수대를 강조한 스펙트럼
    r = 0.63 + 0.00004 * (wl - 1700)
    r -= gaussian_absorption(wl, 1900, 45, 0.12)
    r += rng.normal(0, 0.0015, size=wl.shape)

    # 어깨점(λL, λR) 선택
    lam_l, lam_r = 1800, 2000
    idx_l = np.argmin(np.abs(wl - lam_l))
    idx_r = np.argmin(np.abs(wl - lam_r))

    # Continuum Rc(λ): 양 어깨를 잇는 직선
    r_l, r_r = r[idx_l], r[idx_r]
    rc = r_l + (r_r - r_l) * (wl - lam_l) / (lam_r - lam_l)

    # 연속선 제거
    r_cr = r / rc

    # BD1900 계산: 1 - min(R/Rc)
    bd1900 = 1 - np.min(r_cr[(wl >= lam_l) & (wl <= lam_r)])
    idx_min = np.argmin(r_cr[(wl >= lam_l) & (wl <= lam_r)])
    roi_wl = wl[(wl >= lam_l) & (wl <= lam_r)]
    roi_rcr = r_cr[(wl >= lam_l) & (wl <= lam_r)]
    lam_min, rcr_min = roi_wl[idx_min], roi_rcr[idx_min]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), sharex=True)

    # 패널1: 어깨점 선택
    ax = axes[0]
    ax.plot(wl, r, lw=2, label="R(λ)")
    ax.scatter([lam_l, lam_r], [r_l, r_r], color="tab:red", zorder=4)
    ax.text(lam_l + 3, r_l + 0.005, "λL", color="tab:red")
    ax.text(lam_r + 3, r_r + 0.005, "λR", color="tab:red")
    ax.set_title("1) Select shoulders")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Reflectance")
    ax.grid(alpha=0.25)

    # 패널2: Continuum 직선
    ax = axes[1]
    ax.plot(wl, r, lw=2, label="R(λ)")
    ax.plot(wl, rc, "--", lw=2, label="Rc(λ) (continuum)")
    ax.set_title("2) Build Rc(λ) continuum line")
    ax.set_xlabel("Wavelength (nm)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9)

    # 패널3: R/Rc 와 BD 표시
    ax = axes[2]
    ax.plot(wl, r_cr, color="tab:purple", lw=2, label="R/Rc")
    ax.axhline(1.0, color="gray", lw=1)
    ax.vlines(lam_min, rcr_min, 1.0, color="tab:red", lw=2)
    ax.scatter([lam_min], [rcr_min], color="tab:red", zorder=5)
    ax.text(
        lam_min + 4,
        (1 + rcr_min) / 2,
        f"BD1900 = 1 - min(R/Rc)\n= {bd1900:.3f}",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.75, edgecolor="gray"),
    )
    ax.set_title("3) After continuum removal: BD1900")
    ax.set_xlabel("Wavelength (nm)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9)

    fig.suptitle("(3) Continuum/BD1900 workflow", y=1.03, fontsize=13)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


# ---------- (4) PCA ----------
def run_pca(X, n_components=2):
    """numpy만 사용한 PCA (평균중심화 + 공분산 고유분해)."""
    Xc = X - X.mean(axis=0, keepdims=True)
    cov = np.cov(Xc, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    components = eigvecs[:, :n_components]
    scores = Xc @ components
    explained = eigvals[:n_components] / eigvals.sum()
    return scores, components, explained


def make_pca_figure(out_path="fig4_pca_scores_loadings.png"):
    wl = np.linspace(900, 2500, 180)
    rng = np.random.default_rng(11)

    group_names = ["A", "B", "C", "W"]
    n_time = 6

    spectra = []
    labels = []
    times = []

    for g_idx, g_name in enumerate(group_names):
        for t_idx in range(n_time):
            s = synthesize_spectrum(wl, group_idx=g_idx, time_idx=t_idx, rng=rng)
            # 약간의 개체 차
            s += rng.normal(0, 0.0012, size=wl.shape)
            spectra.append(s)
            labels.append(g_name)
            times.append(t_idx)

    X = np.vstack(spectra)
    scores, components, explained = run_pca(X, n_components=2)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))

    # 점수 플롯
    ax = axes[0]
    colors = {"A": "tab:blue", "B": "tab:green", "C": "tab:orange", "W": "tab:red"}
    for g_name in group_names:
        idx = np.array([i for i, lab in enumerate(labels) if lab == g_name])
        sc = ax.scatter(
            scores[idx, 0],
            scores[idx, 1],
            c=colors[g_name],
            s=58,
            alpha=0.85,
            label=g_name,
            edgecolor="white",
            linewidth=0.6,
        )
        # 시간 진행 방향(간단 연결)
        ax.plot(scores[idx, 0], scores[idx, 1], color=colors[g_name], alpha=0.45, lw=1)

    ax.set_title("PCA Scores (4 groups × time)")
    ax.set_xlabel(f"PC1 ({explained[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({explained[1]*100:.1f}%)")
    ax.grid(alpha=0.25)
    ax.legend(title="Group")

    # 로딩 플롯
    ax = axes[1]
    pc1 = components[:, 0]
    pc2 = components[:, 1]
    ax.plot(wl, pc1, lw=2, label="PC1 loading")
    ax.plot(wl, pc2, lw=2, label="PC2 loading")

    for peak in [950, 1400, 1900, 2400]:
        ax.axvline(peak, color="gray", lw=0.8, alpha=0.5)

    ax.set_title("Loadings (PC1, PC2)")
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Loading weight")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.suptitle("(4) PCA visualization: scores + loadings", y=1.02, fontsize=13)
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    make_rmse_figure("fig1_rmse.png")
    make_sam_figure("fig2_sam.png")
    make_continuum_bd1900_figure("fig3_continuum_bd1900.png")
    make_pca_figure("fig4_pca_scores_loadings.png")
    print("Saved: fig1_rmse.png, fig2_sam.png, fig3_continuum_bd1900.png, fig4_pca_scores_loadings.png")


if __name__ == "__main__":
    main()
