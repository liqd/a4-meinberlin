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
      <div className="save-search-profile">
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
      </div>
    )
  }

  if (searchProfile) {
    return (
      <div className="save-search-profile">
        <a className="save-search-profile__action save-search-profile__action--link" href="/account/search-profiles">
          {viewText}
        </a>
      </div>
    )
  }

  return (
    <div className="save-search-profile">
      <CreateSearchProfileButton {...props} searchProfilesCount={searchProfilesCount} />
    </div>
  )
}

function CreateSearchProfileButton ({
  districts,
  organisations,
  topicChoices,
  participationChoices,
  projectStatus,
  searchProfilesApiUrl,
  appliedFilters,
  searchProfilesCount,
  onSearchProfileCreate
}) {
  const { loading, limitExceeded, error, createSearchProfile } = useCreateSearchProfile({
    searchProfilesApiUrl,
    appliedFilters,
    districts,
    organisations,
    topicChoices,
    participationChoices,
    projectStatus,
    searchProfilesCount,
    onSearchProfileCreate
  })

  if (limitExceeded) {
    return <span className="save-search-profile__action">{limitText}</span>
  }

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
