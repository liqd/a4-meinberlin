function disableContact (disable, disableTextfield) {
  document.querySelectorAll('[id^="id_contact_email_0_"]').forEach(radio => {
    radio.disabled = disable
  })
  const textInput = document.getElementById('id_contact_email_1')
  if (textInput) {
    textInput.disabled = disableTextfield
  }
  const plainEmail = document.getElementById('id_contact_email')
  if (plainEmail) {
    plainEmail.disabled = disable
  }
  const phone = document.getElementById('id_contact_phone')
  if (phone) {
    phone.disabled = disable
  }
  const consent = document.getElementById('id_contact_storage_consent')
  if (consent) {
    consent.disabled = disable
  }
}

function init () {
  const allowContact = document.getElementById('id_allow_contact')
  const accountEmail = document.getElementById('id_contact_email_0_0')
  const otherEmail = document.getElementById('id_contact_email_0_1')
  const textInput = document.getElementById('id_contact_email_1')

  if (!accountEmail) {
    // no account email available, only a plain email field
    disableContact(!allowContact.checked, true)
    allowContact.addEventListener('change', function () {
      disableContact(!this.checked, true)
    })
    return
  }

  let otherEmailChecked = otherEmail.checked

  if (!accountEmail.checked && !otherEmail.checked) {
    accountEmail.checked = true
  }

  if (!allowContact.checked) {
    disableContact(true, true)
  } else if (accountEmail.checked) {
    if (textInput) {
      textInput.disabled = true
    }
  }

  allowContact.addEventListener('change', function () {
    if (this.checked) {
      disableContact(false, !otherEmailChecked)
    } else {
      disableContact(true, true)
    }
  })

  accountEmail.addEventListener('change', function () {
    if (this.checked) {
      if (textInput) {
        textInput.disabled = true
      }
      otherEmailChecked = false
    }
  })

  otherEmail.addEventListener('change', function () {
    if (this.checked) {
      if (textInput) {
        textInput.disabled = false
      }
      otherEmailChecked = true
    }
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
