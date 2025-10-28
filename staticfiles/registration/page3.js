// --- page3.js (with Hindi translations + save Step 3 to server) ---

function setLabelTextPreserveInputs(label, newText) {
  const textNodes = Array.from(label.childNodes).filter(n => n.nodeType === Node.TEXT_NODE);
  if (textNodes.length) {
    textNodes[0].textContent = newText + " ";
  } else {
    label.insertBefore(document.createTextNode(newText + " "), label.firstChild);
  }
}

// Translation toggle
document.getElementById("translateBtn").addEventListener("click", () => {
  const btn = document.getElementById("translateBtn");
  const isEnglish = btn.textContent.includes("Hindi");

  const translations = {
    "Residence Address:": "निवास पता:",
    "Family Members:": "परिवार के सदस्य:",
    "No. of Family Members:": "परिवार के सदस्यों की संख्या:",
    "Grandfather / Grandmother:": "दादा / दादी:",
    "Father / Mother:": "पिता / माता:",
    "Brother / Sister:": "भाई / बहन:",
    "Sister-in-law / Child:": "भाभी / बच्चा:",
    "Own Business Address (if any):": "स्वयं का व्यापार पता (यदि कोई हो):",
    "Professional Business Name (M/s):": "व्यवसाय का नाम (एम/एस):",
    "Address:": "पता:",
    "Interests & Achievements of Mother/Father:": "माता/पिता की रुचियाँ व उपलब्धियाँ:",
    "Any other information / Questions:": "अन्य जानकारी / प्रश्न:",
    "Will you accept a widow/divorcee?": "क्या आप विधवा/तलाकशुदा को स्वीकार करेंगे?",
    "Will you accept a non-vegetarian?": "क्या आप मांसाहारी व्यक्ति को स्वीकार करेंगे?",
    "Will you accept someone who drinks?": "क्या आप शराब पीने वाले व्यक्ति को स्वीकार करेंगे?",
    "Will you accept someone who smokes?": "क्या आप धूम्रपान करने वाले व्यक्ति को स्वीकार करेंगे?",
    "Yes": "हाँ",
    "No": "नहीं",
    "Any": "कोई बंधन नहीं"
  };

  document.querySelectorAll("label, .label").forEach(el => {
    const original = el.textContent.trim().replace(/\s+/g, " ");
    for (const [en, hi] of Object.entries(translations)) {
      if (original.startsWith(isEnglish ? en : hi)) {
        const newText = isEnglish ? hi : en;
        if (el.querySelector("input")) setLabelTextPreserveInputs(el, newText);
        else el.textContent = newText;
        break;
      }
    }
  });

  const placeholderMap = [
    ["Full home address", "पूरा घर का पता"],
    ["Count", "संख्या"],
    ["Count (if any)", "संख्या (यदि हो)"],
    ["Business address", "व्यापार का पता"],
    ["Business name", "व्यवसाय का नाम"],
    ["Describe briefly", "संक्षेप में वर्णन करें"],
    ["Optional additional details", "अतिरिक्त जानकारी (वैकल्पिक)"],
    ["Enter Nukha", "नुखा दर्ज करें"],
    ["Enter Aakay", "आकाय दर्ज करें"]
  ];

  document.querySelectorAll("input, textarea").forEach(input => {
    placeholderMap.forEach(([en, hi]) => {
      if (isEnglish && input.placeholder === en) input.placeholder = hi;
      else if (!isEnglish && input.placeholder === hi) input.placeholder = en;
    });
  });

  const sindhSelect = document.getElementById("sindh");
  if (sindhSelect) {
    const englishOptions = [
      "Select","Sakkar","Shikharpur","Larkana","Hyderabad","Dadu","Kandhkot",
      "Jekmabad","Deherki","Tharparkar","Royedi","Ghotki","Kashmoro",
      "Jamshoro","Sangar","Kherpur","Neerpur","Tando","Bandi",
      "Neerpurkhas","Umarkot","Other"
    ];
    const hindiOptions = [
      "चयन करें","सक्कर","शिखरपुर","लरकाना","हैदराबाद","दादू","कंधकोट",
      "जेकमाबाद","देहरकी","थरपारकर","रोयेदी","घोटकी","काशमोरो",
      "जमशोरो","सांगर","खेरपुर","नीरपुर","टंडो","बांदी",
      "नीरपुरखास","उमरकोट","अन्य"
    ];
    sindhSelect.querySelectorAll("option").forEach((opt, i) => {
      opt.textContent = isEnglish ? hindiOptions[i] : englishOptions[i];
    });
  }

  btn.textContent = isEnglish ? "Translate to English" : "Translate to Hindi";
});

// CSRF helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length+1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Submit Step 3 form
document.getElementById("familyForm").addEventListener("submit", async e => {
  e.preventDefault();

  const allFields = [
    "address","members","grandfather","grandmother","father","mother","brother","sister", "marrieds", "marriedb",
    "FatherPos","BrotherPos","FatherBusiness","FatherBusinessAd", "BrotherBusiness", "BrotherBusinessAd",
    "interests","otherInfo","sindh","nukha","aakay"
  ];

  const data = {};
  for (let id of allFields) {
    const el = document.getElementById(id);
    data[id] = el ? el.value.trim() : "";
  }

  const radios = ["widowAccept","nonVegAccept","drinksAccept","smokesAccept", "drinks", "widow", "nonVeg", "smokes"];
  for (let name of radios) {
    const selected = document.querySelector(`input[name="${name}"]:checked`);
    if (!selected) return alert(`Please select an option for ${name}`);
    data[name] = selected.value;
  }

  const regId = localStorage.getItem("registration_id");
  if (!regId) return alert("Registration ID not found. Complete Step 1 first.");
  data.registration_id = regId;

  try {
    const res = await fetch("/save_step3/", {
      method: "POST",
      headers: {
        "Content-Type":"application/json",
        "X-CSRFToken":csrftoken
      },
      body: JSON.stringify(data)
    });

    if (!res.ok) throw new Error(res.statusText);

    const result = await res.json();
    if (result.success) {
      alert("Your profile has been created! Please login to continue.");
      window.location.href = "/login/";
    } else {
      alert(result.error || "Server error. Try again later.");
    }
  } catch(err) {
    console.error(err);
    alert("Server error. Try again later.");
  }
});
