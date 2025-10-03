// Expose toggle function globally so it can be used by inline onclick handlers
window.toggleDropdown = function (element) {
  const isOpen = element.style.display === 'block'
  if (isOpen) {
    element.style.display = 'none'
  } else {
    element.style.display = 'block'
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
