import django from 'django'
import React, { useState } from 'react'
import Modal from 'adhocracy4/adhocracy4/static/Modal'
import cookie from 'js-cookie'

const baseTranslations = {
  errorTitle: django.gettext('An error occured'),
  button: django.gettext('Remove')
}

const translationsPerType = {
  idea: {
    title: django.gettext('Delete Idea'),
    description: django.gettext('Do you really want to delete this idea?'),
    errorDescription: django.gettext('There has been an error trying to delete the idea. Please try again later.')
  },
  proposal: {
    errorDescription: django.gettext('There has been an error trying to delete the proposal. Please try again later.'),
    title: django.gettext('Delete Proposal'),
    description: django.gettext('Do you really want to delete this proposal?')
  }
}

const DeleteItemModal = ({
  apiUrl,
  successUrl,
  itemType
}) => {
  const [state, setState] = useState('idle')
  const translations = {
    ...baseTranslations,
    ...translationsPerType[itemType]
  }

  const partials = {}

  const submitDelete = async () => {
    try {
      const res = await fetch(apiUrl, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'X-CSRFToken': cookie.get('csrftoken')
        }
      })
      if (!res.ok) throw new Error()
      window.location.href = successUrl
    } catch (e) {
      setState('error')
    }
  }

  if (state === 'error') {
    partials.title = translations.errorTitle
    partials.description = translations.errorDescription
    partials.hideFooter = true
  } else {
    partials.title = translations.title
    partials.description = translations.description
  }

  return (
    <Modal
      partials={partials}
      handleSubmit={submitDelete}
      action={translations.button}
      keepOpenOnSubmit
      btnStyle="cta"
      toggle={translations.button}
    />
  )
}

export default DeleteItemModal
