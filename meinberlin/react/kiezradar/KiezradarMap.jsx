import L from 'leaflet'
import React, { useRef } from 'react'
import { createPortal } from 'react-dom'
import django from 'django'
import { Circle, MapContainer, Marker, useMap, useMapEvents, ZoomControl } from 'react-leaflet'
import { AddressSearch } from 'adhocracy4'
import ControlWrapper from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/ControlWrapper'
import MaplibreGlLayer from 'adhocracy4/adhocracy4/maps_react/static/a4maps_react/MaplibreGlLayer'

const chooseYourRadiusText = django.gettext('Choose your radius')

export default function KiezradarMap ({
  position,
  radius,
  minRadius,
  maxRadius,
  onChange,
  ...mapProps
}) {
  const handleRadiusChange = ({ point, radius }) => {
    onChange({ point, radius })
  }

  const handleAddressChange = (point) => {
    onChange({ point, radius })
  }

  return (
    <>
      <div className="kiezradar__map">
        <div id="mobile-controls" />
        <MapContainer
          zoom={13}
          zoomControl={false}
          center={mapProps.center}
          bounds={mapProps.bounds}
          maxZoom={18}
          style={{ height: '500px', width: '100%' }}
        >
          <MaplibreGlLayer
            attribution={mapProps.attribution}
            baseUrl={mapProps.baseUrl}
            omtToken={mapProps.omtToken}
          />
          <Radius
            position={position}
            radius={radius}
            minRadius={minRadius}
            maxRadius={maxRadius}
            onChange={handleRadiusChange}
          />
          <Search onChange={handleAddressChange} />
          <ZoomControl position="topleft" />
        </MapContainer>
      </div>
    </>
  )
}

function Radius ({
  position,
  radius,
  minRadius,
  maxRadius,
  onChange
}) {
  const markerRef = useRef(null)
  const isTouchDevice = window.matchMedia('(pointer: coarse)').matches

  useMapEvents({
    click: (e) => {
      if (isTouchDevice) {
        onChange({
          point: {
            type: 'Feature',
            geometry: {
              type: 'Point',
              coordinates: [e.latlng.lng, e.latlng.lat]
            }
          },
          radius
        })
      }
    }
  })

  const radiusControls = (
    <RadiusControls
      radius={radius}
      minRadius={minRadius}
      maxRadius={maxRadius}
      onChange={(radius) => {
        const marker = markerRef.current
        if (marker != null) {
          onChange({ point: marker.toGeoJSON(), radius })
        }
      }}
    />
  )

  return (
    <>
      <ControlWrapper position="topright">
        <div className="kiezradar__controls--tablet">{radiusControls}</div>
        {createPortal(
          <div className="kiezradar__controls--mobile">{radiusControls}</div>,
          document.getElementById('mobile-controls')
        )}
      </ControlWrapper>
      <Marker
        icon={L.icon({
          iconUrl: '/static/images/map_pin_kiezradar.svg',
          iconSize: [48, 48],
          iconAnchor: [24, 48]
        })}
        draggable
        eventHandlers={{
          dragend: () => {
            const marker = markerRef.current
            if (marker != null) {
              onChange({ point: marker.toGeoJSON(), radius })
            }
          }
        }}
        position={{
          lat: position[0],
          lng: position[1]
        }}
        ref={markerRef}
      />
      <Circle center={position} color="#00A982" radius={radius} />
    </>
  )
}

function RadiusControls ({ minRadius, maxRadius, radius, onChange }) {
  const rangeValue = ((radius - minRadius) / (maxRadius - minRadius)) * 100
  const rangeBackgroundStyle = {
    background: 'linear-gradient(90deg, #00a982 0, #00a982 ' + rangeValue + '%, #CCC ' + (rangeValue + 0.1) + '%)'
  }

  const handleChange = (e) => {
    const newRangeValue = parseFloat(e.target.value)
    const newRadius = minRadius + (newRangeValue / 100) * (maxRadius - minRadius)
    onChange(newRadius)
  }

  return (
    <div className="kiezradar__radius-controls">
      <div className="kiezradar__radius-info">
        <label className="kiezradar__radius-label" htmlFor="radius">
          {chooseYourRadiusText}
        </label>
        <div className="kiezradar__radius-measurement">
          {(radius / 1000).toLocaleString('de-DE', {
            minimumFractionDigits: 1,
            maximumFractionDigits: 1
          })}
          km
        </div>
      </div>
      <input
        className="kiezradar__range-slider"
        style={rangeBackgroundStyle}
        type="range"
        min="0"
        max="100"
        value={rangeValue}
        onChange={handleChange}
      />
    </div>
  )
}

function Search ({ onChange }) {
  const map = useMap()

  const handleAddressChange = (point) => {
    const [lat, lng] = [...point.geometry.coordinates].reverse()
    map.flyTo({ lat, lng }, 13)
    onChange(point)
  }

  return (
    <ControlWrapper position="topleft" className="kiezradar__map-search">
      <AddressSearch
        apiUrl="https://bplan-prod.liqd.net/api/addresses/"
        onSelectAddress={handleAddressChange}
      />
    </ControlWrapper>
  )
}
