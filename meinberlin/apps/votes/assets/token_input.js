function init () {
  const input = document.getElementById('id_token')

  const formatAndPos = function (char, backspace) {
    let start = 0
    let end = 0
    let pos = 0
    const separator = ' '
    let value = input.value

    if (char !== false) {
      start = input.selectionStart
      end = input.selectionEnd

      if (backspace && start > 0) {
        // handle backspace onkeydown
        start--

        if (value[start] === separator) {
          start--
        }
      }
      // To be able to replace the selection if there is one
      value = value.substring(0, start) + char + value.substring(end)

      pos = start + char.length // caret position
    }

    let d = 0 // digit count
    let gi = 0 // group index
    let newV = ''
    const group = [4, 4, 4]

    for (let i = 0; i < value.length; i++) {
      if (/\W/.test(value[i])) {
        if (start > i) {
          pos--
        }
      } else {
        if (d === group[gi]) {
          newV += separator
          d = 0
          gi++

          if (start >= i) {
            pos++
          }
        }
        newV += value[i]
        d++
      }
      if (d === group[gi] && group.length === gi + 1) {
        // max length
        break
      }
    }
    input.value = newV

    if (char !== false) {
      input.setSelectionRange(pos, pos)
    }
  }

  input.addEventListener('keypress', function (e) {
    const code = e.charCode || e.keyCode || e.which

    // Check for tab and arrow keys (needed in Firefox)
    if (
      code !== 9 &&
      (code < 37 || code > 40) &&
      // and CTRL+C / CTRL+V
      !(e.ctrlKey && (code === 99 || code === 118))
    ) {
      e.preventDefault()

      const char = String.fromCharCode(code)

      // Check string
      if (
        /\W/.test(char) ||
        (this.selectionStart === this.selectionEnd &&
          this.value.replace(/\W/g, '').length >= (/^\W*3[47]/.test(this.value)))
      ) { formatAndPos(char) }
    }
  })

  // backspace doesn't fire the keypress event
  input.addEventListener('keydown', function (e) {
    if (e.keyCode === 8 || e.keyCode === 46) {
      // backspace or delete
      e.preventDefault()
      formatAndPos('', this.selectionStart === this.selectionEnd)
    }
  })

  input.addEventListener('paste', function () {
    // A timeout is needed to get the new value pasted
    setTimeout(function () {
      formatAndPos('')
    }, 50)
  })

  input.addEventListener('blur', function () {
    // reformat onblur just in case (optional)
    formatAndPos(this, false)
  })
}

document.addEventListener('DOMContentLoaded', init, false)
