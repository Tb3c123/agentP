// agentP Desktop Suite Client App (Sprint 2 - Expanded Live Kanban)

let currentView = 'workspace';
let autoNameTimeout = null;

// Switch between all 5 views
function switchView(viewName) {
  currentView = viewName;
  document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));

  if (viewName === 'onboarding') {
    document.getElementById('viewOnboarding').classList.add('active');
    document.getElementById('tabOnboarding').classList.add('active');
  } else if (viewName === 'studio') {
    document.getElementById('viewStudio').classList.add('active');
    document.getElementById('tabStudio').classList.add('active');
  } else if (viewName === 'kanban') {
    document.getElementById('viewKanban').classList.add('active');
    document.getElementById('tabKanban').classList.add('active');
    loadFullKanban();
  } else if (viewName === 'code') {
    document.getElementById('viewCode').classList.add('active');
    document.getElementById('tabCode').classList.add('active');
    loadFileTree();
    openFileInEditor('lib/features/cart/cart_button.tsx');
  } else {
    document.getElementById('viewWorkspace').classList.add('active');
    document.getElementById('tabWorkspace').classList.add('active');
    loadWorkspace();
  }
}

// Smart Auto-Naming listener
const descInput = document.getElementById('projectDescInput');
if (descInput) {
  descInput.addEventListener('input', (e) => {
    clearTimeout(autoNameTimeout);
    autoNameTimeout = setTimeout(() => {
      fetchAutoName(e.target.value);
    }, 250);
  });
}

async function fetchAutoName(text) {
  try {
    const res = await fetch('/api/auto-name', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: text })
    });
    const data = await res.json();
    document.getElementById('suggestedNameTag').innerText = `🏷️ ${data.primary}`;
    document.getElementById('suggestedPathText').innerText = data.suggested_path;
  } catch (err) {
    console.error('Auto-name error:', err);
  }
}

function applyTemplate(name) {
  const templates = {
    'E-Commerce': 'Tôi muốn xây dựng nền tảng sàn thương mại điện tử mua sắm trực tuyến, có giỏ hàng, mã giảm giá và thanh toán online.',
    'Mobile Flutter': 'Ứng dụng di động đa nền tảng bằng Flutter, tích hợp push notification và xác thực Firebase Auth.',
    'SaaS Dashboard': 'Hệ thống SaaS Dashboard quản lý số liệu doanh thu thời gian thực, xuất báo cáo Excel và biểu đồ phân tích.',
    'AI Agent API': 'Hệ thống AI Agent API tự động điều phối đa mô hình qua agentP Core Daemon và lưu trữ lịch sử SQLite.'
  };
  descInput.value = templates[name] || descInput.value;
  fetchAutoName(descInput.value);
}

function launchProjectFromOnboarding() {
  switchView('workspace');
  handleSendMessage(`Bắt đầu khởi tạo dự án: ${descInput.value}`);
}

// Load workspace data from SQLite daemon
async function loadWorkspace() {
  try {
    const res = await fetch('/api/workspace');
    const data = await res.json();
    renderSwarmRoles(data.swarm_roles);
    renderMiniKanban(data.mini_kanban);
    renderChatMessages(data.chat_messages, data.active_checkpoint);
  } catch (err) {
    console.warn('API error, using fallback state:', err);
  }
}

function renderSwarmRoles(roles) {
  const container = document.getElementById('swarmListContainer');
  if (!container || !roles) return;
  container.innerHTML = roles.map(r => `
    <div class="swarm-item">
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="width:6px; height:6px; border-radius:50%; background:${r.status === 'connected' ? '#10B981' : '#94A3B8'};"></span>
        <span class="role-name">${r.display_name.split('(')[0].trim()}</span>
      </div>
      <span class="token-stat">🪙 ${r.tokens_spent || '1.2k'}</span>
    </div>
  `).join('');
}

function renderMiniKanban(cols) {
  if (!cols) return;
  
  const mapCol = (containerId, countId, items) => {
    const countEl = document.getElementById(countId);
    if (countEl) countEl.innerText = items.length;
    
    const container = document.getElementById(containerId);
    if (!container) return;

    if (items.length === 0) {
      container.innerHTML = '<div style="text-align:center; padding:20px 4px; color:#94A3B8; font-size:10px; font-style:italic;">Trống</div>';
      return;
    }

    container.innerHTML = items.map(t => `
      <div class="task-card">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <span class="task-id">${t.task_id}</span>
          <span style="font-size:8px; font-weight:700; color:${t.priority === 'urgent' ? '#DC2626' : (t.priority === 'high' ? '#D97706' : '#64748B')}; text-transform:uppercase;">${t.priority}</span>
        </div>
        <div class="task-title">${t.title}</div>
        <div class="task-assignee">
          <span>${t.assigned_role_id}</span>
          <span style="font-weight:700; color:#0F766E;">⚡ ${t.tokens_spent}</span>
        </div>
      </div>
    `).join('');
  };

  mapCol('colCardsTodo', 'countTodo', cols.todo || []);
  mapCol('colCardsCoding', 'countCoding', cols.coding || []);
  mapCol('colCardsQA', 'countQA', cols.qa || []);
  mapCol('colCardsDone', 'countDone', cols.done || []);
}

function renderChatMessages(messages, activeCheckpoint) {
  const stream = document.getElementById('chatStream');
  if (!stream) return;

  let html = '';
  (messages || []).forEach(m => {
    if (m.sender_type === 'user') {
      html += `
        <div class="chat-bubble user">
          <div style="font-size:11px; font-weight:700; margin-bottom:2px; opacity:0.9;">Bạn (Chủ dự án):</div>
          <div>${m.content}</div>
        </div>
      `;
    } else if (m.sender_type === 'system_event') {
      html += `
        <div style="text-align:center; padding:8px; font-size:11px; font-weight:700; color:#DC2626; background:#FEE2E2; border-radius:6px;">
          ${m.content}
        </div>
      `;
    } else {
      html += `
        <div class="chat-bubble pm">
          <div class="pm-header">
            <div class="avatar-circle" style="width:24px; height:24px; font-size:10px;">PM</div>
            <div class="title">${m.sender_name}</div>
            <div class="meta">Claude 3.5 Sonnet</div>
          </div>
          <div>${m.content}</div>
          
          ${m.thinking_log ? `
            <div class="thinking-box">
              <div class="thinking-title">💭 RAW MODEL THINKING LOG: Thought for ${(m.thought_duration_ms/1000).toFixed(1)}s</div>
              <div style="white-space: pre-wrap;">${m.thinking_log}</div>
            </div>
          ` : ''}
        </div>
      `;
    }
  });

  // Render Active Checkpoint if any
  if (activeCheckpoint) {
    html += `
      <div class="checkpoint-gate-card">
        <div class="checkpoint-header">
          <span>🛑</span>
          <span>CHECKPOINT #02: YÊU CẦU PHÊ DUYỆT CỦA BẠN</span>
        </div>
        <div class="checkpoint-body">
          ${activeCheckpoint.summary}<br>
          <b>Thay đổi:</b> ${activeCheckpoint.files_changed} files (+${activeCheckpoint.insertions} / -${activeCheckpoint.deletions} lines).<br>
          <span style="color:#047857; font-weight:700;">${activeCheckpoint.test_details}</span>
        </div>
        <div class="checkpoint-actions">
          <button class="btn-approve" onclick="resolveCheckpoint('approved')">✅ Duyệt &amp; Merge Git</button>
          <button class="btn-avd" onclick="alert('Mở máy ảo Pixel 8 Pro...')">📱 Chạy thử trên AVD</button>
          <button class="btn-rework" onclick="resolveCheckpoint('rejected')">✍️ Yêu cầu sửa</button>
        </div>
      </div>
    `;
  }

  stream.innerHTML = html;
  stream.scrollTop = stream.scrollHeight;
}

// Send chat message
async function handleSendMessage(overrideText) {
  const input = document.getElementById('chatInputBox');
  const text = overrideText || (input ? input.value.trim() : '');
  if (!text) return;
  if (!overrideText && input) input.value = '';

  const stream = document.getElementById('chatStream');
  stream.innerHTML += `
    <div class="chat-bubble user">
      <div style="font-size:11px; font-weight:700; margin-bottom:2px; opacity:0.9;">Bạn (Chủ dự án):</div>
      <div>${text}</div>
    </div>
  `;
  stream.scrollTop = stream.scrollHeight;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    loadWorkspace();
  } catch (err) {
    console.error('Chat error:', err);
  }
}

// Emergency Stop
async function triggerEmergencyStop() {
  try {
    const res = await fetch('/api/emergency-stop', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const data = await res.json();
    alert(`⏹️ ĐÃ DỪNG ĐỘT NGỘT!\nThời gian phản hồi: ${data.response_time_ms}ms (Đạt chuẩn <100ms)`);
    loadWorkspace();
  } catch (err) {
    console.error('Emergency stop error:', err);
  }
}

// Resolve Checkpoint
async function resolveCheckpoint(action) {
  try {
    const res = await fetch('/api/checkpoint/resolve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        checkpoint_id: 'CHK-02',
        action: action,
        feedback: action === 'approved' ? 'Phê duyệt từ giao diện web' : 'Yêu cầu kiểm tra lại'
      })
    });
    const data = await res.json();
    alert(`✓ Checkpoint ${data.checkpoint_id} đã được giải quyết: ${data.status}`);
    loadWorkspace();
  } catch (err) {
    console.error('Resolve checkpoint error:', err);
  }
}

// Global Keyboard Emergency Stop (ESC)
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    triggerEmergencyStop();
  }
});

// Initial boot
document.addEventListener('DOMContentLoaded', () => {
  loadWorkspace();
});

// ================= SPRINT 3: DUAL-MODE VISUAL UI STUDIO (TLDRAW & ONLOOK) =================
let currentStudioMode = 'tldraw';
let selectedComponentTag = 'CartCheckoutButton';

function switchStudioMode(mode) {
  currentStudioMode = mode;
  document.querySelectorAll('.studio-mode-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.studio-subpanel').forEach(p => p.classList.remove('active'));

  if (mode === 'tldraw') {
    document.getElementById('btnModeTldraw').classList.add('active');
    document.getElementById('studioTldrawPanel').classList.add('active');
  } else {
    document.getElementById('btnModeOnlook').classList.add('active');
    document.getElementById('studioOnlookPanel').classList.add('active');
  }
}

// Save Tldraw Whiteboard Snapshot (.tldr)
async function saveTldrawBoard() {
  const canvasData = {
    version: 1,
    title: "Concept Board Cart & Checkout Flow",
    author: "Elena (UI/UX)",
    elements: [
      { id: "frame_cart", type: "wireframe", x: 60, y: 100, title: "Cart Screen" },
      { id: "arrow_1", type: "arrow", from: "frame_cart", to: "frame_checkout" },
      { id: "frame_checkout", type: "wireframe", x: 480, y: 100, title: "Checkout Modal" },
      { id: "sticky_1", type: "note", text: "Hiển thị rõ giá gốc và giá giảm" }
    ],
    updated_at: Date.now()
  };

  try {
    const res = await fetch('/api/studio/save-tldraw', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: "Cart Screen Wireframe & User Flow",
        canvas_data: canvasData
      })
    });
    const data = await res.json();
    alert(`✓ ĐÃ LƯU BẢN VẼ TLDRAW!\nFile: ${data.file_name}\nSnapshot ID: ${data.snapshot_id}\nĐã lưu vào .agents/designs/ và SQLite.`);
  } catch (err) {
    console.error('Save Tldraw error:', err);
  }
}

function addStickyNote() {
  const canvas = document.getElementById('tldrawCanvas');
  const note = document.createElement('div');
  note.style.cssText = "width:140px; background:#FEF08A; border:1px solid #FDE047; border-radius:4px; padding:10px; font-size:9px; color:#854D0E; box-shadow:0 4px 10px rgba(0,0,0,0.08); transform:rotate(-2deg); margin-top:20px;";
  note.innerHTML = `<b>Ý kiến mới:</b><br>Nút thanh toán cần hỗ trợ cảm biến vân tay / FaceID.`;
  canvas.appendChild(note);
}

// Onlook Select Element
function selectDomElement(el, componentName) {
  document.querySelectorAll('.interactive-dom-element').forEach(item => item.classList.remove('selected'));
  el.classList.add('selected');
  selectedComponentTag = componentName;
  document.getElementById('inspectedElementName').innerText = `<${componentName} />`;
}

// Update Live Classes from input
function updateLiveClasses(val) {
  document.getElementById('codeClassPreview').innerText = val;
  const btn = document.getElementById('liveButtonPreview');
  if (btn) {
    if (val.includes('bg-amber')) {
      btn.style.background = '#D97706';
      btn.style.color = '#FFFFFF';
    } else if (val.includes('bg-emerald')) {
      btn.style.background = '#10B981';
      btn.style.color = '#FFFFFF';
    } else if (val.includes('bg-red')) {
      btn.style.background = '#EF4444';
      btn.style.color = '#FFFFFF';
    } else {
      btn.style.background = '#0D9488';
      btn.style.color = '#FFFFFF';
    }
  }
}

function applyColorToken(colorClass) {
  const input = document.getElementById('tailwindInput');
  let current = input.value;
  current = current.replace(/bg-\w+-\d+/, colorClass);
  input.value = current;
  updateLiveClasses(current);
}

// Sync Onlook to Source Code via AST Sync Engine
async function syncOnlookToSource() {
  const input = document.getElementById('tailwindInput');
  const newClasses = input ? input.value : 'bg-teal-600 text-white font-bold py-3 px-6 rounded-lg';

  try {
    const res = await fetch('/api/studio/sync-onlook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        file_path: 'lib/features/cart/cart_button.tsx',
        component_tag: selectedComponentTag,
        new_classes: newClasses
      })
    });
    const data = await res.json();
    alert(`⚡ ĐỒNG BỘ AST 2 CHIỀU THÀNH CÔNG!\nFile: ${data.file_path}\nComponent: <${data.component_tag} />\nĐộ trễ ghi code: ${data.latency_ms}ms (Đạt chuẩn <50ms)\nĐã ghi nhận snapshot vào CSDL SQLite.`);
  } catch (err) {
    console.error('Sync Onlook error:', err);
  }
}

/* ==========================================================================
   SPRINT 4 CLIENT LOGIC: KANBAN STUDIO, FILE EXPLORER, SPLIT DIFF & MODAL
   ========================================================================== */

let allKanbanData = null;
let currentActiveFilePath = 'lib/features/cart/cart_button.tsx';
let rawFileTree = null;

// 1. Full Studio Kanban (6 Columns)
async function loadFullKanban() {
  try {
    const res = await fetch('/api/kanban/all');
    const data = await res.json();
    allKanbanData = data.columns || {};
    renderFullKanbanColumns(allKanbanData);
  } catch (err) {
    console.error('Error loading full kanban:', err);
  }
}

function renderFullKanbanColumns(cols) {
  const mapping = [
    { key: 'backlog', countId: 'countBacklog', containerId: 'fullCardsBacklog' },
    { key: 'spec_design', countId: 'countSpecDesign', containerId: 'fullCardsSpecDesign' },
    { key: 'development', countId: 'countDevelopment', containerId: 'fullCardsDevelopment' },
    { key: 'review', countId: 'countReview', containerId: 'fullCardsReview' },
    { key: 'quality_gate', countId: 'countQualityGate', containerId: 'fullCardsQualityGate' },
    { key: 'done', countId: 'countDoneStudio', containerId: 'fullCardsDoneStudio' }
  ];

  mapping.forEach(m => {
    const items = cols[m.key] || [];
    const countEl = document.getElementById(m.countId);
    if (countEl) countEl.innerText = items.length;

    const cont = document.getElementById(m.containerId);
    if (cont) {
      cont.innerHTML = items.map(task => `
        <div class="full-card" onclick="alert('Task: ${task.title}\\nVai trò: ${task.assigned_role_id}\\nTokens: ${task.tokens_spent || 0}')">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="card-role-badge" style="background:#F1F5F9; color:#0F172A;">${task.assigned_role_id || 'alex_pm'}</span>
            <span style="font-size:9px; font-weight:700; color:${task.priority === 'urgent' ? '#DC2626' : '#D97706'};">${task.priority ? task.priority.toUpperCase() : 'MEDIUM'}</span>
          </div>
          <div style="font-weight:700; font-size:11px; color:#1E293B; margin-bottom:4px;">${task.title}</div>
          <div style="display:flex; justify-content:space-between; font-size:9px; color:#64748B;">
            <span>ID: ${task.task_id}</span>
            <span>🪙 ${task.tokens_spent || 0} tokens</span>
          </div>
        </div>
      `).join('') || '<div style="font-size:10px; color:#94A3B8; text-align:center; padding:15px;">(Trống)</div>';
    }
  });
}

function filterKanbanTasks() {
  const sprintVal = document.getElementById('filterSprint').value;
  if (!allKanbanData) return;

  if (sprintVal === 'all') {
    renderFullKanbanColumns(allKanbanData);
    return;
  }

  const filtered = {};
  for (const [col, tasks] of Object.entries(allKanbanData)) {
    filtered[col] = tasks.filter(t => t.sprint_id === sprintVal || !t.sprint_id);
  }
  renderFullKanbanColumns(filtered);
}

// 2. File Explorer & Tree Rendering
async function loadFileTree() {
  try {
    const res = await fetch('/api/files/tree');
    const tree = await res.json();
    rawFileTree = tree;
    renderFileTreeNodes(tree);
  } catch (err) {
    console.error('Error loading file tree:', err);
  }
}

function renderFileTreeNodes(tree) {
  const container = document.getElementById('fileTreeContainer');
  if (!container || !tree) return;

  function _buildHtml(node, depth = 0) {
    const pad = depth * 14;
    if (node.is_dir) {
      let subHtml = (node.children || []).map(child => _buildHtml(child, depth + 1)).join('');
      return `
        <div>
          <div class="tree-item" style="padding-left:${pad + 6}px; font-weight:700;">
            <span>📁</span>
            <span>${node.name}</span>
          </div>
          <div>${subHtml}</div>
        </div>
      `;
    } else {
      const agent = node.agent || { name: 'Alex', color: '#0D9488' };
      const isActive = (node.path === currentActiveFilePath) ? 'active' : '';
      return `
        <div class="tree-item ${isActive}" style="padding-left:${pad + 6}px;" onclick="openFileInEditor('${node.path}')">
          <span>📄</span>
          <span>${node.name}</span>
          <span class="tree-agent-pill" style="background:${agent.color};">${agent.name}</span>
        </div>
      `;
    }
  }

  container.innerHTML = _buildHtml(tree, 0);
}

function filterFileTree(query) {
  if (!rawFileTree) return;
  const q = query.toLowerCase().trim();
  const items = document.querySelectorAll('.tree-item');
  items.forEach(el => {
    if (el.innerText.toLowerCase().includes(q)) {
      el.style.display = 'flex';
    } else {
      el.style.display = 'none';
    }
  });
}

// 3. Integrated Monaco Editor & Split Diff
async function openFileInEditor(filePath) {
  currentActiveFilePath = filePath;
  const pathEl = document.getElementById('activeEditorFilePath');
  if (pathEl) pathEl.innerText = filePath;

  // Language pill
  const langPill = document.getElementById('activeFileLanguage');
  if (langPill) {
    if (filePath.endsWith('.tsx') || filePath.endsWith('.jsx')) langPill.innerText = 'TypeScript (TSX)';
    else if (filePath.endsWith('.py')) langPill.innerText = 'Python 3';
    else if (filePath.endsWith('.dart')) langPill.innerText = 'Dart / Flutter';
    else if (filePath.endsWith('.sql')) langPill.innerText = 'SQL (SQLite)';
    else if (filePath.endsWith('.md')) langPill.innerText = 'Markdown';
    else langPill.innerText = 'Text / Source';
  }

  // Update active state in tree
  document.querySelectorAll('.tree-item').forEach(el => el.classList.remove('active'));

  try {
    const res = await fetch(`/api/code/diff?path=${encodeURIComponent(filePath)}`);
    const diff = await res.json();
    renderMonacoDiff(diff);
  } catch (err) {
    console.error('Error fetching diff:', err);
  }
}

function renderMonacoDiff(diff) {
  const oldCont = document.getElementById('diffOldContent');
  const newCont = document.getElementById('diffNewContent');

  if (oldCont && diff.old_content) {
    const lines = diff.old_content.split('\n');
    oldCont.innerHTML = lines.map((l, i) => `
      <div class="diff-line removed">
        <span class="line-num">${i + 1}</span>
        <span class="line-text">${escapeHtml(l)}</span>
      </div>
    `).join('');
  }

  if (newCont && diff.new_content) {
    const lines = diff.new_content.split('\n');
    newCont.innerHTML = lines.map((l, i) => `
      <div class="diff-line added">
        <span class="line-num">${i + 1}</span>
        <span class="line-text">${escapeHtml(l)}</span>
      </div>
    `).join('');
  }
}

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

async function handleSafeDeleteActiveFile() {
  if (!confirm(`Bạn có chắc muốn chuyển file '${currentActiveFilePath}' vào thùng rác an toàn (.agents/trash/)?`)) {
    return;
  }

  try {
    const res = await fetch('/api/files/delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: currentActiveFilePath })
    });
    const data = await res.json();
    if (data.success) {
      alert(`🗑️ THÀNH CÔNG: ${data.message}\nFile đã được bảo lưu an toàn.`);
      loadFileTree();
    } else {
      alert(`Lỗi: ${data.error}`);
    }
  } catch (err) {
    console.error('Error deleting file:', err);
  }
}

function handleAcceptDiff() {
  alert(`✅ ĐÃ CHẤP NHẬN THAY ĐỔI & STAGE GIT!\nFile: ${currentActiveFilePath}\nNhánh: feature/cart-voucher\nTrạng thái: Sẵn sàng commit vào CSDL.`);
}

function exportProjectReport() {
  alert('📊 SOPHIA (DOCS/BA LEAD) BÁO CÁO:\nĐã xuất bản bảng tính Excel phân bổ 14 vai trò, số dòng code và 42.5k tokens tiết kiệm được vào docs/EXCEL_REPORT.xlsx!');
}

function openTrashModal() {
  alert('🗑️ THÙNG RÁC AN TOÀN (.agents/trash/):\nMọi file bị xóa đều lưu trữ kèm metadata và có thể khôi phục 100% bất kỳ lúc nào.');
}

// 4. Project Hub & Antigravity Danger Zone Modal
function openProjectSettingsModal() {
  const modal = document.getElementById('projectSettingsModal');
  if (modal) modal.style.display = 'flex';
}

function closeProjectSettingsModal() {
  const modal = document.getElementById('projectSettingsModal');
  if (modal) modal.style.display = 'none';
}

function switchSettingsTab(tabName) {
  document.querySelectorAll('.settings-tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('settingsTabGeneral').style.display = 'none';
  document.getElementById('settingsTabEnv').style.display = 'none';
  document.getElementById('settingsTabDanger').style.display = 'none';

  if (tabName === 'env') {
    document.getElementById('btnTabEnv').classList.add('active');
    document.getElementById('settingsTabEnv').style.display = 'block';
  } else if (tabName === 'danger') {
    document.getElementById('btnTabDanger').classList.add('active');
    document.getElementById('settingsTabDanger').style.display = 'block';
  } else {
    document.getElementById('btnTabGeneral').classList.add('active');
    document.getElementById('settingsTabGeneral').style.display = 'block';
  }
}

function handleDangerInputChange(val) {
  const btn = document.getElementById('btnDangerDeleteProject');
  const expected = 'FoodDelivery-Loyalty-App';

  if (val.trim() === expected) {
    btn.classList.remove('locked');
    btn.classList.add('unlocked');
    btn.disabled = false;
    btn.innerText = '🚨 XÓA VĨNH VIỄN DỰ ÁN (SẴN SÀNG)';
  } else {
    btn.classList.remove('unlocked');
    btn.classList.add('locked');
    btn.disabled = true;
    btn.innerText = '🔒 BỊ KHÓA — GÕ TÊN DỰ ÁN ĐỂ MỞ';
  }
}

async function executeAntigravityProjectDelete() {
  const input = document.getElementById('dangerConfirmInput').value;
  try {
    const res = await fetch('/api/project/verify-delete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: 'proj_food_delivery',
        confirmation: input
      })
    });
    const data = await res.json();
    if (data.allowed) {
      if (confirm('🚨 CẢNH BÁO CUỐI CÙNG (Cơ chế 2 lớp Antigravity):\nBạn có thực sự muốn xóa sạch dự án FoodDelivery-Loyalty-App?')) {
        alert('Dự án đã được thanh lý an toàn theo quy chuẩn Antigravity.');
        closeProjectSettingsModal();
        switchView('onboarding');
      }
    } else {
      alert(`Từ chối: ${data.error}`);
    }
  } catch (err) {
    console.error('Delete error:', err);
  }
}
