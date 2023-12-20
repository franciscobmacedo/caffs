L.mapbox.accessToken =
  "pk.eyJ1IjoiZm1hY2VkbyIsImEiOiJjbHFjcG05eDQwNHBkMmptc3FrMmhsYWd3In0.xwVmSRfTbh79_TwRqW0i5Q";

const mapPopups = L.mapbox
  .map("map")
  .setView([51.50534963989, -0.090745464245823], 12)
  .addLayer(L.mapbox.styleLayer("mapbox://styles/mapbox/light-v11"));
const myLayer = L.mapbox.featureLayer().addTo(mapPopups);

dataUrl =
  "https://raw.githubusercontent.com/franciscobmacedo/caffs/main/frontend/locations.geojson";
// dataUrl = "locations.geojson";
fetch(dataUrl)
  .then((res) => res.json())
  .then((data) => {
    console.log(data);
    myLayer.setGeoJSON(data);
  });
//   mapPopups.scrollWheelZoom.disable();
