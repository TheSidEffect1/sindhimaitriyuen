
// CSRF token from cookie
// ========================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// ========================
// EN ↔ HI Translation
// ========================
function setLabelTextPreserveInputs(label, newText) {
    const textNodes = Array.from(label.childNodes).filter(n => n.nodeType === Node.TEXT_NODE);
    if (textNodes.length) {
        textNodes[0].textContent = newText + " ";
    } else {
        label.insertBefore(document.createTextNode(newText + " "), label.firstChild);
    }
}

const translateBtn = document.getElementById("translateBtn");
if (translateBtn) {
    translateBtn.addEventListener("click", () => {
        const isEnglish = translateBtn.textContent.includes("Hindi");

        const translations = {
            "Name:":"नाम:","Mobile:":"मोबाइल:","Father:":"पिता:","Mother:":"माता:",
            "House:":"मकान:","Sq. ft:":"वर्ग फुट:","No. of 2 wheeler Vehicles:":"2 पहिया वाहनों की संख्या:",
            "No. of 4 wheeler Vehicles:":"4 पहिया वाहनों की संख्या:","Education:":"शिक्षा:","Subject:":"विषय:",
            "Job/Business:":"नौकरी/व्यवसाय","Age:":"आयु:","Birth Date:":"जन्म तिथि:","Birth Time:":"जन्म समय:",
            "Birth Place:":"जन्म स्थान:","Skin Colour:":"त्वचा का रंग:","Height:":"ऊंचाई:","Weight:":"वजन:",
            "Diseases:":"बीमारियाँ:","Personal Income:":"व्यक्तिगत आय:","Joint Income:":"संयुक्त आय:",
            "Company:":"कंपनी:","Position:":"पद:","Profession:":"पेशा:","Professional Address:":"पेशेवर पता:"
        };

        document.querySelectorAll("label").forEach(label => {
            const original = label.textContent.trim();
            for (const [en, hi] of Object.entries(translations)) {
                if (isEnglish && original.startsWith(en)) setLabelTextPreserveInputs(label, hi);
                else if (!isEnglish && original.startsWith(hi)) setLabelTextPreserveInputs(label, en);
            }
        });

        const placeholderMap = [
            ["Enter full name","पूरा नाम लिखें"],["10-digit number","10 अंकों का नंबर"],
            ["Father's name","पिता का नाम"],["Mother's name","माता का नाम"],
            ["Area in sq. ft","क्षेत्र (वर्ग फुट में)"],["Count","संख्या"],
            ["Degree","डिग्री"],["Main subject","मुख्य विषय"],
            ["Your occupation","आपका व्यवसाय"],["In years","वर्षों में"],
            ["City, State","शहर, राज्य"],["Fair/Medium/Dark","गोरा/मध्यम/श्याम"],
            ["In feet","फीट में"],["In kg","किलोग्राम में"],
            ["If any","यदि कोई हो"],["In ₹ per year","₹ प्रति वर्ष"],
            ["Family income ₹","पारिवारिक आय ₹"],["Company name","कंपनी का नाम"],
            ["Your position","आपका पद"],["Profession type","पेशा प्रकार"],
            ["Office address","ऑफिस का पता"]
        ];

        document.querySelectorAll("input, textarea").forEach(input => {
            placeholderMap.forEach(([en, hi]) => {
                if (isEnglish && input.placeholder === en) input.placeholder = hi;
                else if (!isEnglish && input.placeholder === hi) input.placeholder = en;
            });
        });

        // House dropdown
        const houseSelect = document.getElementById("house");
        if (houseSelect) {
            const firstOption = houseSelect.options[0];
            if (firstOption) firstOption.textContent = isEnglish ? "चुनें" : "Select";
            Array.from(houseSelect.options).forEach(opt => {
                if (opt.dataset.en && opt.dataset.hi) opt.textContent = isEnglish ? opt.dataset.hi : opt.dataset.en;
            });
        }

        // Education dropdown
        const eduSelect = document.getElementById("education");
        if (eduSelect) {
            const firstOption = eduSelect.options[0];
            if (firstOption) firstOption.textContent = isEnglish ? "चुनें" : "Select";
            const eduMap = [
                ["10th pass","10वीं पास"],["12th pass","12वीं पास"],["Diploma","डिप्लोमा"],
                ["Graduate","स्नातक"],["Post Graduate","स्नातकोत्तर"],["Specialization","विशेषज्ञता"],
                ["Doctor","डॉक्टर"],["Engineer","इंजीनियर"],["C.A.","सी.ए."],
                ["Computer","कंप्यूटर"],["Any other","अन्य"]
            ];
            Array.from(eduSelect.options).forEach(opt => {
                const pair = eduMap.find(([en, hi]) => isEnglish ? opt.textContent === en : opt.textContent === hi);
                if (pair) opt.textContent = isEnglish ? pair[1] : pair[0];
            });
        }

        translateBtn.textContent = isEnglish ? "Translate to English" : "Translate to Hindi";
    });
}


// ========================
// Submit Step 2
// ========================
const partnerForm = document.getElementById("partnerForm");
if (!partnerForm) {
    console.error("partnerForm not found!");
} else {
    partnerForm.addEventListener("submit", async e => {
        e.preventDefault();
        console.log("Step 2 form submitted"); // Debug

        const allFields = [
            "house","sqft","floors","vehicles2","vehicles4","education","subject","jobType",
            "age","birthDate","birthTime","birthPlace","skinColour","height","weight",
            "diseases","personalIncome","jointIncome","company","position","profession","profAddress"
        ];

        for (let id of allFields) {
            const el = document.getElementById(id);
            if (!el || !el.value.trim()) {
                alert(`Please fill all required fields: ${id}`);
                if (el) el.focus();
                return;
            }
        }

        const regId = localStorage.getItem("registration_id");
        if (!regId) return alert(" Please fill Page 1 first.");

        const data = {};
        allFields.forEach(id => {
            const el = document.getElementById(id);
            data[id] = el ? el.value : "";
        });
        data.registration_id = regId;

        try {
            const res = await fetch("/save_step2/", {
                method: "POST",
                headers: {"Content-Type":"application/json","X-CSRFToken":csrftoken},
                body: JSON.stringify(data)
            });

            if (!res.ok) {
                console.error("Network response was not ok", res.status, res.statusText);
                alert("Server returned an error.");
                return;
            }

            const result = await res.json();
            if (result.success) {
                alert("Step 2 data saved successfully! Moving to Page 3...");
                window.location.href = "/page3/";
            } else {
                alert(result.error || "Server error. Try again later.");
            }
        } catch(err) {
            console.error(err);
            alert("Server error. Try again later.");
        }
    });
}

