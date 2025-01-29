import React from 'react'
import django from 'django'
import Kiezradar from './Kiezradar'

const newKiezText = django.gettext('New Kiezradar')

export default function NewKiezradar (props) {
  return (
    <>
      <h2>{newKiezText}</h2>
      <Kiezradar {...props} />
    </>
  )
}
