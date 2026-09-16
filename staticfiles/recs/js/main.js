// Shared helpers used across pages.

function getCsrfToken() {
  return window.CSRF_TOKEN;
}

function showToast(message, isError) {
  const toast = document.getElementById("toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.toggle("error", !!isError);
  toast.classList.add("show");
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove("show"), 4000);
}

function openModal(id) {
  const overlay = document.getElementById(id);
  if (overlay) overlay.classList.add("open");
}

function closeModal(id) {
  const overlay = document.getElementById(id);
  if (overlay) overlay.classList.remove("open");
}

async function postJSON(url, data) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken(),
    },
    body: JSON.stringify(data),
  });
  let payload = {};
  try {
    payload = await response.json();
  } catch (err) {
    payload = { status: "error", message: "Something went wrong." };
  }
  return { ok: response.ok, payload };
}

// Wire up every modal's close button + click-outside-to-close, site-wide.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-close-modal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      btn.closest(".modal-overlay").classList.remove("open");
    });
  });

  document.querySelectorAll(".modal-overlay").forEach((overlay) => {
    overlay.addEventListener("click", (event) => {
      if (event.target === overlay) overlay.classList.remove("open");
    });
  });

  initHomePage();
  initKarmaCheck();
});

function initKarmaCheck() {
  const karmaCheckBtn = document.getElementById("karma-check-btn");
  const karmaForm = document.getElementById("karma-form");
  const karmaResult = document.getElementById("karma-result");
  const karmaCountValue = document.getElementById("karma-count-value");
  if (!karmaCheckBtn || !karmaForm) return;

  karmaCheckBtn.addEventListener("click", () => {
    karmaForm.reset();
    karmaForm.classList.remove("hidden");
    karmaResult.classList.add("hidden");
    openModal("karma-overlay");
  });

  karmaForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitBtn = karmaForm.querySelector("button[type=submit]");
    submitBtn.disabled = true;

    const { ok, payload } = await postJSON("/api/karma/", {
      email: document.getElementById("karma-email").value.trim(),
    });

    submitBtn.disabled = false;

    if (!ok) {
      showToast(payload.message || "Couldn't look that up.", true);
      return;
    }

    karmaCountValue.textContent = payload.points;
    karmaForm.classList.add("hidden");
    karmaResult.classList.remove("hidden");
  });
}

function showDuplicateModal(fromOverlayId, message) {
  if (fromOverlayId) closeModal(fromOverlayId);
  document.getElementById("duplicate-message").textContent = message;
  openModal("duplicate-overlay");
}

function initHomePage() {
  const kickoffForm = document.getElementById("kickoff-form");
  if (!kickoffForm) return; // not on the home page

  const kickoffInput = document.getElementById("kickoff-input");
  const modalTitleEcho = document.getElementById("modal-title-echo");
  const recForm = document.getElementById("rec-form");
  const recTypeSelect = document.getElementById("rec-type");
  const otherTypeWrap = document.getElementById("other-type-wrap");
  const otherTypeInput = document.getElementById("rec-other-type");
  const inviteFriendBtn = document.getElementById("invite-friend-btn");
  const inviteForm = document.getElementById("invite-form");

  kickoffForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const title = kickoffInput.value.trim();
    if (!title) return;
    modalTitleEcho.textContent = title;
    openModal("modal-overlay");
  });

  recTypeSelect.addEventListener("change", () => {
    const isOther = recTypeSelect.value === "other";
    otherTypeWrap.classList.toggle("hidden", !isOther);
    otherTypeInput.required = isOther;
  });

  recForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const submitBtn = recForm.querySelector("button[type=submit]");
    submitBtn.disabled = true;

    const { ok, payload } = await postJSON("/api/submit/", {
      title: kickoffInput.value.trim(),
      name: document.getElementById("rec-name").value.trim(),
      email: document.getElementById("rec-email").value.trim(),
      rec_type: recTypeSelect.value,
      other_type_label: otherTypeInput.value.trim(),
      description: document.getElementById("rec-description").value.trim(),
    });

    submitBtn.disabled = false;

    if (!ok) {
      showToast(payload.message || "Something went wrong.", true);
      return;
    }

    if (payload.status === "duplicate") {
      showDuplicateModal("modal-overlay", payload.message);
      return;
    }

    closeModal("modal-overlay");
    recForm.reset();
    otherTypeWrap.classList.add("hidden");
    kickoffInput.value = "";
    showToast(payload.message || "Thanks for the recommendation!");
  });

  if (inviteFriendBtn) {
    inviteFriendBtn.addEventListener("click", () => {
      openModal("invite-overlay");
    });
  }

  if (inviteForm) {
    inviteForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const submitBtn = inviteForm.querySelector("button[type=submit]");
      submitBtn.disabled = true;

      const { ok, payload } = await postJSON("/api/invite/", {
        inviter_name: document.getElementById("invite-your-name").value.trim(),
        inviter_email: document.getElementById("invite-your-email").value.trim(),
        friend_name: document.getElementById("invite-friend-name").value.trim(),
        friend_email: document.getElementById("invite-friend-email").value.trim(),
      });

      submitBtn.disabled = false;

      if (!ok) {
        showToast(payload.message || "Couldn't send that invite.", true);
        return;
      }

      if (payload.status === "duplicate") {
        showDuplicateModal("invite-overlay", payload.message);
        return;
      }

      closeModal("invite-overlay");
      inviteForm.reset();
      showToast(payload.message || "Invite sent!");
    });
  }
}
