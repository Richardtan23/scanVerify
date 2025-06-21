document.addEventListener('DOMContentLoaded', () => {
  const tbody = document.querySelector('#reportsTable tbody');
  const clearBtn = document.getElementById('clearBtn');

  // Load reports
  chrome.storage.local.get({ reports: [] }, (data) => {
    tbody.innerHTML = data.reports.map(report => `
      <tr>
        <td><a href="${report.url}" target="_blank">${report.url}</a></td>
        <td>${new Date(report.date).toLocaleString()}</td>
        <td>${report.status}</td>
      </tr>
    `).join('');
  });

  // Clear reports
  clearBtn.addEventListener('click', () => {
    chrome.storage.local.set({ reports: [] }, () => {
      tbody.innerHTML = '';
      alert("All reports cleared!");
    });
  });
});