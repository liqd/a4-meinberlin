/* global django */
import { renderToString } from 'react-dom/server'
import React, { Component } from 'react'
import { withCookies } from 'react-cookie'
import PopUp from './PopUp'
import { maps } from 'adhocracy4'
import 'leaflet.markercluster'

const addressSearchStr = django.gettext('Address search')
const addressSearchCapStr = django.gettext('Address Search')
const nothingStr = django.gettext('Nothing to show')
const closeInfoBoxStr = django.gettext('Close information box')
const projectsNotShownStr = django.gettext('Projects without spacial reference are not shown on the map. Please have a look at the project list.')

const L = window.L
const $ = window.$

const addressIcon = L.icon({
  iconUrl: '/static/images/address_search_marker.svg',
  shadowUrl: '/static/images/map_shadow_01.svg',
  iconSize: [30, 36],
  iconAnchor: [15, 36],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
})

const itemIcon = L.icon({
  iconUrl: '/static/images/map_pin_default.svg',
  shadowUrl: '/static/images/map_shadow_01.svg',
  iconSize: [30, 36],
  iconAnchor: [15, 36],
  shadowSize: [40, 54],
  shadowAnchor: [20, 54],
  zIndexOffset: 1000
})

const pointToLatLng = function (point) {
  if (point.geometry !== '') {
    return {
      lat: point.geometry.coordinates[1],
      lng: point.geometry.coordinates[0]
    }
  }
}

const apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'

class PlansMap extends Component {
  constructor (props) {
    super(props)

    const showInfoBox = !this.props.cookies.get('plansMapHideInfoBox')
    this.state = {
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      showInfoBox,
      showInfoBoxUser: showInfoBox,
      filters: {
        status: -1,
        participation: -1,
        district: -1
      }
    }
  }

  componentDidMount () {
    this.map = this.setupMap()
    this.addDistrictLayers(this.map)
    this.cluster = L.markerClusterGroup({
      showCoverageOnHover: false
    }).addTo(this.map)
    this.markers = this.addMarkers(this.cluster)
  }

  componentDidUpdate (prevProps) {
    if (prevProps.currentDistrict !== this.props.currentDistrict) {
      this.zoomToDistrict(this.props.currentDistrict)
      this.unsetLayerStyle(prevProps.currentDistrict)
    }
    this.cluster.clearLayers()
    this.markers = this.addMarkers(this.cluster)
  }

  componentWillUnmount () {
    if (this.map !== undefined) {
      this.map.remove()
    }
  }

  bindMap (element) {
    this.mapElement = element
  }

  setupMap () {
    const map = maps.createMap(L, this.mapElement, {
      attribution: this.props.attribution,
      baseUrl: this.props.baseurl,
      useVectorMap: this.props.useVectorMap,
      mapboxToken: this.props.mapboxToken,
      omtToken: this.props.omtToken,
      scrollWheelZoom: false,
      zoomControl: false,
      maxZoom: 18,
      dragging: this.props.draggingEnabled
    })
    new L.Control.Zoom({ position: this.props.zoomPosition }).addTo(map)
    return map
  }

  unsetLayerStyle (district) {
    if (district !== '-1' && district !== this.props.nonValue) {
      const layer = this.disctrictLayerLookup[district]
      layer.setStyle({ weight: 1 })
    }
  }

  zoomToDistrict (district) {
    if (district !== '-1' && district !== this.props.nonValue) {
      const layer = this.disctrictLayerLookup[district]
      this.map.fitBounds(layer.getBounds())
      layer.setStyle({ weight: 3 })
    } else {
      this.map.fitBounds(this.props.bounds)
    }
  }

  addDistrictLayers (map) {
    const districtStyle = {
      color: '#253276',
      weight: 1,
      opacity: 1,
      fillOpacity: 0
    }
    const districLayers = L.geoJSON(this.props.districts, { style: districtStyle }).addTo(map)
    const districtNames = this.props.districtnames
    this.disctrictLayerLookup = {}
    /* eslint-disable */
    districLayers.getLayers().map((layer, i) => {
      this.disctrictLayerLookup[districtNames[i].toString()] = layer
    })
    /* eslint-enable */
    this.zoomToDistrict(this.props.currentDistrict)
  }

  getTopicList (item) {
    const topicList = item.topics.map((val) => {
      return this.props.topicChoices[val]
    })
    return topicList
  }

  getPopUpContent (item) {
    return renderToString(
      <PopUp
        item={item}
        itemTopics={this.getTopicList(item)}
      />
    )
  }
  /* eslint-disable */
  addMarkers (cluster) {
    this.props.items.map((item, i) => {
      if (item.point !== '' && item.point.geometry) {
        const marker = L.marker(pointToLatLng(item.point), { icon: itemIcon })
        cluster.addLayer(marker)
        marker.bindPopup(this.getPopUpContent(item))
        return marker
      }
    })
  }
  /* eslint-enable */

  displayResults (geojson) {
    this.setState(
      {
        displayResults: true,
        showInfoBox: false,
        searchResults: geojson.features
      }
    )
  }

  displayErrorMessage () {
    this.setState(
      {
        displayError: true,
        showInfoBox: false
      }
    )
    setTimeout(function () {
      this.setState(
        {
          displayError: false,
          showInfoBox: this.state.showInfoBoxUser
        })
    }.bind(this), 2000)
  }

  displayAdressMarker (geojson) {
    if (this.state.address) {
      this.map.removeLayer(this.state.address)
    }
    const addressMarker = L.geoJSON(geojson, {
      pointToLayer: function (feature, latlng) {
        return L.marker(latlng, { icon: addressIcon })
      }
    }).addTo(this.map)
    this.map.flyToBounds(addressMarker.getBounds(), { maxZoom: 13 })
    this.setState(
      {
        address: addressMarker,
        showInfoBox: this.state.showInfoBoxUser
      }
    )
  }

  onAddressSearchSubmit (event) {
    event.preventDefault()
    const address = event.target[0].value
    $.ajax(apiUrl, {
      data: { address },
      context: this,
      success: function (geojson) {
        const count = geojson.count
        if (count === 0) {
          this.displayErrorMessage()
        } else if (count === 1) {
          this.displayAdressMarker(geojson)
        } else {
          this.displayResults(geojson)
        }
      }
    })
  }

  onAddressSearchChange (event) {
    if (event.target.value === '' && this.state.address) {
      this.map.removeLayer(this.state.address)
      this.setState({
        address: null
      })
    }
  }

  selectSearchResult (event) {
    const index = parseInt(event.target.value, 10)
    const address = this.state.searchResults[index]
    this.displayAdressMarker(address)
    this.setState(
      { displayResults: false }
    )
  }

  closeInfoBox () {
    this.setState(
      {
        showInfoBox: false,
        showInfoBoxUser: false
      }
    )
    this.props.cookies.set('plansMapHideInfoBox', 1, { path: '/' })
  }

  render () {
    return (
      <div className="map-list-combined__map" ref={this.bindMap.bind(this)}>
        <div className="map-list-combined__map__search">
          <form onSubmit={e => this.onAddressSearchSubmit(e)} data-embed-target="ignore">
            <div className="input-group">
              <label
                htmlFor="id-map-address-search"
                className="visually-hidden"
              >
                {addressSearchStr}
              </label>
              <input
                className="form-control"
                type="search"
                id="id-map-address-search"
                placeholder={addressSearchCapStr}
                onChange={e => this.onAddressSearchChange(e)}
              />
              <button
                className="btn btn--light input-group__after"
                type="submit"
              >
                <i className="fa fa-search" aria-hidden="true" />
                <span className="visually-hidden">
                  {addressSearchStr}
                </span>
              </button>
            </div>
            {this.state.displayResults &&
              <ul aria-labelledby="id_filter_address">
                {this.state.searchResults.map((name, i) => {
                  return (
                    <li key={i}>
                      <button
                        type="button"
                        value={i}
                        onClick={this.selectSearchResult.bind(this)}
                      >
                        {name.properties.strname} {name.properties.hsnr} in {name.properties.plz} {name.properties.bezirk_name}
                      </button>
                    </li>
                  )
                })}
              </ul>}

            {this.state.displayError &&
              <ul aria-labelledby="id_filter_address" className="map-list-combined__map__search__error">
                <li>{nothingStr}</li>
              </ul>}

          </form>
        </div>
        {this.state.showInfoBox &&
          <div className="map-infobox">
            <button className="infobox__close" id="close" aria-label={closeInfoBoxStr} onClick={this.closeInfoBox.bind(this)}><i className="fa fa-times" /></button>
            <i className="fa fa-info-circle" aria-hidden="true" /><span>{projectsNotShownStr}</span>
          </div>}
      </div>
    )
  }
}

export default withCookies(PlansMap)
