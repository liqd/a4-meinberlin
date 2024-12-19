import cookie from 'js-cookie'
import React, { useState, useEffect } from 'react'
import django from 'django'
import Spinner from '../contrib/Spinner'

const titleText = django.gettext('Search Profiles')
const descriptionText = django.gettext(
  'In this area you manage your search profiles.'
)
const noSavedProfilesText = django.gettext('No saved search profiles')
const findProjectsText = django.gettext('Find projects')
const yourSavedProfilesText = django.gettext('Your saved search profiles')
const renameText = django.gettext('Rename')
const deleteText = django.gettext('Delete')
const renameSearchProfileText = django.gettext('Rename search profile')
const cancelText = django.gettext('Cancel')
const saveText = django.gettext('Save')
const savingText = django.gettext('Saving')
const viewProjectsText = django.gettext('View projects')
const errorText = django.gettext('Error')
const errorSearchProfilesText = django.gettext(
  'Failed to fetch search profiles'
)
const errorDeleteSearchProfilesText = django.gettext(
  'Failed to delete search profile'
)
const errorUpdateSearchProfilesText = django.gettext(
  'Failed to update search profile'
)
const alertHeadlineText = django.gettext(
  'Search profile successfully deleted'
)
const alertText = django.gettext(
  'Your changes have been deleted.'
)

export default function SearchProfiles (props) {
  return (
    <>
      <h1>{titleText}</h1>
      <p>{descriptionText}</p>
      <SearchProfileList {...props} />
    </>
  )
}

function SearchProfileList ({ apiUrl, planListUrl }) {
  const [alert, setAlert] = useState(false)
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
      {alert && <Alert onClose={() => setAlert(false)} />}
      {searchProfiles.length === 0
        ? (
          <>
            <h2 className="search-profiles-list__title">{noSavedProfilesText}</h2>
            <a href={planListUrl} className="button button--light">
              <i className="fa-solid fa-magnifying-glass mr-1" />
              {findProjectsText}
            </a>
          </>
          )
        : (
          <>
            <h2 className="search-profiles-list__title">
              {yourSavedProfilesText} ({searchProfiles.length})
            </h2>
            {searchProfiles.map((profile) => (
              <SearchProfile
                key={profile.id}
                apiUrl={apiUrl}
                planListUrl={planListUrl}
                profile={profile}
                onDelete={(id) => {
                  setAlert(true)
                  setSearchProfiles((prevSearchProfiles) =>
                    prevSearchProfiles.filter((profile) => profile.id !== id)
                  )
                }}
              />
            ))}
          </>
          )}
    </>
  )
}

function SearchProfile ({ apiUrl, planListUrl, profile: profile_, onDelete }) {
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [profile, setProfile] = useState(profile_)

  const handleDelete = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(apiUrl + profile.id + '/', {
        headers: {
          'X-CSRFToken': cookie.get('csrftoken')
        },
        method: 'DELETE'
      })

      if (!response.ok) {
        throw new Error(errorDeleteSearchProfilesText)
      }

      onDelete(profile.id)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(apiUrl + profile.id + '/', {
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'X-CSRFToken': cookie.get('csrftoken')
        },
        method: 'PATCH',
        body: JSON.stringify({ name: e.target.elements.name.value })
      })

      if (!response.ok) {
        throw new Error(errorUpdateSearchProfilesText)
      }

      const data = await response.json()
      setProfile(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsEditing(false)
      setLoading(false)
    }
  }

  return (
    <div className="search-profile">
      <div className="search-profile__header">
        <h3 className="search-profile__title">{profile.name}</h3>
        {!isEditing && (
          <div className="search-profile__header-buttons">
            <Buttons
              onEdit={() => setIsEditing(true)}
              onDelete={handleDelete}
              loading={loading}
            />
          </div>
        )}
      </div>
      {error && <div className="search-profile__error">{errorText + ': ' + error}</div>}
      {isEditing && (
        <form className="form--base panel--heavy search-profile__form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">{renameSearchProfileText}</label>
            <input id="name" name="name" type="text" required />
          </div>
          <div className="form-actions">
            <div className="form-actions__left">
              <button className="link" onClick={() => setIsEditing(false)}>
                {cancelText}
              </button>
            </div>
            <div className="form-actions__right">
              <button
                className="button"
                type="submit"
                disabled={loading}
              >
                {loading ? savingText + '...' : saveText}
              </button>
            </div>
          </div>
        </form>
      )}
      <div className="search-profile__footer">
        <a href={planListUrl + '?search-profile=' + profile.id} className="button button--light search-profile__view-projects">
          {viewProjectsText}
        </a>
        {!isEditing && (
          <div className="search-profile__footer-buttons">
            <Buttons
              onEdit={() => setIsEditing(true)}
              onDelete={handleDelete}
              loading={loading}
            />
          </div>
        )}
      </div>
    </div>
  )
}

function Buttons ({ onEdit, onDelete, loading }) {
  return (
    <div className="search-profile__buttons">
      <button
        className="search-profile__button"
        onClick={onEdit}
      >
        <i className="fa-solid fa-pencil mr-1" />
        {renameText}
      </button>
      <button
        className="search-profile__button"
        onClick={onDelete}
        disabled={loading}
      >
        <i className="fa-classic fa-regular fa-trash-can mr-1" />
        {deleteText}
      </button>
    </div>
  )
}

function Alert ({ onClose }) {
  return (
    <div className="search-profile__alert">
      <div className="search-profile__alert-container">
        <div
          className="alert alert--success"
          role="alert"
          aria-live="polite"
          aria-atomic="true"
        >
          <div className="alert__content">
            <h3 className="alert__headline">
              {alertHeadlineText}
            </h3>
            <p className="alert__text">
              {alertText}
            </p>
            <button
              type="button"
              className="alert__close"
              onClick={onClose}
              aria-label="Close"
            >
              <i className="fa fa-times" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
