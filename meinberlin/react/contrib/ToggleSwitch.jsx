import React from 'react'
import { classNames } from 'adhocracy4'

export const ToggleSwitch = ({
  onSwitchStr,
  uniqueId,
  toggleSwitch,
  defaultChecked,
  checked,
  className,
  labelLeft = true
}) => (
  <div className={classNames('toggle-switch form-check', className)}>
    {labelLeft && <label className="toggle-switch__label" htmlFor={uniqueId}>{onSwitchStr}</label>}
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
    {!labelLeft && <label className="toggle-switch__label toggle-switch__label--right" htmlFor={uniqueId}>{onSwitchStr}</label>}
  </div>
)
