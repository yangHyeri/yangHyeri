# Grammar Lens + PCA 분석 예시

이 저장소는 두 가지 미니 프로젝트를 포함합니다.

1. **Grammar Lens**: 영어 문장을 입력하면 핵심 문법 용례를 한국어로 설명해주는 학습용 웹앱
2. **PCA 분석 예시**: CSV/엑셀 데이터에 PCA를 적용하는 Python 스크립트

---

## 1) Grammar Lens (영어 문법 용례 해설기)

### 실행

```bash
python -m http.server 8000
```

브라우저에서 `http://localhost:8000` 접속 후 문장을 입력해 분석 버튼을 누르세요.

### 현재 제공되는 분석 포인트

- `would have had to` 결합 구조 상세 설명
- `if` + `would have` 기반 과거 가정 의미 안내
- 단순과거 문장 식별

> 참고: 현재는 학습용 룰 기반 분석기이며, 점진적으로 문법 패턴을 추가할 수 있습니다.

---

## 2) PCA 분석 스크립트

간단한 **PCA(Principal Component Analysis)** 분석을 실행하는 예시 스크립트를 제공합니다.

### 빠른 시작

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

### 샘플 데이터로 실행

```bash
python pca_analysis.py --sample iris --plot-out iris_pca.png
```

## 출력

- 선택한 PCA 차원으로 변환된 데이터(`pca_output.csv`)
- 설명 분산 비율(콘솔 출력)
- 산점도 이미지(옵션)


## 3) 연구개념도 한글 번역

- `hyperspectral_framework_ko.md`: 논문용 연구개념도 문구를 프레임 구조에 맞춰 한글로 옮긴 버전

