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
