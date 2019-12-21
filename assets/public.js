// const mainMap = document.querySelector('#mainMap');
// mainMap.style.height = '700px';
// /operatorl

// var scheduled = document.querySelector('#scheduled');
// var reserved = document.querySelector('#reserved');
// scheduled.style.margin-top=reserved.style.margin-top+'px';

var HttpClient = function() {
  this.get = function(aUrl, aCallback) {
    var anHttpRequest = new XMLHttpRequest();
    anHttpRequest.onreadystatechange = function() {
      if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200) aCallback(anHttpRequest.responseText);
    };
    anHttpRequest.open('GET', aUrl, true);
    anHttpRequest.send(null);
  };
};

var theurl = 'https://ms.goyal.club/list'; //'https://api.exchangeratesapi.io/latest';//'http://api.ipinfodb.com/v3/ip-city/?key=9d64fcfdfacc213c7ddf4ef911dfe97b55e4696be3532bf8302876c09sadaad06b&format=json&ip=40.77.167.44';
// theurl
var client = new HttpClient();
client.get(theurl, function(response) {
  var response1 = JSON.parse(response);
  alert(response);
});
var parkingLots = [
  [28.61, 77.23],
  [28.65, 77.19]
];
var map = new MapmyIndia.Map('mainMap', { center: [28.61, 77.23], zoomControl: true, hybrid: true, search: true, location: true }); /*map initialized*/

map.setZoom(11);
for (var index = 0; index < parkingLots.length; index++) {
  var icon = L.divIcon({
    className: 'my-div-icon',
    // html:'<div class="popper">' + index+1 + '</div>',
    html: "<img class='popper'  src=" + "'https://maps.mapmyindia.com/images/2.png'>" + '<span class="my-div-span">' + (index + 1) + '</span>',
    iconSize: [10, 10],
    popupAnchor: [12, -10]
  });
  var mk = addMarker({
    position: parkingLots[index],
    title: 'hi',
    draggable: false,
    icon: icon
  });
}

function test() {
  document.getElementById('test').innerHTML = console.log(response);
}

function addMarker(req) {
  var mk = new L.marker(req.position, {
    draggable: req.draggable,
    icon: req.icon,
    title: req.title
  });
  mk.bindPopup(req.title);
  map.addLayer(mk);
  return mk;
}

map.on('click', function(e) {
  var pt = e.latlng;
  // console.log(pt);
  document.getElementById('test').innerHTML = pt;
  // var mk = new L.marker(pt, {title:"hi",draggable:true});
  // mk.bindPopup('YO');
  // //mk.addTo(map);
  // map.addLayer(mk);
  var icon = L.divIcon({
    className: 'my-div-icon',
    // html:'<div class="popper">' + index+1 + '</div>',
    html: "<img class='popper'  src=" + "'https://maps.mapmyindia.com/images/2.png'>" + '<span class="my-div-span">' + (index + 1) + '</span>',
    iconSize: [2, 10],
    popupAnchor: [12, -10]
  });
  var mk = addMarker({
    position: pt,
    draggable: false,
    icon: icon,
    title: 'Hi'
  });
});
