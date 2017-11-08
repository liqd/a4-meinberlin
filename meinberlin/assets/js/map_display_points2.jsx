var $ = require('jquery')
var L = window.L

var icon = L.icon({
  iconUrl: '/static/images/map_pin_01_2x.png',
  shadowUrl: '/static/images/map_shadow_01_2x.png',
  iconSize: [30, 45],
  iconAnchor: [15, 45],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54]
})

var activeIcon = L.icon({
  iconUrl: '/static/images/map_pin_active_01_2x.png',
  shadowUrl: '/static/images/map_shadow_01_2x.png',
  iconSize: [30, 45],
  iconAnchor: [15, 45],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54]
})

var createMap = function (element, baseurl, attribution, polygon) {
  var basemap = baseurl + '{z}/{x}/{y}.png'
  var baselayer = L.tileLayer(basemap, { attribution: attribution })
  var map = new L.Map(element, { scrollWheelZoom: false })
  baselayer.addTo(map)

  var polygonStyle = {
    'color': '#0076ae',
    'weight': 2,
    'opacity': 1,
    'fillOpacity': 0.2
  }

  var basePolygon = L.geoJson(polygon, {style: polygonStyle}).addTo(map)
  basePolygon.on('dblclick', function (event) {
    map.zoomIn()
  })

  map.fitBounds(basePolygon.getBounds())
  map.options.minZoom = map.getZoom()

  return map
}

$(function () {
  var $wrapper = $('.map-list')
  var $map = $wrapper.find('[data-map="display_points"]')
  var $list = $wrapper.find('.map-list__list')

  $map.addClass('map-list__map')

  var polygon = JSON.parse($map[0].getAttribute('data-polygon'))
  var points = JSON.parse($map[0].getAttribute('data-points'))
  var baseurl = $map.attr('data-baseurl')
  var attribution = $map.attr('data-attribution')

  var map = createMap($map[0], baseurl, attribution, polygon)

  var markers = []

  $list.children().each(function (i, el) {
    var point = points.features[i].geometry.coordinates
    var marker = L.marker({lng: point[0], lat: point[1]}, {icon: icon}).addTo(map)
    markers.push(marker)

    marker.on('click', function () {
      $list.children().each(function (j, point) {
        if (i === j) {
          $(point).addClass('is-selected')
          $(point).scrollintoview()
          markers[j].setIcon(activeIcon)
        } else {
          $(point).removeClass('is-selected')
          markers[j].setIcon(icon)
        }
      })
    })
  })
})
