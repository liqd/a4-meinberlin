import React from 'react'
import django from 'django'

const translations = {
  supportButtonDisabled: django.gettext('Support button inactive.'),
  support: django.pgettext('button text', 'Support'),
  supported: django.gettext('Supported')
}

const SupportButton = ({
  userRatingData,
  isReadOnly,
  clickHandler,
  isArchived
}) => {
  const getSupportClass = () => {
    if (isReadOnly || isArchived) {
      return 'button--proposal--read-only'
    }
    if (userRatingData.userHasRating) {
      return 'button--proposal--selected'
    }
  }

  const getSupportClickStr = () => {
    if (isReadOnly) {
      return translations.supportButtonDisabled
    }
  }

  return (
    <button
      className={'button button--fulltone button--light button--proposal ' + getSupportClass()}
      aria-disabled={isReadOnly}
      aria-pressed={userRatingData.userHasRating}
      disabled={isReadOnly || isArchived}
      onClick={() => clickHandler(userRatingData.userHasRating ? 0 : 1)}
      title={getSupportClickStr()}
    >
      {userRatingData.userHasRating ? translations.supported : translations.support}
      <i className="fas fa-hands-clapping" aria-hidden="true" />
    </button>
  )
}

export default SupportButton
