import React, { useId, useRef, useState } from 'react'
import { classNames } from '../helpers'

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

function getTargets (choices, focusedIndex) {
  return {
    first: choices[0],
    last: choices[choices.length - 1],
    next: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex + 1) : null,
    prev: typeof focusedIndex === 'number' ? getLoopedIndex(choices, focusedIndex - 1) : null
  }
}

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
  const defaultValueArray = Array.isArray(defaultValue) ? defaultValue : [defaultValue]
  // Use values prop if provided (controlled), otherwise use internal state (uncontrolled)
  const [internalValue, setInternalValue] = useState(defaultValueArray)
  const active = values ?? internalValue

  const [focused, setFocused] = useState(null)
  const [opened, setOpened] = useState(false)

  const comboboxRef = useRef(null)
  const typed = useRef('')

  const containerId = useId()
  const labelId = useId()

  const classes = classNames(
    'form-control input__element multi-select__container',
    opened && 'multi-select__container--opened',
    className
  )
  const comboboxClasses = classNames(
    'form-control multi-select__combobox',
    comboboxClassName
  )

  const activeItems = choices.filter(choice => active.includes(choice.value))
  const focusedItem = choices.find((choice) => choice.value === focused)
  const focusedIndex = choices.findIndex(choice => choice.value === focused)
  const targets = getTargets(choices, focusedIndex)

  const toggleOption = (v) => {
    const newValues = toggleValue(v, active)
    if (values === undefined) setInternalValue(newValues)
    if (onChange) onChange(newValues)
  }

  return (
    <div className="form-group multi-select">
      <p id={labelId} className="label">
        {label}
      </p>
      <div
        role="combobox"
        className={comboboxClasses}
        aria-controls={containerId}
        aria-expanded={opened}
        aria-activedescendant={focusedItem?.value}
        aria-labelledby={labelId}
        aria-haspopup
        tabIndex={0}
        ref={comboboxRef}
        onClick={() => {
          if (!opened) {
            setFocused(targets.first.value)
          }
          setOpened(!opened)
        }}
        onBlur={(e) => {
          if (e.relatedTarget?.classList.contains('multi-select__option')) {
            comboboxRef.current?.focus()
            return
          }
          setOpened(false)
        }}
        onKeyDown={(e) => {
          const key = e.key
          switch (key) {
            case ' ':
              e.preventDefault()
              if (!opened) {
                setFocused(targets.first.value)
                setOpened(true)
              } else {
                toggleOption(focused)
              }
              break
            case 'Enter':
              e.preventDefault()

              if (opened && focused) {
                toggleOption(focused)
              } else if (!opened) {
                setFocused(targets.first.value)
              }
              setOpened(!opened)
              break
            case 'Escape':
              setOpened(false)
              break
            case 'ArrowUp':
              e.preventDefault()
              setFocused(targets.prev?.value)
              break
            case 'ArrowDown':
              e.preventDefault()
              setFocused(targets.next?.value)
              if (!opened) {
                setFocused(targets.first.value)
                setOpened(true)
              }
              break
            case 'Home':
              e.preventDefault()
              setFocused(targets.first.value)
              break
            case 'End':
              e.preventDefault()
              setFocused(targets.last.value)
              break
          }
          if (key.length === 1) {
            typed.current += key
            const filtered = choices.filter(choice => choice.name.toLowerCase().startsWith(typed.current.toLowerCase()))
            if (filtered.length) {
              setFocused(filtered[0].value)
            }
            setTimeout(() => { typed.current = '' }, 200)
          }
        }}
      >
        {activeItems.length ? activeItems.map(item => item.name).join(', ') : placeholder}
      </div>
      <ul
        role="listbox"
        aria-multiselectable="true"
        id={containerId}
        className={classes}
        {...rest}
      >
        {
          choices.map((choice) => {
            const liClasses = classNames(
              liClassName,
              'multi-select__option',
              active.includes(choice.value) && 'multi-select__option--active',
              focusedItem?.value === choice.value && 'multi-select__option--focus'
            )

            return (
              // No keyboard event is needed here. Keyboard management happens
              // in the combobox element, where the focus is kept at all times.
              // see https://www.w3.org/WAI/ARIA/apg/patterns/combobox/
              // eslint-disable-next-line jsx-a11y/click-events-have-key-events
              <li
                key={choice.value}
                role="option"
                aria-selected={active.includes(choice.value)}
                onClick={() => {
                  toggleOption(choice.value)
                  setFocused(choice.value)
                }}
                className={liClasses}
                ref={focusedItem?.value === choice.value ? (node) => node?.scrollIntoView({ block: 'nearest' }) : null}
                tabIndex={-1}
              >
                <span>{choice.name}</span>
                {active.includes(choice.value) && <i className="bicon bicon-check" aria-hidden="true" />}
              </li>
            )
          })
        }
      </ul>
    </div>
  )
}
