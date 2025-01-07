import React, { useState } from 'react'
import django from 'django'
import SearchProfileList from './SearchProfileList'
import SearchProfileAlert from './SearchProfileAlert'

const titleText = django.gettext('Search Profiles')
const descriptionText = django.gettext(
  'In this area you manage your search profiles.'
)

export default function SearchProfiles (props) {
  const [alert, setAlert] = useState(false)

  return (
    <>
      {alert && <SearchProfileAlert onClose={() => setAlert(false)} />}
      <h1>{titleText}</h1>
      <p>{descriptionText}</p>
      <SearchProfileList {...props} onAlert={() => setAlert(true)} />
    </>
  )
}
