const SAMPLE_SENTENCE =
  'Packing took about 30 minutes, and if we wanted to eat inside the restaurant, we would have had to wait much longer.';

const refs = {
  input: document.getElementById('sentenceInput'),
  analyzeBtn: document.getElementById('analyzeBtn'),
  sampleBtn: document.getElementById('sampleBtn'),
  chips: document.getElementById('chips'),
  explanation: document.getElementById('explanation'),
};

refs.analyzeBtn.addEventListener('click', () => {
  const sentence = refs.input.value.trim();
  if (!sentence) {
    renderResult({
      tags: ['입력 필요'],
      text: '문장을 먼저 입력해주세요.',
    });
    return;
  }

  const result = analyzeSentence(sentence);
  renderResult(result);
});

refs.sampleBtn.addEventListener('click', () => {
  refs.input.value = SAMPLE_SENTENCE;
  refs.input.focus();
});

function renderResult({ tags, text }) {
  refs.chips.innerHTML = '';
  tags.forEach((tag) => {
    const chip = document.createElement('span');
    chip.className = 'chip';
    chip.textContent = tag;
    refs.chips.appendChild(chip);
  });

  refs.explanation.textContent = text;
  refs.explanation.classList.remove('empty');
}

function analyzeSentence(sentence) {
  const normalized = sentence.toLowerCase();
  const tags = [];
  const lines = [];

  if (containsWouldHaveHadTo(normalized)) {
    tags.push('핵심: would have had to');
    lines.push(
      '🔎 "would have had to"는 과거 가정문에서 자주 나오는 결합 표현입니다.',
      '',
      '1) would',
      '- 조동사로, 여기서는 "가정 상황이라면 ~했을 텐데"라는 뉘앙스를 만듭니다.',
      '',
      '2) have had to',
      '- had to = "~해야 했다" (과거 의무)',
      '- 여기에 have가 붙어 would have had to가 되면, 실제로 벌어진 과거가 아니라 "그랬다면 과거에 ~해야 했을 것"이라는 뜻이 됩니다.',
      '',
      '즉, "we would have had to wait"는 "(만약 식당 안에서 먹으려고 했다면) 우리는 더 오래 기다려야 했을 텐데"에 가깝습니다.'
    );
  }

  if (normalized.includes('if ') && normalized.includes('would have')) {
    tags.push('가정법 (혼합/과거 가정)');
    lines.push(
      '',
      '💡 if절 + would have 구문이 함께 쓰여 과거의 가정/결과를 설명하고 있습니다.',
      '문맥에 따라 전형적 형태(if + had p.p., would have p.p.)에서 조금 변형되어도 의미는 "사실과 다른 과거 상황"을 가리킬 수 있습니다.'
    );
  }

  if (normalized.includes('took')) {
    tags.push('단순과거');
    lines.push('', '🕒 "Packing took about 30 minutes"는 실제로 일어난 사실을 단순과거로 서술한 부분입니다.');
  }

  if (tags.length === 0) {
    tags.push('기본 분석');
    lines.push(
      '아직 이 문장에 대한 상세 룰이 없어서 기본 설명을 제공합니다.',
      '- 조동사(would, could, might)와 완료형(have + p.p.)을 먼저 찾아보세요.',
      '- if절이 있으면 가정법 가능성을 확인해보세요.'
    );
  }

  return {
    tags,
    text: lines.join('\n'),
  };
}

function containsWouldHaveHadTo(text) {
  return /would\s+have\s+had\s+to/.test(text);
}
