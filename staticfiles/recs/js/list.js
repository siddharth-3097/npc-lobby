document.addEventListener("DOMContentLoaded", () => {
  const filterChips = document.querySelectorAll(".filter-chip");
  const rows = document.querySelectorAll(".rec-row");
  const selectBoxes = document.querySelectorAll(".rec-select");
  const sendListBar = document.getElementById("send-list-bar");
  const selectedCount = document.getElementById("selected-count");
  const sendListBtn = document.getElementById("send-list-btn");
  const sendListForm = document.getElementById("send-list-form");
  const thankYouButtons = document.querySelectorAll(".btn-love");
  const thankYouForm = document.getElementById("thankyou-form");
  const thankYouTitleEcho = document.getElementById("thankyou-title-echo");

  let activeThankYouId = null;

  // --- Filters ---
  filterChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      filterChips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      const filter = chip.dataset.filter;
      rows.forEach((row) => {
        const match = filter === "all" || row.dataset.type === filter;
        row.classList.toggle("hidden", !match);
      });
    });
  });

  // --- Selection ---
  function updateSelectionBar() {
    const checked = document.querySelectorAll(".rec-select:checked");
    selectedCount.textContent = `${checked.length} selected`;
    sendListBar.classList.toggle("hidden", checked.length === 0);
  }

  selectBoxes.forEach((box) => box.addEventListener("change", updateSelectionBar));

  sendListBtn.addEventListener("click", () => {
    openModal("send-list-overlay");
  });

  sendListForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const ids = Array.from(document.querySelectorAll(".rec-select:checked")).map(
      (box) => box.dataset.id
    );
    const email = document.getElementById("send-list-email").value.trim();
    const submitBtn = sendListForm.querySelector("button[type=submit]");
    submitBtn.disabled = true;

    const { ok, payload } = await postJSON("/api/send-list/", { email, ids });

    submitBtn.disabled = false;

    if (!ok) {
      showToast(payload.message || "Couldn't send your list.", true);
      return;
    }

    closeModal("send-list-overlay");
    sendListForm.reset();
    showToast(payload.message || "List sent!");
  });

  // --- Thank you ---
  thankYouButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      activeThankYouId = btn.dataset.recId;
      thankYouTitleEcho.textContent = btn.dataset.recTitle;
      openModal("thankyou-overlay");
    });
  });

  thankYouForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!activeThankYouId) return;

    const submitBtn = thankYouForm.querySelector("button[type=submit]");
    submitBtn.disabled = true;

    const { ok, payload } = await postJSON("/api/thank-you/", {
      recommendation_id: activeThankYouId,
      sender_name: document.getElementById("thankyou-name").value.trim(),
      sender_email: document.getElementById("thankyou-email").value.trim(),
      message: document.getElementById("thankyou-message").value.trim(),
    });

    submitBtn.disabled = false;

    if (!ok) {
      showToast(payload.message || "Couldn't send that thank you.", true);
      return;
    }

    if (payload.status === "duplicate") {
      closeModal("thankyou-overlay");
      document.getElementById("duplicate-message").textContent = payload.message;
      openModal("duplicate-overlay");
      activeThankYouId = null;
      return;
    }

    closeModal("thankyou-overlay");
    thankYouForm.reset();
    showToast(payload.message || "Thank you sent!");

    const originalBtn = document.querySelector(
      `.btn-love[data-rec-id="${activeThankYouId}"]`
    );
    if (originalBtn) {
      originalBtn.disabled = true;
      originalBtn.classList.add("loved");
      originalBtn.setAttribute("aria-label", "Thanked");
    }
    activeThankYouId = null;
  });
});
