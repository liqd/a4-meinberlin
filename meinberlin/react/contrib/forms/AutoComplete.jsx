import React, { useState } from 'react'
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

const defaultFilterFn = (choice, text) => choice.name.toLowerCase().includes(text.toLowerCase())

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
  hideLabel,
  onChangeInput,
  filterFn,
  placeholder,
  before,
  after,
  ...comboboxProps
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
    ...comboboxProps,
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

  const actualFilterFn = filterFn || defaultFilterFn
  const filteredChoices = text !== '' ? choices.filter(choice => actualFilterFn(choice, text)) : choices

  const onChangeHandler = (e) => {
    setText(e.target.value)
    onChangeInput?.(e.target.value)
  }

  return (
    <div className="form-group multi-select multi-select--autocomplete">
      <p id={labelId} className={classNames('label', hideLabel && 'aural')}>
        {label}
      </p>
      <div className="multi-select__input-wrapper form-control">
        {before && <div className="multi-select__before">{before}</div>}
        {comboboxProps.isMultiple && (
          <div className="multi-select__selected">
            {activeItems.map((choice) => choice.name).join(', ')}
          </div>
        )}
        <input
          type="text"
          value={text}
          onChange={onChangeHandler}
          placeholder={placeholder}
          className={comboboxClasses}
          {...comboboxAttrs}
        />
        {after && <div className="multi-select__after">{after}</div>}
      </div>
      {filteredChoices.length > 0 && (
        <ul className={classes} {...listboxAttrs}>
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
      )}
    </div>
  )
}
