//This code was taken from the documentation page on the Google API website 
//
// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;

 function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 34.05473, lng: -118.24515 },
    zoom: 6,
  });
  infoWindow = new google.maps.InfoWindow();
  
  const locationButton = document.createElement("button");

  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          infoWindow.setPosition(pos);
          infoWindow.setContent("Location found.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        },
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });

  //information in infowindow for each marker
const locations = [
  {
    position: { lat: 34.17485, lng:-118.05792 },
    title: "Cancer Support Community Greater San Gabriel Valley",
    content:`
      <div id="content">
        <h3>Cancer Support Community Greater San Gabriel Valley</h3>
        <div id="bodyContent">
          <p><b>Address: 331 W Sierra Madre Blvd, Sierra Madre, CA 91024 </b></p> 
          <p><b>Phone Number: +1(626)796-1083 </b><p>
          <p><b>Website: <a href="http://www.cancersupportsgv.org/">http://www.cancersupportsgv.org</a></b><p>
        </div>
      </div>
    `,
  },
  {
    position: { lat: 34.04823, lng: -118.45677 },
    title: "Cancer Support Community Los Angeles",
    content: `
      <div id="content">
        <h3>Cancer Support Community Los Angeles</h3>
        <div id="bodyContent">
          <p><b>Address: 1990 S Bundy Dr #100, Los Angeles, CA 90025 </b></p> 
          <p><b>Phone Number: +1(310)314-2555 </b><p>
          <p><b>Website: <a href="http://cancersupportla.org/">https://www.cancersupportsgv.org</a></b><p>
        </div>
      </div>
    `,
  },
  {
    position: { lat: 33.80630, lng: -118.32809 },
    title: "Cancer Support Community  South Bay",
    content: `
    <div id="content">
      <h3>Cancer Support Community South Bay</h3>
      <div id="bodyContent">
        <p><b>Address: 2601 Airport Dr #100, Torrance, CA 90505 </b></p> 
        <p><b>Phone Number: +1(310)376-3550 </b><p>
        <p><b>Website: <a href="http://cscsouthbay.org/">http://cscsouthbay.org</a></b><p>
      </div>
    </div>
  `,
  },
  // Add more locations as needed
];


//for each marker, put info in marker and title
locations.forEach((location) => {
  const infowindow = new google.maps.InfoWindow({
    content: location.content,
    ariaLabel: location.title, 
  });

  const marker = new google.maps.Marker({
    position: location.position,
    map,
    title: location.title,
  });

  //when clicked, open infowindow
  marker.addListener("click", () => {
    infowindow.open({
      anchor: marker,
      map,
    });
  });
});
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation.",
  );
  infoWindow.open(map);
}

window.initMap = initMap;




