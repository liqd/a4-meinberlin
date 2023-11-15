import React from 'react'

export const Select = ({ onSelect, choices, label, placeholder, id, ...rest }) => {
  const onSelectWrapper = (e) => {
    const choice = choices.find(choice => choice[0] === e.target.value)
    onSelect(choice)
  }

  return (
    <div className="form-group select">
      <label htmlFor={id} className="form-label select__label">
        {label}
      </label>
      <div className="select__wrapper">
        <select className="form-control select__input" id={id} onChange={onSelectWrapper} {...rest}>
          {placeholder && <option value="">{placeholder}</option>}
          {choices.map((choice, idx) => (
            <option key={'filter-choice_' + idx} value={choice[0]}>
              {choice[1]}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
