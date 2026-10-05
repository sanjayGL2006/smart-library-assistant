"use strict";
const input = document.getElementById("q");
const tbody = document.getElementById("results");
function row(s) {
    const tr = document.createElement("tr");
    const link = document.createElement("a");
    link.href = s.url;
    link.textContent = s.student_id;
    const first = document.createElement("td");
    first.appendChild(link);
    tr.appendChild(first);
    for (const text of [s.name, s.email, s.phone]) {
        const td = document.createElement("td");
        td.textContent = text; // textContent avoids XSS
        tr.appendChild(td);
    }
    return tr;
}
async function search(q) {
    if (!tbody)
        return;
    const res = await fetch(`/api/students/?q=${encodeURIComponent(q)}`);
    const data = await res.json();
    tbody.replaceChildren(...data.results.map(row));
}
let timer;
input?.addEventListener("input", () => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => search(input.value), 250);
});
search("");
