import React from 'react'
import { classNames } from 'adhocracy4'
import useCombobox from 'adhocracy4/adhocracy4/static/forms/useCombobox'

export const GroupMultiSelect = ({
  label,
  className,
  liClassName,
  comboboxClassName,
  groups,
  onChange,
  placeholder,
  values,
  defaultValue = [],
  ...rest
}) => {
  const { opened, labelId, activeItems, listboxAttrs, comboboxAttrs, getChoicesAttr } = useCombobox({
    choices: groups.map(({ choices }) => choices.map((choice) => choice)).flat(),
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
      <ul className={classes} role="listbox" {...listboxAttrs} {...rest}>
        {groups.map(({ title, info, choices }) => (
          <li key={title} role="group" className="a4-combo-box__group-item" aria-labelledby={'group-' + title}>
            <span id={'group-' + title} className="a4-combo-box__title">
              {title}
            </span>
            {info && <span className="a4-combo-box__info">{info}</span>}
            {choices.length > 0 && (
              <ul className="a4-combo-box__group-dropdown">
                {choices.map((choice) => {
                  const { active, focused, ...attrs } = getChoicesAttr(choice)
                  const liClasses = classNames(
                    liClassName,
                    'a4-combo-box__option',
                    active && 'a4-combo-box__option--active',
                    focused && 'a4-combo-box__option--focus'
                  )

                  return (
                    <li key={choice.value} className={liClasses} {...attrs}>
                      <span>{choice.name}</span>
                      {active && (
                        <i className="bicon bicon-check" aria-hidden="true" />
                      )}
                    </li>
                  )
                })}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  )
}
