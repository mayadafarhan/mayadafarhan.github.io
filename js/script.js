/* ------------------------------------------------------------------
   CONTACT SETTINGS: fill these two values, save, and push to GitHub.
   Buttons appear automatically once a value is set.
   email:    "name@example.com"
   whatsapp: international format, digits only, e.g. "201001234567"
------------------------------------------------------------------- */
const CONFIG = {
  email: "",
  whatsapp: ""
};

(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const email = CONFIG.email.trim();
  const phone = CONFIG.whatsapp.replace(/\D/g, "");

  if (email) {
    const a = $("btn-email");
    a.href = "mailto:" + email + "?subject=" + encodeURIComponent("Hello Mayada") ;
    a.target = "_self";
    a.hidden = false;
  }
  if (phone) {
    const a = $("btn-wa");
    a.href = "https://wa.me/" + phone + "?text=" + encodeURIComponent("Hi Mayada, I found your digital card and would like to connect.");
    a.hidden = false;
  }
  if (email || phone) {
    $("connect").hidden = false;
    $("btn-vcard").hidden = false;
  }

  // "Save contact" builds a .vcf file in the browser (no server needed).
  $("btn-vcard").addEventListener("click", function () {
    const lines = [
      "BEGIN:VCARD", "VERSION:3.0",
      "N:Farhan;Mayada Mohamed;;;", "FN:Mayada Mohamed Farhan",
      "TITLE:AI & Data Science Engineer | Python Developer"
    ];
    if (email) lines.push("EMAIL;TYPE=INTERNET:" + email);
    if (phone) lines.push("TEL;TYPE=CELL:+" + phone);
    lines.push(
      "URL:https://v0-ai-engineer-portfolio-xi-gules.vercel.app/",
      "URL:https://www.linkedin.com/in/mayada-mohamed-farhan/",
      "END:VCARD"
    );
    const url = URL.createObjectURL(new Blob([lines.join("\r\n")], { type: "text/vcard" }));
    const a = Object.assign(document.createElement("a"), { href: url, download: "Mayada-Mohamed-Farhan.vcf" });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
})();
