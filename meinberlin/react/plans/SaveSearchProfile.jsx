import React, { useState } from 'react'
import django from 'django'
import { useCreateSearchProfile } from '../kiezradar/use-create-search-profile'
import Modal from '../contrib/Modal'
import { alert as Alert } from 'adhocracy4'
import { useSearchParams } from 'react-router-dom'

const modalTitleText = django.gettext('Login or register to save a search profile')
const modalMessageText = django.gettext('To save your search profile and access it later, please log in or create an account.')
const modalButtonText = django.gettext('Continue to login')
const alertTitleText = django.gettext('Please note, your current selection won’t be saved automatically')
const alertMessageText = django.gettext('After logging in, you can create and save a new search profile.')
const viewText = django.gettext('View search profiles')
const limitText = django.gettext('You can only create 10 search profiles.')
const saveText = django.gettext('Save search profile')
const savingText = django.gettext('Saving')

export default function SaveSearchProfile ({
  isAuthenticated,
  searchProfile,
  ...props
}) {
  const [searchParams] = useSearchParams()
  const [modal, setModal] = useState(false)

  if (!isAuthenticated) {
    return (
      <>
        {modal && (
          <Modal
            title={modalTitleText}
            message={modalMessageText}
            buttonText={modalButtonText}
            onConfirm={() => {
              const nextUrl = window.location.pathname + '?' + searchParams.toString()
              const encodedNext = encodeURIComponent(nextUrl)
              window.location = '/accounts/login/?next=' + encodedNext
              setModal(false)
            }}
            onClose={() => setModal(false)}
          >
            <Alert
              title={alertTitleText}
              message={alertMessageText}
            />
          </Modal>
        )}
        <div className="save-search-profile">
          <button
            className="save-search-profile__action save-search-profile__action--button"
            type="button"
            onClick={() => setModal(!modal)}
            aria-haspopup="dialog"
            aria-expanded={modal}
          >
            <Icon />
            {saveText}
          </button>
        </div>
      </>
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
      <CreateSearchProfileButton {...props} />
    </div>
  )
}

function CreateSearchProfileButton ({
  districts,
  organisations,
  topicChoices,
  participationChoices,
  projectStatus,
  kiezradars,
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
    kiezradars,
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
