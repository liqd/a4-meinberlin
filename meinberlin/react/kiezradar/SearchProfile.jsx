import React, { useState } from 'react'
import django from 'django'
import SearchProfileButtons from './SearchProfileButtons'
import { updateItem } from '../contrib/helpers'
import PushNotificationToggle from './PushNotificationToggle'

const renameSearchProfileText = django.gettext('Rename search profile')
const cancelText = django.gettext('Cancel')
const saveText = django.gettext('Save')
const savingText = django.gettext('Saving')
const viewProjectsText = django.gettext('View projects')
const plansText = django.gettext('Plans')
const errorText = django.gettext('Error')
const errorDeleteSearchProfilesText = django.gettext(
  'Failed to delete search profile'
)
const errorUpdateSearchProfilesText = django.gettext(
  'Failed to update search profile'
)
const statusNames = {
  running: django.gettext('ongoing'),
  future: django.gettext('upcoming'),
  done: django.gettext('done')
}

export default function SearchProfile ({ apiUrl, planListUrl, profile: profile_, onDelete }) {
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [profile, setProfile] = useState(profile_)

  const handleDelete = async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await updateItem({}, apiUrl + profile.id + '/', 'DELETE')

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
      const response = await updateItem({ name: e.target.elements.name.value }, apiUrl + profile.id + '/', 'PATCH')

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

  const filters = [
    profile.districts,
    profile.topics,
    profile.project_types,
    profile.status.map((status) => ({ name: statusNames[status.name] })),
    profile.organisations
  ]
    .map((filter) => filter.map(({ name }) => name))

  const selection = [
    [profile.query_text],
    ...filters,
    [profile.plans_only ? plansText : null]
  ]
    .map((names) => names.join(', '))
    .filter(Boolean)

  return (
    <div className="search-profile">
      <div className="search-profile__header">
        <div>
          <h3 className="search-profile__title">{profile.name}</h3>
          <ul className="search-profile__filters">
            {selection.map((filter) => (
              <li key={filter} className="search-profile__filter">{filter}</li>
            ))}
          </ul>
        </div>
        {!isEditing && (
          <div className="search-profile__header-buttons">
            <SearchProfileButtons
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
            <input
              id="name"
              name="name"
              type="text"
              defaultValue={profile.name}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault()
                  e.target.form.requestSubmit()
                }
              }}
              required
            />
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
        <PushNotificationToggle
          id={profile.id}
          apiUrl={apiUrl}
          checked={profile.notification}
          onError={(error) => setError(error)}
        />
        <a href={planListUrl + '?search-profile=' + profile.id} className="button button--light search-profile__view-projects">
          {viewProjectsText}
        </a>
        {!isEditing && (
          <div className="search-profile__footer-buttons">
            <SearchProfileButtons
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
