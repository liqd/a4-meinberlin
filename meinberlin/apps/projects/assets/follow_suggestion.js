import Cookies from 'js-cookie'

import { ACTION_EVENT } from '../../../assets/js/action-events'

const actionPatterns = [
  { url: /\/comments\//, methods: ['POST'] },
  { url: /\/ratings\//, methods: ['POST', 'PATCH'] },
  { url: /\/tokenvotes(\/|$)/, methods: ['POST', 'DELETE'] },
  { url: /\/likes\//, methods: ['POST'] },
  { url: /\/polls\/[^/]+\/vote\//, methods: ['POST'] }
]

function isActionRequest (url, method) {
  if (!url || !method) return false
  const requestMethod = method.toUpperCase()
  return actionPatterns.some(
    (pattern) =>
      pattern.methods.includes(requestMethod) && pattern.url.test(url)
  )
}

function getBanner () {
  return document.querySelector('[data-follow-suggestion]')
}

function showState (banner, state) {
  banner.hidden = false
  banner.querySelectorAll('[data-follow-suggestion-state]').forEach((element) => {
    element.hidden = element.dataset.followSuggestionState !== state
  })
}

function claim (banner) {
  if (!banner || banner.dataset.claiming === 'true' || banner.dataset.shown === 'true') {
    return
  }

  banner.dataset.claiming = 'true'
  $.ajax({
    url: banner.dataset.claimUrl,
    method: 'POST',
    dataType: 'json',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
  })
    .done((data) => {
      banner.dataset.shown = 'true'
      if (data && data.show) {
        showState(banner, 'initial')
      }
    })
    .always(() => {
      delete banner.dataset.claiming
    })
}

function followProject (banner) {
  const buttons = banner.querySelectorAll(
    '[data-follow-suggestion-follow], [data-follow-suggestion-retry]'
  )
  buttons.forEach((button) => {
    button.disabled = true
  })

  $.ajax({
    url: banner.dataset.followUrl,
    method: 'PUT',
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({ enabled: true }),
    dataType: 'json',
    headers: { 'X-CSRFToken': Cookies.get('csrftoken') }
  })
    .done(() => {
      showState(banner, 'confirmation')
      banner.dataset.shown = 'true'
    })
    .fail(() => {
      showState(banner, 'error')
    })
    .always(() => {
      buttons.forEach((button) => {
        button.disabled = false
      })
    })
}

function setupBanner (banner) {
  banner.addEventListener('click', (event) => {
    const closeButton = event.target.closest('[data-follow-suggestion-close]')
    if (closeButton) {
      event.preventDefault()
      banner.hidden = true
      banner.dataset.dismissed = 'true'
      return
    }

    const followButton = event.target.closest(
      '[data-follow-suggestion-follow], [data-follow-suggestion-retry]'
    )
    if (followButton) {
      event.preventDefault()
      followProject(banner)
    }
  })

  if (banner.dataset.initialTrigger === 'true') {
    claim(banner)
  } else if (!banner.hidden) {
    // Server-rendered confirmation after login/registration.
    banner.dataset.shown = 'true'
  }
}

function init () {
  const banner = getBanner()
  if (!banner) return

  setupBanner(banner)

  $(document).on('ajaxSuccess', function (event, xhr, settings) {
    if (isActionRequest(settings.url, settings.type)) {
      claim(banner)
    }
  })

  document.addEventListener(ACTION_EVENT, function (event) {
    const { url, method } = event.detail || {}
    if (isActionRequest(url, method)) {
      claim(banner)
    }
  })
}

document.addEventListener('DOMContentLoaded', init, false)
