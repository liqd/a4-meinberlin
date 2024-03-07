import React from 'react'
import django from 'django'

const translated = {
  status: django.gettext('Status: '),
  ariaLabel: django.gettext('Status Indicator')
}

export const ModeratorStatus = ({ modStatus, modStatusDisplay }) => {
  if (!modStatus || !modStatusDisplay) {
    return null // Don't render the component if either prop is missing
  }

  const modTypeClass = 'moderator-status__label--' + modStatus.toLowerCase()

  return (
    <div className="moderator-status" aria-label={translated.ariaLabel}>
      <span className={'moderator-status__color-indicator ' + modTypeClass} aria-hidden="true" />
      <span>
        <strong>
          {translated.status}
        </strong>
        {modStatusDisplay.length > 1 && modStatusDisplay}
      </span>
    </div>
  )
}
