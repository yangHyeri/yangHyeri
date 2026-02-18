# IPA Quest + PCA 분석 예시

이 저장소는 두 가지 미니 프로젝트를 포함합니다.

1. **IPA Quest**: 영어 발음기호(IPA)를 게임처럼 학습해 사전 발음기호만 보고 단어를 읽는 훈련 앱
2. **PCA 분석 예시**: CSV/엑셀 데이터에 PCA를 적용하는 Python 스크립트

---

## 1) IPA Quest (영어 발음기호 마스터 게임)

### 바로 실행 (학습 시작)

```bash
python -m http.server 8000
```

브라우저에서 `http://localhost:8000` 접속 후 학습하세요.

### 서버 접속이 안 될 때 (권장)

`ipa_quest_standalone.html` 파일을 더블클릭해서 브라우저로 열면 됩니다.
로컬 서버(`localhost`) 없이도 학습 가능합니다.

### 제공 모드

- **기호→소리**: IPA 기호를 보고 소리를 맞히는 기본 훈련
- **단어 읽기**: 단어 + 발음기호를 보고 읽기 선택
- **직접 타이핑**: 정답을 직접 입력하는 실전 모드
- **오답 복습**: 틀린 단어만 모아 재훈련

### 학습 기능

- 점수, 레벨, 연속 정답, 정확도
- 마스터리 추적(항목별 숙련도)
- 오답 자동 누적 및 복습
- 브라우저 저장(localStorage)으로 학습 진도 유지
- Web Speech API 발음 재생

### 하루 20분 추천 루틴

1. 기호→소리 10문제
2. 단어 읽기 10문제
3. 직접 타이핑 5문제
4. 오답 복습 5문제

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
