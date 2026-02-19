# PCA 분석 예시

이 저장소는 간단한 **PCA(Principal Component Analysis)** 분석을 실행하는 예시 스크립트를 제공합니다.

## 빠른 시작

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### CSV/엑셀 파일로 실행

```bash
python pca_analysis.py --input data.csv --target target --n-components 2 --plot-out pca_plot.png
```

- `--input`: CSV/Excel 파일 경로
- `--target`: 라벨(목표) 컬럼명(선택)
- `--n-components`: PCA 차원 수(기본: 2)
- `--plot-out`: 산점도 저장 경로(선택)

### 초분광(하이퍼스펙트럴) 엑셀 예시

```bash
python pca_analysis.py --input fx10_swir.xlsx --target class --n-components 2 --plot-out hyperspectral_pca.png
```

- 숫자형 컬럼(파장대 반사율)이 자동 선택됩니다.

### 샘플 데이터로 실행

```bash
python pca_analysis.py --sample iris --plot-out iris_pca.png
```

## 출력

- 선택한 PCA 차원으로 변환된 데이터(`pca_output.csv`)
- 설명 분산 비율(콘솔 출력)
- 산점도 이미지(옵션)

## JCH 수식 시각화 그림 생성

아래 스크립트는 가상 스펙트럼 데이터를 생성해, JCH 석회 모르타르 문맥의 핵심 수식 4종(RMSE, SAM, Continuum/BD1900, PCA)을 비전공자용 그림으로 저장합니다.

```bash
python jch_equation_visualizations.py
```

생성 파일:

- `fig1_rmse.png`
- `fig2_sam.png`
- `fig3_continuum_bd1900.png`
- `fig4_pca_scores_loadings.png`
