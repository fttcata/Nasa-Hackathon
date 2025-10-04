map.addListener("click", function(e) {
  document.getElementById("latitude").value = e.latLng.lat();
  document.getElementById("longitude").value = e.latLng.lng();
});
function placeMarker(latLng, map, label) {
  if (state.marker) state.marker.setMap(null);
  state.marker = new google.maps.Marker({ position: latLng, map: map });
  state.latLng = { lat: latLng.lat?.() ?? latLng.lat, lng: latLng.lng?.() ?? latLng.lng };

  document.getElementById('latitude').value = state.latLng.lat;
  document.getElementById('longitude').value = state.latLng.lng;
}
document.getElementById('weatherForm').addEventListener('submit', function() {
  document.getElementById('spinner').style.display = 'flex';
});
