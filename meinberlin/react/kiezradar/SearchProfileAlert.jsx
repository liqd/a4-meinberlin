import React from 'react'
import django from 'django'

const alertHeadlineText = django.gettext(
  'Search profile successfully deleted'
)
const alertText = django.gettext('Your changes have been deleted.')

export default function SearchProfileAlert ({ onClose }) {
  return (
    <div className="search-profile__alert">
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
  )
}
