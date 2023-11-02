import React from 'react'
import django from 'django'

const translated = {
  status: django.gettext('Status: '),
  ariaLabel: django.gettext('Status Indicator')
}

export const ModeratorStatus = ({ badges }) => {
  const [, modStatus, modType] = badges
  const modTypeClass = 'label--' + modType.toLowerCase()

  return (
    <div className="moderator-status" aria-label={translated.ariaLabel}>
      <span className={'moderator-status__color-indicator ' + modTypeClass} aria-hidden="true" />
      <span>
        <strong>
          {translated.status}
        </strong>
        {badges.length > 1 && modStatus}
      </span>
    </div>
  )
}
