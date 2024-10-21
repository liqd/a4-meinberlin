import React from 'react'
import { classNames } from './helpers'

export const ToggleSwitch = ({
  onSwitchStr,
  uniqueId,
  toggleSwitch,
  defaultChecked,
  checked,
  className
}) => (
  <div className={classNames('toggle-switch form-check', className)}>
    <label className="toggle-switch__label" htmlFor={uniqueId}>{onSwitchStr}</label>
    <input
      type="checkbox"
      name={uniqueId}
      id={uniqueId}
      className="toggle-switch__input"
      onChange={toggleSwitch}
      defaultChecked={defaultChecked}
      checked={checked}
    />
    <span className="toggle-switch__display" hidden>
      <i className="bicon bicon-check toggle-switch__icon toggle-switch__icon--on" aria-hidden="true" />
      <i className="bicon bicon-times toggle-switch__icon toggle-switch__icon--off" aria-hidden="true" />
    </span>
  </div>
)
