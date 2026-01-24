#!/usr/bin/env python
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional
    plt = None


def load_sample(sample_name: str) -> tuple[pd.DataFrame, pd.Series | None]:
    if sample_name == "iris":
        from sklearn.datasets import load_iris

        data = load_iris(as_frame=True)
        return data.data, data.target
    raise ValueError(f"지원하지 않는 샘플입니다: {sample_name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PCA 분석 스크립트")
    parser.add_argument("--input", type=Path, help="입력 CSV/Excel 파일 경로")
    parser.add_argument("--target", type=str, help="타겟 컬럼명(선택)")
    parser.add_argument("--n-components", type=int, default=2, help="PCA 차원 수")
    parser.add_argument("--plot-out", type=Path, help="PCA 산점도 저장 경로(선택)")
    parser.add_argument("--sample", choices=["iris"], help="내장 샘플 데이터")
    return parser.parse_args()


def load_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {path}")
    suffix = path.suffix.lower()
    if suffix in {".csv", ".txt"}:
        return pd.read_csv(path)
    if suffix in {".xls", ".xlsx"}:
        return pd.read_excel(path)
    raise ValueError(f"지원하지 않는 파일 형식입니다: {suffix}")


def run_pca(features: pd.DataFrame, target: pd.Series | None, n_components: int) -> pd.DataFrame:
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(scaled)

    explained = pca.explained_variance_ratio_
    print("설명 분산 비율:", np.round(explained, 4))

    columns = [f"PC{i + 1}" for i in range(n_components)]
    output = pd.DataFrame(transformed, columns=columns)
    if target is not None:
        output["target"] = target.values
    return output


def save_plot(output: pd.DataFrame, plot_out: Path) -> None:
    if plt is None:
        raise RuntimeError("matplotlib이 설치되어 있지 않습니다.")
    if output.shape[1] < 2:
        raise ValueError("산점도를 그리려면 최소 2개의 PCA 차원이 필요합니다.")

    plt.figure(figsize=(8, 6))
    if "target" in output.columns:
        for label, group in output.groupby("target"):
            plt.scatter(group["PC1"], group["PC2"], label=str(label), alpha=0.7)
        plt.legend(title="target")
    else:
        plt.scatter(output["PC1"], output["PC2"], alpha=0.7)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA 결과")
    plt.tight_layout()
    plt.savefig(plot_out)
    print(f"산점도 저장: {plot_out}")


def main() -> None:
    args = parse_args()

    if args.sample:
        features, target = load_sample(args.sample)
    elif args.input:
        data = load_table(args.input)
        target = None
        if args.target:
            if args.target not in data.columns:
                raise ValueError(f"타겟 컬럼을 찾을 수 없습니다: {args.target}")
            target = data[args.target]
            data = data.drop(columns=[args.target])
        features = data.select_dtypes(include=[np.number])
        if features.empty:
            raise ValueError("PCA에 사용할 수 있는 숫자형 컬럼이 없습니다.")
    else:
        raise ValueError("--input 또는 --sample 옵션이 필요합니다.")

    output = run_pca(features, target, args.n_components)
    output.to_csv("pca_output.csv", index=False)
    print("PCA 결과 저장: pca_output.csv")

    if args.plot_out:
        save_plot(output, args.plot_out)


if __name__ == "__main__":
    main()
