import React from 'react'
import django from 'django'

const translated = {
  status: django.gettext('Status: ')
}

export const ListItemAmpel = ({ badges }) => {
  const [, , modType] = badges // Destructuring to get the third element
  const modTypeClass = 'label--' + modType.toLowerCase()

  return (
    <div className="list-item__ampel">
      <span className={'list-item__ampel-indicator ' + modTypeClass} />
      <span>
        <strong>
          {translated.status}
        </strong>
        {badges.length > 1 && (badges[1])}
      </span>
    </div>
  )
}
