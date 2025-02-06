import React from 'react'
import django from 'django'
import { useParams } from 'react-router-dom'
import Kiezradar from './Kiezradar'
import { alert as Alert } from 'adhocracy4'

const editText = django.gettext('Edit')
const errorKiezText = django.gettext('Failed to fetch Kiez')
const errorText = django.gettext('Error')

export default function EditKiezradar ({ kiezradars, ...props }) {
  const { id } = useParams()
  const kiezradar = kiezradars?.find(
    (kiezradar) => kiezradar.id === parseInt(id, 10)
  )

  if (!kiezradar) {
    return (
      <div className="kiezradar__error">
        <Alert type="danger" message={errorText + ': ' + errorKiezText} />
      </div>
    )
  }

  return (
    <>
      <h2>{editText + ' ' + kiezradar.name}</h2>
      <Kiezradar {...props} kiezradar={kiezradar} />
    </>
  )
}
