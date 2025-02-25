document.addEventListener('DOMContentLoaded', function () {
  initModuleDialog()
})

function initModuleDialog () {
  const button = document.getElementById('module-blueprint-btn')
  const dialog = document.getElementById('module-blueprint-list')

  if (!button || !dialog) return

  // Move dialog to <body> for proper behavior
  document.body.appendChild(dialog)

  button.addEventListener('click', function (e) {
    e.preventDefault()
    const url = button.getAttribute('href')

    fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.text()
      })
      .then(html => {
        // Check if the response is a full HTML page
        if (html.includes('<html') && html.includes('<head')) {
          // Create a temporary element to parse the HTML
          const tempDoc = document.implementation.createHTMLDocument()
          tempDoc.documentElement.innerHTML = html

          const contentElement = tempDoc.querySelector('.module-blueprint-list') ||
            tempDoc.querySelector('.blueprint-dialog__body') ||
            tempDoc.querySelector('main')

          if (contentElement) {
            // Extract only the content we need
            html = contentElement.innerHTML
          } else {
            console.warn('Could not extract content from full page response')
          }
        }

        dialog.querySelector('.blueprint-dialog__body').innerHTML = html
        dialog.showModal()
      })
      .catch(error => console.error('Error loading dialog content:', error))
  })

  const closeButtons = dialog.querySelectorAll("[data-action='close-dialog']")
  closeButtons.forEach(btn => {
    btn.addEventListener('click', function () {
      dialog.close()
    })
  })

  dialog.addEventListener('click', handleBackdropClick)
  function handleBackdropClick (event) {
    if (event.target === dialog) {
      dialog.close()
    }
  }
}
