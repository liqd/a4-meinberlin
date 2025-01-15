import React from 'react'
import { classNames } from '../helpers'
import useCombobox from './useCombobox'

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
    'form-control input__element multi-select__container',
    opened && 'multi-select__container--opened',
    className
  )
  const comboboxClasses = classNames(
    'form-control multi-select__combobox',
    comboboxClassName
  )

  return (
    <div className="form-group multi-select">
      <p id={labelId} className="label">
        {label}
      </p>
      <div className={comboboxClasses} {...comboboxAttrs}>
        {activeItems.length ? activeItems.map(item => item.name).join(', ') : placeholder}
      </div>
      <ul className={classes} {...listboxAttrs} {...rest}>
        {
          choices.map((choice) => {
            const { active, focused, ...attrs } = getChoicesAttr(choice)
            const liClasses = classNames(
              liClassName,
              'multi-select__option',
              active && 'multi-select__option--active',
              focused && 'multi-select__option--focus'
            )

            return (
              // No keyboard event is needed here. Keyboard management happens
              // in the combobox element, where the focus is kept at all times.
              // see https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
              // eslint-disable-next-line jsx-a11y/click-events-have-key-events
              <li
                key={choice.value}
                className={liClasses}
                {...attrs}
              >
                <span>{choice.name}</span>
                {active && <i className="bicon bicon-check" aria-hidden="true" />}
              </li>
            )
          })
        }
      </ul>
    </div>
  )
}
