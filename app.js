const symbolQuiz = [
  { ipa: '/iː/', sound: '길게 이', examples: ['see', 'team'], distractors: ['짧은 이', '에', '어'] },
  { ipa: '/ɪ/', sound: '짧은 이', examples: ['sit', 'ship'], distractors: ['길게 이', '에이', '아'] },
  { ipa: '/æ/', sound: '애', examples: ['cat', 'map'], distractors: ['아', '에', '어'] },
  { ipa: '/ʌ/', sound: '어(짧게)', examples: ['cup', 'love'], distractors: ['오', '애', '아'] },
  { ipa: '/ɑː/', sound: '아(길게)', examples: ['car', 'father'], distractors: ['오', '어', '애'] },
  { ipa: '/ɔː/', sound: '오(길게)', examples: ['law', 'call'], distractors: ['아', '우', '어'] },
  { ipa: '/uː/', sound: '우(길게)', examples: ['blue', 'food'], distractors: ['짧은 우', '오', '아'] },
  { ipa: '/ʊ/', sound: '짧은 우', examples: ['book', 'good'], distractors: ['길게 우', '어', '오'] },
  { ipa: '/eɪ/', sound: '에이', examples: ['name', 'day'], distractors: ['에', '아이', '오우'] },
  { ipa: '/aɪ/', sound: '아이', examples: ['time', 'my'], distractors: ['에이', '오이', '아'] },
  { ipa: '/oʊ/', sound: '오우', examples: ['go', 'home'], distractors: ['오', '아우', '어'] },
  { ipa: '/aʊ/', sound: '아우', examples: ['now', 'house'], distractors: ['오우', '아이', '어'] },
  { ipa: '/θ/', sound: '혀를 이 사이에 둔 쓰', examples: ['think', 'bath'], distractors: ['스', '즈', '트'] },
  { ipa: '/ð/', sound: '혀를 이 사이에 둔 즈', examples: ['this', 'mother'], distractors: ['더', '스', '브'] },
  { ipa: '/ʃ/', sound: '쉬', examples: ['she', 'mission'], distractors: ['스', '치', '지'] },
  { ipa: '/tʃ/', sound: '취', examples: ['chair', 'watch'], distractors: ['쉬', '츠', '티'] },
  { ipa: '/dʒ/', sound: '쥐', examples: ['job', 'bridge'], distractors: ['즈', '취', '지'] }
];

const wordQuiz = [
  { word: 'schedule', ipa: '/ˈskedʒuːl/', reading: '스케줄', aliases: ['스케쥴'], meaning: '일정표' },
  { word: 'enough', ipa: '/ɪˈnʌf/', reading: '이너프', aliases: [], meaning: '충분한' },
  { word: 'colonel', ipa: '/ˈkɜːrnəl/', reading: '커널', aliases: ['커널(컬널X)'], meaning: '대령' },
  { word: 'island', ipa: '/ˈaɪlənd/', reading: '아일랜드', aliases: [], meaning: '섬' },
  { word: 'choir', ipa: '/ˈkwaɪər/', reading: '콰이어', aliases: [], meaning: '합창단' },
  { word: 'fruit', ipa: '/fruːt/', reading: '프루트', aliases: [], meaning: '과일' },
  { word: 'world', ipa: '/wɜːrld/', reading: '월드', aliases: [], meaning: '세계' },
  { word: 'genre', ipa: '/ˈʒɑːnrə/', reading: '장르', aliases: ['잔르'], meaning: '장르' },
  { word: 'heart', ipa: '/hɑːrt/', reading: '하트', aliases: [], meaning: '심장' },
  { word: 'earth', ipa: '/ɜːrθ/', reading: '얼쓰', aliases: ['어스'], meaning: '지구' }
];

const STORAGE_KEY = 'ipa-quest-progress-v2';

const state = {
  mode: 'symbol',
  score: 0,
  streak: 0,
  level: 1,
  total: 0,
  correct: 0,
  current: null,
  mastery: new Map(),
  wrongItems: [],
  answered: false,
};

const refs = {
  level: document.getElementById('level'),
  score: document.getElementById('score'),
  streak: document.getElementById('streak'),
  accuracy: document.getElementById('accuracy'),
  questionTitle: document.getElementById('questionTitle'),
  promptArea: document.getElementById('promptArea'),
  subText: document.getElementById('subText'),
  choices: document.getElementById('choices'),
  feedback: document.getElementById('feedback'),
  nextBtn: document.getElementById('nextBtn'),
  speakBtn: document.getElementById('speakBtn'),
  resetBtn: document.getElementById('resetBtn'),
  masteryList: document.getElementById('masteryList'),
  modeHint: document.getElementById('modeHint'),
  modeButtons: [...document.querySelectorAll('.mode-btn')],
  typingArea: document.getElementById('typingArea'),
  typingInput: document.getElementById('typingInput'),
  submitTypingBtn: document.getElementById('submitTypingBtn'),
};

function shuffle(list) {
  return [...list].sort(() => Math.random() - 0.5);
}

function saveProgress() {
  const payload = {
    score: state.score,
    streak: state.streak,
    level: state.level,
    total: state.total,
    correct: state.correct,
    mastery: [...state.mastery.entries()],
    wrongItems: state.wrongItems,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

function loadProgress() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return;
  try {
    const parsed = JSON.parse(raw);
    state.score = parsed.score || 0;
    state.streak = parsed.streak || 0;
    state.level = parsed.level || 1;
    state.total = parsed.total || 0;
    state.correct = parsed.correct || 0;
    state.mastery = new Map(parsed.mastery || []);
    state.wrongItems = parsed.wrongItems || [];
  } catch {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function pickReviewItem() {
  if (!state.wrongItems.length) return null;
  return state.wrongItems[Math.floor(Math.random() * state.wrongItems.length)];
}

function getTypingAccepted(item) {
  return [item.reading, ...(item.aliases || [])].map((v) => v.replaceAll(' ', '').toLowerCase());
}

function prepareTypingMode(item = null) {
  const picked = item || wordQuiz[Math.floor(Math.random() * wordQuiz.length)];
  state.current = { ...picked, key: `typing:${picked.word}` };
  refs.questionTitle.textContent = '직접 타이핑: IPA 보고 읽기 입력';
  refs.promptArea.textContent = `${picked.word}  ${picked.ipa}`;
  refs.subText.textContent = `뜻: ${picked.meaning}`;
  refs.modeHint.textContent = '선택지가 없으니, 실제 시험처럼 스스로 읽기를 적어보세요.';
  refs.typingArea.classList.remove('hidden');
  refs.typingInput.value = '';
  refs.typingInput.focus();
}

function buildChoiceQuestion(pool, kind) {
  if (kind === 'symbol') {
    const item = pool[Math.floor(Math.random() * pool.length)];
    const answers = shuffle([item.sound, ...item.distractors]).slice(0, 4);
    state.current = { ...item, answer: item.sound, key: `symbol:${item.ipa}` };
    refs.questionTitle.textContent = '기호를 보고 소리를 고르세요';
    refs.promptArea.textContent = item.ipa;
    refs.subText.textContent = `예시: ${item.examples.join(', ')}`;
    refs.modeHint.textContent = '모음 길이(ː), 강세(ˈ), 혀 위치를 확인하세요.';
    return answers;
  }

  const item = pool[Math.floor(Math.random() * pool.length)];
  const distractors = shuffle(wordQuiz.filter((w) => w.word !== item.word)).slice(0, 3).map((w) => w.reading);
  const answers = shuffle([item.reading, ...distractors]);
  state.current = { ...item, answer: item.reading, key: `${kind}:${item.word}` };
  refs.questionTitle.textContent = kind === 'review' ? '오답 복습 모드' : '사전 발음기호만 보고 단어 읽기';
  refs.promptArea.textContent = `${item.word}  ${item.ipa}`;
  refs.subText.textContent = `뜻: ${item.meaning}`;
  refs.modeHint.textContent = kind === 'review'
    ? '틀렸던 단어를 다시 맞히면 오답 목록에서 제거됩니다.'
    : '강세(ˈ) 위치와 장모음(ː)을 먼저 체크하고 읽으세요.';
  return answers;
}

function nextQuestion() {
  state.answered = false;
  refs.nextBtn.disabled = true;
  refs.feedback.textContent = '';
  refs.feedback.className = 'feedback';
  refs.choices.innerHTML = '';
  refs.typingArea.classList.add('hidden');

  if (state.mode === 'typing') {
    prepareTypingMode();
    return;
  }

  if (state.mode === 'review') {
    const review = pickReviewItem();
    if (!review) {
      refs.questionTitle.textContent = '오답 복습 모드';
      refs.promptArea.textContent = '🎉 복습할 오답이 없습니다!';
      refs.subText.textContent = '다른 모드에서 문제를 풀고 다시 오세요.';
      refs.modeHint.textContent = '오답이 생기면 자동으로 여기에 쌓입니다.';
      return;
    }
    const options = buildChoiceQuestion([review], 'review');
    options.forEach(makeChoiceButton);
    return;
  }

  const options = state.mode === 'symbol'
    ? buildChoiceQuestion(symbolQuiz, 'symbol')
    : buildChoiceQuestion(wordQuiz, 'word');
  options.forEach(makeChoiceButton);
}

function makeChoiceButton(answer) {
  const btn = document.createElement('button');
  btn.className = 'choice';
  btn.textContent = answer;
  btn.onclick = () => checkChoiceAnswer(answer, btn);
  refs.choices.appendChild(btn);
}

function markWrongItem(item) {
  if (!item.word) return;
  if (!state.wrongItems.some((w) => w.word === item.word)) {
    state.wrongItems.push({ word: item.word, ipa: item.ipa, reading: item.reading, meaning: item.meaning });
  }
}

function removeWrongItem(item) {
  if (!item.word) return;
  state.wrongItems = state.wrongItems.filter((w) => w.word !== item.word);
}

function applyResult(isCorrect, explicitAnswer = '') {
  state.total += 1;
  if (isCorrect) {
    state.correct += 1;
    state.streak += 1;
    const bonus = 12 + Math.min(state.streak, 10);
    state.score += bonus;
    refs.feedback.textContent = `정답! +${bonus}점`; 
    refs.feedback.classList.add('ok');
    removeWrongItem(state.current);
  } else {
    state.streak = 0;
    state.score = Math.max(0, state.score - 5);
    const answerText = state.current.answer || state.current.reading;
    refs.feedback.textContent = `오답! ${explicitAnswer ? `(입력: ${explicitAnswer}) ` : ''}정답은 "${answerText}"`;
    refs.feedback.classList.add('bad');
    markWrongItem(state.current);
  }

  const currentMastery = state.mastery.get(state.current.key) || 0;
  state.mastery.set(state.current.key, Math.max(0, currentMastery + (isCorrect ? 1 : -1)));

  state.level = Math.floor(state.score / 150) + 1;
  renderStatus();
  renderMastery();
  refs.nextBtn.disabled = false;
  saveProgress();
}

function checkChoiceAnswer(answer, selectedBtn) {
  if (state.answered) return;
  state.answered = true;

  const isCorrect = answer === state.current.answer;
  [...refs.choices.children].forEach((btn) => {
    if (btn.textContent === state.current.answer) btn.classList.add('correct');
  });
  if (!isCorrect) selectedBtn.classList.add('wrong');

  applyResult(isCorrect);
}

function checkTypingAnswer() {
  if (state.answered || state.mode !== 'typing') return;
  const user = refs.typingInput.value.trim();
  if (!user) {
    refs.feedback.textContent = '입력 후 제출해주세요.';
    refs.feedback.className = 'feedback bad';
    return;
  }
  state.answered = true;
  const normalized = user.replaceAll(' ', '').toLowerCase();
  const accepted = getTypingAccepted(state.current);
  const isCorrect = accepted.includes(normalized);
  applyResult(isCorrect, user);
}

function renderStatus() {
  refs.level.textContent = String(state.level);
  refs.score.textContent = String(state.score);
  refs.streak.textContent = String(state.streak);
  const acc = state.total === 0 ? 0 : Math.round((state.correct / state.total) * 100);
  refs.accuracy.textContent = `${acc}%`;
}

function renderMastery() {
  refs.masteryList.innerHTML = '';
  const top = [...state.mastery.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);

  if (!top.length) {
    const li = document.createElement('li');
    li.textContent = '아직 데이터가 없어요. 첫 문제를 풀어보세요!';
    refs.masteryList.appendChild(li);
    return;
  }

  top.forEach(([key, val]) => {
    const li = document.createElement('li');
    const status = val >= 3 ? '🔥 마스터' : val >= 1 ? '📈 진행중' : '🔁 복습필요';
    li.textContent = `${key} — ${status}`;
    refs.masteryList.appendChild(li);
  });
}

function speakCurrent() {
  if (!state.current) return;
  const utt = new SpeechSynthesisUtterance();
  utt.lang = 'en-US';
  utt.text = state.current.examples?.[0] || state.current.word || '';
  speechSynthesis.cancel();
  speechSynthesis.speak(utt);
}

function resetProgress() {
  localStorage.removeItem(STORAGE_KEY);
  state.score = 0;
  state.streak = 0;
  state.level = 1;
  state.total = 0;
  state.correct = 0;
  state.mastery = new Map();
  state.wrongItems = [];
  renderStatus();
  renderMastery();
  nextQuestion();
}

refs.modeButtons.forEach((btn) => {
  btn.addEventListener('click', () => {
    refs.modeButtons.forEach((b) => b.classList.remove('active'));
    btn.classList.add('active');
    state.mode = btn.dataset.mode;
    nextQuestion();
  });
});

refs.nextBtn.addEventListener('click', nextQuestion);
refs.speakBtn.addEventListener('click', speakCurrent);
refs.resetBtn.addEventListener('click', resetProgress);
refs.submitTypingBtn.addEventListener('click', checkTypingAnswer);
refs.typingInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') checkTypingAnswer();
});

loadProgress();
renderStatus();
renderMastery();
nextQuestion();
