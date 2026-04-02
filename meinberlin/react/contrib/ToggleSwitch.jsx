import React from 'react'
import { classNames } from 'adhocracy4'

export const ToggleSwitch = ({
  switchStr,
  uniqueId,
  toggleSwitch,
  defaultChecked,
  checked,
  className,
  labelLeft = true,
  size = 'large',
  ariaLabelledBy
}) => (
  <div className={classNames('toggle-switch form-check', className)}>
    {labelLeft && switchStr && !ariaLabelledBy && <label className="toggle-switch__label" htmlFor={uniqueId}>{switchStr}</label>}
    <input
      type="checkbox"
      name={uniqueId}
      id={uniqueId}
      className="toggle-switch__input"
      onChange={toggleSwitch}
      defaultChecked={defaultChecked}
      checked={checked}
      aria-labelledby={ariaLabelledBy || (labelLeft && switchStr ? undefined : uniqueId + '-label')}
    />
    <span className={classNames('toggle-switch__display', size === 'small' && 'toggle-switch__display--small')} hidden>
      <i className="bicon bicon-check toggle-switch__icon toggle-switch__icon--on" aria-hidden="true" />
      <i className="bicon bicon-times toggle-switch__icon toggle-switch__icon--off" aria-hidden="true" />
    </span>
    {!labelLeft && !ariaLabelledBy && switchStr && (
      <label id={uniqueId + '-label'} className={classNames('toggle-switch__label', size !== 'small' && 'toggle-switch__label--right', size === 'small' && 'toggle-switch__label--small')} htmlFor={uniqueId}>{switchStr}</label>
    )}
  </div>
)
