// AdaptiveAI Universal Client-Side Engine (GitHub Pages & Vercel Ready)
const CATALOG = {"topics": [{"id": "variables", "name": "Variables", "world": "Python World", "unlock_after": null}, {"id": "conditions", "name": "Conditions", "world": "Python World", "unlock_after": "variables"}, {"id": "loops", "name": "Loops", "world": "Python World", "unlock_after": "conditions"}, {"id": "functions", "name": "Functions", "world": "Python World", "unlock_after": "loops"}, {"id": "oop", "name": "OOP", "world": "Python World", "unlock_after": "functions"}, {"id": "files", "name": "File Handling", "world": "Python World", "unlock_after": "oop"}], "questions": [{"id": "var-b-1", "topic": "variables", "difficulty": "beginner", "prompt": "What does this print?\n\n```python\nx = 5\nprint(type(x))\n```", "choices": ["<class 'int'>", "<class 'str'>", "5", "int()"], "answer": 0, "hints": ["Look at the value assigned to x.", "5 without quotes is a whole number.", "type() reports the Python type, not the value."], "explain": "5 is an integer, so type(x) is <class 'int'>."}, {"id": "var-b-2", "topic": "variables", "difficulty": "beginner", "prompt": "Which assignment creates a string?", "choices": ["n = 10", "n = 10.0", "n = \"10\"", "n = True"], "answer": 2, "hints": ["Strings are text.", "Quotes wrap text in Python.", "\"10\" is text that looks like a number."], "explain": "Quotes make \"10\" a str. 10 is int, 10.0 is float."}, {"id": "var-i-1", "topic": "variables", "difficulty": "intermediate", "prompt": "After these lines, what is y?\n\n```python\nx = 3\ny = x\nx = 8\n```", "choices": ["3", "8", "11", "Error"], "answer": 0, "hints": ["Integers are copied by value here.", "y = x copies the current value of x.", "Changing x later does not rewrite y."], "explain": "y stored 3. Rebinding x to 8 does not change y."}, {"id": "var-i-2", "topic": "variables", "difficulty": "intermediate", "prompt": "What is the result of `bool(0)`?", "choices": ["True", "False", "0", "Error"], "answer": 1, "hints": ["Some values are \"falsy\".", "Empty and zero-like values become False.", "0 is falsy, so bool(0) is False."], "explain": "0, 0.0, \"\", [], and None are falsy."}, {"id": "var-a-1", "topic": "variables", "difficulty": "advanced", "prompt": "What does this print?\n\n```python\na = [1]\nb = a\na.append(2)\nprint(b)\n```", "choices": ["[1]", "[1, 2]", "[2]", "Error"], "answer": 1, "hints": ["Lists are mutable objects.", "b = a copies the reference, not a new list.", "append changes the same list both names point to."], "explain": "a and b refer to one list, so append is visible through b."}, {"id": "cond-b-1", "topic": "conditions", "difficulty": "beginner", "prompt": "Which operator means \"equal to\" in Python?", "choices": ["=", "==", "===", "eq"], "answer": 1, "hints": ["= is assignment.", "Comparisons use a doubled equals.", "Use == to test equality."], "explain": "= assigns. == compares. Python has no ===."}, {"id": "cond-b-2", "topic": "conditions", "difficulty": "beginner", "prompt": "What does this print if n = 4?\n\n```python\nif n % 2 == 0:\n    print(\"even\")\nelse:\n    print(\"odd\")\n```", "choices": ["even", "odd", "4", "nothing"], "answer": 0, "hints": ["% is remainder.", "Even numbers have remainder 0 when divided by 2.", "4 % 2 == 0 is True."], "explain": "4 is even, so the if branch runs."}, {"id": "cond-i-1", "topic": "conditions", "difficulty": "intermediate", "prompt": "What is printed?\n\n```python\nx = 7\nif x > 10:\n    print(\"A\")\nelif x > 5:\n    print(\"B\")\nelse:\n    print(\"C\")\n```", "choices": ["A", "B", "C", "A then B"], "answer": 1, "hints": ["elif is only tried if the if failed.", "7 > 10 is False.", "7 > 5 is True, so \"B\" prints and else is skipped."], "explain": "First condition fails, second succeeds. Only one branch runs."}, {"id": "cond-i-2", "topic": "conditions", "difficulty": "intermediate", "prompt": "Which expression is True?", "choices": ["True and False", "False or False", "not True", "True or False"], "answer": 3, "hints": ["and needs both True.", "or needs at least one True.", "True or False is True."], "explain": "or is True if any operand is True."}, {"id": "cond-a-1", "topic": "conditions", "difficulty": "advanced", "prompt": "What does this print?\n\n```python\nprint(\"yes\" if 0 else \"no\")\n```", "choices": ["yes", "no", "0", "Error"], "answer": 1, "hints": ["This is a ternary (conditional expression).", "The condition is 0.", "0 is falsy, so the else value is chosen."], "explain": "value_if_true if condition else value_if_false. 0 is falsy \u2192 \"no\"."}, {"id": "loop-b-1", "topic": "loops", "difficulty": "beginner", "prompt": "How many times does this print Hello?\n\n```python\nfor i in range(3):\n    print(\"Hello\")\n```", "choices": ["2", "3", "4", "Infinite"], "answer": 1, "hints": ["range(n) goes 0, 1, ..., n-1.", "That is n values.", "range(3) \u2192 0, 1, 2."], "explain": "range(3) yields three integers, so three prints."}, {"id": "loop-b-2", "topic": "loops", "difficulty": "beginner", "prompt": "What is the last number printed?\n\n```python\nfor i in range(1, 4):\n    print(i)\n```", "choices": ["1", "3", "4", "0"], "answer": 1, "hints": ["range(start, stop) excludes stop.", "It runs while i < 4.", "Values are 1, 2, 3."], "explain": "The stop bound is exclusive, so 4 is not printed."}, {"id": "loop-i-1", "topic": "loops", "difficulty": "intermediate", "prompt": "What is s after this loop?\n\n```python\ns = 0\nfor n in [2, 4, 6]:\n    s += n\n```", "choices": ["6", "12", "24", "0"], "answer": 1, "hints": ["+= adds into s.", "Add each list item in order.", "2+4+6 = 12."], "explain": "The loop accumulates the list sum: 12."}, {"id": "loop-i-2", "topic": "loops", "difficulty": "intermediate", "prompt": "Which loop is most likely infinite?", "choices": ["for i in range(10): pass", "while True: break", "i = 0\\nwhile i < 5:\\n    i += 1", "i = 0\\nwhile i < 5:\\n    print(i)"], "answer": 3, "hints": ["An infinite loop never reaches a false condition.", "If i never changes, i < 5 stays True.", "The last option prints i forever."], "explain": "Without i += 1, i stays 0 and the while never ends."}, {"id": "loop-a-1", "topic": "loops", "difficulty": "advanced", "prompt": "What does this print?\n\n```python\nfor i in range(5):\n    if i == 2:\n        continue\n    if i == 4:\n        break\n    print(i, end=\"\")\n```", "choices": ["01234", "013", "0134", "0123"], "answer": 1, "hints": ["continue skips the rest of this iteration.", "break leaves the loop entirely.", "2 is skipped; 4 never prints; output is 013."], "explain": "Prints 0,1; skips 2; prints 3; breaks at 4."}, {"id": "fn-b-1", "topic": "functions", "difficulty": "beginner", "prompt": "How do you define a function named greet?", "choices": ["function greet():", "def greet():", "func greet():", "define greet():"], "answer": 1, "hints": ["Python uses a short keyword.", "It is def, not function.", "def greet(): is the header."], "explain": "Python function definitions start with def."}, {"id": "fn-b-2", "topic": "functions", "difficulty": "beginner", "prompt": "What does this return?\n\n```python\ndef add(a, b):\n    return a + b\nprint(add(2, 3))\n```", "choices": ["23", "5", "None", "Error"], "answer": 1, "hints": ["return sends a value back to the caller.", "+ on ints adds numerically.", "2 + 3 is 5."], "explain": "add returns the integer sum 5."}, {"id": "fn-i-1", "topic": "functions", "difficulty": "intermediate", "prompt": "What is printed?\n\n```python\ndef f(x):\n    x = x + 1\n    return x\nn = 4\nf(n)\nprint(n)\n```", "choices": ["4", "5", "None", "Error"], "answer": 0, "hints": ["The return value is ignored.", "n is an int passed by assignment.", "Rebinding x inside f does not change n."], "explain": "f(n) returns 5 but n stays 4 because the result is unused."}, {"id": "fn-i-2", "topic": "functions", "difficulty": "intermediate", "prompt": "What is the default return value of a function with no return?", "choices": ["0", "False", "None", "Error"], "answer": 2, "hints": ["Every function returns something.", "If you omit return, Python still returns an object.", "That object is None."], "explain": "Missing return is the same as return None."}, {"id": "fn-a-1", "topic": "functions", "difficulty": "advanced", "prompt": "What does this print?\n\n```python\ndef f(xs=[]):\n    xs.append(1)\n    return xs\nprint(f(), f())\n```", "choices": ["[1] [1]", "[1] [1, 1]", "[1, 1] [1, 1]", "Error"], "answer": 1, "hints": ["Default arguments are evaluated once.", "The same list is reused across calls.", "First call [1], second call [1, 1]."], "explain": "Mutable defaults persist. Both calls share one list."}, {"id": "oop-b-1", "topic": "oop", "difficulty": "beginner", "prompt": "Which keyword starts a class definition?", "choices": ["object", "class", "struct", "def"], "answer": 1, "hints": ["Functions use def.", "Types/blueprints use another keyword.", "class Name: is the header."], "explain": "Python classes are defined with class."}, {"id": "oop-b-2", "topic": "oop", "difficulty": "beginner", "prompt": "What is the first parameter of an instance method usually called?", "choices": ["this", "self", "cls", "me"], "answer": 1, "hints": ["It refers to the instance.", "Python convention is not this.", "Use self."], "explain": "Instance methods take self as the first parameter by convention."}, {"id": "oop-i-1", "topic": "oop", "difficulty": "intermediate", "prompt": "What does this print?\n\n```python\nclass P:\n    def __init__(self, n):\n        self.n = n\nprint(P(3).n)\n```", "choices": ["P", "3", "n", "Error"], "answer": 1, "hints": ["__init__ runs when you construct P(3).", "self.n stores the argument.", "P(3).n is 3."], "explain": "The constructor saves n on the instance."}, {"id": "oop-i-2", "topic": "oop", "difficulty": "intermediate", "prompt": "Inheritance in Python is written as:", "choices": ["class Dog extends Animal:", "class Dog(Animal):", "class Dog implements Animal:", "class Dog <- Animal:"], "answer": 1, "hints": ["Python lists the parent in parentheses.", "Not Java's extends.", "class Dog(Animal):"], "explain": "Subclass syntax is class Child(Parent):"}, {"id": "oop-a-1", "topic": "oop", "difficulty": "advanced", "prompt": "What is printed?\n\n```python\nclass A:\n    x = 1\na = A(); b = A()\na.x = 2\nprint(A.x, b.x, a.x)\n```", "choices": ["2 2 2", "1 1 2", "1 2 2", "2 1 2"], "answer": 1, "hints": ["x on the class is shared until an instance overrides it.", "a.x = 2 creates an instance attribute on a only.", "A.x and b.x stay 1; a.x is 2."], "explain": "Assignment on a shadows the class attribute for a only."}, {"id": "file-b-1", "topic": "files", "difficulty": "beginner", "prompt": "Which mode opens a file for reading text?", "choices": ["\"w\"", "\"r\"", "\"a\"", "\"rb\""], "answer": 1, "hints": ["w writes (and truncates).", "a appends.", "r reads."], "explain": "\"r\" is read text. \"rb\" is read bytes."}, {"id": "file-b-2", "topic": "files", "difficulty": "beginner", "prompt": "Why is `with open(path) as f:` recommended?", "choices": ["It makes the file faster", "It closes the file automatically", "It encrypts the file", "It skips errors"], "answer": 1, "hints": ["Files should be closed after use.", "with is a context manager.", "The file closes even if an error happens inside the block."], "explain": "The with statement guarantees close()."}, {"id": "file-i-1", "topic": "files", "difficulty": "intermediate", "prompt": "What does f.read() return for a text file?", "choices": ["A list of lines", "A str", "bytes", "An int"], "answer": 1, "hints": ["Text mode vs binary mode matters.", "read() with no size reads everything.", "In text mode the result is a str."], "explain": "Text-mode read() returns the whole contents as str."}, {"id": "file-i-2", "topic": "files", "difficulty": "intermediate", "prompt": "Which call writes a line with a newline?", "choices": ["f.write(\"hi\")", "f.write(\"hi\\n\")", "f.read(\"hi\\n\")", "print(f, \"hi\")"], "answer": 1, "hints": ["write does not add a newline for you.", "Include \\n in the string.", "f.write(\"hi\\n\")"], "explain": "write() dumps exactly the string you pass."}, {"id": "file-a-1", "topic": "files", "difficulty": "advanced", "prompt": "What happens if you `open(path, \"w\")` on an existing file?", "choices": ["It appends", "It fails", "It truncates (erases) the file", "It opens read-only"], "answer": 2, "hints": ["w means write.", "Write mode starts from an empty file.", "Existing contents are truncated."], "explain": "Mode \"w\" creates or truncates. Use \"a\" to append."}]};

const TOPICS_ORDER = ['variables', 'conditions', 'loops', 'functions', 'oop', 'files'];
const TOPIC_LABELS = {
  variables: 'Variables',
  conditions: 'Conditions',
  loops: 'Loops',
  functions: 'Functions',
  oop: 'OOP',
  files: 'File Handling'
};
const MASTERY_UNLOCK = 0.72;
const MIN_ATTEMPTS_UNLOCK = 3;
const DIFFICULTY_RANK = { beginner: 0, intermediate: 1, advanced: 2 };

// --- Storage Helper ---
const Storage = {
  getUsers: () => JSON.parse(localStorage.getItem('aai_users') || '[]'),
  saveUsers: (u) => localStorage.setItem('aai_users', JSON.stringify(u)),
  getSkills: () => JSON.parse(localStorage.getItem('aai_skills') || '{}'),
  saveSkills: (s) => localStorage.setItem('aai_skills', JSON.stringify(s)),
  getAttempts: () => JSON.parse(localStorage.getItem('aai_attempts') || '[]'),
  saveAttempts: (a) => localStorage.setItem('aai_attempts', JSON.stringify(a)),
  getSession: () => JSON.parse(localStorage.getItem('aai_session') || 'null'),
  saveSession: (u) => localStorage.setItem('aai_session', JSON.stringify(u)),
  clearSession: () => localStorage.removeItem('aai_session'),
};

let currentUser = null;
let currentQuestion = null;
let hintsUsed = 0;
let lastWrongContext = null;
let questionStartTime = Date.now();

document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
});

function showAuthAlert(msg, type = 'error') {
  const box = document.getElementById('authAlertBox');
  if (box) {
    box.innerHTML = `<div class="alert alert-${type}">⚠️ ${msg}</div>`;
    box.style.display = 'block';
  } else {
    alert(msg);
  }
}

function clearAuthAlert() {
  const box = document.getElementById('authAlertBox');
  if (box) {
    box.innerHTML = '';
    box.style.display = 'none';
  }
}

function checkAuth() {
  const session = Storage.getSession();
  if (session) {
    const users = Storage.getUsers();
    currentUser = users.find(u => u.id === session.id) || session;
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

  const teacherNavLi = document.getElementById('nav-teacher-li');
  if (currentUser.role !== 'student') {
    teacherNavLi.style.display = 'block';
  } else {
    teacherNavLi.style.display = 'none';
  }

  const roleTitle = currentUser.role.charAt(0).toUpperCase() + currentUser.role.slice(1);
  const uidChip = currentUser.student_uid ? `<div class="chip">🆔 ${currentUser.student_uid}</div>` : '';
  const level = 1 + Math.floor(currentUser.xp / 400);

  document.getElementById('navUserBadge').innerText = `${currentUser.username} (${roleTitle})`;
  document.getElementById('userHud').innerHTML = `
    <div class="chip">${currentUser.role === 'student' ? '🎓 Student' : currentUser.role === 'teacher' ? '👩‍🏫 Teacher' : '👤 Educator'}</div>
    <div class="chip">👤 ${currentUser.username}</div>
    ${uidChip}
    <div class="chip">🏆 LV ${level}</div>
    <div class="chip">✨ ${currentUser.xp} XP</div>
    <div class="chip">🔥 ${currentUser.streak} streak</div>
  `;

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

  document.querySelectorAll('.nav-item').forEach(link => link.classList.remove('active'));

  if (viewName === 'play') loadPlayQuestion();
  if (viewName === 'skill_map') loadSkillMap();
  if (viewName === 'dashboard') loadDashboard();
  if (viewName === 'leaderboard') loadLeaderboard();
  if (viewName === 'teacher') loadTeacherDashboard();
}

function switchAuthTab(tab) {
  clearAuthAlert();
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  if (tab === 'login') {
    document.getElementById('tabLoginBtn').classList.add('active');
    document.getElementById('tab-login-form').style.display = 'block';
    document.getElementById('tab-join-form').style.display = 'none';
  } else {
    document.getElementById('tabJoinBtn').classList.add('active');
    document.getElementById('tab-login-form').style.display = 'none';
    document.getElementById('tab-join-form').style.display = 'block';
  }
}

function toggleVerifyMethod() {
  const methodEl = document.querySelector('input[name="verifyMethod"]:checked');
  const method = methodEl ? methodEl.value : 'reg_num';
  if (method === 'reg_num') {
    document.getElementById('verifyRegBox').style.display = 'block';
    document.getElementById('verifyCardBox').style.display = 'none';
  } else {
    document.getElementById('verifyRegBox').style.display = 'none';
    document.getElementById('verifyCardBox').style.display = 'block';
  }
}

function generateStudentUid() {
  const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let res = 'STU-';
  for (let i = 0; i < 6; i++) {
    res += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return res;
}

function submitLogin() {
  clearAuthAlert();
  const u = document.getElementById('loginUsername').value.trim();
  const p = document.getElementById('loginPassword').value;

  if (!u || !p) {
    showAuthAlert('Username and password are required.');
    return;
  }

  const users = Storage.getUsers();
  const user = users.find(x => x.username.toLowerCase() === u.toLowerCase() && x.password === p);

  if (user) {
    currentUser = user;
    Storage.saveSession(user);
    renderAuthenticated();
  } else {
    showAuthAlert('Invalid username or wrong password.');
  }
}

function submitRegister() {
  clearAuthAlert();
  const role = document.getElementById('joinRole').value;
  const u = document.getElementById('joinUsername').value.trim();
  const p = document.getElementById('joinPassword').value;
  const methodEl = document.querySelector('input[name="verifyMethod"]:checked');
  const method = methodEl ? methodEl.value : 'reg_num';

  if (!u || !p) {
    showAuthAlert('Username and password are required.');
    return;
  }

  const users = Storage.getUsers();
  if (users.find(x => x.username.toLowerCase() === u.toLowerCase())) {
    showAuthAlert('That username is already taken. Please choose another.');
    return;
  }

  let uniInfo = 'Unverified';
  if (method === 'reg_num') {
    const reg = document.getElementById('joinRegNum').value.trim();
    if (!reg) {
      showAuthAlert('University Registration Number is required.');
      return;
    }
    uniInfo = `REG: ${reg}`;
  } else {
    const fileInput = document.getElementById('joinIdCardFile');
    if (!fileInput.files || !fileInput.files[0]) {
      showAuthAlert('University ID Card upload is required.');
      return;
    }
    uniInfo = `CARD: ${fileInput.files[0].name}`;
  }

  const newId = Date.now();
  const studentUid = (role === 'student') ? generateStudentUid() : null;

  const newUser = {
    id: newId,
    username: u,
    password: p,
    role: role,
    student_uid: studentUid,
    uni_id_card: uniInfo,
    claimed_by_teacher_id: null,
    xp: 0,
    streak: 0,
    diagnostic_done: false,
    diag_idx: 0,
    badges: [],
  };

  users.push(newUser);
  Storage.saveUsers(users);

  // Initialize skills with 0.0 starting mastery
  const allSkills = Storage.getSkills();
  allSkills[newId] = {};
  TOPICS_ORDER.forEach(t => {
    allSkills[newId][t] = { mastery: 0.0, n: 0 };
  });
  Storage.saveSkills(allSkills);

  currentUser = newUser;
  Storage.saveSession(newUser);
  renderAuthenticated();
}

function logout() {
  Storage.clearSession();
  currentUser = null;
  renderUnauthenticated();
}

// --- Adaptive Engine Logic ---
function topicUnlocked(userSkills, topic) {
  const idx = TOPICS_ORDER.indexOf(topic);
  if (idx === 0) return true;
  const prevTopic = TOPICS_ORDER[idx - 1];
  const row = userSkills[prevTopic] || { mastery: 0, n: 0 };
  return row.n >= MIN_ATTEMPTS_UNLOCK && row.mastery >= MASTERY_UNLOCK;
}

function recommendTopic(userSkills) {
  const unlocked = TOPICS_ORDER.filter(t => topicUnlocked(userSkills, t));
  unlocked.sort((a, b) => (userSkills[a]?.mastery || 0) - (userSkills[b]?.mastery || 0));
  return unlocked[0] || 'variables';
}

function recommendDifficulty(mastery) {
  if (mastery < 0.5) return 'beginner';
  if (mastery < 0.75) return 'intermediate';
  return 'advanced';
}

function updateMastery(mastery, correct, hintsCount, difficulty) {
  const weight = 0.22 + 0.06 * (DIFFICULTY_RANK[difficulty] || 1);
  let observed = correct ? 1.0 : 0.0;
  if (hintsCount > 0) {
    observed *= Math.max(0.35, 1.0 - 0.2 * hintsCount);
  }
  return Math.max(0.0, Math.min(1.0, mastery + weight * (observed - mastery)));
}

function loadPlayQuestion() {
  hintsUsed = 0;
  const container = document.getElementById('playQuestionContainer');
  const allSkills = Storage.getSkills();
  const userSkills = allSkills[currentUser.id] || {};

  if (!currentUser.diagnostic_done) {
    const diagIdx = currentUser.diag_idx || 0;
    if (diagIdx >= TOPICS_ORDER.length) {
      currentUser.diagnostic_done = true;
      const users = Storage.getUsers();
      const uIdx = users.findIndex(x => x.id === currentUser.id);
      if (uIdx >= 0) { users[uIdx].diagnostic_done = true; Storage.saveUsers(users); }
      Storage.saveSession(currentUser);

      container.innerHTML = `
        <div class="card" style="text-align: center; padding: 2.5rem;">
          <h2 style="color: var(--primary);">🎉 Diagnostic Assessment Complete!</h2>
          <p style="margin: 1rem 0;">Your live skill profile has been seeded. Jump into Adaptive Mode now!</p>
          <button class="btn btn-primary" onclick="loadPlayQuestion()">Start Adaptive Mode ➔</button>
        </div>
      `;
      return;
    }

    const targetTopic = TOPICS_ORDER[diagIdx];
    const pool = CATALOG.questions.filter(q => q.topic === targetTopic);
    const begPool = pool.filter(q => q.difficulty === 'beginner');
    currentQuestion = begPool[0] || pool[0];
    questionStartTime = Date.now();

    renderQuestionUI(currentQuestion, `Diagnostic Question ${diagIdx + 1} of ${TOPICS_ORDER.length}`);
  } else {
    const topic = recommendTopic(userSkills);
    const m = userSkills[topic]?.mastery || 0;
    const diff = recommendDifficulty(m);
    let pool = CATALOG.questions.filter(q => q.topic === topic && q.difficulty === diff);
    if (pool.length === 0) pool = CATALOG.questions.filter(q => q.topic === topic);
    currentQuestion = pool[Math.floor(Math.random() * pool.length)] || CATALOG.questions[0];
    questionStartTime = Date.now();

    renderQuestionUI(currentQuestion, `Live ${TOPIC_LABELS[topic]} Mastery: ${Math.round(m * 100)}%`);
  }
}

function renderQuestionUI(q, statusBadge) {
  const container = document.getElementById('playQuestionContainer');
  let choicesHtml = q.choices.map((c, i) => `
    <label style="display: block; background: #FFFFFF; border: 1px solid var(--border); border-radius: 12px; padding: 0.85rem 1.25rem; margin-bottom: 0.6rem; cursor: pointer; font-weight: 500;">
      <input type="radio" name="playChoice" value="${i}" style="margin-right: 0.6rem;" />
      ${c}
    </label>
  `).join('');

  container.innerHTML = `
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <span class="kicker">${TOPIC_LABELS[q.topic]} · ${q.difficulty.toUpperCase()}</span>
        <span style="font-family: 'Fira Code', monospace; font-size: 0.85rem; color: var(--text-muted);">${statusBadge}</span>
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

function submitAnswer() {
  const selected = document.querySelector('input[name="playChoice"]:checked');
  if (!selected) return alert('Please select an option first.');

  const chosenIdx = parseInt(selected.value);
  const correct = (chosenIdx === currentQuestion.answer);
  const elapsed = (Date.now() - questionStartTime) / 1000;

  const allSkills = Storage.getSkills();
  const userSkills = allSkills[currentUser.id] || {};
  const oldRow = userSkills[currentQuestion.topic] || { mastery: 0.0, n: 0 };

  const newMastery = updateMastery(oldRow.mastery, correct, hintsUsed, currentQuestion.difficulty);
  userSkills[currentQuestion.topic] = { mastery: newMastery, n: oldRow.n + 1 };
  allSkills[currentUser.id] = userSkills;
  Storage.saveSkills(allSkills);

  const xpGained = correct ? (hintsUsed > 0 ? 50 : 100) : 0;
  currentUser.xp += xpGained;
  currentUser.streak = correct ? (currentUser.streak + 1) : 0;

  if (!currentUser.diagnostic_done) {
    currentUser.diag_idx = (currentUser.diag_idx || 0) + 1;
  }

  // Update user storage
  const users = Storage.getUsers();
  const uIdx = users.findIndex(x => x.id === currentUser.id);
  if (uIdx >= 0) {
    users[uIdx] = currentUser;
    Storage.saveUsers(users);
  }
  Storage.saveSession(currentUser);

  // Log attempt
  const attempts = Storage.getAttempts();
  attempts.push({
    userId: currentUser.id,
    topic: currentQuestion.topic,
    questionId: currentQuestion.id,
    difficulty: currentQuestion.difficulty,
    choiceIndex: chosenIdx,
    correct: correct,
    responseTime: elapsed,
    hintsUsed: hintsUsed,
    timestamp: new Date().toISOString(),
  });
  Storage.saveAttempts(attempts);

  renderAuthenticated();

  const container = document.getElementById('playQuestionContainer');
  if (correct) {
    container.innerHTML = `
      <div class="card" style="border-left: 5px solid var(--primary);">
        <div class="alert alert-success">✅ <b>Correct!</b> +${xpGained} XP · Live Mastery now ${Math.round(newMastery * 100)}% · Streak ${currentUser.streak}</div>
        <p style="margin-bottom: 1rem;">${currentQuestion.explain}</p>
        <button class="btn btn-primary" onclick="loadPlayQuestion()">Next Challenge ➔</button>
      </div>
    `;
  } else {
    lastWrongContext = {
      topic: TOPIC_LABELS[currentQuestion.topic],
      picked: currentQuestion.choices[chosenIdx],
      target: currentQuestion.choices[currentQuestion.answer],
      explain: currentQuestion.explain,
    };

    container.innerHTML = `
      <div class="card" style="border-left: 5px solid #DC2626;">
        <div class="alert alert-error">❌ <b>Not quite.</b> +0 XP.</div>
        <p><b>Your Pick:</b> <code>${lastWrongContext.picked}</code> | <b>Target:</b> <code>${lastWrongContext.target}</code></p>
        <p style="margin: 0.75rem 0;">${lastWrongContext.explain}</p>
        <button class="btn btn-primary" onclick="loadPlayQuestion()" style="margin-bottom: 1.5rem;">Continue to Next Question ➔</button>

        <div class="card" style="background: #FFFFFF; border: 1px solid var(--border);">
          <h3 style="color: var(--primary);">🤖 AI Doubt Clarifier Chatbot</h3>
          <div class="chat-box" id="doubtChatLogs">
            <div class="chat-msg assistant">
              <b>🤖 AI Tutor:</b> You selected <code>${lastWrongContext.picked}</code>, but the correct answer is <code>${lastWrongContext.target}</code>.<br/>
              <b>Concept Breakdown:</b> ${lastWrongContext.explain}<br/><br/>
              <i>Ask me any doubt or follow-up question below!</i>
            </div>
          </div>
          <div style="display: flex; gap: 0.75rem;">
            <input type="text" id="doubtInput" placeholder="Ask AI Tutor why this option was false..." style="flex-grow: 1;" onkeypress="if(event.key==='Enter') sendDoubtMessage()" />
            <button class="btn btn-primary" onclick="sendDoubtMessage()">Ask AI</button>
          </div>
        </div>
      </div>
    `;
  }
}

function sendDoubtMessage() {
  const input = document.getElementById('doubtInput');
  const query = input.value.trim();
  if (!query || !lastWrongContext) return;

  const chatLogs = document.getElementById('doubtChatLogs');
  chatLogs.innerHTML += `<div class="chat-msg user"><b>You:</b> ${query}</div>`;
  input.value = '';
  chatLogs.scrollTop = chatLogs.scrollHeight;

  const qLower = query.toLowerCase();
  let reply = '';
  if (qLower.includes('why') || qLower.includes('explain') || qLower.includes('how')) {
    reply = `In Python **${lastWrongContext.topic}**, choosing \`${lastWrongContext.picked}\` is incorrect because: ${lastWrongContext.explain}. The target \`${lastWrongContext.target}\` follows Python syntax standards.`;
  } else if (qLower.includes('example') || qLower.includes('code')) {
    reply = `Here is a clear snippet for **${lastWrongContext.topic}**:\n\n\`\`\`python\n# Targeted Concept: ${lastWrongContext.target}\n# Rule: ${lastWrongContext.explain}\n\`\`\`\nPractice similar code to master it!`;
  } else {
    reply = `Great question on **${lastWrongContext.topic}**! Remember that \`${lastWrongContext.target}\` is standard here. ${lastWrongContext.explain} Keep going!`;
  }

  chatLogs.innerHTML += `<div class="chat-msg assistant"><b>🤖 AI Tutor:</b> ${reply.replace(/\n/g, '<br/>')}</div>`;
  chatLogs.scrollTop = chatLogs.scrollHeight;
}

function loadSkillMap() {
  const allSkills = Storage.getSkills();
  const userSkills = allSkills[currentUser.id] || {};
  let html = '';

  TOPICS_ORDER.forEach(t => {
    const unlocked = topicUnlocked(userSkills, t);
    const row = userSkills[t] || { mastery: 0, n: 0 };
    const status = unlocked ? 'UNLOCKED' : 'LOCKED';
    const badgeClass = unlocked ? 'badge-green' : 'badge-red';

    html += `
      <div class="card" style="border-left: 5px solid ${unlocked ? 'var(--primary)' : '#94A3B8'};">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h3>${TOPIC_LABELS[t]}</h3>
          <span class="badge ${badgeClass}">${status}</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          Mastery: <b>${Math.round(row.mastery * 100)}%</b> · ${row.n} attempts
          ${unlocked ? ` · unlock next at ${Math.round(MASTERY_UNLOCK * 100)}% mastery & ${MIN_ATTEMPTS_UNLOCK} attempts` : ''}
        </p>
        <div class="progress-container">
          <div class="progress-bar" style="width: ${Math.min(100, Math.round(row.mastery * 100))}%;"></div>
        </div>
      </div>
    `;
  });

  document.getElementById('skillMapNodes').innerHTML = html;
}

function loadDashboard() {
  const allSkills = Storage.getSkills();
  const userSkills = allSkills[currentUser.id] || {};
  const allAttempts = Storage.getAttempts().filter(a => a.userId === currentUser.id);

  let totalMastery = 0;
  let weakestTopic = 'variables';
  let minM = 999;

  TOPICS_ORDER.forEach(t => {
    const m = userSkills[t]?.mastery || 0;
    totalMastery += m;
    if (m < minM) { minM = m; weakestTopic = t; }
  });

  const avgMastery = totalMastery / TOPICS_ORDER.length;
  const level = 1 + Math.floor(currentUser.xp / 400);

  let skillBars = '';
  TOPICS_ORDER.forEach(t => {
    const m = userSkills[t]?.mastery || 0;
    skillBars += `
      <div style="margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; font-weight: 600; font-size: 0.9rem;">
          <span>${TOPIC_LABELS[t]}</span>
          <span>${Math.round(m * 100)}%</span>
        </div>
        <div class="progress-container">
          <div class="progress-bar" style="width: ${Math.min(100, Math.round(m * 100))}%;"></div>
        </div>
      </div>
    `;
  });

  document.getElementById('studentDashboardContent').innerHTML = `
    <div class="grid-cols-4" style="margin-bottom: 1.5rem;">
      <div class="card" style="text-align: center;"><div class="kicker">LEVEL</div><h2>${level}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">XP</div><h2>${currentUser.xp}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">STREAK</div><h2>🔥 ${currentUser.streak}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">OVERALL SKILL</div><h2>${Math.round(avgMastery * 100)}%</h2></div>
    </div>

    <div class="card">
      <h3>🎯 What should I learn next?</h3>
      <div class="alert alert-info"><b>Focus on ${TOPIC_LABELS[weakestTopic]}</b> — Current mastery is ${Math.round(minM * 100)}%. Practice challenges to unlock advanced topics!</div>
      <p><b>Today's Mission:</b> Complete 5 challenges in <b>${TOPIC_LABELS[weakestTopic]}</b>.</p>
    </div>

    <div class="card">
      <h3>📈 Skill Mastery Distribution</h3>
      ${skillBars}
    </div>
  `;
}

function loadLeaderboard() {
  const users = Storage.getUsers();
  users.sort((a, b) => b.xp - a.xp);

  let html = '';
  users.forEach((p, idx) => {
    const rank = idx + 1;
    const medal = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : `${rank}.`;
    const youBadge = (p.id === currentUser.id) ? ' <span class="badge badge-green">YOU</span>' : '';
    const lvl = 1 + Math.floor((p.xp || 0) / 400);

    html += `
      <div class="card" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <div>
          <span style="font-size: 1.25rem; margin-right: 0.75rem;">${medal}</span>
          <b>${p.username}</b>${youBadge} · <span style="color: var(--text-muted);">LV ${lvl} (${p.role})</span>
        </div>
        <div>
          <b>${p.xp || 0} XP</b> · 🔥 ${p.streak || 0} streak
        </div>
      </div>
    `;
  });

  document.getElementById('leaderboardList').innerHTML = html || '<div class="alert alert-info">No players registered yet.</div>';
}

function loadTeacherDashboard() {
  const users = Storage.getUsers();
  const allSkills = Storage.getSkills();
  const allAttempts = Storage.getAttempts();

  const claimed = users.filter(u => u.claimed_by_teacher_id === currentUser.id && u.role === 'student');

  if (claimed.length === 0) {
    document.getElementById('teacherAnalyticsContent').innerHTML = `
      <div class="alert alert-info">
        💡 <b>No students currently under observation.</b><br/>
        Ask your students for their unique <b>Student ID (<code>STU-XXXXXX</code>)</b> and enter it above to start observing their learning path.
      </div>
    `;
    return;
  }

  const studentAnalyses = claimed.map(s => {
    const sSkills = allSkills[s.id] || {};
    const sAttempts = allAttempts.filter(a => a.userId === s.id);
    let totM = 0;
    let weakest = 'variables';
    let minM = 999;

    TOPICS_ORDER.forEach(t => {
      const m = sSkills[t]?.mastery || 0;
      totM += m;
      if (m < minM) { minM = m; weakest = t; }
    });

    const avgM = totM / TOPICS_ORDER.length;
    let cat = 'Needs Intervention';
    if (avgM >= 0.65) cat = 'Performing Well';
    else if (avgM >= 0.40) cat = 'Moderate';

    let verifyStr = s.uni_id_card || 'Unverified';
    if (verifyStr.startsWith('REG:')) verifyStr = `Reg No: ${verifyStr.substring(5)}`;
    else if (verifyStr.startsWith('CARD:')) verifyStr = `ID Card Uploaded (${verifyStr.substring(6)})`;

    return {
      id: s.id,
      username: s.username,
      student_uid: s.student_uid,
      verification: verifyStr,
      overall_mastery: avgM,
      category: cat,
      weakest_topic: TOPIC_LABELS[weakest],
      weakest_mastery: minM,
      attempts_count: sAttempts.length,
      xp: s.xp || 0,
      streak: s.streak || 0,
    };
  });

  const well = studentAnalyses.filter(s => s.category === 'Performing Well');
  const mod = studentAnalyses.filter(s => s.category === 'Moderate');
  const struggle = studentAnalyses.filter(s => s.category === 'Needs Intervention');

  let listHtml = studentAnalyses.map(s => {
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
          Overall Mastery: <b>${Math.round(s.overall_mastery * 100)}%</b> | XP: <b>${s.xp}</b> | Attempts: <b>${s.attempts_count}</b> | Weakest: <b>${s.weakest_topic} (${Math.round(s.weakest_mastery * 100)}%)</b>
        </p>
      </div>
    `;
  }).join('');

  document.getElementById('teacherAnalyticsContent').innerHTML = `
    <div class="grid-cols-4" style="margin-bottom: 1.5rem;">
      <div class="card" style="text-align: center;"><div class="kicker">TOTAL OBSERVED</div><h2>${claimed.length}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">🟢 PERFORMING WELL</div><h2>${well.length}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">🟡 MODERATE</div><h2>${mod.length}</h2></div>
      <div class="card" style="text-align: center;"><div class="kicker">🔴 INTERVENTION</div><h2>${struggle.length}</h2></div>
    </div>
    <h3>📋 Observed Students Performance Roster</h3>
    <div style="margin-top: 1rem;">${listHtml}</div>
  `;
}

function claimStudent() {
  const uid = document.getElementById('teacherClaimInput').value.trim();
  const feedback = document.getElementById('claimFeedback');
  if (!uid) return alert('Please enter a Student ID.');

  const users = Storage.getUsers();
  const student = users.find(u => (u.student_uid || '').toUpperCase() === uid.toUpperCase());

  if (!student) {
    feedback.innerHTML = `<div class="alert alert-error">Student ID not found. Please verify the unique ID.</div>`;
    return;
  }

  if (student.role !== 'student') {
    feedback.innerHTML = `<div class="alert alert-error">The provided ID does not belong to a student account.</div>`;
    return;
  }

  if (student.claimed_by_teacher_id && student.claimed_by_teacher_id !== currentUser.id) {
    feedback.innerHTML = `<div class="alert alert-error">This student is already in observation with someone else.</div>`;
    return;
  }

  if (student.claimed_by_teacher_id === currentUser.id) {
    feedback.innerHTML = `<div class="alert alert-info">Student ${student.username} (${student.student_uid}) is already in your observation list.</div>`;
    return;
  }

  student.claimed_by_teacher_id = currentUser.id;
  Storage.saveUsers(users);

  feedback.innerHTML = `<div class="alert alert-success">Student ${student.username} (${student.student_uid}) added to your observation list!</div>`;
  document.getElementById('teacherClaimInput').value = '';
  loadTeacherDashboard();
}

function togglePasswordVisibility(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    btn.innerHTML = '🙈';
    btn.setAttribute('title', 'Hide password');
  } else {
    input.type = 'password';
    btn.innerHTML = '👁️';
    btn.setAttribute('title', 'Show password');
  }
}
