import React from 'react'
import django from 'django'

const translated = {
  more: django.gettext('More')
}

export const ListItemBadges = props => {
  const getClass = () => {
    return 'label label--big' // Apply the same class for all badges
  }

  // only return icon for pointLabels
  const hasPointLabelIcon = (type) => {
    if (type !== 'point_label') {
      return
    }
    return <i className="fas fa-map-marker-alt u-icon-spacing" aria-hidden="true" />
  }

  return (
    <div className="list-item__labels">
      {props.badges.map((badge, idx) => {
        // Hide the label if it's 'moderator_status'
        if (badge[0] === 'moderator_status') {
          return null
        }
        return (
          <div
            key={'badge_' + idx}
            className={getClass(badge)}
          >
            {hasPointLabelIcon(badge[0])}
            {badge[1]}
          </div>
        )
      })}
      {props.numOfMoreBadges > 0 &&
        <div className="label__link label--big">
          <a
            href={props.proposalUrl}
            className="list-item__link"
          >
            {props.numOfMoreBadges + ' ' + translated.more}
          </a>
        </div>}
    </div>
  )
}
