import React from 'react'

export const IconSwitch = ({ buttons, viewModeStr, fullWidth }) => (
  <div className={'icon-switch' + (fullWidth ? ' icon-switch--full-width' : '')}>
    <span className="text--strong">{viewModeStr}</span>
    <div className="icon-switch__group" role="group">
      {buttons.map((button) => (
        <button
          className={'button button--light' + (button.isActive ? ' button--fulltone' : '')}
          onClick={button.handleClick}
          aria-label={button.ariaLabel}
          aria-pressed={button.isActive ? 'true' : 'false'}
          key={button.id}
        >
          <span className={button.icon + ' mr-1'} aria-hidden="true" />
          {button.label}
        </button>
      ))}
    </div>
  </div>
)
