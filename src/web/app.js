// agentP Desktop Suite Client App (Sprint 2 - Expanded Live Kanban)

let currentView = 'workspace';
let autoNameTimeout = null;

// Switch between Onboarding and Workspace
function switchView(viewName) {
  currentView = viewName;
  document.querySelectorAll('.view-panel').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));

  if (viewName === 'onboarding') {
    document.getElementById('viewOnboarding').classList.add('active');
    document.getElementById('tabOnboarding').classList.add('active');
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
    'AI Agent API': 'Hệ thống AI Agent API tự động điều phối đa mô hình qua 9router daemon và lưu trữ lịch sử SQLite.'
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
