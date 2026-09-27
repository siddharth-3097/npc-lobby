// Sunday Karma Hoarding quiz, /quiz page only.

document.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("start-quiz-btn");
  if (!startBtn) return; // not on the quiz page

  const landing = document.getElementById("quiz-landing");
  const questionPanel = document.getElementById("quiz-question-panel");
  const progressEl = document.getElementById("quiz-progress");
  const promptEl = document.getElementById("quiz-prompt");
  const optionsEl = document.getElementById("quiz-options");
  const nextBtn = document.getElementById("quiz-next-btn");
  const emojiEl = document.getElementById("quiz-emoji");
  const submitForm = document.getElementById("quiz-submit-form");
  const finalScoreEcho = document.getElementById("quiz-final-score-echo");
  const leaderboardEl = document.getElementById("quiz-leaderboard");

  let questions = [];
  let index = 0;
  let score = 0;
  let answered = false;

  startBtn.addEventListener("click", async () => {
    startBtn.disabled = true;
    try {
      const response = await fetch("/quiz/api/questions/");
      const payload = await response.json();
      questions = payload.questions || [];
    } catch (err) {
      questions = [];
    }
    startBtn.disabled = false;

    if (!questions.length) {
      showToast("Couldn't load the quiz. Try again in a bit.", true);
      return;
    }

    index = 0;
    score = 0;
    landing.classList.add("hidden");
    questionPanel.classList.remove("hidden");
    renderQuestion();
  });

  function renderQuestion() {
    answered = false;
    const total = questions.length;
    const question = questions[index];

    progressEl.textContent = `Question ${index + 1} of ${total}`;

    if (question.style === "emoji" && question.prompt.includes("\n")) {
      const [emojiPart, ...rest] = question.prompt.split("\n");
      emojiEl.textContent = emojiPart;
      emojiEl.classList.remove("hidden");
      promptEl.textContent = rest.join(" ").trim();
      promptEl.classList.add("quiz-prompt-centered");
    } else {
      emojiEl.textContent = "";
      emojiEl.classList.add("hidden");
      promptEl.textContent = question.prompt;
      promptEl.classList.remove("quiz-prompt-centered");
    }

    optionsEl.innerHTML = "";
    nextBtn.classList.add("hidden");
    nextBtn.textContent = index === total - 1 ? "See your score" : "Next question";

    ["a", "b", "c"].forEach((key) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-option";
      btn.textContent = question.options[key];
      btn.dataset.option = key;
      btn.addEventListener("click", () => selectOption(key));
      optionsEl.appendChild(btn);
    });
  }

  function selectOption(selected) {
    if (answered) return;
    answered = true;

    const correct = questions[index].correct_option;

    Array.from(optionsEl.children).forEach((btn) => {
      btn.disabled = true;
      if (btn.dataset.option === correct) {
        btn.classList.add("quiz-option-correct");
      } else if (btn.dataset.option === selected) {
        btn.classList.add("quiz-option-wrong");
      }
    });

    if (selected === correct) score += 1;

    nextBtn.classList.remove("hidden");
  }

  nextBtn.addEventListener("click", () => {
    index += 1;
    if (index < questions.length) {
      renderQuestion();
      return;
    }

    questionPanel.classList.add("hidden");
    finalScoreEcho.textContent = `${score}/${questions.length}`;
    submitForm.reset();
    openModal("quiz-submit-overlay");
  });

  submitForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitBtn = submitForm.querySelector("button[type=submit]");
    submitBtn.disabled = true;

    const { ok, payload } = await postJSON("/quiz/api/submit/", {
      name: document.getElementById("quiz-name").value.trim(),
      email: document.getElementById("quiz-email").value.trim(),
      score: score,
      total: questions.length,
    });

    submitBtn.disabled = false;

    if (!ok) {
      showToast(payload.message || "Couldn't save that score.", true);
      return;
    }

    closeModal("quiz-submit-overlay");
    landing.classList.remove("hidden");

    if (payload.first_time) {
      showToast("Score locked in! +3 karma is yours.");
    } else {
      showToast(`You already played. Your locked-in score is ${payload.score}/${payload.total_questions}.`);
    }

    renderLeaderboard(payload.leaderboard || []);
  });

  function renderLeaderboard(rows) {
    leaderboardEl.innerHTML = "";

    if (!rows.length) {
      const empty = document.createElement("p");
      empty.className = "empty-state";
      empty.textContent = "no one's played yet. be the first to hoard some karma.";
      leaderboardEl.appendChild(empty);
      return;
    }

    rows.forEach((row, i) => {
      const rowEl = document.createElement("div");
      rowEl.className = "quiz-leaderboard-row";
      rowEl.innerHTML = `
        <span class="quiz-leaderboard-rank pixel">${i + 1}</span>
        <span class="quiz-leaderboard-name"></span>
        <span class="quiz-leaderboard-score">${row.score}/${row.total_questions}</span>
      `;
      rowEl.querySelector(".quiz-leaderboard-name").textContent = row.name;
      leaderboardEl.appendChild(rowEl);
    });
  }
});
