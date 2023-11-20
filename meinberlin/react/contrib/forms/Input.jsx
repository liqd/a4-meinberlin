import React from 'react'
// FIXME: remove if not needed anymore
export const Input = ({ label, id, before, children, className, ...rest }) => {
  const classNames = [
    'form-control input__element',
    before && 'input__element--before',
    className,
    children && 'input__element--after'
  ].filter(Boolean).join(' ')

  return (
    <div className="form-group">
      <label htmlFor={id} className="form-label">
        {label}
      </label>
      <div className="input">
        {before &&
          <div className="input__before">{before}</div>}
        <input
          className={classNames}
          type="text" id={id} {...rest}
        />
        {children &&
          <div className="input__after">{children}</div>}
      </div>
    </div>
  )
}
