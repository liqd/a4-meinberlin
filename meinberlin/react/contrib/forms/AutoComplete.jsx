import React, { useId, useRef, useState } from 'react'
import { classNames } from '../helpers'
import useCombobox from './useCombobox'

/*
 * Returns the item at the given index in an array, wrapping around
 * if index is out of bounds.
 */
export const getLoopedIndex = (array, index) => {
  const length = array.length
  const wrappedIndex = ((index % length) + length) % length
  return array[wrappedIndex]
}

export const toggleValue = (value, values) => {
  const shouldRemove = values.includes(value)
  let newValues = [...values, value]
  if (shouldRemove) {
    newValues = values.filter(item => item !== value)
  }
  return newValues
}

/*
  Choice formatting looks like:
  { name: 'Swedish', value: 'sv' },
  { name: 'English', value: 'en' }
  Values need to be unique!
 */
export const AutoComplete = ({
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
  const {
    opened,
    labelId,
    activeItems,
    listboxAttrs,
    comboboxAttrs,
    getChoicesAttr
  } = useCombobox({
    choices,
    values,
    defaultValue,
    onChange,
    isAutoComplete: true
  })
  const [text, setText] = useState('')
  const classes = classNames(
    'form-control input__element multi-select__container',
    opened && 'multi-select__container--opened',
    className
  )
  const comboboxClasses = classNames(
    'form-control multi-select__combobox',
    comboboxClassName
  )

  const filteredChoices = choices.filter(choice => choice.name.toLowerCase().includes(text.toLowerCase()))

  return (
    <div className="form-group multi-select">
      <p id={labelId} className="label">
        {label}
      </p>
      <input type="text" value={text} onChange={e => setText(e.target.value)} placeholder={placeholder} className={comboboxClasses} {...comboboxAttrs} />
      <ul className={classes} {...listboxAttrs} {...rest}>
        {
          filteredChoices.map((choice) => {
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
