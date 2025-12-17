(function () {
  'use strict'

  const VALIDATE_CLASS = 'js-validate'
  const CLIENT_ERROR_CLASS = 'client-validation-error'

  const gettext = window.gettext || function (msg) { return msg }
  const ngettext = window.ngettext || function (singular, plural, count) {
    return count === 1 ? singular : plural
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll(`form.${VALIDATE_CLASS}`).forEach(setupFormValidation)
  })

  function setupFormValidation (form) {
    form.setAttribute('novalidate', 'novalidate')

    let errorContainer = form.querySelector('.client-validation-errors')
    if (!errorContainer) {
      errorContainer = document.createElement('div')
      errorContainer.class = 'client-validation-errors'
      errorContainer.style.display = 'none'
      form.insertBefore(errorContainer, form.firstChild)
    }

    form.addEventListener('submit', function (event) {
      clearAllClientErrors(form)

      const requiredFields = this.querySelectorAll('[required]')
      const emptyFields = []

      requiredFields.forEach(field => {
        const isEmpty = field.type === 'checkbox' ? !field.checked : field.value.trim() === ''
        if (isEmpty) {
          emptyFields.push({
            element: field,
            name: getFieldLabel(field),
            type: field.type
          })
          field.classList.add('field-error')
          field.setAttribute('aria-invalid', 'true')
        }
      })

      if (emptyFields.length > 0) {
        event.preventDefault()
        showClientErrors(emptyFields, errorContainer)
        emptyFields[0].element.focus()
        announceErrors(emptyFields.length)
        return false
      }
    })

    form.querySelectorAll('[required]').forEach(field => {
      field.addEventListener('input', function () {
        if (this.value.trim() !== '') {
          this.classList.remove('field-error')
          this.removeAttribute('aria-invalid')
        }
      })
    })
  }

  function showClientErrors (emptyFields, errorContainer) {
    errorContainer.innerHTML = ''

    const errorList = document.createElement('ul')
    errorList.className = 'errorlist'
    errorList.setAttribute('aria-live', 'assertive')
    errorList.setAttribute('aria-atomic', 'true')

    emptyFields.forEach(fieldData => {
      const errorItem = document.createElement('li')
      errorItem.className = `message message--error ${CLIENT_ERROR_CLASS}`
      errorItem.textContent = getErrorMessage(fieldData)
      errorList.appendChild(errorItem)
    })

    errorContainer.appendChild(errorList)
    errorContainer.style.display = 'block'

    // Remove server-side errors
    removeServerErrors(errorContainer.closest('form'))
  }

  function removeServerErrors (form) {
    // Find and remove all server error containers
    const serverErrorLists = form.querySelectorAll('.errorlist:not(.client-validation-errors .errorlist)')
    serverErrorLists.forEach(list => {
      // Only remove if it's not our client container
      if (!list.closest('.client-validation-errors')) {
        list.remove()
      }
    })

    // Also clear field-specific server errors
    form.querySelectorAll('.field-error').forEach(field => {
      const fieldContainer = field.closest('.form-group, .password-field-wrapper')
      if (fieldContainer) {
        const fieldErrors = fieldContainer.querySelector('.errorlist')
        if (fieldErrors && !fieldErrors.closest('.client-validation-errors')) {
          fieldErrors.remove()
        }
      }
    })
  }

  function clearAllClientErrors (form) {
    const clientContainer = form.querySelector('.client-validation-errors')
    if (clientContainer) {
      clientContainer.innerHTML = ''
      clientContainer.style.display = 'none'
    }

    form.querySelectorAll('.field-error').forEach(field => {
      field.classList.remove('field-error')
      field.removeAttribute('aria-invalid')
    })
  }

  function getFieldLabel (field) {
    const label = document.querySelector(`label[for="${field.id}"]`)
    if (label) {
      return label.textContent
        .replace(/\*/g, '')
        .replace(/\(required\)/gi, '')
        .trim()
    }
    return field.placeholder || field.name || gettext('This field')
  }

  function getErrorMessage (fieldData) {
    const fieldLabel = fieldData.name.toLowerCase()
    const fieldType = fieldData.type

    if (fieldLabel.includes('password') || fieldType === 'password') {
      return gettext('Please enter your password.')
    } else if (fieldLabel.includes('email') || fieldType === 'email') {
      return gettext('Please enter your email address.')
    } else if (fieldLabel.includes('username') || fieldLabel.includes('benutzername')) {
      return gettext('Please enter your username.')
    } else if (fieldLabel.includes('terms_of_use') || fieldLabel.includes('terms')) {
      return gettext('You must accept the terms of use.')
    } else {
      return gettext('This field is required.')
    }
  }

  function announceErrors (errorCount) {
    const announcement = document.createElement('div')
    announcement.setAttribute('role', 'alert')
    announcement.setAttribute('aria-live', 'assertive')
    announcement.className = 'sr-only'

    if (errorCount === 1) {
      announcement.textContent = gettext('The form contains an error.')
    } else {
      announcement.textContent = ngettext(
        'The form contains an error.',
        'The form contains %s errors.',
        errorCount
      ).replace('%s', errorCount)
    }

    document.body.appendChild(announcement)
    setTimeout(() => announcement.remove(), 1000)
  }
})()
