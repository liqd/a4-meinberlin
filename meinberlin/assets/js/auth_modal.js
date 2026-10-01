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

function activateCaptcha (container) {
  if (!container.querySelector('.captcheck_container')) return

  const scripts = container.querySelectorAll('script[src]')
  if (scripts.length === 0) {
    document.dispatchEvent(new Event('a4.embed.ready'))
    return
  }

  scripts.forEach(function (script) {
    script.addEventListener('load', function () {
      document.dispatchEvent(new Event('a4.embed.ready'))
    })
  })
}

function init () {
  const dialog = document.getElementById('auth-modal')
  if (!dialog) return

  const body = document.getElementById('auth-modal-body')
  if (!body) return

  const labels = {
    show: dialog.getAttribute('data-show-password') || 'Show password',
    hide: dialog.getAttribute('data-hide-password') || 'Hide password'
  }

  // htmx loads the auth fragment into the body; open the dialog once it arrived.
  document.body.addEventListener('htmx:afterSwap', function (event) {
    if (event.detail.target !== body) return
    if (!dialog.open) dialog.showModal()
    activateCaptcha(body)
  })

  dialog.addEventListener('click', function (event) {
    if (event.target.closest('.js-auth-modal-close') || event.target === dialog) {
      dialog.close()
    }
  })

  dialog.addEventListener('close', function () {
    body.innerHTML = ''
  })
  dialog.addEventListener('cancel', function () {
    body.innerHTML = ''
  })

  enablePasswordToggles(dialog, labels)
}

document.addEventListener('DOMContentLoaded', init, false)
