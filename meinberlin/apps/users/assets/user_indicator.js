function init () {
  const userIndicator = document.querySelectorAll('#js-user-indicator')
  if (userIndicator) {
    let closeTimeout
    const trigger = document.querySelector('#js-user-indicator-trigger')
    const dropdown = document.querySelector('#js-user-indicator-dropdown')
    const close = document.querySelector('#js-user-indicator-close')
    const container = document.querySelector('#js-user-indicator')

    function closeDropdown () {
      document.removeEventListener('click', outsideClickListener)
      dropdown.style.display = 'none'
      container.classList.remove('is-open')
      trigger.setAttribute('aria-expanded', false)
      clearTimeout(closeTimeout)
    }

    function openDropdown () {
      if (container.classList.contains('is-open')) {
        closeDropdown()
      } else {
        dropdown.style.display = 'block'
        container.classList.add('is-open')
        trigger.setAttribute('aria-expanded', true)

        document.addEventListener('click', outsideClickListener)
      }
    }

    function outsideClickListener (e) {
      if (!container.contains(e.target) && e.target !== close) {
        closeDropdown()
      }
    }

    trigger.addEventListener('click', function (event) {
      event.preventDefault()
      openDropdown()
    })

    close.addEventListener('click', function (event) {
      event.stopPropagation() // Prevent the event from bubbling up to the document
      closeDropdown()
    })

    dropdown.addEventListener('keyup', function (e) {
      if (e.keyCode === 27) {
        closeDropdown()
        trigger.focus()
      }
    })

    dropdown.addEventListener('focusout', function (e) {
      closeTimeout = setTimeout(function () {
        if (!dropdown.contains(e.relatedTarget)) {
          closeDropdown()
        }
      }, 10)
    })
  }
}

document.addEventListener('DOMContentLoaded', init, false)
