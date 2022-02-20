let map;

 function initMap() {
     var myLatlong = new google.maps.LatLng(53.65914, 0.072050);

     var mapOptions = {
         zoom: 18,
         center: myLatlong,
         mapTypeId: google.maps.MapTypeId.ROADMAP
     };

     var map = new google.maps.Map(document.getElementById('map'),
     mapOptions);

     var mapDiv = document.getElementById('map').getElementsByTagName('div')[0];
	mapDiv.appendChild(document.getElementById("HamburgerMenu"));


     if (navigator.geolocation) {
         navigator.geolocation.getCurrentPosition(function (position) {
             initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
             map.setCenter(initialLocation);
         });
     }

 }
