import React from 'react'

export const Input = ({ label, id, before, children, className, ...rest }) => (
  <div className="form-group">
    <label htmlFor={id} className="form-label">
      {label}
    </label>
    <div className="input">
      {before &&
        <div className="input__before">{before}</div>}
      <input
        className={'form-control input__element ' + (before && 'input__element--before ') + className + (children && ' input__element--after')}
        type="text" id={id} {...rest}
      />
      {children &&
        <div className="input__after">{children}</div>}
    </div>
  </div>
)
