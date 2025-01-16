import React from 'react'
import django from 'django'
import { useCreateSearchProfile } from '../kiezradar/use-create-search-profile'

const loginText = django.gettext('Login to save search profiles')
const viewText = django.gettext('View search profiles')
const limitText = django.gettext('You can only create 10 search profiles.')
const saveText = django.gettext('Save search profile')
const savingText = django.gettext('Saving')

export default function SaveSearchProfile ({
  isAuthenticated,
  searchProfile,
  searchProfilesCount,
  ...props
}) {
  if (!isAuthenticated) {
    return (
      <a
        className="save-search-profile__action save-search-profile__action--link"
        href={
          '/accounts/login/?next=' +
          window.location.pathname +
          window.location.search
        }
      >
        <Icon />
        {loginText}
      </a>
    )
  }

  if (searchProfilesCount > 10) {
    return <span className="save-search-profile__action">{limitText}</span>
  }

  if (searchProfile) {
    return (
      <a className="save-search-profile__action save-search-profile__action--link" href="/account/search-profiles">
        {viewText}
      </a>
    )
  }

  return <CreateSearchProfileButton {...props} />
}

function CreateSearchProfileButton ({
  districts,
  organisations,
  topicChoices,
  participationChoices,
  projectStatus,
  searchProfilesApiUrl,
  appliedFilters,
  onSearchProfileCreate
}) {
  const { loading, error, createSearchProfile } = useCreateSearchProfile({
    searchProfilesApiUrl,
    appliedFilters,
    districts,
    organisations,
    topicChoices,
    participationChoices,
    projectStatus,
    onSearchProfileCreate
  })

  if (error) {
    return <span className="save-search-profile__error">{error}</span>
  }

  return (
    <button
      className="save-search-profile__action save-search-profile__action--button"
      type="button"
      onClick={createSearchProfile}
      disabled={loading}
    >
      {loading ? savingText + '...' : <><Icon />{saveText}</>}
    </button>
  )
}

function Icon () {
  return <i className="fa-solid fa-heart mr-1" aria-hidden="true" />
}
