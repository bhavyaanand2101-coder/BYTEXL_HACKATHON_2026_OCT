import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Replace CSS
new_css = """    /* Firebase Auth Screen Overlay — Dark Theme */
    #auth-overlay-screen {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: #0a0a0a;
      z-index: 500;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      font-family: var(--font-sans);
    }
    .auth-outer {
      width: 460px;
      max-width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;
    }
    .auth-hero { text-align: center; }
    .auth-role-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      background: rgba(139,92,246,0.15);
      border: 1px solid rgba(139,92,246,0.35);
      border-radius: 20px;
      padding: 5px 14px;
      font-size: 0.75rem;
      font-weight: 700;
      color: #c4b5fd;
      letter-spacing: 0.01em;
      margin-bottom: 14px;
    }
    .auth-hero h1 {
      font-size: 1.95rem;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: -0.03em;
      margin: 0 0 8px;
    }
    .auth-hero p {
      font-size: 0.83rem;
      color: #94a3b8;
      margin: 0;
      line-height: 1.5;
    }
    /* Role Tab switcher */
    .auth-role-tabs {
      display: flex;
      background: #1a1a2e;
      border-radius: 12px;
      padding: 5px;
      gap: 4px;
      width: 100%;
    }
    .auth-role-tab {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 8px;
      border: none;
      background: transparent;
      color: #64748b;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: var(--font-sans);
    }
    .auth-role-tab.active {
      background: #252540;
      color: #e2e8f0;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .auth-role-tab:hover:not(.active) { color: #94a3b8; }
    /* Portal card */
    .auth-card {
      background: #141420;
      border: 1px solid #252540;
      border-radius: 16px;
      width: 100%;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .auth-card-header {
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }
    .auth-card-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: rgba(139,92,246,0.18);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .auth-card-icon svg { color: #a78bfa; }
    .auth-card-title {
      font-size: 1rem;
      font-weight: 700;
      color: #f1f5f9;
      margin: 0 0 3px;
    }
    .auth-card-subtitle {
      font-size: 0.78rem;
      color: #64748b;
      margin: 0;
    }
    /* Info strip */
    .auth-info-strip {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      background: rgba(139,92,246,0.08);
      border: 1px solid rgba(139,92,246,0.2);
      border-radius: 8px;
      padding: 9px 12px;
    }
    .auth-info-strip-text {
      font-size: 0.75rem;
      color: #a78bfa;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .btn-quick-demo {
      background: #7c3aed;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 6px 12px;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s ease;
      font-family: var(--font-sans);
    }
    .btn-quick-demo:hover { background: #6d28d9; }
    /* Input groups */
    .auth-input-group {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }
    .auth-input-label {
      font-size: 0.8rem;
      font-weight: 600;
      color: #94a3b8;
    }
    .auth-input-wrapper {
      position: relative;
      display: flex;
      align-items: center;
    }
    .auth-input-icon {
      position: absolute;
      left: 13px;
      color: #475569;
      pointer-events: none;
      display: flex;
      align-items: center;
    }
    .auth-input {
      width: 100%;
      background: #0f0f1a;
      border: 1px solid #252540;
      border-radius: 10px;
      padding: 11px 12px 11px 40px;
      font-size: 0.875rem;
      color: #e2e8f0;
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
      font-family: var(--font-sans);
      box-sizing: border-box;
    }
    .auth-input::placeholder { color: #334155; }
    .auth-input:focus {
      border-color: #7c3aed;
      box-shadow: 0 0 0 3px rgba(124,58,237,0.15);
    }
    /* Primary CTA */
    .btn-auth-primary {
      width: 100%;
      background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
      color: #fff;
      border: none;
      border-radius: 10px;
      padding: 13px 20px;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
      font-family: var(--font-sans);
      letter-spacing: 0.01em;
      box-shadow: 0 4px 16px rgba(124,58,237,0.3);
    }
    .btn-auth-primary:hover {
      background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
      box-shadow: 0 6px 20px rgba(124,58,237,0.4);
      transform: translateY(-1px);
    }
    /* Demo pills */
    .demo-role-pill {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 14px;
      background: #0f0f1a;
      border: 1px solid #252540;
      border-radius: 8px;
      cursor: pointer;
      font-size: 0.78rem;
      transition: all 0.15s ease;
    }
    .demo-role-pill:hover {
      background: #1a1a2e;
      border-color: #7c3aed;
    }
    .btn-google {
      background: #141420;
      border: 1px solid #252540;
      color: #94a3b8;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      padding: 10px 14px;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.83rem;
      cursor: pointer;
      transition: all 0.15s ease;
      width: 100%;
      font-family: var(--font-sans);
    }
    .btn-google:hover { background: #1a1a2e; border-color: #475569; color: #e2e8f0; }

"""
content = re.sub(r'/\* Firebase Auth Screen Overlay \*/.*?/\* User Profile Dropdown Menu \*/', new_css + '    /* User Profile Dropdown Menu */', content, flags=re.DOTALL)

# 2. Replace HTML
new_html = """  <!-- ════════════════════════════════════════════════════════════════════ -->
  <!-- FIREBASE AUTHENTICATION SCREEN OVERLAY — DARK THEME -->
  <!-- ════════════════════════════════════════════════════════════════════ -->
  <div id="auth-overlay-screen">
    <div class="auth-outer">

      <!-- Hero -->
      <div class="auth-hero">
        <div class="auth-role-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
          Role-Based Campus Portal
        </div>
        <h1>Sign In to CampusPulse</h1>
        <p>Choose your account type to access your tailored dashboard and tools.</p>
      </div>

      <!-- Role Tab switcher -->
      <div class="auth-role-tabs" id="auth-role-tabs">
        <button class="auth-role-tab active" id="tab-faculty" onclick="switchPortalRole('faculty')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          Faculty Login
        </button>
        <button class="auth-role-tab" id="tab-student" onclick="switchPortalRole('student')">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
          Student Login
        </button>
      </div>

      <!-- Faculty Portal Card -->
      <div class="auth-card" id="auth-card-faculty">
        <div class="auth-card-header">
          <div class="auth-card-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          </div>
          <div>
            <div class="auth-card-title">Faculty &amp; Advisor Portal</div>
            <div class="auth-card-subtitle">Full access to student performance matrices, risk bands, and action queues.</div>
          </div>
        </div>

        <div class="auth-info-strip">
          <div class="auth-info-strip-text">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Faculty role only: <strong>Student Risk Matrix &amp; Advisory Insights</strong>
          </div>
          <button class="btn-quick-demo" onclick="quickDemoLogin('teacher')">Quick Demo Login</button>
        </div>

        <div class="auth-input-group">
          <label class="auth-input-label">Advisor / Faculty ID</label>
          <div class="auth-input-wrapper">
            <span class="auth-input-icon">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </span>
            <input type="text" id="auth-signin-email" class="auth-input" placeholder="adv_001" value="ananya.sharma@campuspulse.edu">
          </div>
        </div>

        <div class="auth-input-group">
          <label class="auth-input-label">Password</label>
          <div class="auth-input-wrapper">
            <span class="auth-input-icon">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            </span>
            <input type="password" id="auth-signin-password" class="auth-input" placeholder="••••••••••" value="campuspulse2026">
          </div>
        </div>

        <button class="btn-auth-primary" onclick="handleFirebaseEmailSignIn()" id="btn-signin-submit">
          Sign In to Faculty Portal
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </button>
      </div>

      <!-- Student Portal Card (hidden by default) -->
      <div class="auth-card" id="auth-card-student" style="display:none;">
        <div class="auth-card-header">
          <div class="auth-card-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>
          </div>
          <div>
            <div class="auth-card-title">Student Portal</div>
            <div class="auth-card-subtitle">Access your academic dossier, placement sprint scores, and success roadmap.</div>
          </div>
        </div>

        <div class="auth-info-strip">
          <div class="auth-info-strip-text">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Student role only: <strong>Personal Dashboard &amp; What-If Simulator</strong>
          </div>
          <button class="btn-quick-demo" onclick="quickDemoLogin('student')">Quick Demo Login</button>
        </div>

        <div class="auth-input-group">
          <label class="auth-input-label">Student Roll Number</label>
          <div class="auth-input-wrapper">
            <span class="auth-input-icon">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </span>
            <input type="text" id="auth-student-id" class="auth-input" placeholder="2023CSE001">
          </div>
        </div>

        <div class="auth-input-group">
          <label class="auth-input-label">Password</label>
          <div class="auth-input-wrapper">
            <span class="auth-input-icon">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            </span>
            <input type="password" id="auth-student-password" class="auth-input" placeholder="••••••••••">
          </div>
        </div>

        <button class="btn-auth-primary" onclick="quickDemoLogin('student')">
          Sign In to Student Portal
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </button>
      </div>

      <!-- Footer -->
      <div style="font-size:0.72rem; color:#475569; text-align:center; letter-spacing:0.01em;">
        Protected by Firebase Authentication &amp; SHA-256 Audit Trail
      </div>
    </div>
  </div>

"""

content = re.sub(r'<!-- ════════════════════════════════════════════════════════════════════ -->\n  <!-- FIREBASE AUTHENTICATION SCREEN OVERLAY -->\n  <!-- ════════════════════════════════════════════════════════════════════ -->\n  <div id="auth-overlay-screen">.*?</div>\n    </div>\n  </div>', new_html.strip(), content, flags=re.DOTALL)

# 3. Insert JS function
js_func = """
  <script>
    function switchPortalRole(role) {
      document.querySelectorAll('.auth-role-tab').forEach(b => b.classList.remove('active'));
      var activeTab = document.getElementById('tab-' + role);
      if (activeTab) activeTab.classList.add('active');
      var facultyCard = document.getElementById('auth-card-faculty');
      var studentCard = document.getElementById('auth-card-student');
      if (facultyCard) facultyCard.style.display = role === 'faculty' ? 'flex' : 'none';
      if (studentCard) studentCard.style.display = role === 'student' ? 'flex' : 'none';
    }
"""

content = content.replace("<script>", js_func)

with open("index.html", "w") as f:
    f.write(content)
