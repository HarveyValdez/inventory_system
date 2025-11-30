/**
 * Admin Reports Management JavaScript
 */

async function updateReportStatus(reportId, action) {
  const row = document.getElementById(`report-row-${reportId}`);
  const statusCell = document.getElementById(`status-cell-${reportId}`);
  
  if (!row) return;

  try {
    const headers = {
      "Content-Type": "application/json"
    };

    if (window.VortexConfig.csrfToken) {
      headers["X-CSRFToken"] = window.VortexConfig.csrfToken;
    }

    const response = await fetch(`/admin/report_action/${reportId}`, {
      method: "POST",
      headers: headers,
      body: JSON.stringify({ action: action })
    });

    if (!response.ok) throw new Error('Network error');

    if (action === 'delete') {
      row.style.transition = 'opacity 0.3s ease';
      row.style.opacity = '0';
      setTimeout(() => row.remove(), 300);
    } else if (action === 'read') {
      statusCell.innerHTML = '<span class="badge bg-warning">Read</span>';
      row.classList.remove('table-danger');
      row.classList.add('table-light');
    }
  } catch (e) {
    console.error("Error updating report:", e);
    alert("❌ Failed to update report. Check console for details.");
  }
}

async function markAllRead() {
  if (!confirm("Mark all unread reports as read?")) return;
  
  const unreadRows = document.querySelectorAll('.table-danger');
  let successCount = 0;

  for (let row of unreadRows) {
    const reportId = row.id.split('-')[1];
    try {
      await updateReportStatus(reportId, 'read');
      successCount++;
      await new Promise(resolve => setTimeout(resolve, 100)); // Rate limit
    } catch (e) {
      console.error(`Failed to mark report ${reportId} as read`, e);
    }
  }
  
  showFlashMessage(`✅ Marked ${successCount} reports as read`, "success");
}

function replyToUser(userId, reportId) {
  const message = prompt("Enter your reply to the user:");
  if (message && message.trim()) {
    alert(`Reply sent to user #${userId}!\n\nMessage: ${message.trim()}\n\n(Email integration pending)`);
    updateReportStatus(reportId, 'read');
  }
}

function viewUserDetails(userId) {
  window.open(`/manage_users?user=${userId}`, '_blank', 
    'width=800,height=600,scrollbars=yes');
}

function filterReports() {
  const status = document.getElementById('statusFilter').value;
  const type = document.getElementById('typeFilter').value;
  const url = new URL(window.location.href);
  
  if (status !== 'all') url.searchParams.set('status', status);
  else url.searchParams.delete('status');
  
  if (type !== 'all') url.searchParams.set('type', type);
  else url.searchParams.delete('type');
  
  window.location.href = url.toString();
}

function refreshReports() {
  const refreshBtn = event.target.closest('button');
  refreshBtn.classList.add('fa-spin');
  setTimeout(() => location.reload(), 500);
}

// Page load animations
document.addEventListener('DOMContentLoaded', function() {
  const rows = document.querySelectorAll('tbody tr');
  rows.forEach((row, index) => {
    row.style.opacity = '0';
    row.style.transform = 'translateX(-20px)';
    row.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    setTimeout(() => {
      row.style.opacity = '1';
      row.style.transform = 'translateX(0)';
    }, 50 * index);
  });
});