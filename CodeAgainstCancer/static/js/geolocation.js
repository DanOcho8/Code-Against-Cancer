//This code was taken from the documentation page on the Google API website 
//
// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
let map, infoWindow;

 function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 40.14227, lng: -101.96751 },
    zoom: 3,
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
    position: { lat: 34.16207, lng:-118.05962 },
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
    position: { lat: 34.03431, lng: -118.45574 },
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
    position: { lat: 33.79347, lng: -118.32912 },
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
  {
    position: { lat: 33.46979, lng: -112.06667 },
    title: "Cancer Support Community Arizona",
    content: `
    <div id="content">
      <h3>Cancer Support Community Arizona</h3>
      <div id="bodyContent">
        <p><b>Address: 360 E Palm Ln, Phoenix, AZ 85004 </b></p> 
        <p><b>Phone Number: +1(602)712-1006 </b><p>
        <p><b>Website: <a href="http://www.cscaz.org/">http://www.cscaz.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 45.67820, lng: -111.05146 },
    title: "Cancer Support Community Montana",
    content: `
    <div id="content">
      <h3>Cancer Support Community Montana</h3>
      <div id="bodyContent">
        <p><b>Address: 102 S 11th Ave, Bozeman, MT 59715 </b></p> 
        <p><b>Phone Number: +1(406)582-1600 </b><p>
        <p><b>Website: <a href="https://cancersupportmontana.org/">https://cancersupportmontana.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 32.87895, lng: -96.76287 },
    title: "Cancer Support Community North Texas",
    content: `
    <div id="content">
      <h3>Cancer Support Community North Texas</h3>
      <div id="bodyContent">
        <p><b>Address: 8196 Walnut Hill Ln LL10, Dallas, TX 75231 </b></p> 
        <p><b>Phone Number: +1(214)345-8230 </b><p>
        <p><b>Website: <a href="http://cancersupporttexas.org/">http://cancersupporttexas.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 38.60054, lng: -90.45217 },
    title: "Cancer Support Community of Greater St Louis",
    content: `
    <div id="content">
      <h3>Cancer Support Community of Greater St Louis</h3>
      <div id="bodyContent">
        <p><b>Address: 1058 Old Des Peres Rd, Des Peres, MO 63131 </b></p> 
        <p><b>Phone Number: +1(314)238-2000 </b><p>
        <p><b>Website: <a href="http://www.cancersupportstl.org/">http://www.cancersupportstl.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 33.90701, lng: -84.34935 },
    title: "Cancer Support Community Atlanta (Wellness Community Atlanta)",
    content: `
    <div id="content">
      <h3>Cancer Support Community Atlanta (Wellness Community Atlanta)</h3>
      <div id="bodyContent">
        <p><b>Address: in Center Pointe, 1100 Johnson Ferry Rd NE Bldg 2, Atlanta, GA 30342 </b></p> 
        <p><b>Phone Number: +1(404)843-1880 </b><p>
        <p><b>Website: <a href="http://www.cscatlanta.org/">http://www.cscatlanta.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 37.59682, lng: -83.90259 },
    title: "Cancer Support Community East Tennessee",
    content: `
    <div id="content">
      <h3>Cancer Support Community East Tennessee</h3>
      <div id="bodyContent">
        <p><b>Address: 6204 Baum Dr, Knoxville, TN 37919 </b></p> 
        <p><b>Phone Number: +1(865)546-4661 </b><p>
        <p><b>Website: <a href="http://www.cancersupportet.org/">http://www.cancersupportet.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 40.05280, lng: -83.05218 },
    title: "Cancer Support Community Ohio",
    content: `
    <div id="content">
      <h3>Cancer Support Community Ohio</h3>
      <div id="bodyContent">
        <p><b>Address: 1200 Old Henderson Rd, Columbus, OH 43220 </b></p> 
        <p><b>Phone Number: +1(614)884-4673 </b><p>
        <p><b>Website: <a href="https://www.cancersupportohio.org/">https://www.cancersupportohio.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 42.25744, lng: -83.68135 },
    title: "Cancer Support Community of Greater Ann Arbor",
    content: `
    <div id="content">
      <h3>Cancer Support Community of Greater Ann Arbor</h3>
      <div id="bodyContent">
        <p><b>Address: 2010 Hogback Rd #3, Ann Arbor, MI 48105 </b></p> 
        <p><b>Phone Number: +1(734)975-2500 </b><p>
        <p><b>Website: <a href="https://www.cancersupportannarbor.org/">https://www.cancersupportannarbor.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 37.93322, lng: -122.07271 },
    title: "Cancer Support Community San Francisco Bay Area",
    content: `
    <div id="content">
      <h3>Cancer Support Community San Francisco Bay Area</h3>
      <div id="bodyContent">
        <p><b>Address: 3276 McNutt Ave, Walnut Creek, CA 94597 </b></p> 
        <p><b>Phone Number: +1(925)933-0107 </b><p>
        <p><b>Website: <a href="http://www.cancersupport.net/">http://www.cancersupport.net</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 37.28286, lng: -107.87803 },
    title: "Cancer Support Community Southwest Colorado",
    content: `
    <div id="content">
      <h3>Cancer Support Community Southwest Colorado</h3>
      <div id="bodyContent">
        <p><b>Address: 1701 Main Ave Suite C, Durango, CO 81301 </b></p> 
        <p><b>Phone Number: +1(970)403-3711 </b><p>
        <p><b>Website: <a href="http://www.cancersupportswco.org/">http://www.cancersupportswco.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 40.72824, lng: -74.00382 },
    title: "Red Door Community formerly Gilda's Club NYC",
    content: `
    <div id="content">
      <h3>Red Door Community formerly Gilda's Club NYC</h3>
      <div id="bodyContent">
        <p><b>Address: 195 W Houston St, New York, NY 10014 </b></p> 
        <p><b>Phone Number: +1(212)647-9700 </b><p>
        <p><b>Website: <a href="http://www.reddoorcommunity.org/">http://www.reddoorcommunity.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 41.91841, lng: -87.64821 },
    title: "Imerman Angels",
    content: `
    <div id="content">
      <h3>Imerman Angels</h3>
      <div id="bodyContent">
        <p><b>Address: 2001 N Halsted St, Chicago, IL 60614 </b></p> 
        <p><b>Phone Number: +1(866)463-7626 </b><p>
        <p><b>Website: <a href="http://www.imermanangels.org/">http://www.imermanangels.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 41.87839, lng: -87.65227 },
    title: "National Ovarian Cancer Coalition",
    content: `
    <div id="content">
      <h3>National Ovarian Cancer Coalition</h3>
      <div id="bodyContent">
        <p><b>Address: 1436 W Randolph St #201, Chicago, IL 60607 </b></p> 
        <p><b>Phone Number: +1(312)226-9410 </b><p>
        <p><b>Website: <a href="https://ovarian.org/">https://ovarian.org/</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 47.67679, lng: -122.34985 },
    title: "Cancer Lifeline",
    content: `
    <div id="content">
      <h3>Cancer Lifeline</h3>
      <div id="bodyContent">
        <p><b>Address: 6522 Fremont Ave N, Seattle, WA 98103 </b></p> 
        <p><b>Phone Number: +1(206)297-2100 </b><p>
        <p><b>Website: <a href="https://www.cancerlifeline.org//">https://www.cancerlifeline.org</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 43.15213, lng: -77.59635 },
    title: "Cancer Support Community at Gilda's Club Rochester",
    content: `
    <div id="content">
      <h3>Cancer Support Community at Gilda's Club Rochester</h3>
      <div id="bodyContent">
        <p><b>Address: 255 Alexander St, Rochester, NY 14607 </b></p> 
        <p><b>Phone Number: +1(585)423-9700 </b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 33.03833, lng: -117.23865 },
    title: "Cancer Angels of San Diego",
    content: `
    <div id="content">
      <h3>Cancer Angels of San Diego</h3>
      <div id="bodyContent">
        <p><b>Address: 2240 Encinitas Blvd #D Box 327, Encinitas, CA </b></p> 
        <p><b>Phone Number: +1(585)423-9700 </b><p>
        <p><b>Website: <a href="http://www.cancerangelsofsandiego.org/contact">http://www.cancerangelsofsandiego.org/contact</a></b><p>
      </div>
    </div>
  `,
  },
  {
    position: { lat: 33.51959, lng: -117.16751 },
    title: "Michelle's Place Cancer Resource Center",
    content: `
    <div id="content">
      <h3>Michelle's Place Cancer Resource Center</h3>
      <div id="bodyContent">
        <p><b>Address: 41669 Winchester Rd Ste 101, Temecula, CA 92590 </b></p> 
        <p><b>Phone Number: +1(951)699-5455 </b><p>
        <p><b>Website: <a href="https://www.michellesplace.org/">https://www.michellesplace.org</a></b><p>
      </div>
    </div>
  `,
  },
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




