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

---

## 3) JCH 논문용: 7개 수식 학습 순서 (초분광 보존 분석)

아래 순서대로 보면 수식들이 서로 어떻게 이어지는지 빠르게 잡을 수 있습니다.

### Step 0. 데이터 신뢰성 확인 (SNR)

- 아이디어: **신호(평균) / 잡음(표준편차)**
- 해석: SNR이 높아야 뒤 수식(RMSE, SAM, BD, PCA)의 결론도 신뢰 가능

### Step 1. Eq.(1) RMSE — “얼마나 달라졌나(크기)”

- 비교: 기준 시점 `R0(λ)` vs 현재 `Rt(λ)`
- 의미: 전체 파장에서 변화량의 절대 크기를 1개 숫자로 요약
- 포인트: 값이 작을수록 장기 안정성 높음

### Step 2. Eq.(2) SAM — “모양이 달라졌나(형태)”

- 비교: 두 스펙트럼 벡터 사이의 각도
- 의미: 밝기 스케일 변화보다 **형태 변화**(흡수대 패턴)에 민감
- 포인트: `SAM ≈ 0°`이면 형태 유지

### Step 3. Eq.(3) R950/R1000 — “950 nm 지문 있나?”

- 계산: `mean(945–955) / mean(995–1005)`
- 의미: 조명/알베도 영향을 줄이고 950 nm 상대 피처만 강조
- 포인트: 1보다 충분히 크면 950 부근 피크/숄더 가능성

### Step 4. Eq.(4) Continuum — “흡수대 위 기준선 만들기”

- 계산: 흡수대 양쪽 어깨를 직선으로 연결(선형 보간)
- 의미: 흡수대가 없었다면 따라갔을 배경선 정의

### Step 5. Eq.(5) Continuum Removed Reflectance — “기준선으로 정규화”

- 계산: `Rcr(λ)=R(λ)/Rc(λ)`
- 의미: 어깨는 1.0 근처, 흡수대 바닥은 1.0보다 작게 정렬
- 포인트: 서로 다른 시편의 밝기 차이를 보정

### Step 6. Eq.(6) BD1900 — “1900 nm 흡수 깊이 수치화”

- 계산: `BD = 1 - Rcr(λc)`
- 의미: 수분/H2O/OH 관련 흡수 강도를 단일 지표로 표현
- 포인트: 클수록 흡수대 깊음(수분/OH 관련 신호 강함)

### Step 7. Eq.(7) PCA Score — “수백 파장을 2~3축으로 압축”

- 계산: `tk = Xc × pk`
- 의미: 시편 간 전체 분광 패턴 유사도/차이를 좌표로 시각화
- 포인트: 점이 가까우면 스펙트럼 유사, 멀면 상이

### 논문 해석용 1분 체크리스트

- RMSE↑ + SAM↓: 밝기/수준은 변했지만 형태는 유지
- RMSE↓ + SAM↑: 전체 수준은 비슷하지만 형태 변화 존재
- R950/R1000↑: 950 nm 특징 피처 강화
- BD1900↑: 1900 nm 수분/OH 흡수대 심화
- PCA에서 군집 분리↑: 처리군 간 분광학적 차이 확대

### 추천 학습 루틴 (실제 적용)

1. 동일 ROI에서 기준 시점/현재 시점 스펙트럼 정리
2. RMSE·SAM 계산 후 “크기 vs 형태” 분리 해석
3. 950 nm 밴드비와 1900 nm BD로 특징 대역 해석
4. 마지막에 PCA로 전체 패턴 일관성 확인
