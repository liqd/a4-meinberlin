const MODAL_ID = 'auth-modal'
const OPEN_CLASS = 'js-auth-modal-open'
const CLOSE_CLASS = 'js-auth-modal-close'
const BODY_CLASS = 'js-auth-modal-body'
const CONTENT_SELECTOR = '.narrow-wrapper'
const AUTH_PATH_PREFIX = '/accounts/'
const loadedScriptSources = new Set()

function currentPathWithQuery () {
  return window.location.pathname + window.location.search
}

function resolveAuthUrl (trigger) {
  const raw = trigger.getAttribute('data-auth-modal-url') ||
    trigger.getAttribute('href') ||
    trigger.getAttribute('action')
  if (!raw) return null

  const url = new URL(raw, window.location.origin)
  if (!url.searchParams.get('next')) {
    url.searchParams.set('next', currentPathWithQuery())
  }
  return url.toString()
}

function extractContent (html) {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  return doc.querySelector(CONTENT_SELECTOR) || doc.querySelector('main')
}

function enablePasswordToggles (root, labels) {
  root.addEventListener('click', function (event) {
    const button = event.target.closest('.password-toggle-btn')
    if (!button || !root.contains(button)) return
    event.preventDefault()

    const wrapper = button.closest('.password-field-wrapper')
    const input = wrapper ? wrapper.querySelector('input') : null
    const icon = button.querySelector('i')
    if (!input) return

    if (input.type === 'password') {
      input.type = 'text'
      if (icon) icon.className = 'fas fa-eye-slash'
      button.setAttribute('aria-label', labels.hide)
    } else {
      input.type = 'password'
      if (icon) icon.className = 'fas fa-eye'
      button.setAttribute('aria-label', labels.show)
    }
  })
}

function scriptAlreadyLoaded (src, container) {
  if (loadedScriptSources.has(src)) return true
  return Array.from(document.querySelectorAll('script[src]')).some(function (script) {
    return !container.contains(script) && script.getAttribute('src') === src
  })
}

function activateScripts (container) {
  let pending = 0
  const notifyReady = function () {
    pending -= 1
    if (pending <= 0) {
      document.dispatchEvent(new Event('a4.embed.ready'))
    }
  }

  container.querySelectorAll('script').forEach(function (oldScript) {
    const src = oldScript.getAttribute('src')
    if (src && scriptAlreadyLoaded(src, container)) {
      loadedScriptSources.add(src)
      oldScript.remove()
      return
    }
    if (src) loadedScriptSources.add(src)

    const script = document.createElement('script')
    Array.from(oldScript.attributes).forEach(function (attr) {
      script.setAttribute(attr.name, attr.value)
    })
    script.textContent = oldScript.textContent

    if (src) {
      pending += 1
      script.addEventListener('load', notifyReady)
      script.addEventListener('error', notifyReady)
    }
    oldScript.replaceWith(script)
  })

  if (pending === 0 && container.querySelector('.captcheck_container')) {
    document.dispatchEvent(new Event('a4.embed.ready'))
  }
}

function init () {
  const modal = document.getElementById(MODAL_ID)
  if (!modal) return

  const body = modal.querySelector('.' + BODY_CLASS)
  if (!body) return

  const loadingText = modal.getAttribute('data-loading') || 'Loading …'
  const errorText = modal.getAttribute('data-error') || 'Something went wrong.'
  const labels = {
    show: modal.getAttribute('data-show-password') || 'Show password',
    hide: modal.getAttribute('data-hide-password') || 'Hide password'
  }

  let lastTrigger = null

  function showError () {
    body.innerHTML = '<p class="auth-modal__message auth-modal__message--error">' +
      errorText + '</p>'
  }

  function focusContent () {
    const focusable = body.querySelector(
      'input:not([type="hidden"]), button:not(.password-toggle-btn), a[href]'
    )
    if (focusable) focusable.focus()
  }

  function runContentInits () {
    activateScripts(body)
  }

  function render (html) {
    const content = extractContent(html)
    if (!content) {
      showError()
      return
    }
    body.innerHTML = ''
    body.appendChild(document.importNode(content, true))
    body.scrollTop = 0
    runContentInits()
    focusContent()
  }

  function handleResponse (response) {
    if (response.redirected && response.url) {
      const target = response.url
      closeModal()
      window.location.assign(target)
      return Promise.resolve()
    }

    const contentType = response.headers.get('content-type') || ''
    if (contentType.indexOf('application/json') === -1) {
      return response.text().then(render)
    }

    return response.json().catch(function () {
      return null
    }).then(function (data) {
      if (!data) {
        showError()
        return
      }
      if (data.location) {
        closeModal()
        window.location.assign(data.location)
        return
      }
      if (data.html) {
        render(data.html)
        return
      }
      showError()
    })
  }

  function load (url) {
    body.innerHTML = '<p class="auth-modal__message">' + loadingText + '</p>'
    window.fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        Accept: 'application/json'
      },
      credentials: 'same-origin'
    }).then(handleResponse).catch(showError)
  }

  function openFromTrigger (trigger) {
    const url = resolveAuthUrl(trigger)
    if (!url) return
    lastTrigger = trigger
    if (!modal.open) modal.showModal()
    load(url)
  }

  function closeModal () {
    if (modal.open) modal.close()
  }

  function reset () {
    body.innerHTML = ''
    if (lastTrigger && typeof lastTrigger.focus === 'function') {
      lastTrigger.focus()
    }
    lastTrigger = null
  }

  function submitForm (form) {
    const method = (form.getAttribute('method') || 'get').toUpperCase()
    window.fetch(form.action, {
      method,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        Accept: 'application/json'
      },
      body: new FormData(form),
      credentials: 'same-origin'
    }).then(handleResponse).catch(showError)
  }

  function isInternalAuthLink (link) {
    if (link.target && link.target !== '_self') return false
    const url = new URL(link.href, window.location.origin)
    return url.origin === window.location.origin &&
      url.pathname.indexOf(AUTH_PATH_PREFIX) === 0
  }

  document.addEventListener('submit', function (event) {
    const form = event.target.closest && event.target.closest('.' + OPEN_CLASS)
    if (!form) return
    event.preventDefault()
    openFromTrigger(form)
  }, true)

  document.addEventListener('click', function (event) {
    const openTrigger = event.target.closest('a.' + OPEN_CLASS)
    if (openTrigger) {
      event.preventDefault()
      openFromTrigger(openTrigger)
      return
    }

    const closeButton = event.target.closest('.' + CLOSE_CLASS)
    if (closeButton && modal.contains(closeButton)) {
      event.preventDefault()
      closeModal()
      return
    }

    const link = event.target.closest('a[href]')
    if (link && body.contains(link) && isInternalAuthLink(link)) {
      event.preventDefault()
      load(link.href)
    }
  })

  modal.addEventListener('submit', function (event) {
    const form = event.target
    if (!form || !body.contains(form)) return
    event.preventDefault()
    submitForm(form)
  })

  modal.addEventListener('click', function (event) {
    if (event.target === modal) closeModal()
  })

  modal.addEventListener('close', reset)
  modal.addEventListener('cancel', reset)

  enablePasswordToggles(modal, labels)
}

document.addEventListener('DOMContentLoaded', init, false)
