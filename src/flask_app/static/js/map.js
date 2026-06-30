// src/flask_app/static/js/map.js
// Initialise Leaflet map and load GeoJSON data from /api/map

document.addEventListener('DOMContentLoaded', function() {
  const map = L.map('map').setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  fetch('/api/map')
    .then(r => r.json())
    .then(geojson => {
      L.geoJSON(geojson, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(latlng, {
            radius: 6,
            fillColor: '#ff7f0e',
            color: '#fff',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          });
        },
        onEachFeature: function (feature, layer) {
          const props = feature.properties || {};
          const popup = `<b>${props.name || 'Location'}</b><br>Type: ${props.type}`;
          layer.bindPopup(popup);
        }
      }).addTo(map);
    })
    .catch(err => console.error('Map fetch error', err));
});
