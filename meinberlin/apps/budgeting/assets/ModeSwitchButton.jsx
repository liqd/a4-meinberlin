import React from 'react'
import django from 'django'

export const ModeSwitchButton = () => {
  return (
    <div class="l-wrapper u-spacer-bottom u-spacer-top-double">
      <div class="l-center-8">
        <div className="control-bar">
          <div class="btn-group__container">
            <div class="btn-group" role="group">
              <div class="btn btn--light switch--btn active" aria-label="{% trans 'View as list' %}">
                <i class="fa fa-list" aria-hidden="true" />
                <span>{django.gettext('List')}</span>
              </div>
              <a class="btn btn--light" href="?=map" aria-label="{% trans 'View as map' %}">
                <i class="fa fa-map" aria-hidden="true" />
                <span>{django.gettext('Map')}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
