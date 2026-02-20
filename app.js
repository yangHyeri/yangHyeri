const equations = [
  {
    id: 'home',
    navLabel: 'Home',
    cardTitle: '학습 가이드',
    short: '7개 수식의 역할을 한 흐름으로 이해하기',
    tag: '개요',
    detailTitle: '전체 분석 흐름',
    detailSummary: 'SNR로 데이터 품질을 점검한 뒤, RMSE/SAM으로 장기 안정성, 밴드 기반 지표로 특징 파장대, 마지막으로 PCA로 전체 구조를 요약합니다.',
    formula: 'SNR(λ) = μ(λ) / σ(λ)',
    points: [
      'SNR이 충분히 높아야 나머지 수식 해석의 신뢰도가 확보됩니다.',
      'RMSE는 변화량(크기), SAM은 변화양상(형태)을 분리해 봅니다.',
      'R950/R1000 + BD1900으로 특정 대역의 화학적 거동을 해석합니다.',
      'PCA score로 전체 스펙트럼 분산 구조를 시각적으로 확인합니다.'
    ]
  },
  {
    id: 'eq1',
    navLabel: 'Eq.1 RMSE',
    cardTitle: 'RMSE',
    short: '기준 스펙트럼 대비 반사율 수준의 절대 변화량',
    tag: '장기 안정성',
    detailTitle: 'Eq.(1) RMSE — 전체 변화량',
    detailSummary: '시간이 지나며 기준 스펙트럼에서 얼마나 멀어졌는지를 파장 전체에서 계산합니다.',
    formula: 'RMSE = √[(1/N) Σ (Rt(λi) - R0(λi))²]',
    points: [
      '값이 작을수록 초기 상태와 유사해 분광학적 안정성이 높습니다.',
      '밝기/형태가 함께 섞여 반영되므로 SAM과 함께 해석해야 합니다.',
      '보존 처리 장기 모니터링에서 총 변화량 레이더 역할을 합니다.'
    ]
  },
  {
    id: 'eq2',
    navLabel: 'Eq.2 SAM',
    cardTitle: 'SAM',
    short: '스펙트럼 형태(shape)의 각도 기반 변화 측정',
    tag: '장기 안정성',
    detailTitle: 'Eq.(2) SAM — 스펙트럼 형태 변화',
    detailSummary: '두 스펙트럼 벡터의 각도를 계산해 밝기 스케일 영향보다 패턴 변화에 집중합니다.',
    formula: 'SAM = cos⁻¹[(Rt · R0) / (|Rt||R0|)]',
    points: [
      'SAM ≈ 0°이면 형태가 유사합니다.',
      '조명이나 거칠기 영향으로 전체 반사율이 바뀌어도 방향이 같으면 SAM은 작게 유지됩니다.',
      '흡수대 위치·깊이 변화 같은 물질 고유 패턴 변화를 민감하게 포착합니다.'
    ]
  },
  {
    id: 'eq3',
    navLabel: 'Eq.3 R950/R1000',
    cardTitle: 'R950/R1000',
    short: '950 nm 부근 상대 반사율 밴드비',
    tag: '특징 파장대',
    detailTitle: 'Eq.(3) R950/R1000 — 950 nm 지문',
    detailSummary: '950 nm 주변과 1000 nm 주변 반사율 평균의 비로 특정 피처의 존재를 강조합니다.',
    formula: 'R950/R1000 = mean(R945–955) / mean(R995–1005)',
    points: [
      '분모로 정규화해 조명·알베도 공통 변화를 줄입니다.',
      '1에 가까우면 평탄, 높을수록 950 nm 피크/숄더 가능성이 큽니다.',
      '처리제 구분에 유용한 분광 지문 지표로 활용됩니다.'
    ]
  },
  {
    id: 'eq4',
    navLabel: 'Eq.4 Continuum',
    cardTitle: 'Continuum',
    short: '흡수대 분석을 위한 연속선 기준 직선',
    tag: '특징 파장대',
    detailTitle: 'Eq.(4) Continuum — 기준선 정의',
    detailSummary: '흡수대 양쪽 어깨를 잇는 선형 보간으로 기준선을 구성합니다.',
    formula: 'Rc(λ) = Rl + (Rr - Rl) × (λ - λl) / (λr - λl)',
    points: [
      '흡수대가 없었다면 따랐을 배경 스펙트럼을 가정합니다.',
      '시편 간 절대 밝기 차이를 보정하는 준비 단계입니다.',
      '다음 식(Eq.5, Eq.6)의 기준값 Rc(λ)를 제공합니다.'
    ]
  },
  {
    id: 'eq5',
    navLabel: 'Eq.5 CR',
    cardTitle: 'Continuum Removal',
    short: '연속선으로 정규화한 흡수대 형태',
    tag: '특징 파장대',
    detailTitle: 'Eq.(5) Continuum-Removed Reflectance',
    detailSummary: '실측 반사율을 연속선으로 나눠 흡수대 형태를 정규화합니다.',
    formula: 'Rcr(λ) = R(λ) / Rc(λ)',
    points: [
      '어깨 구간은 1.0 근처, 흡수대 중심은 1.0 미만으로 표현됩니다.',
      '절대 반사율 차이보다 상대적 흡수 형태 비교에 강합니다.',
      'BD 계산을 위한 직접 입력값을 제공합니다.'
    ]
  },
  {
    id: 'eq6',
    navLabel: 'Eq.6 BD',
    cardTitle: 'BD (Band Depth)',
    short: '1900 nm 흡수대 상대적 깊이',
    tag: '특징 파장대',
    detailTitle: 'Eq.(6) BD1900 — 수분/OH 흡수 강도',
    detailSummary: '연속선 제거 반사율을 이용해 1900 nm 흡수대 깊이를 수치화합니다.',
    formula: 'BD = 1 - Rcr(λc) = 1 - R(λc)/Rc(λc)',
    points: [
      '값이 클수록 흡수대가 깊고 수분/OH 관련 신호가 강합니다.',
      '직접 R(1900) 비교보다 밝기 보정된 해석이 가능합니다.',
      '가속 조건에서 처리 방식별 수분 거동 차이를 판단하는 핵심 지표입니다.'
    ]
  },
  {
    id: 'eq7',
    navLabel: 'Eq.7 PCA',
    cardTitle: 'PCA Score',
    short: '전체 스펙트럼 분산 구조의 차원 축소 요약',
    tag: '차원축소',
    detailTitle: 'Eq.(7) PCA Score — 분산 구조 요약',
    detailSummary: '평균 중심화 데이터 Xc를 로딩 벡터 pk에 투영해 각 시편의 점수 tk를 계산합니다.',
    formula: 'tk = Xc × pk',
    points: [
      '가까운 점은 유사 스펙트럼, 먼 점은 이질 스펙트럼을 뜻합니다.',
      '시간 경과 궤적을 통해 처리군의 변화 방향을 파악할 수 있습니다.',
      '단일 지표가 아닌 전체 파장 구조를 함께 고려합니다.'
    ]
  }
];

const symbolDict = {
  'λ': '파장 (wavelength)',
  'μ(λ)': '해당 파장의 평균 신호',
  'σ(λ)': '해당 파장의 표준편차(잡음 크기)',
  'N': '전체 파장 밴드 수',
  'Rt(λi)': '시점 t에서 i번째 파장의 반사율',
  'R0(λi)': '기준 시점에서 i번째 파장의 반사율',
  'Rl': '흡수대 왼쪽 어깨 반사율',
  'Rr': '흡수대 오른쪽 어깨 반사율',
  'Rc(λ)': '연속선 반사율',
  'Rcr(λ)': '연속선 제거 반사율',
  'λc': '흡수대 중심 파장',
  'Xc': '평균 중심화 데이터 행렬',
  'pk': 'k번째 주성분 로딩 벡터',
  'tk': 'k번째 주성분 점수'
};

const refs = {
  topNav: document.getElementById('topNav'),
  cards: document.getElementById('equationCards'),
  detailTitle: document.getElementById('detailTitle'),
  detailSummary: document.getElementById('detailSummary'),
  detailFormula: document.getElementById('detailFormula'),
  detailPoints: document.getElementById('detailPoints')
};

function symbolized(formula) {
  const keys = Object.keys(symbolDict).sort((a, b) => b.length - a.length);
  let rendered = formula;
  keys.forEach((key) => {
    const safe = key.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    rendered = rendered.replace(new RegExp(safe, 'g'), `<span class="symbol" data-tip="${symbolDict[key]}">${key}</span>`);
  });
  return rendered;
}

function renderNav() {
  refs.topNav.innerHTML = '';
  equations.forEach((eq) => {
    const btn = document.createElement('button');
    btn.className = 'tab-btn';
    btn.textContent = eq.navLabel;
    btn.dataset.id = eq.id;
    btn.addEventListener('click', () => setActive(eq.id));
    refs.topNav.appendChild(btn);
  });
}

function renderCards() {
  refs.cards.innerHTML = '';
  equations.filter((eq) => eq.id !== 'home').forEach((eq, idx) => {
    const card = document.createElement('article');
    card.className = 'eq-card';
    card.dataset.id = eq.id;
    card.innerHTML = `
      <p class="eq-index">EQUATION ${idx + 1}</p>
      <h3>${eq.cardTitle}</h3>
      <p>${eq.short}</p>
      <span class="tag">${eq.tag}</span>
    `;
    card.addEventListener('click', () => setActive(eq.id));
    refs.cards.appendChild(card);
  });
}

function renderDetail(eq) {
  refs.detailTitle.textContent = eq.detailTitle;
  refs.detailSummary.textContent = eq.detailSummary;
  refs.detailFormula.innerHTML = symbolized(eq.formula);
  refs.detailPoints.innerHTML = '';
  eq.points.forEach((text) => {
    const li = document.createElement('li');
    li.textContent = text;
    refs.detailPoints.appendChild(li);
  });
}

function setActive(id) {
  const selected = equations.find((eq) => eq.id === id) || equations[0];
  renderDetail(selected);

  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.id === selected.id);
  });

  document.querySelectorAll('.eq-card').forEach((card) => {
    card.classList.toggle('active', card.dataset.id === selected.id);
  });
}

renderNav();
renderCards();
setActive('home');
