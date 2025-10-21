import 'bootstrap' // load bootstrap components
import 'django'
import 'select2' // used to select projects in containers

import '../../apps/actions/assets/timestamps.js'
import '../../apps/newsletters/assets/dynamic_fields.js'
import '../../apps/contrib/assets/dropdown.js'
import './navigation_primary.js'

// map search function
import 'adhocracy4/adhocracy4/maps/static/a4maps/a4maps_address.js'

// expose react components
import {
  commentsAsync as ReactCommentsAsync,
  follows as ReactFollows,
  ratings as ReactRatings,
  reports as ReactReports,
  widget as ReactWidget
} from 'adhocracy4'

function init () {
  ReactWidget.initialise('a4', 'comment_async', ReactCommentsAsync.renderComment)
  ReactWidget.initialise('a4', 'follows', ReactFollows.renderFollow)
  ReactWidget.initialise('a4', 'ratings', ReactRatings.renderRatings)
  ReactWidget.initialise('a4', 'reports', ReactReports.renderReports)

  if ($.fn.select2) {
    $('.js-select2').select2()
    $('.select2__no-search').select2({
      minimumResultsForSearch: -1
    })
  }
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
document.addEventListener('DOMContentLoaded', function () {
  // Password toggle functionality
  document.querySelectorAll('.password-toggle-btn').forEach(function (button) {
    button.addEventListener('click', function () {
      const wrapper = this.closest('.password-field-wrapper')
      const passwordInput = wrapper.querySelector('input')
      const icon = this.querySelector('i')

      if (passwordInput.type === 'password') {
        passwordInput.type = 'text'
        icon.className = 'fas fa-eye-slash'
        this.setAttribute('aria-label', '{% translate "Hide password" %}')
      } else {
        passwordInput.type = 'password'
        icon.className = 'fas fa-eye'
        this.setAttribute('aria-label', '{% translate "Show password" %}')
      }
    })
  })
})

// This function is overwritten with custom behavior in embed.js.
export function getCurrentPath () {
  return location.pathname
}
