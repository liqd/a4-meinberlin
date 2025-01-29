import React, { useEffect, useState } from 'react'
import django from 'django'
import { useParams } from 'react-router-dom'
import Kiezradar from './Kiezradar'
import Loading from './Loading'
import { alert as Alert } from 'adhocracy4'

const editText = django.gettext('Edit')
const errorKiezText = django.gettext('Failed to fetch Kiez')
const errorText = django.gettext('Error')

export default function EditKiezradar (props) {
  const { id } = useParams()
  const [kiezradar, setKiezradar] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchKiezradar = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(props.apiUrl + id)

        if (!response.ok) {
          throw new Error(errorKiezText)
        }

        const data = await response.json()
        setKiezradar(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchKiezradar()
  }, [])

  return (
    <div aria-live="polite">
      {loading
        ? <Loading />
        : error
          ? (
            <div className="kiezradar__error">
              <Alert type="danger" message={errorText + ': ' + error} />
            </div>
            )
          : (
            <>
              <h2>{editText + ' ' + kiezradar.name}</h2>
              <Kiezradar {...props} kiezradar={kiezradar} />
            </>
            )}
    </div>
  )
}
