import React, { Suspense, useState } from 'react'
import django from 'django'
import { useNavigate } from 'react-router-dom'
import { updateItem } from '../contrib/helpers'
import { alert as Alert } from 'adhocracy4'

const KiezradarMap = React.lazy(() => import('./KiezradarMap'))

const loadingMapText = django.gettext('Loading map...')
const nameYourKiezText = django.gettext('Name your Kiez selection')
const saveText = django.gettext('Save Kiez selection')
const savingText = django.gettext('Saving')
const errorText = django.gettext('Error')
const errorUpdateKiezText = django.gettext('Failed to update kiezradar filter')

const CENTRAL_BERLIN = [13.4050, 52.5200]
const MIN_RADIUS = 500
const MAX_RADIUS = 3000

const defaultPoint = {
  type: 'Feature',
  geometry: {
    type: 'Point',
    coordinates: CENTRAL_BERLIN
  }
}

export default function Kiezradar ({
  kiezradar,
  apiUrl,
  kiezradarFiltersUrl,
  limitExceeded,
  onKiezradarSave,
  ...props
}) {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [point, setPoint] = useState(kiezradar?.point ?? defaultPoint)
  const [radius, setRadius] = useState(kiezradar?.radius ?? MIN_RADIUS)

  const handleLocationChange = ({ point, radius }) => {
    setPoint(point)
    setRadius(radius)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const payload = {
        name: e.target.elements.name.value,
        point,
        radius
      }
      const url = apiUrl + (kiezradar ? kiezradar.id + '/' : '')
      const method = kiezradar ? 'PATCH' : 'POST'

      const response = await updateItem(payload, url, method)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(errorUpdateKiezText)
      }

      onKiezradarSave(data)
      navigate(kiezradarFiltersUrl)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const markerPosition = [...point.geometry.coordinates].reverse()

  return (
    <>
      {(error) && (
        <div className="kiezradar__error">
          <Alert
            type="danger"
            message={errorText + ': ' + error}
          />
        </div>
      )}
      <Suspense fallback={<div>{loadingMapText}</div>}>
        <KiezradarMap
          {...props}
          center={kiezradar ? markerPosition : null}
          position={markerPosition}
          radius={radius}
          minRadius={MIN_RADIUS}
          maxRadius={MAX_RADIUS}
          onChange={handleLocationChange}
        />
      </Suspense>
      <form className="form--base" onSubmit={handleSubmit}>
        <div className="form-group form-group form-group--inline fullspace align-bottom">
          <div className="form-group">
            <label htmlFor="name">{nameYourKiezText}*</label>
            <input
              id="name"
              name="name"
              type="text"
              defaultValue={kiezradar?.name}
              required
              autoComplete="organization"
            />
          </div>
          <div className="kiezradar__form-button">
            <button
              className="button"
              type="submit"
              disabled={loading || (!kiezradar && limitExceeded)}
            >
              {loading ? savingText + '...' : saveText}
            </button>
          </div>
        </div>
      </form>
    </>
  )
}
