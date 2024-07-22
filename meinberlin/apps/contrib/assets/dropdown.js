class Dropdown {
  constructor (container) {
    this.container = container
    this.trigger = container.querySelector('[data-dropdown-trigger]')
    this.dropdown = container.querySelector('[data-dropdown-menu]')
    this.closeTimeout = null

    this.init()
  }

  init () {
    this.trigger.addEventListener('click', (event) => this.toggleDropdown(event))
    this.dropdown.addEventListener('keyup', (event) => this.handleKeyup(event))
    this.dropdown.addEventListener('focusout', (event) => this.handleFocusout(event))
  }

  toggleDropdown (event) {
    event.preventDefault()
    if (this.container.classList.contains('is-open')) {
      this.closeDropdown()
    } else {
      this.openDropdown()
    }
  }

  openDropdown () {
    this.dropdown.style.display = 'block'
    this.container.classList.add('is-open')
    this.trigger.setAttribute('aria-expanded', true)
    document.addEventListener('click', this.outsideClickListener)
  }

  closeDropdown (event) {
    if (event) event.stopPropagation()
    document.removeEventListener('click', this.outsideClickListener)
    this.dropdown.style.display = 'none'
    this.container.classList.remove('is-open')
    this.trigger.setAttribute('aria-expanded', false)
    clearTimeout(this.closeTimeout)
  }

  handleKeyup (event) {
    if (event.keyCode === 27) {
      this.closeDropdown()
      this.trigger.focus()
    }
  }

  handleFocusout (event) {
    this.closeTimeout = setTimeout(() => {
      if (!this.dropdown.contains(event.relatedTarget)) {
        this.closeDropdown()
      }
    }, 10)
  }

  outsideClickListener = (event) => {
    if (!this.container.contains(event.target) && event.target !== this.close) {
      this.closeDropdown()
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const dropdowns = document.querySelectorAll('[data-dropdown]')
  dropdowns.forEach(dropdown => new Dropdown(dropdown))
})
