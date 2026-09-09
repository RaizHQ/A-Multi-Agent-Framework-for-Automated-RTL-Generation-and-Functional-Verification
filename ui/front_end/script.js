document.addEventListener('DOMContentLoaded', () => {
  // --- 1. DOM Element Selection ---
  const form = document.getElementById("firForm");
  const experience = document.getElementById("experience");
  const levels = document.querySelectorAll(".level");
  
  // Conditional Wrappers & Inputs
  const singleCutoff = document.getElementById("singleCutoff");
  const dualFrequency = document.getElementById("dualFrequency");
  const filterType = document.getElementById("filterType");
  
  const tapMode = document.getElementById("tapMode");
  const tapValueWrap = document.getElementById("tapValueWrap");
  
  const designMethod = document.getElementById("designMethod");
  const kaiserBetaWrap = document.getElementById("kaiserBetaWrap");
  
  const source = document.getElementById("source");
  const adcResolutionWrap = document.getElementById("adcResolutionWrap");
  
  const clockDomains = document.getElementById("clockDomains");
  const firClockWrap = document.getElementById("firClockWrap");

  // --- 2. Experience Level Management ---
  function setMode(mode) {
    experience.value = mode;
    
    // Toggle advanced section visibility
    document.querySelectorAll(".advanced-only").forEach(el => {
      el.style.display = (mode === "advanced" || mode === "expert") ? "block" : "none";
    });
    
    // Toggle expert section visibility
    document.querySelectorAll(".expert-only").forEach(el => {
      el.style.display = (mode === "expert") ? "block" : "none";
    });
    
    // Update active state on navigation buttons
    levels.forEach(el => {
      el.classList.toggle("active", el.dataset.level === mode);
    });
    
    updateProgress();
  }

  // Bind experience level events
  levels.forEach(btn => btn.addEventListener("click", () => setMode(btn.dataset.level)));
  experience.addEventListener("change", (e) => setMode(e.target.value));

  // --- 3. Conditional Field Logic ---
  function conditional() {
    const type = filterType.value;
    const dual = (type === "Band-pass" || type === "Band-stop");
    
    // Filter Frequencies
    dualFrequency.style.display = dual ? "grid" : "none";
    singleCutoff.style.display = dual ? "none" : "flex";
    
    // Taps/Order Input
    const customTaps = tapMode.value !== "auto";
    tapValueWrap.style.display = customTaps ? "flex" : "none";
    
    // Kaiser Beta
    kaiserBetaWrap.style.display = designMethod.value === "Kaiser Window" ? "flex" : "none";
    
    // ADC Resolution
    adcResolutionWrap.style.display = source.value === "ADC" ? "flex" : "none";
    
    // Separate Clocks
    firClockWrap.style.display = clockDomains.value === "Separate clocks" ? "flex" : "none";
  }

  // Bind conditional events
  [filterType, tapMode, designMethod, source, clockDomains].forEach(el => {
    el.addEventListener("change", conditional);
  });

  // --- 4. Dynamic Progress Bar ---
  function updateProgress() {
    const required = [...form.querySelectorAll("input[required], select[required], textarea[required]")]
      .filter(el => el.offsetParent !== null);
      
    const done = required.filter(el => {
      return el.type === "checkbox" ? el.checked : el.value.trim() !== "";
    }).length;
    
    const pct = required.length ? Math.round((done / required.length) * 100) : 0;
    
    document.getElementById("progressBar").style.width = pct + "%";
    document.getElementById("progressText").textContent = pct + "%";
  }

  form.addEventListener("input", updateProgress);
  form.addEventListener("change", updateProgress);

  // --- 5. Form Submission & Backend Request ---
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const data = new FormData(form);
    const obj = {};
    
    for (const [k, v] of data.entries()) {
      if (k === "verify" || k === "output") {
        if (!obj[k]) obj[k] = [];
        obj[k].push(v);
      } else {
        obj[k] = v;
      }
    }
    
    obj.generatedAt = new Date().toISOString();
    
    localStorage.setItem("requirements", JSON.stringify(obj, null, 2));

    try {
      // Updated to target the explicit localhost port to avoid CORS/routing failures
      const response = await fetch('http://localhost:3000/api/save-requirements', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(obj),
      });

      if (response.ok) {
        alert("Design specification saved to server folders!");
      } else {
        alert("Failed to save file on the server.");
      }
    } catch (error) {
      console.error("Error saving file:", error);
      alert("Server error encountered.");
    }
  });

  // --- 6. Initialization ---
  setMode("basic");
  conditional();
  updateProgress();
});