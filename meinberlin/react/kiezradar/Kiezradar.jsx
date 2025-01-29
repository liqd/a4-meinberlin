import React, { Suspense, useState } from 'react'
import django from 'django'
import { useNavigate } from 'react-router-dom'
import { updateItem } from '../contrib/helpers'
import { alert as Alert } from 'adhocracy4'

const KiezradarMap = React.lazy(() => import('./KiezradarMap'))

const nameYourKiezText = django.gettext('Name your Kiez selection')
const saveText = django.gettext('Save Kiez selection')
const savingText = django.gettext('Saving')
const errorText = django.gettext('Error')
const errorLimitedExceededText = django.gettext(
  'Users can only have up to 5 kiezradar filters. Delete a filter to create a new one.'
)
const errorUpdateKiezText = django.gettext('Failed to update kiezradar filter')

export default function Kiezradar ({ kiezradar, ...props }) {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [limitExceeded, setLimitExceeded] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const payload = {
        name: e.target.elements.name.value,
        radius: e.target.elements.radius.value
      }
      const url = props.apiUrl + (kiezradar ? kiezradar.id + '/' : '')
      const method = kiezradar ? 'PATCH' : 'POST'

      const response = await updateItem(payload, url, method)
      const data = await response.json()

      if (data.non_field_errors) {
        setLimitExceeded(true)
        throw new Error(errorLimitedExceededText)
      }

      if (!response.ok) {
        throw new Error(errorUpdateKiezText)
      }

      navigate(props.kiezradarFiltersUrl)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

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
      <Suspense fallback={<div>Loading map...</div>}>
        <KiezradarMap />
      </Suspense>
      <form className="form--base" onSubmit={handleSubmit}>
        <input name="radius" type="hidden" value={kiezradar?.radius ?? 500.0} />
        <div className="form-group form-group form-group--inline fullspace align-bottom">
          <div className="form-group">
            <label htmlFor="name">{nameYourKiezText}*</label>
            <input
              id="name"
              name="name"
              type="text"
              defaultValue={kiezradar?.name}
              required
            />
          </div>
          <div className="kiezradar__form-button">
            <button
              className="button"
              type="submit"
              disabled={loading || limitExceeded}
            >
              {loading ? savingText + '...' : saveText}
            </button>
          </div>
        </div>
      </form>
    </>
  )
}
