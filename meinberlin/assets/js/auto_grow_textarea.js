/* Auto-grows elements matching SELECTOR. The native CSS approach
   (`field-sizing: content`) would make this script obsolete, but it only
   reached cross-browser support in mid-2026 (Firefox 152, Safari 26.2) and
   older browsers are still in use, so this JS fallback is kept for now. */

const SELECTOR = '.js-auto-grow-textarea'

function resize (textarea) {
  const border = textarea.offsetHeight - textarea.clientHeight
  textarea.style.height = 'auto'
  textarea.style.height = textarea.scrollHeight + border + 'px'
}

function resizeAll () {
  document.querySelectorAll(SELECTOR).forEach(resize)
}

document.addEventListener('input', function (event) {
  if (event.target.matches(SELECTOR)) {
    resize(event.target)
  }
})

document.addEventListener('DOMContentLoaded', resizeAll, false)
document.addEventListener('a4.embed.ready', resizeAll, false)

window.addEventListener('resize', resizeAll)
