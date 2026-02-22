/**
 * static/script.js
 * ----------------
 * DASHBOARD JAVASCRIPT
 *
 * PASTE LOCATION: library_system/static/script.js  (replace the whole file)
 *
 * Auth changes from original:
 *   - getToken() reads JWT from localStorage
 *   - apiFetch() adds "Authorization: Bearer <token>" header automatically
 *   - If any API call returns 401, user is sent to /login
 *   - logout() clears the token and redirects to /login
 *   - On load, fetches /auth/me to get the logged-in user's name for the header
 */

// ─────────────────────────────────────────────
// TOKEN HELPERS
// ─────────────────────────────────────────────

function getToken() {
  return localStorage.getItem("lms_token");
}

function logout() {
  localStorage.removeItem("lms_token");
  window.location.href = "/login";
}

// Guard: redirect to login if not authenticated
if (!getToken()) {
  window.location.href = "/login";
}

// ─────────────────────────────────────────────
// TOAST NOTIFICATIONS
// ─────────────────────────────────────────────

function showToast(message, type = "success") {
  const container = document.getElementById("toast-container");
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span>${type === "success" ? "✓" : "✕"}</span> ${message}`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3500);
}

// ─────────────────────────────────────────────
// GENERIC API HELPER (with auth header)
// ─────────────────────────────────────────────

async function apiFetch(url, options = {}) {
  const token = getToken();

  try {
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        // Attach the JWT on every request
        "Authorization": `Bearer ${token}`
      },
      ...options
    });

    // Token expired or invalid → force re-login
    if (res.status === 401) {
      localStorage.removeItem("lms_token");
      window.location.href = "/login";
      return;
    }

    if (res.status === 204) return null;   // DELETE returns no body

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "An error occurred");
    return data;

  } catch (err) {
    showToast(err.message, "error");
    throw err;
  }
}

// ─────────────────────────────────────────────
// LOAD CURRENT USER INTO HEADER
// ─────────────────────────────────────────────

async function loadCurrentUser() {
  try {
    const user = await apiFetch("/auth/me");
    const el = document.getElementById("user-display");
    if (el && user) {
      el.textContent = `👤 ${user.username}`;
    }
  } catch (_) {
    // If /me fails the 401 handler above will redirect
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
  showToast(`"${payload.title}" added!`);
  form.reset();
  loadBooks();
}

async function deleteBook(id) {
  if (!confirm("Delete this book from the catalog?")) return;
  try {
    await apiFetch(`/books/${id}`, { method: "DELETE" });
    showToast("Book deleted.");
    loadBooks();
  } catch (_) {
    // apiFetch already showed the error toast with the server's message
  }
}

function populateBookSelect(books) {
  document.querySelectorAll(".book-select").forEach(sel => {
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
    tbody.innerHTML += `<tr><td>${m.id}</td><td>${escHtml(m.name)}</td></tr>`;
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
  document.querySelectorAll(".member-select").forEach(sel => {
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
    tbody.innerHTML = `<tr class="empty-row"><td colspan="5">No books currently issued.</td></tr>`;
    return;
  }

  txns.forEach(t => {
    tbody.innerHTML += `
      <tr>
        <td>${t.id}</td>
        <td>${escHtml(t.book_title || t.book_id)}</td>
        <td>${escHtml(t.member_name || t.member_id)}</td>
        <td>${t.issue_date}</td>
        <td><button class="btn btn-success btn-sm" onclick="returnBook(${t.id})">↩ Return</button></td>
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
  loadBooks();
  loadTransactions();
}

async function returnBook(transactionId) {
  const res = await apiFetch(`/transactions/return/${transactionId}`, { method: "PUT" });
  showToast(`"${res.book_title}" returned by ${res.member_name}.`);
  loadBooks();
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
// UTILS
// ─────────────────────────────────────────────

function escHtml(str) {
  const d = document.createElement("div");
  d.textContent = String(str);
  return d.innerHTML;
}

// ─────────────────────────────────────────────
// INIT
// ─────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("add-book-form").addEventListener("submit", addBook);
  document.getElementById("register-member-form").addEventListener("submit", registerMember);
  document.getElementById("issue-book-form").addEventListener("submit", issueBook);
  document.getElementById("return-book-form").addEventListener("submit", returnBySearch);
  document.getElementById("logout-btn").addEventListener("click", logout);

  loadCurrentUser();
  loadBooks();
  loadMembers();
  loadTransactions();
});