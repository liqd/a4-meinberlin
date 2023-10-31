import React from 'react'
import django from 'django'

const translated = {
  status: django.gettext('Status: ')
}

export const ListItemAmpel = props => {
  return (
    <div className="list-item__ampel">
      <strong>
        {translated.status}
      </strong>
      {props.badges.length > 1 && (
        <span>
          {props.badges[1]}
        </span>
      )}
    </div>
  )
}
