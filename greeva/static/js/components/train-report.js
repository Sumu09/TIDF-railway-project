// Grid.js Table Setup
new gridjs.Grid({
  columns: [
    { name: "Serial No.", width: "100px" },
    {
      name: "Train Name",
      width: "200px",
      formatter: (cell, row) => {
        const trainNameEncoded = encodeURIComponent(cell);
        return gridjs.html(
          `<a href="/train-details?name=${trainNameEncoded}" class="fw-bold text-info">${cell}</a>`
        );
      },
    },

    {
      name: "Train Status",
      formatter: (cell, row) => {
        const color = cell === "Finished" ? "green" : "red";
        const trainName = row.cells[1].data; // Get train name from the row
        const trainNameEncoded = encodeURIComponent(trainName);
        return gridjs.html(`
        <a href="/train-report?train=${trainNameEncoded}&status=${cell}" target="_blank" class="status-cell"
           style="background-color:${color}; color:white; padding:4px 8px; border-radius:4px; cursor:pointer; text-decoration:none;">
            ${cell}
        </a>
                `);
      },
    },
  ],
  data: [
    ["1", "Golden Express", "Finished"],
    ["2", "Silver Arrow", "unFinished"],
    ["3", "Blue Mountain", "Finished"],
    ["4", "Red Falcon", "unFinished"],
    ["5", "Eastern Star", "Finished"],
    ["6", "Western Breeze", "Finished"],
    ["7", "Sunrise Special", "Finished"],
    ["8", "Night Rider", "Finished"],
    ["9", "Desert Queen", "Finished"],
  ],
  pagination: {
    limit: 5,
  },
}).render(document.getElementById("table-fixed-header"));
