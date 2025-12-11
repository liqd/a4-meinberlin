import React from 'react'
import { classNames } from 'adhocracy4'
import useCombobox from 'adhocracy4/adhocracy4/static/forms/useCombobox'

/*
  Choice formatting looks like:
  { name: 'Swedish', value: 'sv' },
  { name: 'English', value: 'en' }
  Values need to be unique!
 */
export const MultiSelect = ({
  label,
  className,
  liClassName,
  comboboxClassName,
  choices,
  onChange,
  placeholder,
  values,
  defaultValue = [],
  ...rest
}) => {
  const { opened, labelId, activeItems, listboxAttrs, comboboxAttrs, getChoicesAttr } = useCombobox({
    choices,
    values,
    defaultValue,
    onChange,
    isMultiple: true
  })
  const classes = classNames(
    'form-control input__element a4-combo-box__container',
    opened && 'a4-combo-box__container--opened',
    className
  )
  const comboboxClasses = classNames(
    'form-control a4-combo-box__combobox',
    comboboxClassName
  )

  return (
    <div className="form-group a4-combo-box">
      <p id={labelId} className="label">
        {label}
      </p>
      <div className={comboboxClasses} {...comboboxAttrs}>
        {activeItems.length ? activeItems.map(item => item.name).join(', ') : placeholder}
      </div>
      <ul className={classes} {...listboxAttrs} {...rest}>
        {
    choices.map((choice, index) => {
      const choiceAttrs = getChoicesAttr(choice, index)
      const liClasses = classNames(
        liClassName,
        'a4-combo-box__option',
        choiceAttrs.active && 'a4-combo-box__option--active',
        choiceAttrs.focused && 'a4-combo-box__option--focus'
      )

      return (
        <li
          key={choice.value}
          className={liClasses}
          {...choiceAttrs}
        >
          <span>{choice.name}</span>
          {choiceAttrs.active && <i className="bicon bicon-check" aria-hidden="true" />}
        </li>
      )
    })
  }
      </ul>
    </div>
  )
}
