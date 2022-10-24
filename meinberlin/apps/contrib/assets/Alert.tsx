import React from 'react'
import django from 'django'

interface AlertProps {
  type: string | undefined
  message: string
  onClick: () => void
}

const closeStr: string = django.gettext('Close')

export const Alert = ({
  type,
  message,
  onClick
}: AlertProps): JSX.Element | null => {
  if (type !== undefined && type !== '') {
    return (
      <div className={`alert alert--${type}`} role="alert">
        <div className="container">
          {message}
          <button
            className="alert__close"
            title={closeStr}
            onClick={onClick}
          >
            <i className="fa fa-times" aria-label={closeStr} />
          </button>
        </div>
      </div>
    )
  }

  return null
}
