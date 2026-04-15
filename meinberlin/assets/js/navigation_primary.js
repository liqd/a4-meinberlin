// Expose toggle function globally so it can be used by inline onclick handlers
window.toggleDropdown = function (element, button) {
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
// Initialize dropdown toggles with js-nav-toggle class
document.addEventListener('DOMContentLoaded', function () {
  const toggleButtons = document.querySelectorAll('.js-nav-toggle')
  toggleButtons.forEach(button => {
    // Find the dropdown - it's the next sibling element with class 'hamburger-nav__list--sub'
    const dropdownElement = button.nextElementSibling
    if (dropdownElement && dropdownElement.classList.contains('hamburger-nav__list--sub')) {
      // Remove any existing inline onclick handlers
      button.removeAttribute('onclick')
      // Add click event listener
      button.addEventListener('click', function (e) {
        e.preventDefault()
        window.toggleDropdown(dropdownElement, this)
      })
      // Initialize ARIA attributes if not present
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
