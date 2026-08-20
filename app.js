let currentUser = null;
let currentQuestion = null;
let hintsUsed = 0;
let lastWrongContext = null;

document.addEventListener('DOMContentLoaded', async () => {
  await checkAuth();
});

async function checkAuth() {
  const res = await fetch('/api/me');
  const data = await res.json();
  if (data.user) {
    currentUser = data.user;
    renderAuthenticated();
  } else {
    currentUser = null;
    renderUnauthenticated();
  }
}

function renderUnauthenticated() {
  document.getElementById('sidebar').style.display = 'none';
  document.getElementById('topNav').style.display = 'none';
  document.getElementById('view-auth').style.display = 'block';
  document.getElementById('view-app').style.display = 'none';
}

function renderAuthenticated() {
  document.getElementById('sidebar').style.display = 'flex';
  document.getElementById('topNav').style.display = 'flex';
  document.getElementById('view-auth').style.display = 'none';
  document.getElementById('view-app').style.display = 'block';

  // Role permissions: hide teacher view for students
  const teacherNavLi = document.getElementById('nav-teacher-li');
  if (currentUser.role !== 'student') {
    teacherNavLi.style.display = 'block';
  } else {
    teacherNavLi.style.display = 'none';
  }

  // Render HUD
  const roleTitle = currentUser.role.charAt(0).toUpperCase() + currentUser.role.slice(1);
  const uidChip = currentUser.student_uid ? `<div class="chip">🆔 ${currentUser.student_uid}</div>` : '';
  document.getElementById('navUserBadge').innerText = `${currentUser.username} (${roleTitle})`;
  document.getElementById('userHud').innerHTML = `
    <div class="chip">${currentUser.role === 'student' ? '🎓 Student' : currentUser.role === 'teacher' ? '👩‍🏫 Teacher' : '👤 Educator'}</div>
    <div class="chip">👤 ${currentUser.username}</div>
    ${uidChip}
    <div class="chip">🏆 LV ${currentUser.level}</div>
    <div class="chip">✨ ${currentUser.xp} XP</div>
    <div class="chip">🔥 ${currentUser.streak} streak</div>
  `;

  // Render Home Greeting
  document.getElementById('homeKicker').innerText = `WELCOME BACK · ${currentUser.role.toUpperCase()} ACCOUNT ${currentUser.student_uid ? '· ' + currentUser.student_uid : ''}`;
  document.getElementById('homeGreeting').innerText = `Hello, ${currentUser.username}! 👋`;

  renderHomeCards();
  switchView('home');
}

function renderHomeCards() {
  let cardsHtml = `
    <div class="card">
      <h3>🎮 Play / Diagnostic</h3>
      <p style="color: #475569; margin-bottom: 1rem;">Start adaptive problem solving or complete your initial skill diagnostic.</p>
      <button class="btn btn-outline btn-block" onclick="switchView('play')">Go to Play Mode ➔</button>
    </div>
    <div class="card">
      <h3>🗺️ Skill Map</h3>
      <p style="color: #475569; margin-bottom: 1rem;">Explore your Python World skill tree and track unlocked topic nodes.</p>
      <button class="btn btn-outline btn-block" onclick="switchView('skill_map')">Explore Skill Map ➔</button>
    </div>
    <div class="card">
      <h3>📊 Student Dashboard</h3>
      <p style="color: #475569; margin-bottom: 1rem;">View your personalized progress, accuracy metrics, and recommended next topics.</p>
      <button class="btn btn-outline btn-block" onclick="switchView('dashboard')">View Dashboard ➔</button>
    </div>
  `;

  if (currentUser.role !== 'student') {
    cardsHtml += `
      <div class="card">
        <h3>👩‍🏫 Teacher View & Leaderboard</h3>
        <p style="color: #475569; margin-bottom: 1rem;">Analyze student performance, observe student IDs, or check XP standings.</p>
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-outline" style="flex: 1;" onclick="switchView('leaderboard')">Leaderboard 🏆</button>
          <button class="btn btn-primary" style="flex: 1;" onclick="switchView('teacher')">Teacher View 👩‍🏫</button>
        </div>
      </div>
    `;
  } else {
    cardsHtml += `
      <div class="card">
        <h3>🏆 Arena Leaderboard</h3>
        <p style="color: #475569; margin-bottom: 1rem;">Compare your XP standings and streaks on the class leaderboard.</p>
        <button class="btn btn-outline btn-block" onclick="switchView('leaderboard')">View Leaderboard 🏆</button>
      </div>
    `;
  }

  document.getElementById('homeCardsGrid').innerHTML = cardsHtml;
}

function switchView(viewName) {
  const views = ['home', 'play', 'skill_map', 'dashboard', 'leaderboard', 'teacher'];
  views.forEach(v => {
    const el = document.getElementById(`subview-${v}`);
    if (el) el.style.display = (v === viewName) ? 'block' : 'none';
  });

  // Update nav active link
  document.querySelectorAll('.nav-item').forEach(link => link.classList.remove('active'));

  if (viewName === 'play') loadPlayQuestion();
  if (viewName === 'skill_map') loadSkillMap();
  if (viewName === 'dashboard') loadDashboard();
  if (viewName === 'leaderboard') loadLeaderboard();
  if (viewName === 'teacher') loadTeacherDashboard();
}

function switchAuthTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  if (tab === 'login') {
    document.querySelector('.tab-btn:first-child').classList.add('active');
    document.getElementById('tab-login-form').style.display = 'block';
    document.getElementById('tab-join-form').style.display = 'none';
  } else {
    document.querySelector('.tab-btn:last-child').classList.add('active');
    document.getElementById('tab-login-form').style.display = 'none';
    document.getElementById('tab-join-form').style.display = 'block';
  }
}

function toggleVerifyMethod() {
  const method = document.querySelector('input[name="verifyMethod"]:checked').value;
  if (method === 'reg_num') {
    document.getElementById('verifyRegBox').style.display = 'block';
    document.getElementById('verifyCardBox').style.display = 'none';
  } else {
    document.getElementById('verifyRegBox').style.display = 'none';
    document.getElementById('verifyCardBox').style.display = 'block';
  }
}

async function submitLogin() {
  const u = document.getElementById('loginUsername').value.trim();
  const p = document.getElementById('loginPassword').value;
  if (!u || !p) return alert('Username and password required.');

  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: u, password: p }),
  });
  const data = await res.json();
  if (data.success) {
    currentUser = data.user;
    renderAuthenticated();
  } else {
    alert(data.error || 'Login failed.');
  }
}

async function submitRegister() {
  const role = document.getElementById('joinRole').value;
  const u = document.getElementById('joinUsername').value.trim();
  const p = document.getElementById('joinPassword').value;
  const method = document.querySelector('input[name="verifyMethod"]:checked').value;

  if (!u || !p) return alert('Username and password required.');

  const formData = new FormData();
  formData.append('role', role);
  formData.append('username', u);
  formData.append('password', p);
  formData.append('verify_method', method);

  if (method === 'reg_num') {
    const reg = document.getElementById('joinRegNum').value.trim();
    if (!reg) return alert('University Registration Number is required.');
    formData.append('reg_num', reg);
  } else {
    const fileInput = document.getElementById('joinIdCardFile');
    if (!fileInput.files || !fileInput.files[0]) return alert('University ID Card file is required.');
    formData.append('id_card_file', fileInput.files[0]);
  }

  const res = await fetch('/api/auth/register', { method: 'POST', body: formData });
  const data = await res.json();
  if (data.success) {
    currentUser = data.user;
    renderAuthenticated();
  } else {
    alert(data.error || 'Registration failed.');
  }
}

async function logout() {
  await fetch('/api/auth/logout', { method: 'POST' });
  currentUser = null;
  renderUnauthenticated();
}

async function loadPlayQuestion() {
  hintsUsed = 0;
  const container = document.getElementById('playQuestionContainer');
  container.innerHTML = `<div class="card">Loading question...</div>`;

  const res = await fetch('/api/play/next');
  const data = await res.json();

  if (data.diagnostic_completed) {
    container.innerHTML = `
      <div class="card" style="text-align: center; padding: 2.5rem;">
        <h2 style="color: var(--primary);">🎉 Diagnostic Assessment Complete!</h2>
        <p style="margin: 1rem 0;">Your live skill profile has been seeded. Jump into Adaptive Mode now!</p>
        <button class="btn btn-primary" onclick="loadPlayQuestion()">Start Adaptive Mode ➔</button>
      </div>
    `;
    return;
  }

  currentQuestion = data.question;
  const q = data.question;

  let choicesHtml = q.choices.map((c, i) => `
    <label style="display: block; background: #FFFFFF; border: 1px solid var(--border); border-radius: 12px; padding: 0.85rem 1.25rem; margin-bottom: 0.6rem; cursor: pointer; font-weight: 500;">
      <input type="radio" name="playChoice" value="${i}" style="margin-right: 0.6rem;" />
      ${c}
    </label>
  `).join('');

  container.innerHTML = `
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <span class="kicker">${q.topic_name} · ${q.difficulty.toUpperCase()}</span>
        <span style="font-family: 'Fira Code', monospace; font-size: 0.85rem; color: var(--text-muted);">${data.progress || data.mastery_info || ''}</span>
      </div>
      <div style="font-size: 1.15rem; font-weight: 600; line-height: 1.6; margin-bottom: 1.25rem;">
        ${q.prompt.replace(/\n/g, '<br/>')}
      </div>
      <div style="margin-bottom: 1.25rem;">${choicesHtml}</div>
      <div style="display: flex; gap: 1rem;">
        <button class="btn btn-outline" onclick="useHint()">Need a Hint (${hintsUsed}/3)</button>
        <button class="btn btn-primary" onclick="submitAnswer()">Lock in Answer ➔</button>
      </div>
      <div id="hintsBox" style="margin-top: 1rem;"></div>
    </div>
    <div id="doubtChatBoxWrapper"></div>
  `;
}

function useHint() {
  if (!currentQuestion) return;
  if (hintsUsed < currentQuestion.hints.length) {
    hintsUsed++;
    const box = document.getElementById('hintsBox');
    box.innerHTML = '';
    for (let i = 0; i < hintsUsed; i++) {
      box.innerHTML += `<div class="alert alert-warning">💡 <b>Hint ${i + 1}:</b> ${currentQuestion.hints[i]}</div>`;
    }
  }
}

async function submitAnswer() {
  const selected = document.querySelector('input[name="playChoice"]:checked');
  if (!selected) return alert('Please select an option first.');

  const chosenIdx = parseInt(selected.value);
  const res = await fetch('/api/play/submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question_id: currentQuestion.id, choice_index: chosenIdx, hints_used: hintsUsed }),
  });
  const data = await res.json();

  currentUser.xp = data.new_xp;
  currentUser.streak = data.streak;
  currentUser.level = data.level;
  checkAuth();

  const container = document.getElementById('playQuestionContainer');
  if (data.correct) {
    container.innerHTML = `
      <div class="card" style="border-left: 5px solid var(--primary);">
        <div class="alert alert-success">✅ <b>Correct!</b> +${data.xp_gained} XP · Live Mastery now ${(data.mastery * 100).toFixed(0)}% · Streak ${data.streak}</div>
        <p style="margin-bottom: 1rem;">${data.explain}</p>
        <button class="btn btn-primary" onclick="loadPlayQuestion()">Next Challenge ➔</button>
      </div>
    `;
  } else {
    lastWrongContext = data;
    container.innerHTML = `
      <div class="card" style="border-left: 5px solid #DC2626;">
        <div class="alert alert-error">❌ <b>Not quite.</b> +${data.xp_gained} XP.</div>
        <p><b>Your Pick:</b> <code>${data.picked}</code> | <b>Target:</b> <code>${data.target}</code></p>
        <p style="margin: 0.75rem 0;">${data.explain}</p>
        <button class="btn btn-primary" onclick="loadPlayQuestion()" style="margin-bottom: 1.5rem;">Continue to Next Question ➔</button>

        <!-- AI Doubt Clarifier Chatbot -->
        <div class="card" style="background: #FFFFFF; border: 1px solid var(--border);">
          <h3 style="color: var(--primary);">🤖 AI Doubt Clarifier Chatbot</h3>
          <div class="chat-box" id="doubtChatLogs">
            <div class="chat-msg assistant">
              <b>🤖 AI Tutor:</b> You selected <code>${data.picked}</code>, but the correct answer is <code>${data.target}</code>.<br/>
              <b>Concept Breakdown:</b> ${data.explain}<br/><br/>
              <i>Ask me any doubt or follow-up question below!</i>
            </div>
          </div>
          <div style="display: flex; gap: 0.75rem;">
            <input type="text" id="doubtInput" placeholder="Ask AI Tutor to explain why this option was false..." style="flex-grow: 1;" onkeypress="if(event.key==='Enter') sendDoubtMessage()" />
            <button class="btn btn-primary" onclick="sendDoubtMessage()">Ask AI</button>
          </div>
        </div>
      </div>
    `;
  }
}

async function sendDoubtMessage() {
  const input = document.getElementById('doubtInput');
  const query = input.value.trim();
  if (!query || !lastWrongContext) return;

  const chatLogs = document.getElementById('doubtChatLogs');
  chatLogs.innerHTML += `<div class="chat-msg user"><b>You:</b> ${query}</div>`;
  input.value = '';
  chatLogs.scrollTop = chatLogs.scrollHeight;

  const res = await fetch('/api/chat/doubt', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      topic: lastWrongContext.topic,
      picked: lastWrongContext.picked,
      target: lastWrongContext.target,
      explain: lastWrongContext.explain,
      query: query,
    }),
  });
  const data = await res.json();
  chatLogs.innerHTML += `<div class="chat-msg assistant"><b>🤖 AI Tutor:</b> ${data.reply}</div>`;
  chatLogs.scrollTop = chatLogs.scrollHeight;
}

async function loadSkillMap() {
  const res = await fetch('/api/skill_map');
  const data = await res.json();
  const nodes = data.nodes;

  let html = '';
  nodes.forEach(n => {
    const status = n.unlocked ? 'UNLOCKED' : 'LOCKED';
    const badgeClass = n.unlocked ? 'badge-green' : 'badge-red';
    html += `
      <div class="card" style="border-left: 5px solid ${n.unlocked ? 'var(--primary)' : '#94A3B8'};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h3>${n.name}</h3>
          <span class="badge ${badgeClass}">${status}</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          Mastery: <b>${(n.mastery * 100).toFixed(0)}%</b> · ${n.attempts} attempts
          ${n.unlocked ? ` · unlock next at ${n.unlock_threshold}` : ''}
        </p>
        <div class="progress-container">
          <div class="progress-bar" style="width: ${Math.min(100, n.mastery * 100)}%;"></div>
        </div>
      </div>
    `;
  });

  document.getElementById('skillMapNodes').innerHTML = html;
}

async function loadDashboard() {
  const res = await fetch('/api/dashboard');
  const data = await res.json();

  let skillBars = '';
  for (const [topic, m] of Object.entries(data.skills)) {
    skillBars += `
      <div style="margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem;">
          <span>${topic}</span>
          <span>${(m * 100).toFixed(0)}%</span>
        </div>
        <div class="progress-container">
          <div class="progress-bar" style="width: ${Math.min(100, m * 100)}%;"></div>
        </div>
      </div>
    `;
  }

  document.getElementById('studentDashboardContent').innerHTML = `
    <div class="grid-cols-4" style="margin-bottom: 1.5rem;">
      <div class="card" style="text-align: center;"><div class="kicker">LEVEL</div><h2>${currentUser.level}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">XP</div><h2>${currentUser.xp}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">STREAK</div><h2>🔥 ${currentUser.streak}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">OVERALL SKILL</div><h2>${(data.overall_mastery * 100).toFixed(0)}%</h2></div>
    </div>

    <div class="card">
      <h3>🎯 What should I learn next?</h3>
      <div class="alert alert-info"><b>${data.next_learn}</b> — ${data.next_learn_why}</div>
      <p><b>Today's Mission:</b> Complete 5 challenges in <b>${data.weakest_topic}</b>.</p>
    </div>

    <div class="card">
      <h3>📈 Skill Mastery Distribution</h3>
      ${skillBars}
    </div>
  `;
}

async function loadLeaderboard() {
  const res = await fetch('/api/leaderboard');
  const data = await res.json();

  let html = '';
  data.leaderboard.forEach(p => {
    const medal = p.rank === 1 ? '🥇' : p.rank === 2 ? '🥈' : p.rank === 3 ? '🥉' : `${p.rank}.`;
    const youBadge = p.is_you ? ' <span class="badge badge-green">YOU</span>' : '';
    html += `
      <div class="card" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <div>
          <span style="font-size: 1.25rem; margin-right: 0.75rem;">${medal}</span>
          <b>${p.username}</b>${youBadge} · <span style="color: var(--text-muted);">LV ${p.level}</span>
        </div>
        <div>
          <b>${p.xp} XP</b> · 🔥 ${p.streak} streak
        </div>
      </div>
    `;
  });

  document.getElementById('leaderboardList').innerHTML = html;
}

async function loadTeacherDashboard() {
  const res = await fetch('/api/teacher/students');
  const data = await res.json();
  const students = data.students || [];

  if (students.length === 0) {
    document.getElementById('teacherAnalyticsContent').innerHTML = `
      <div class="alert alert-info">
        💡 <b>No students currently under observation.</b><br/>
        Ask your students for their unique <b>Student ID (<code>STU-XXXXXX</code>)</b> and enter it above to start observing their learning path.
      </div>
    `;
    return;
  }

  const well = students.filter(s => s.category === 'Performing Well');
  const mod = students.filter(s => s.category === 'Moderate');
  const struggle = students.filter(s => s.category === 'Needs Intervention');

  let studentsListHtml = students.map(s => {
    const badgeClass = s.category === 'Performing Well' ? 'badge-green' : s.category === 'Moderate' ? 'badge-yellow' : 'badge-red';
    return `
      <div class="card" style="margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
          <div>
            <b>${s.username}</b> · <code>${s.student_uid}</code> · <span style="font-size: 0.85rem; color: var(--text-muted);">🛡️ ${s.verification}</span>
          </div>
          <span class="badge ${badgeClass}">${s.category}</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.6rem;">
          Overall Mastery: <b>${(s.overall_mastery * 100).toFixed(0)}%</b> | XP: <b>${s.xp}</b> | Attempts: <b>${s.attempts_count}</b> | Weakest: <b>${s.weakest_topic} (${(s.weakest_mastery * 100).toFixed(0)}%)</b>
        </p>
      </div>
    `;
  }).join('');

  document.getElementById('teacherAnalyticsContent').innerHTML = `
    <div class="grid-cols-4" style="margin-bottom: 1.5rem;">
      <div class="card" style="text-align: center;"><div class="kicker">TOTAL OBSERVED</div><h2>${students.length}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">🟢 PERFORMING WELL</div><h2>${well.length}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">🟡 MODERATE</div><h2>${mod.length}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">🔴 INTERVENTION</div><h2>${struggle.length}</h2></div>
    </div>
    <h3>📋 Observed Students Performance Roster</h3>
    <div style="margin-top: 1rem;">${studentsListHtml}</div>
  `;
}

async function claimStudent() {
  const uid = document.getElementById('teacherClaimInput').value.trim();
  if (!uid) return alert('Please enter a Student ID.');

  const res = await fetch('/api/teacher/claim', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ student_uid: uid }),
  });
  const data = await res.json();
  const feedback = document.getElementById('claimFeedback');
  if (data.status === 'success') {
    feedback.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
    document.getElementById('teacherClaimInput').value = '';
    loadTeacherDashboard();
  } else if (data.status === 'info') {
    feedback.innerHTML = `<div class="alert alert-info">${data.message}</div>`;
  } else {
    feedback.innerHTML = `<div class="alert alert-error">${data.message || data.error}</div>`;
  }
}
