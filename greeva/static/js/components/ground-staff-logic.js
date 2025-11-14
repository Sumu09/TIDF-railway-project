// Ground Staff Logic JavaScript for tables-gridjs.html
// This file handles the train table display and navigation

function dateTime() {
  const now = new Date();
  return now.toLocaleString("en-US", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

// Fetch trains data from the Flask backend with authentication
JWT_AUTH.fetchWithAuth("http://127.0.0.1:5000/trains")
  .then((res) => res.json())
  .then((data) => {
    // Set station name in the card header if available
    if (data.station_name) {
      const stationNameHeader = document.querySelector(".card-title.mb-0");
      if (stationNameHeader) {
        stationNameHeader.textContent = data.station_name;
      }
    }

    // Transform data to gridjs format: [[sl_no, name, time, status, report_id], ...]
    const tableData = (data.trains || []).map((item) => [
      item.sl_no,
      item.name,
      item.time,
      item.status,
      item.report_id, // Include report_id as the 5th column
    ]);

    new gridjs.Grid({
      columns: [
        {
          name: "Sl no.",
          width: "100px",
          sort: true,
        },
        {
          name: "Train Name",
          width: "280px",
          formatter: (cell, row) => {
            const trainId = row.cells[0].data;
            const trainStatus = row.cells[3].data;
            // If unfinished, show input and update button
            if (trainStatus === "unfinished" || trainStatus === "Unfinished") {
              return gridjs.html(`
                <div style="display: flex; justify-content: center; align-items: center; gap: 8px; width: 100%;">
                  <input type="text" id="train-name-input-${trainId}" value="" placeholder="Enter train name" style="width: 120px; padding: 2px 6px; font-size: 14px; text-align: center;" />
                  <button class="btn btn-sm btn-primary" style="padding: 2px 8px; font-size: 13px;" onclick="updateTrainName(${trainId})">Update</button>
                </div>
              `);
            } else {
              return gridjs.html(
                `<a href="/ground-staff?name=${encodeURIComponent(
                  cell
                )}&status=${trainStatus}&id=${trainId}" style="color: #011bff; text-decoration: none; font-weight: 500;">${cell}</a>`
              );
            }
          },
          sort: true,
        },
        {
          name: "Train Time",
          width: "120px",
          formatter: (cell) => {
            // If cell is a valid date string, format it, else show as is
            if (!cell) return "";
            if (/^\d{1,2}:\d{2}(\s?[APMapm]{2})?$/.test(cell.trim())) {
              return gridjs.html(
                `<span style="color: #011bff; text-decoration: none; font-weight: 500;">${cell}</span>`
              );
            }
            // Try to parse as date
            const dateObj = new Date(cell);
            if (!isNaN(dateObj.getTime())) {
              return gridjs.html(
                `<span style="color: #011bff; text-decoration: none; font-weight: 500;">${dateObj.toLocaleString(
                  "en-US",
                  {
                    year: "numeric",
                    month: "short",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                    hour12: true,
                  }
                )}</span>`
              );
            }
            // Fallback: show as is
            return gridjs.html(
              `<span style="color: #011bff; text-decoration: none; font-weight: 500;">${cell}</span>`
            );
          },
          sort: true,
        },
        {
          name: "Train Status",
          width: "180px",
          formatter: (cell, row) => {
            // Use row.cells[4].data for reportId
            const reportId = row.cells[4].data;
            const status = cell; // "Finished" or "Unfinished"
            const bgColor = status === "Finished" ? "#28a745" : "#dc3545";
            const hoverColor = status === "Finished" ? "#218838" : "#c82333";

            // Always link to train-report page using report_id
            return gridjs.html(
              `<a href="/train-report?id=${encodeURIComponent(reportId)}"
                 style="background-color: ${bgColor};
                        color: white;
                        padding: 8px 16px;
                        border-radius: 6px;
                        text-decoration: none;
                        font-weight: 500;
                        display: inline-block;
                        transition: all 0.3s ease;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                 onmouseover="this.style.backgroundColor='${hoverColor}';
                              this.style.transform='translateY(-2px)';
                              this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';"
                 onmouseout="this.style.backgroundColor='${bgColor}';
                             this.style.transform='translateY(0px)';
                             this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                ${status}
              </a>`
            );
          },
          sort: true,
        },
        // Add this hidden column for report_id
        {
          id: "report_id",
          name: "Report ID",
          hidden: true,
        },
      ],
      sort: true,
      resizable: true,
      pagination: {
        enabled: true,
        limit: 10,
        summary: true,
      },
      search: {
        enabled: true,
        placeholder: "Search trains...",
      },
      fixedHeader: true,
      height: "auto",
      data: tableData,
      style: {
        table: {
          "font-size": "14px",
          "border-collapse": "collapse",
        },
        th: {
          "background-color": "#f8f9fa",
          "font-weight": "600",
          "text-align": "center",
          padding: "12px 8px",
          border: "1px solid #dee2e6",
        },
        td: {
          "text-align": "center",
          padding: "10px 8px",
          border: "1px solid #dee2e6",
        },
      },
    }).render(document.getElementById("table-fixed-header"));

    // Expose updateTrainName globally for inline button
    window.updateTrainName = function (trainId) {
      const input = document.getElementById(`train-name-input-${trainId}`);
      if (!input) return;
      const newName = input.value.trim();
      if (!newName) {
        alert("Please enter a train name.");
        return;
      }
      // Find the report_id for this row (trainId is sl_no, not report_id)
      let reportId = null;
      // Find the row in the tableData that matches this sl_no
      for (const row of tableData) {
        if (row[0] === trainId) {
          reportId = row[4];
          break;
        }
      }
      if (!reportId) {
        alert("Could not find report ID for this train.");
        return;
      }
      // Send PATCH request to backend using report_id
      JWT_AUTH.fetchWithAuth(`http://127.0.0.1:5000/trains/${reportId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            // Update the table row in-place (no reload)
            const rowEl = input.closest("tr");
            if (rowEl) {
              // Update name cell
              const nameCell = rowEl.querySelector(`td:nth-child(2)`);
              if (nameCell) {
                nameCell.innerHTML = `<a href="/ground-staff?name=${encodeURIComponent(
                  newName
                )}&status=Finished&id=${trainId}" style="color: #011bff; text-decoration: none; font-weight: 500;">${newName}</a>`;
              }
              // Update status cell
              const statusCell = rowEl.querySelector(`td:nth-child(4)`);
              if (statusCell) {
                statusCell.innerHTML = `<a href="/train-report?id=${encodeURIComponent(
                  reportId
                )}"
                    style="background-color: #28a745; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 500; display: inline-block; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                    onmouseover="this.style.backgroundColor='#218838';this.style.transform='translateY(-2px)';this.style.boxShadow='0 4px 8px rgba(0,0,0,0.2)';"
                    onmouseout="this.style.backgroundColor='#28a745';this.style.transform='translateY(0px)';this.style.boxShadow='0 2px 4px rgba(0,0,0,0.1)';">
                    Finished
                  </a>`;
              }
            }
            alert("Train name updated successfully!");
          } else {
            alert(data.error || "Update failed.");
          }
        })
        .catch((err) => {
          alert("Network error. Please try again.");
        });
    };
  });

// In train-report.html
const urlParams = new URLSearchParams(window.location.search);
const trainId = urlParams.get("id");
if (trainId) {
  fetch(`http://127.0.0.1:5000/train-report?id=${trainId}`, {
    headers: {
      Authorization: "Bearer " + localStorage.getItem("authToken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Fill your table with data, leaving cells blank if data[field] is empty
    });
}
