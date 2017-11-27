var React = require('react')
var classNames = require('classnames')

const MenuItem = (props) => {
  const {eventKey, disabled, onClick, onSelect, children, className} = props

  function handleClick (event) {
    if (onClick) {
      onClick(event)
    }

    if (disabled) {
      event.preventDefault()
      return
    }

    if (onSelect) {
      onSelect(eventKey, event)
    }
  }

  return (
    <button
      type="button"
      className={classNames('dropdown-item', className)}
      value={eventKey}
      onClick={handleClick}
    >
      {children}
    </button>
  )
}

const DropdownButton = (props) => {
  const {id, disabled, onSelect, pullRight, title, children, dropdownClassName, buttonClassName} = props
  return (
    <div className={classNames('dropdown', dropdownClassName, {'dropdown--right': pullRight})}>
      <button
        type="button"
        className={classNames('dropdown-toggle', 'btn', 'btn--select', buttonClassName)}
        data-toggle="dropdown"
        aria-haspopup="true"
        aria-expanded="false"
        id={id}
        disabled={disabled}
      >
        {title}
        <i className="fa fa-caret-down" aria-hidden="true" />
      </button>
      <ul aria-labelledby={id} className="dropdown-menu">
        {React.Children.map(children, (child) => {
          return (
            <li>
              {React.cloneElement(child, {
                onSelect: (eventKey, event) => {
                  if (child.props.onSelect) {
                    child.props.onSelect(eventKey, event)
                  }
                  if (onSelect) {
                    onSelect(eventKey, event)
                  }
                }
              })}
            </li>
          )
        })}
      </ul>
    </div>
  )
}

module.exports = {DropdownButton, MenuItem}
