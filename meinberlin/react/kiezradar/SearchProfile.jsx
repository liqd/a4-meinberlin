import React, { useCallback, useState } from 'react'
import django from 'django'
import SearchProfileButtons from './SearchProfileButtons'
import { toFilterList, toSearchParams, updateItem } from '../contrib/helpers'
import PushNotificationToggle from './PushNotificationToggle'
import { alert as Alert } from 'adhocracy4'
import Modal from '../contrib/Modal'
import { validProjectStates } from '../projects/getDefaultState'

const renameSearchProfileText = django.gettext('Rename search profile')
const cancelText = django.gettext('Cancel')
const saveText = django.gettext('Save')
const savingText = django.gettext('Saving')
const deleteText = django.gettext('Remove')
const viewProjectsText = django.gettext('View projects')
const errorText = django.gettext('Error')
const errorDeleteSearchProfilesText = django.gettext(
  'Failed to delete search profile'
)
const errorUpdateSearchProfilesText = django.gettext(
  'Failed to update search profile'
)
const confirmDeletionText = (name) =>
  django.interpolate(
    django.gettext('Confirm deletion of %(name)s'),
    { name },
    true
  )
const confirmDeletionDescriptionText = django.gettext('You will no longer receive notifications about new participation projects with the selected filters.')

export default function SearchProfile ({ apiUrl, planListUrl, searchProfile, onSave, onDelete }) {
  const [isEditing, setIsEditing] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [deleteModal, setDeleteModal] = useState(null)

  const handleDelete = useCallback(async () => {
    setLoading(true)
    setError(null)

    try {
      const response = await updateItem({}, apiUrl + searchProfile.id + '/', 'DELETE')

      if (!response.ok) {
        throw new Error(errorDeleteSearchProfilesText)
      }

      onDelete(searchProfile)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [apiUrl, searchProfile, onDelete])

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await updateItem(
        { name: e.target.elements.name.value },
        apiUrl + searchProfile.id + '/',
        'PATCH'
      )

      if (!response.ok) {
        throw new Error(errorUpdateSearchProfilesText)
      }

      const data = await response.json()
      onSave(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsEditing(false)
      setLoading(false)
    }
  }, [apiUrl, searchProfile, onSave])

  const selection = toFilterList(searchProfile).map((names) => names.join(', '))

  return (
    <>
      {deleteModal?.searchProfile && (
        <Modal
          title={confirmDeletionText(deleteModal.searchProfile.name)}
          message={confirmDeletionDescriptionText}
          buttonText={deleteText}
          onConfirm={() => handleDelete()}
          onClose={() => setDeleteModal(null)}
        />
      )}
      <div className="search-profile">
        <div className="search-profile__header">
          <div>
            <h3 className="search-profile__title">{searchProfile.name}</h3>
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
                onDelete={() => setDeleteModal({ searchProfile })}
                loading={loading}
              />
            </div>
          )}
        </div>
        {error && <Alert type="danger" title={errorText} message={error} />}
        {isEditing && (
          <form className="form--base panel--heavy search-profile__form" onSubmit={handleSubmit}>
            <fieldset disabled={loading}>
              <div className="form-group">
                <label htmlFor="name">{renameSearchProfileText}</label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  defaultValue={searchProfile.name}
                  required
                />
              </div>
              <div className="form-actions">
                <div className="form-actions__left search-profile__form-cancel">
                  <button type="button" className="link" onClick={() => setIsEditing(false)}>
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
            </fieldset>
          </form>
        )}
        <div className="search-profile__footer">
          <PushNotificationToggle
            id={searchProfile.id}
            apiUrl={apiUrl}
            checked={searchProfile.notification}
            onError={(error) => setError(error)}
          />
          <a href={planListUrl + '?' + toQueryString(searchProfile)} className="button button--light search-profile__view-projects">
            {viewProjectsText}
          </a>
          {!isEditing && (
            <div className="search-profile__footer-buttons">
              <SearchProfileButtons
                onEdit={() => setIsEditing(true)}
                onDelete={() => setDeleteModal({ searchProfile })}
                loading={loading}
              />
            </div>
          )}
        </div>
      </div>
    </>
  )
}

function toQueryString (searchProfile) {
  return toSearchParams({
    'search-profile': searchProfile.id,
    search: searchProfile.query_text || undefined,
    districts: searchProfile.districts.map(district => district.name),
    organisation: searchProfile.organisations.map(organisation => organisation.name),
    participations: searchProfile.project_types.map(participation => participation.id),
    topics: searchProfile.topics.map((topic) => topic.code),
    plansOnly: searchProfile.plans_only,
    projectState: searchProfile.status.map(status => validProjectStates[status.status]),
    kiezradars: searchProfile.kiezradars.map(kiezradar => kiezradar.name)
  }).toString()
}
