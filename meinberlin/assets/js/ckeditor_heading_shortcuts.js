/* Keyboard shortcuts for headings in CKEditor 5 instances created by
   django_ckeditor_5. Ctrl+Alt+0/1/2/3 mirror Google Docs and Word. */
(function () {
  'use strict'

  const SHORTCUTS = [
    ['Ctrl+Alt+0', 'paragraph'],
    ['Ctrl+Alt+1', 'heading1'],
    ['Ctrl+Alt+2', 'heading2'],
    ['Ctrl+Alt+3', 'heading3']
  ]

  const MAX_INIT_ATTEMPTS = 100
  const RETRY_DELAY = 100

  function attach (editor) {
    if (!editor || editor.headingShortcutsAttached) return
    if (!editor.commands.get('heading')) return
    editor.headingShortcutsAttached = true

    SHORTCUTS.forEach(function (shortcut) {
      editor.keystrokes.set(shortcut[0], function (data, cancel) {
        editor.execute('heading', { value: shortcut[1] })
        cancel()
      })
    })
  }

  let attempts = 0

  function init () {
    const textareas = document.querySelectorAll('.django_ckeditor_5')
    if (!textareas.length) return

    const editors = window.editors || {}

    Array.prototype.forEach.call(textareas, function (textarea) {
      if (!textarea.id) return
      if (editors[textarea.id]) attach(editors[textarea.id])
      if (typeof window.ckeditorRegisterCallback === 'function') {
        window.ckeditorRegisterCallback(textarea.id, attach)
      }
    })

    const allAttached = Array.prototype.every.call(
      textareas,
      function (textarea) {
        return (
          textarea.id &&
          editors[textarea.id] &&
          editors[textarea.id].headingShortcutsAttached
        )
      }
    )

    if (!allAttached && attempts++ < MAX_INIT_ATTEMPTS) {
      window.setTimeout(init, RETRY_DELAY)
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init)
  } else {
    init()
  }
})()
