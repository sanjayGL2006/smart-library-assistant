interface StudentDTO {
  id: number;
  student_id: string;
  name: string;
  email: string;
  phone: string;
  url: string;
}

const input = document.getElementById("q") as HTMLInputElement | null;
const tbody = document.getElementById("results") as HTMLTableSectionElement | null;

function row(s: StudentDTO): HTMLTableRowElement {
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

async function search(q: string): Promise<void> {
  if (!tbody) return;
  const res = await fetch(`/api/students/?q=${encodeURIComponent(q)}`);
  const data: { results: StudentDTO[] } = await res.json();
  tbody.replaceChildren(...data.results.map(row));
}

let timer: number | undefined;
input?.addEventListener("input", () => {
  window.clearTimeout(timer);
  timer = window.setTimeout(() => search(input.value), 250);
});
search("");
