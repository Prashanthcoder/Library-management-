/**
 * script.js
 * ---------
 * Handles all API communication and DOM updates for the Library dashboard.
 * Pattern: each section has a load() function that fetches data and renders it.
 */

const API = "";  // Same origin — FastAPI serves both API and frontend

// ─────────────────────────────────────────────
// TOAST NOTIFICATIONS
// ─────────────────────────────────────────────

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${type === "success" ? "✓" : "✕"}</span> ${message}`;
  container.appendChild(toast);
  // Auto-remove after 3.5 seconds
  setTimeout(() => toast.remove(), 3500);
}

// ─────────────────────────────────────────────
// GENERIC API HELPER
// ─────────────────────────────────────────────

async function apiFetch(url, options = {}) {
  try {
    const res = await fetch(API + url, {
      headers: { "Content-Type": "application/json" },
      ...options
    });
    if (res.status === 204) return null;  // No content (DELETE)
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "An error occurred");
    return data;
  } catch (err) {
    showToast(err.message, "error");
    throw err;  // Re-throw so callers can react
  }
}

// ─────────────────────────────────────────────
// BOOKS
// ─────────────────────────────────────────────

async function loadBooks() {
  const books = await apiFetch("/books/");
  const tbody = document.getElementById("books-tbody");
  tbody.innerHTML = "";

  if (!books || books.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="5">No books in catalog yet.</td></tr>`;
    return;
  }

  books.forEach(book => {
    const qtyClass = book.quantity === 0 ? "qty-low" : "qty-ok";
    tbody.innerHTML += `
      <tr>
        <td>${book.id}</td>
        <td>${escHtml(book.title)}</td>
        <td>${escHtml(book.author)}</td>
        <td><span class="qty ${qtyClass}">${book.quantity}</span></td>
        <td>
          <button class="btn btn-danger btn-sm" onclick="deleteBook(${book.id})">🗑 Delete</button>
        </td>
      </tr>`;
  });

  // Also refresh the book select dropdowns
  populateBookSelect(books);
}

async function addBook(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    title:    form.title.value.trim(),
    author:   form.author.value.trim(),
    quantity: parseInt(form.quantity.value)
  };
  await apiFetch("/books/", { method: "POST", body: JSON.stringify(payload) });
  showToast(`"${payload.title}" added successfully!`);
  form.reset();
  loadBooks();
}

async function deleteBook(id) {
  if (!confirm("Delete this book from the catalog?")) return;
  await apiFetch(`/books/${id}`, { method: "DELETE" });
  showToast("Book deleted.");
  loadBooks();
}

function populateBookSelect(books) {
  const selects = document.querySelectorAll(".book-select");
  selects.forEach(sel => {
    const current = sel.value;
    sel.innerHTML = `<option value="">— Select a book —</option>`;
    books.forEach(b => {
      sel.innerHTML += `<option value="${b.id}">${escHtml(b.title)} (qty: ${b.quantity})</option>`;
    });
    sel.value = current;
  });
}

// ─────────────────────────────────────────────
// MEMBERS
// ─────────────────────────────────────────────

async function loadMembers() {
  const members = await apiFetch("/members/");
  const tbody = document.getElementById("members-tbody");
  tbody.innerHTML = "";

  if (!members || members.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="2">No members registered yet.</td></tr>`;
    return;
  }

  members.forEach(m => {
    tbody.innerHTML += `
      <tr>
        <td>${m.id}</td>
        <td>${escHtml(m.name)}</td>
      </tr>`;
  });

  populateMemberSelect(members);
}

async function registerMember(e) {
  e.preventDefault();
  const form = e.target;
  const payload = { name: form.memberName.value.trim() };
  await apiFetch("/members/", { method: "POST", body: JSON.stringify(payload) });
  showToast(`Member "${payload.name}" registered!`);
  form.reset();
  loadMembers();
}

function populateMemberSelect(members) {
  const selects = document.querySelectorAll(".member-select");
  selects.forEach(sel => {
    const current = sel.value;
    sel.innerHTML = `<option value="">— Select a member —</option>`;
    members.forEach(m => {
      sel.innerHTML += `<option value="${m.id}">${escHtml(m.name)}</option>`;
    });
    sel.value = current;
  });
}

// ─────────────────────────────────────────────
// TRANSACTIONS
// ─────────────────────────────────────────────

async function loadTransactions() {
  const txns = await apiFetch("/transactions/");
  const tbody = document.getElementById("txns-tbody");
  tbody.innerHTML = "";

  if (!txns || txns.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="5">No books are currently issued.</td></tr>`;
    return;
  }

  txns.forEach(t => {
    tbody.innerHTML += `
      <tr>
        <td>${t.id}</td>
        <td>${escHtml(t.book_title || t.book_id)}</td>
        <td>${escHtml(t.member_name || t.member_id)}</td>
        <td>${t.issue_date}</td>
        <td>
          <button class="btn btn-success btn-sm" onclick="returnBook(${t.id})">↩ Return</button>
        </td>
      </tr>`;
  });
}

async function issueBook(e) {
  e.preventDefault();
  const form = e.target;
  const payload = {
    book_id:   parseInt(form.issueBook.value),
    member_id: parseInt(form.issueMember.value)
  };
  if (!payload.book_id || !payload.member_id) {
    showToast("Please select both a book and a member.", "error");
    return;
  }
  const res = await apiFetch("/transactions/issue", { method: "POST", body: JSON.stringify(payload) });
  showToast(`"${res.book_title}" issued to ${res.member_name}!`);
  form.reset();
  loadBooks();        // Quantity changed
  loadTransactions();
}

async function returnBook(transactionId) {
  const res = await apiFetch(`/transactions/return/${transactionId}`, { method: "PUT" });
  showToast(`"${res.book_title}" returned by ${res.member_name}.`);
  loadBooks();        // Quantity restored
  loadTransactions();
}

async function returnBySearch(e) {
  e.preventDefault();
  const id = parseInt(document.getElementById("returnTxnId").value);
  if (!id) { showToast("Please enter a transaction ID.", "error"); return; }
  const res = await apiFetch(`/transactions/return/${id}`, { method: "PUT" });
  showToast(`"${res.book_title}" returned!`);
  e.target.reset();
  loadBooks();
  loadTransactions();
}

// ─────────────────────────────────────────────
// UTILITIES
// ─────────────────────────────────────────────

/** Escape HTML to prevent XSS from user-entered data */
function escHtml(str) {
  const d = document.createElement("div");
  d.textContent = String(str);
  return d.innerHTML;
}

// ─────────────────────────────────────────────
// INIT — wire up forms and load data
// ─────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("add-book-form").addEventListener("submit", addBook);
  document.getElementById("register-member-form").addEventListener("submit", registerMember);
  document.getElementById("issue-book-form").addEventListener("submit", issueBook);
  document.getElementById("return-book-form").addEventListener("submit", returnBySearch);

  // Load all data on page ready
  loadBooks();
  loadMembers();
  loadTransactions();
});