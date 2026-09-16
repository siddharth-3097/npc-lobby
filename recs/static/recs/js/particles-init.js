document.addEventListener("DOMContentLoaded", () => {
  if (typeof particlesJS === "undefined") return;

  particlesJS("particles-js", {
    particles: {
      number: { value: 45, density: { enable: true, value_area: 900 } },
      color: { value: ["#7c3aed", "#22d3ee", "#4ade80", "#facc15", "#ff2ec4"] },
      shape: { type: "edge" },
      opacity: { value: 0.35, random: true, anim: { enable: false } },
      size: { value: 3, random: true },
      line_linked: {
        enable: true,
        distance: 130,
        color: "#b8b6ae",
        opacity: 0.25,
        width: 1,
      },
      move: {
        enable: true,
        speed: 1,
        direction: "none",
        random: true,
        straight: false,
        out_mode: "out",
      },
    },
    interactivity: {
      detect_on: "window",
      events: {
        onhover: { enable: true, mode: "grab" },
        onclick: { enable: false },
        resize: true,
      },
      modes: {
        grab: { distance: 140, line_linked: { opacity: 0.45 } },
      },
    },
    retina_detect: true,
  });
});
