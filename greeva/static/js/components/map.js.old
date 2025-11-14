// scripts.js

// This function will be called by the Google Maps API script in the HTML
function initMap() {
  // 1. Create the map, centered on a default location (e.g., Guwahati)
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 7, // Zoomed out a bit to see more stations
    center: { lat: 26.1722, lng: 91.7458 }, // Centered on Guwahati
  });

  // 2. Fetch station data from your Python backend API
  fetchStationsAndAddMarkers(map);
}

async function fetchStationsAndAddMarkers(map) {
  try {
    // **FIX: Update the URL to match the new route in app.py**
    const response = await fetch("http://127.0.0.1:5001/api/stations");
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const stations = await response.json();

    // 3. Loop through each station and create a marker
    stations.forEach((station) => {
      // Ensure the station has valid latitude and longitude
      if (station.latitude && station.longitude) {
        const marker = new google.maps.Marker({
          // The position object expects numbers, float conversion is good practice
          position: {
            lat: parseFloat(station.latitude),
            lng: parseFloat(station.longitude),
          },
          map: map,
          title: station.name, // This will now work because we selected 'Station_Name as name'
          animation: google.maps.Animation.DROP,
        });

        // (Optional) Add an info window to show station name on click
        const infoWindow = new google.maps.InfoWindow({
          content: `<h6>${station.name}</h6>`, // This will also work now
        });

        marker.addListener("click", () => {
          infoWindow.open(map, marker);
        });
      }
    });
  } catch (error) {
    console.error("Error fetching station data:", error);
    // Display an error message to the user on the map itself
    document.getElementById("map").innerHTML =
      "Could not load station data. Make sure the backend server is running and there are no errors in its console.";
  }
}
