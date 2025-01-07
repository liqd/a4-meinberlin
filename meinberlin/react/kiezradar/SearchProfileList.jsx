import React, { useState, useEffect } from 'react'
import django from 'django'
import Spinner from '../contrib/Spinner'
import SearchProfile from './SearchProfile'

const noSavedProfilesText = django.gettext('No saved search profiles')
const findProjectsText = django.gettext('Find projects')
const yourSavedProfilesText = django.gettext('Your saved search profiles')
const errorText = django.gettext('Error')
const errorSearchProfilesText = django.gettext(
  'Failed to fetch search profiles'
)

export default function SearchProfileList ({ apiUrl, planListUrl, onAlert }) {
  const [searchProfiles, setSearchProfiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchSearchProfiles = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(apiUrl)

        if (!response.ok) {
          throw new Error(errorSearchProfilesText)
        }

        const data = await response.json()
        setSearchProfiles(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchSearchProfiles()
  }, [])

  if (loading) {
    return <Spinner />
  }

  if (error) {
    return (
      <div className="search-profiles-list__error">
        {errorText}: {error}
      </div>
    )
  }

  return (
    <>
      <h2>{searchProfiles.length === 0 ? noSavedProfilesText : yourSavedProfilesText + ' ' + searchProfiles.length}</h2>
      {searchProfiles.length === 0
        ? (
          <a href={planListUrl} className="button button--light">
            <i className="fa-solid fa-magnifying-glass mr-1" />
            {findProjectsText}
          </a>
          )
        : (
            searchProfiles.map((profile) => (
              <SearchProfile
                key={profile.id}
                apiUrl={apiUrl}
                planListUrl={planListUrl}
                profile={profile}
                onDelete={(id) => {
                  onAlert()
                  setSearchProfiles((prevSearchProfiles) =>
                    prevSearchProfiles.filter((profile) => profile.id !== id)
                  )
                }}
              />
            ))
          )}
    </>
  )
}
