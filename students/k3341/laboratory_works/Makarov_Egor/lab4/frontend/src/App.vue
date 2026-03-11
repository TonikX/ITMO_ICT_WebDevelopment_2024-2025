<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;600;700&family=Onest:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #0d0f14;
  --surface: #14171f;
  --surface2: #1c2030;
  --border: #252a38;
  --accent: #5b6ef5;
  --accent-glow: rgba(91,110,245,0.25);
  --text: #e8eaf0;
  --text-muted: #6b7280;
  --error: #f87171;
  --success: #34d399;
  --radius: 14px;
}

html, body {
  min-height: 100vh;
  background: var(--bg);
  color: var(--text);
  font-family: 'Onest', sans-serif;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background:
    radial-gradient(ellipse 60% 50% at 50% -10%, rgba(91,110,245,0.18), transparent),
    var(--bg);
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 40px 36px;
  box-shadow: 0 24px 60px rgba(0,0,0,0.5);
}

.auth-header { text-align: center; margin-bottom: 32px; }

.logo-mark {
  width: 48px; height: 48px;
  border-radius: 12px;
  background: var(--accent);
  box-shadow: 0 0 24px var(--accent-glow);
  color: #fff;
  font-family: 'Unbounded', sans-serif;
  font-size: 20px; font-weight: 700;
  display: inline-flex; align-items: center; justify-content: center;
  margin-bottom: 16px;
}

.auth-header h1 {
  font-family: 'Unbounded', sans-serif;
  font-size: 22px; font-weight: 600; margin-bottom: 6px;
}

.subtitle { color: var(--text-muted); font-size: 14px; }

.auth-form, .edit-form { display: flex; flex-direction: column; gap: 18px; }

.field { display: flex; flex-direction: column; gap: 6px; }

label {
  font-size: 13px; font-weight: 500; color: var(--text-muted);
  letter-spacing: 0.03em; text-transform: uppercase;
}

input {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text);
  font-family: 'Onest', sans-serif;
  font-size: 15px;
  padding: 12px 14px;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none; width: 100%;
}

input::placeholder { color: var(--text-muted); }
input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }

.btn-primary {
  background: var(--accent); color: #fff; border: none;
  border-radius: 10px; padding: 13px;
  font-family: 'Onest', sans-serif; font-size: 15px; font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 0 20px var(--accent-glow);
  display: flex; align-items: center; justify-content: center; gap: 8px;
}

.btn-primary:hover:not(:disabled) {
  opacity: 0.9; transform: translateY(-1px);
  box-shadow: 0 4px 24px var(--accent-glow);
}

.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-secondary {
  background: transparent; color: var(--text-muted);
  border: 1px solid var(--border); border-radius: 10px; padding: 13px;
  font-family: 'Onest', sans-serif; font-size: 15px;
  cursor: pointer; transition: border-color 0.2s, color 0.2s;
}

.btn-secondary:hover { border-color: var(--accent); color: var(--text); }

.btn-edit {
  background: transparent; color: var(--accent);
  border: 1px solid var(--accent); border-radius: 8px;
  padding: 6px 14px;
  font-family: 'Onest', sans-serif; font-size: 13px;
  cursor: pointer; transition: background 0.2s;
}

.btn-edit:hover { background: var(--accent-glow); }

.btn-logout {
  display: flex; align-items: center; gap: 6px;
  background: transparent; color: var(--text-muted);
  border: 1px solid var(--border); border-radius: 8px;
  padding: 7px 14px;
  font-family: 'Onest', sans-serif; font-size: 13px;
  cursor: pointer; transition: color 0.2s, border-color 0.2s;
  margin-left: auto;
}

.btn-logout:hover { color: var(--error); border-color: var(--error); }

.error-msg {
  background: rgba(248,113,113,0.1);
  border: 1px solid rgba(248,113,113,0.3);
  color: var(--error); border-radius: 8px;
  padding: 10px 14px; font-size: 14px;
}

.success-msg { color: var(--success); font-size: 14px; margin-top: 12px; }

.auth-link { text-align: center; margin-top: 24px; font-size: 14px; color: var(--text-muted); }
.auth-link a { color: var(--accent); text-decoration: none; }
.auth-link a:hover { text-decoration: underline; }

.profile-page {
  flex: 1;
  display: flex; align-items: flex-start; justify-content: center;
  padding: 48px 24px;
  background:
    radial-gradient(ellipse 60% 40% at 80% 20%, rgba(91,110,245,0.12), transparent),
    var(--bg);
}

.profile-card { width: 100%; max-width: 560px; display: flex; flex-direction: column; gap: 2px; }

.profile-header {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius) var(--radius) 0 0;
  padding: 28px 28px 24px;
  display: flex; align-items: center; gap: 16px;
}

.avatar {
  width: 52px; height: 52px; border-radius: 14px;
  background: var(--accent); box-shadow: 0 0 20px var(--accent-glow);
  color: #fff; font-family: 'Unbounded', sans-serif;
  font-size: 20px; font-weight: 700;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

.profile-title h1 { font-family: 'Unbounded', sans-serif; font-size: 18px; font-weight: 600; }

.role-badge {
  display: inline-block; font-size: 12px; color: var(--accent);
  background: var(--accent-glow); border: 1px solid rgba(91,110,245,0.3);
  border-radius: 6px; padding: 2px 8px; margin-top: 4px;
}

.profile-section {
  background: var(--surface); border: 1px solid var(--border);
  border-top: none; padding: 24px 28px;
}

.profile-section:last-child { border-radius: 0 0 var(--radius) var(--radius); }

.profile-section h2 {
  font-family: 'Unbounded', sans-serif; font-size: 13px; font-weight: 600;
  color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 16px;
}

.section-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.section-head h2 { margin-bottom: 0; }

.info-grid { display: flex; flex-direction: column; gap: 12px; }

.info-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px; background: var(--surface2);
  border-radius: 8px; border: 1px solid var(--border);
}

.info-label { font-size: 13px; color: var(--text-muted); }
.info-value { font-size: 14px; font-weight: 500; }

.edit-actions { display: flex; gap: 10px; }
.edit-actions .btn-primary { flex: 1; }
.edit-actions .btn-secondary { flex: 1; }

.spinner {
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff;
  border-radius: 50%; animation: spin 0.6s linear infinite;
}

.app-layout { min-height: 100vh; display: flex; flex-direction: column; }

.navbar {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 32px;
  height: 60px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 10;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: 'Unbounded', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}

.navbar-brand .logo-mark {
  width: 32px; height: 32px;
  border-radius: 8px;
  font-size: 14px;
  margin-bottom: 0;
  box-shadow: none;
}

.navbar-links {
  display: flex;
  gap: 4px;
  margin-left: 8px;
}

.navbar-links a {
  color: var(--text-muted);
  text-decoration: none;
  font-size: 14px;
  padding: 6px 12px;
  border-radius: 8px;
  transition: color 0.2s, background 0.2s;
}

.navbar-links a:hover,
.navbar-links a.router-link-active {
  color: var(--text);
  background: var(--surface2);
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ── Dashboard shared styles ── */
.dash-content { display: flex; flex-direction: column; gap: 16px; }

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px 28px;
}

.section-title {
  font-family: 'Unbounded', sans-serif;
  font-size: 13px; font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.section-hint {
  font-family: 'Onest', sans-serif;
  font-size: 11px; font-weight: 400;
  text-transform: none;
  letter-spacing: 0;
  color: var(--text-muted);
  margin-left: 8px;
}

.section-head {
  display: flex; align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.section-head .section-title { margin-bottom: 0; }

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 16px;
}

.form-grid .field.full { grid-column: 1 / -1; }
.form-grid .field.align-end { display: flex; align-items: flex-end; }

.form-actions { display: flex; gap: 10px; margin-top: 16px; }
.form-actions .btn-primary, .form-actions .btn-secondary { min-width: 120px; }

textarea {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text);
  font-family: 'Onest', sans-serif;
  font-size: 15px;
  padding: 12px 14px;
  outline: none;
  width: 100%;
  resize: vertical;
  transition: border-color 0.2s, box-shadow 0.2s;
}
textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-glow); }

select {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  color: var(--text);
  font-family: 'Onest', sans-serif;
  font-size: 15px;
  padding: 12px 14px;
  outline: none;
  width: 100%;
  cursor: pointer;
  transition: border-color 0.2s;
}
select:focus { border-color: var(--accent); }
option { background: var(--surface2); }

.flash {
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  animation: fadeIn 0.2s ease;
}
.flash.success { background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3); color: var(--success); }
.flash.error   { background: rgba(248,113,113,0.1); border: 1px solid rgba(248,113,113,0.3); color: var(--error); }
@keyframes fadeIn { from { opacity: 0; transform: translateY(-4px); } to { opacity: 1; transform: none; } }

.empty-hint { color: var(--text-muted); font-size: 14px; padding: 10px 0; }

.members-list { display: flex; flex-direction: column; gap: 8px; margin-bottom: 4px; }
.member-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 14px;
  background: var(--surface2); border: 1px solid var(--border); border-radius: 8px;
}
.member-info { display: flex; flex-direction: column; gap: 2px; }
.member-name { font-size: 14px; font-weight: 500; }
.member-meta { font-size: 12px; color: var(--text-muted); }

.btn-icon {
  width: 30px; height: 30px;
  border-radius: 7px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 13px;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}
.btn-icon:hover { background: var(--surface2); color: var(--text); }
.btn-icon.danger:hover { background: rgba(248,113,113,0.1); border-color: rgba(248,113,113,0.4); color: var(--error); }

.badge {
  display: inline-block; font-size: 11px; font-weight: 600;
  border-radius: 6px; padding: 2px 8px;
}
.badge-green { background: rgba(52,211,153,0.12); border: 1px solid rgba(52,211,153,0.3); color: var(--success); }
.badge-gray  { background: var(--surface2); border: 1px solid var(--border); color: var(--text-muted); }

.score-badge {
  display: inline-flex; align-items: center;
  font-family: 'Unbounded', sans-serif; font-size: 13px; font-weight: 600;
  color: var(--accent);
  background: var(--accent-glow);
  border: 1px solid rgba(91,110,245,0.3);
  border-radius: 8px;
  padding: 3px 10px;
}
.score-badge.sm { font-size: 11px; padding: 2px 8px; }

.solutions-list { display: flex; flex-direction: column; gap: 10px; }
.solution-card {
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  background: var(--surface);
}
.solution-card.inner { background: var(--surface2); }
.sol-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 8px; gap: 12px;
}
.sol-title { font-size: 15px; font-weight: 500; margin-bottom: 6px; }
.sol-meta { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.sol-desc { font-size: 13px; color: var(--text-muted); line-height: 1.6; margin: 8px 0; }
.eval-summary { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }

.meta-chip {
  font-size: 12px; color: var(--text-muted);
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 5px; padding: 2px 8px;
}

.eval-form {
  margin-top: 14px; padding-top: 14px;
  border-top: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 12px;
}
.score-row { display: flex; flex-direction: column; gap: 8px; }
.score-buttons { display: flex; gap: 6px; flex-wrap: wrap; }
.score-btn {
  width: 34px; height: 34px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text-muted);
  font-size: 13px; font-weight: 500;
  cursor: pointer;
  transition: all 0.15s;
}
.score-btn:hover { border-color: var(--accent); color: var(--accent); }
.score-btn.active { background: var(--accent); border-color: var(--accent); color: #fff; }

.all-evals { margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); display: flex; flex-direction: column; gap: 8px; }
.eval-row { display: flex; align-items: center; gap: 10px; }
.eval-who { font-size: 13px; font-weight: 500; }
.eval-comment { font-size: 13px; color: var(--text-muted); }

.task-desc { font-size: 14px; line-height: 1.7; color: var(--text); white-space: pre-line; }
.resources-label { font-size: 11px; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 12px; }
.resources-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.resource-row { margin-top: 10px; }
.resource-link {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 13px; color: var(--accent);
  background: var(--accent-glow);
  border: 1px solid rgba(91,110,245,0.3);
  border-radius: 8px; padding: 6px 12px;
  text-decoration: none; transition: background 0.2s;
}
.resource-link:hover { background: rgba(91,110,245,0.3); }
.resource-link.consultation { background: rgba(52,211,153,0.1); border-color: rgba(52,211,153,0.3); color: var(--success); }
.resource-link.consultation:hover { background: rgba(52,211,153,0.2); }

.link { color: var(--accent); text-decoration: none; font-size: 13px; }
.link:hover { text-decoration: underline; }

.checkbox-row { justify-content: flex-start !important; }
.checkbox-label {
  display: flex; align-items: center; gap: 8px;
  font-size: 14px; color: var(--text); cursor: pointer;
  text-transform: none; letter-spacing: 0;
}
.checkbox-label input[type=checkbox] {
  width: 16px; height: 16px; accent-color: var(--accent);
}

.admin-table-wrap { overflow-x: auto; margin-top: 12px; }
.admin-table {
  width: 100%; border-collapse: collapse; font-size: 14px;
}
.admin-table th {
  text-align: left; padding: 8px 12px;
  font-size: 11px; font-weight: 600;
  color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em;
  border-bottom: 1px solid var(--border);
}
.admin-table td { padding: 10px 12px; border-bottom: 1px solid var(--border); vertical-align: middle; }
.admin-table tr:last-child td { border-bottom: none; }
.admin-table tr:hover td { background: rgba(255,255,255,0.02); }
.id-cell { color: var(--text-muted); font-size: 12px; width: 40px; }
.center { text-align: center; }
.table-title { font-weight: 500; }
.table-sub { font-size: 12px; color: var(--text-muted); }

.assign-row { display: flex; gap: 6px; align-items: center; }
.assign-select { padding: 6px 10px; font-size: 13px; min-width: 140px; }
.actions-row { display: flex; gap: 6px; }

.inner-form {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 16px;
}

.tags-row { display: flex; flex-wrap: wrap; gap: 5px; }
.tag {
  font-size: 11px; color: var(--text-muted);
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 5px; padding: 2px 7px;
}
.mt-4  { margin-top: 4px; }
.mt-16 { margin-top: 16px; }

.state-box {
  display: flex; flex-direction: column;
  align-items: center; gap: 12px;
  padding: 60px 0; color: var(--text-muted);
}
.error-state { color: var(--error); }
.big-spinner {
  width: 32px; height: 32px;
  border: 3px solid var(--border); border-top-color: var(--accent);
  border-radius: 50%; animation: spin 0.7s linear infinite;
}
</style>