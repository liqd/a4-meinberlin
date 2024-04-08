const Dropdown = {
  toggleDropdown (event) {
    const dropdown = event.currentTarget.parentNode
    const isOpen = dropdown.getAttribute('aria-expanded') === 'true'

    dropdown.setAttribute('aria-expanded', !isOpen)

    const menu = dropdown.querySelector('.dropdown__menu')
    menu.classList.toggle('dropdown__menu--show', !isOpen)

    if (!isOpen) {
      const menu = dropdown.querySelector('.dropdown__menu')
      menu.firstElementChild.focus()
    }
  },

  closeDropdown (event) {
    const dropdowns = document.querySelectorAll('.js-dropdown')
    dropdowns.forEach(function (dropdown) {
      const isOpen = dropdown.getAttribute('aria-expanded') === 'true'
      if (isOpen && !dropdown.contains(event.target)) {
        dropdown.setAttribute('aria-expanded', 'false')
        const menu = dropdown.querySelector('.dropdown__menu')
        menu.classList.remove('dropdown__menu--show')
      }
    })
  },

  init () {
    const dropdowns = document.querySelectorAll('.js-dropdown')
    if (dropdowns.length > 0) {
      dropdowns.forEach(function (button) {
        button.addEventListener('click', Dropdown.toggleDropdown)
      })

      document.addEventListener('click', Dropdown.closeDropdown)
    }
  }
}

export default Dropdown
