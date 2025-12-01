// ========================
// CSRF Token Setup
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
const csrftoken = window.csrftoken;

// ========================
// Image previews & Base64
// ========================
let passportBase64 = '';
let fullBase64 = '';

function handleImageInput(inputId, previewId, callback) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener("change", e => {
        const file = e.target.files[0];
        const img = document.getElementById(previewId);
        if (file) {
            const reader = new FileReader();
            reader.onload = function(event) {
                if (img) img.src = event.target.result;
                if (callback) callback(event.target.result);
            };
            reader.readAsDataURL(file);
        } else {
            if (img) img.src = '';
            if (callback) callback('');
        }
    });
}

handleImageInput("passportPhotoInput", "passportPreview", val => passportBase64 = val);
handleImageInput("fullPhotoInput", "fullPreview", val => fullBase64 = val);

// ========================
// Aadhar formatting
// ========================
const aadharInput = document.getElementById("aadhar");
if (aadharInput) {
    aadharInput.addEventListener("input", e => {
        const raw = e.target.value.replace(/\D/g, "").slice(0, 12);
        e.target.value = raw.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
    });
}

// ========================
// Mobile formatting
// ========================
["yourMob", "fatherMob", "motherMob"].forEach(id => {
    const input = document.getElementById(id);
    if (!input) return;
    input.addEventListener("input", e => {
        const raw = e.target.value.replace(/\D/g, "").slice(0, 10);
        e.target.value = raw.replace(/(\d{5})(?=\d)/g, "$1 ").trim();
    });
});

// ========================
// OTP Verification
// ========================

let otpVerified = false;

document.getElementById("sendOtp").addEventListener("click", async () => {
    const mobInput = document.getElementById("yourMob");
    if (!mobInput) return;
    const mob = mobInput.value.replace(/\s/g, "");

    if (mob.length !== 10) {
        alert("Enter a valid 10-digit mobile number!");
        return;
    }

    try {
        const res = await fetch("/send_otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({ mobile: mob })
        });

        const result = await res.json();

        if (result.success) {
            document.getElementById("otpVerifySection").classList.remove("hidden");
            alert("OTP sent to your mobile number.");
        } else {
            alert(result.error || "Failed to send OTP.");
        }
    } catch (err) {
        alert("Server error. Try again.");
    }
});


document.getElementById("verifyOtp").addEventListener("click", async () => {
    const mob = document.getElementById("yourMob").value.replace(/\s/g, "");
    const otp = document.getElementById("otpInput").value.trim();

    try {
        const res = await fetch("/verify_otp/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify({ mobile: mob, otp })
        });

        const result = await res.json();

        if (result.success) {
            otpVerified = true;
            alert("OTP Verified!");
            document.getElementById("nextBtn").disabled = false;
        } else {
            alert(result.error || "OTP verification failed.");
        }
    } catch (err) {
        alert("Server error. Try again.");
    }
});


// ========================
// Form Submission (Step 1)
// ========================
const nextBtn = document.getElementById("nextBtn");
if (nextBtn) {
    nextBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        if (!otpVerified) return alert("Please verify OTP first!");

        const requiredFields = [
            "yourName", "yourMob", "fatherName", "fatherMob",
            "motherName", "motherMob", "city", "state", "email",
            "password", "confirmPassword", "aadhar", "bloodGroup", "partnerChoice"
        ];

        // Validate fields
        for (let id of requiredFields) {
            const el = document.getElementById(id);
            if (!el || !el.value.trim()) {
                alert(`Please fill out the ${el ? el.placeholder || id : id} field.`);
                if (el) el.focus();
                return;
            }
        }

        const genderChecked = document.querySelector('input[name="gender"]:checked');
        if (!genderChecked) return alert("Please select your gender.");

        if (document.getElementById("password").value !== document.getElementById("confirmPassword").value)
            return alert("Passwords do not match!");

        if (document.getElementById("aadhar").value.replace(/\s/g, "").length !== 12)
            return alert("Enter a valid 12-digit Aadhar number.");

        for (let id of ["yourMob", "fatherMob", "motherMob"]) {
            const val = document.getElementById(id).value.replace(/\s/g, "");
            if (val.length !== 10) return alert(`Please enter a valid 10-digit mobile number for ${id}.`);
        }

        if (!passportBase64) return alert("Please upload your passport photo.");
        if (!fullBase64) return alert("Please upload your full photo.");

        // Prepare JSON data
        const formData = {
            yourName: document.getElementById("yourName").value,
            yourMob: document.getElementById("yourMob").value,
            fatherName: document.getElementById("fatherName").value,
            fatherMob: document.getElementById("fatherMob").value,
            motherName: document.getElementById("motherName").value,
            motherMob: document.getElementById("motherMob").value,
            city: document.getElementById("city").value,
            state: document.getElementById("state").value,
            password: document.getElementById("password").value,
            email: document.getElementById("email").value,
            aadhar: document.getElementById("aadhar").value,
            bloodGroup: document.getElementById("bloodGroup").value,
            partnerChoice: document.getElementById("partnerChoice").value,
            gender: genderChecked.value,
            passportPhoto: passportBase64,
            fullPhoto: fullBase64
        };

        try {
            const res = await fetch("/save_registration/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken
                },
                body: JSON.stringify(formData)
            });

            const result = await res.json();

            if (result.success) {
                // Save registration_id in localStorage for Page 2
                if (result.registration_id) {
                    localStorage.setItem("registration_id", result.registration_id);
                }
                alert("Registration saved! Moving to next page...");
                window.location.href = "/page2/";
            } else {
                alert(result.error || "Server error. Try again later.");
            }
        } catch (err) {
            console.error(err);
            alert("Server error. Try again later.");
        }
    });
}
