import React, { useEffect, useState } from 'react'
import django from 'django'
import Loading from './Loading'
import { alert as Alert } from 'adhocracy4'
import SearchProfile from './SearchProfile'

const titleText = django.gettext('Search Profiles')
const descriptionText = django.gettext(
  'In this area you manage your search profiles.'
)
const errorText = django.gettext('Error')
const errorSearchProfilesText = django.gettext(
  'Failed to fetch search profiles'
)
const searchProfileDeletedTitle = (name) => django.interpolate(
  django.gettext('%(name)s has been deleted successfully'),
  { name },
  true
)
const searchProfileDeletedText = django.gettext(
  'You will no longer receive notifications about projects that correspond to the filters of this Saved Search.'
)

const findProjectsText = django.gettext('Find projects')
const limitExceededTitle = django.gettext('You have reached the limit of saved search profiles')
const limitExceededText = django.gettext('You are using the maximum number of 10 search profiles. To save a new one, you must delete an existing profile.')

export default function SearchProfiles (props) {
  const [loading, setLoading] = useState(false)
  const [searchProfiles, setSearchProfiles] = useState([])
  const [error, setError] = useState(null)
  const [alert, setAlert] = useState(null)

  useEffect(() => {
    const fetchSearchProfiles = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(props.apiUrl)

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

  const handleAlert = ({ title, message }) => {
    setAlert({ title, message })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const limitExceeded = searchProfiles.length === 10

  return (
    <>
      {limitExceeded && (
        <Alert
          title={limitExceededTitle}
          message={limitExceededText}
        />
      )}
      {error && (
        <Alert
          type="danger"
          title={errorText}
          message={error}
          onClick={() => setError(null)}
        />
      )}
      {alert && (
        <Alert
          type="success"
          title={alert.title}
          message={alert.message}
          onClick={() => setAlert(null)}
        />
      )}
      <h1>
        {titleText}
      </h1>
      <p>{descriptionText}</p>
      <div aria-live="polite">
        {loading
          ? <Loading />
          : (
              searchProfiles.length === 0
                ? (
                  <a href={props.planListUrl} className="button button--light">
                    <i className="fa-solid fa-magnifying-glass mr-1" />
                    {findProjectsText}
                  </a>
                  )
                : (
                    searchProfiles.map((searchProfile) => (
                      <SearchProfile
                        key={searchProfile.id}
                        apiUrl={props.apiUrl}
                        planListUrl={props.planListUrl}
                        searchProfile={searchProfile}
                        onSave={(searchProfile) =>
                          setSearchProfiles((prevSearchProfiles) =>
                            prevSearchProfiles.map((previousSearchProfile) =>
                              previousSearchProfile.id === searchProfile.id
                                ? searchProfile
                                : previousSearchProfile
                            )
                          )}
                        onDelete={(searchProfile) => {
                          setSearchProfiles((prevSearchProfiles) =>
                            prevSearchProfiles.filter(
                              (profile) => profile.id !== searchProfile.id
                            )
                          )

                          handleAlert({
                            title: searchProfileDeletedTitle(searchProfile.name),
                            message: searchProfileDeletedText
                          })
                        }}
                      />
                    ))
                  )
            )}
      </div>
    </>
  )
}
