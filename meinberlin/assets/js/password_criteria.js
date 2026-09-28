const DEFAULT_MIN_LENGTH = 10
const REQUIRED_CATEGORY_COUNT = 3

const CATEGORY_PATTERNS = {
  uppercase: /[A-Z]/,
  lowercase: /[a-z]/,
  number: /[0-9]/,
  special: /[^A-Za-z0-9]/
}

export function evaluatePassword (password, username, minLength) {
  const value = password || ''
  const categoryDetails = {}
  let categoryCount = 0

  Object.keys(CATEGORY_PATTERNS).forEach(function (name) {
    const met = CATEGORY_PATTERNS[name].test(value)
    categoryDetails[name] = met
    if (met) categoryCount += 1
  })

  const normalizedUsername = (username || '').trim().toLowerCase()
  const usernameMet = normalizedUsername === '' ||
    value.toLowerCase().indexOf(normalizedUsername) === -1

  return {
    length: value.length >= (minLength || DEFAULT_MIN_LENGTH),
    username: usernameMet,
    categories: categoryCount >= REQUIRED_CATEGORY_COUNT,
    categoryDetails
  }
}

function findField (container, attribute) {
  const selector = container.getAttribute(attribute)
  if (!selector) return null
  const scope = container.closest('form') || document
  return scope.querySelector(selector)
}

function updateCriterion (container, name, met) {
  const item = container.querySelector('[data-criterion="' + name + '"]')
  if (!item) return
  item.classList.toggle('is-met', met)

  const status = item.querySelector('.password-criteria__status')
  if (status) {
    status.textContent = met
      ? container.getAttribute('data-met-text') || ''
      : container.getAttribute('data-unmet-text') || ''
  }
}

function updatePills (container, categoryDetails) {
  Object.keys(categoryDetails).forEach(function (name) {
    const pill = container.querySelector('[data-category="' + name + '"]')
    if (pill) pill.classList.toggle('is-met', categoryDetails[name])
  })
}

function updateSubmit (container, allMet) {
  const form = container.closest('form')
  if (!form) return
  const submit = form.querySelector('[type="submit"]')
  if (submit) submit.disabled = !allMet
}

export function update (container) {
  const input = findField(container, 'data-password-input')
  if (!input) return false

  const usernameField = findField(container, 'data-username-input')
  const minLength = parseInt(container.getAttribute('data-min-length'), 10)
  const result = evaluatePassword(
    input.value,
    usernameField ? usernameField.value : '',
    minLength
  )

  updateCriterion(container, 'length', result.length)
  updateCriterion(container, 'username', result.username)
  updateCriterion(container, 'categories', result.categories)
  updatePills(container, result.categoryDetails)

  const allMet = result.length && result.username && result.categories
  container.classList.toggle('is-valid', allMet)
  updateSubmit(container, allMet)
  return allMet
}

function syncVisibility (container) {
  const input = findField(container, 'data-password-input')
  if (!input) return
  const focused = document.activeElement === input
  container.hidden = !(focused || input.value.length > 0)
}

function bindContainer (container) {
  if (container.dataset.passwordCriteriaReady === 'true') return
  container.dataset.passwordCriteriaReady = 'true'

  const input = findField(container, 'data-password-input')
  if (!input) return

  const usernameField = findField(container, 'data-username-input')

  input.addEventListener('input', function () {
    update(container)
    syncVisibility(container)
  })
  input.addEventListener('focus', function () {
    update(container)
    syncVisibility(container)
  })
  input.addEventListener('blur', function () {
    syncVisibility(container)
  })

  if (usernameField) {
    usernameField.addEventListener('input', function () {
      update(container)
    })
  }

  if (container.id) {
    const describedBy = input.getAttribute('aria-describedby')
    if (!describedBy) {
      input.setAttribute('aria-describedby', container.id)
    } else if (describedBy.indexOf(container.id) === -1) {
      input.setAttribute('aria-describedby', describedBy + ' ' + container.id)
    }
  }

  update(container)
  syncVisibility(container)
}

export function init (root) {
  const scope = root || document
  if (!scope || !scope.querySelectorAll) return
  const containers = scope.querySelectorAll('[data-password-criteria]')
  containers.forEach(bindContainer)
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', function () {
    init(document)
  }, false)

  document.addEventListener('htmx:afterSwap', function (event) {
    init(event.detail.target)
  })
}
