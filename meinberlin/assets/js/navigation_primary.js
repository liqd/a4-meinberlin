document.addEventListener('DOMContentLoaded', function () {
// eslint-disable-next-line space-before-function-paren -- linter erroneously treating this like anonymous function
  function toggleDropdown(element, button) {
    const isOpen = element.style.display === 'block' || element.classList.contains('active')
    if (isOpen) {
      element.style.display = 'none'
      element.classList.remove('active')
      if (button) {
        button.setAttribute('data-dropdown-open', 'false')
      }
    } else {
      element.style.display = 'block'
      element.classList.add('active')
      if (button) {
        button.setAttribute('data-dropdown-open', 'true')
      }
    }
    // Sync the status of the injected Berlin.de toggle button if present
    const li = element.closest ? element.closest('li') : null
    if (li) {
      const toggler = li.querySelector ? li.querySelector('.subtree__toggler') : null
      if (toggler) {
        toggler.setAttribute('aria-expanded', isOpen ? 'false' : 'true')
      }
    }
  }

  const toggleButtons = document.querySelectorAll('.js-nav-toggle')
  toggleButtons.forEach(button => {
    // Look for dropdown by multiple possible selectors
    let dropdownElement = button.nextElementSibling
    if (!dropdownElement || !dropdownElement.classList.contains('hamburger-nav__list--sub')) {
      // Try finding by id if next sibling doesn't work
      const parentLi = button.closest('.hamburger-nav__item--dropdown')
      if (parentLi) {
        dropdownElement = parentLi.querySelector('.hamburger-nav__list--sub')
      }
    }

    if (dropdownElement && dropdownElement.classList.contains('hamburger-nav__list--sub')) {
      button.removeAttribute('onclick')
      button.addEventListener('click', function (e) {
        e.preventDefault()
        e.stopPropagation() // Prevent Berlin.de navigation from also handling it
        toggleDropdown(dropdownElement, this)
      })
      if (!button.hasAttribute('data-dropdown-open')) {
        const isOpen = dropdownElement.style.display === 'block' || dropdownElement.classList.contains('active')
        button.setAttribute('data-dropdown-open', isOpen ? 'true' : 'false')
      }
    }
  })

  // Open dropdowns that contain active links
  document.querySelectorAll('.hamburger-nav__list--sub .hamburger-nav__link--active').forEach(activeLink => {
    const dropdown = activeLink.closest('.hamburger-nav__list--sub')
    if (dropdown && (dropdown.style.display !== 'block' && !dropdown.classList.contains('active'))) {
      dropdown.style.display = 'block'
      dropdown.classList.add('active')
      const button = dropdown.previousElementSibling
      if (button && button.classList.contains('js-nav-toggle')) {
        button.setAttribute('data-dropdown-open', 'true')
      }
    }
  })
})
