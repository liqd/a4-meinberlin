function disableContact (disable, disableTextfield) {
  const accountEmail = document.getElementById('id_contact_email_0_0')
  const otherEmail = document.getElementById('id_contact_email_0_1')
  const emailTextfield = getEmailTextfield()

  if (accountEmail) {
    accountEmail.disabled = disable
  }
  if (otherEmail) {
    otherEmail.disabled = disable
  }
  if (emailTextfield) {
    emailTextfield.disabled = disableTextfield
  }
  document.getElementById('id_contact_phone').disabled = disable
  document.getElementById('id_contact_storage_consent').disabled = disable
}

// guests get a single email input instead of the radio buttons
function getEmailTextfield () {
  return (
    document.getElementById('id_contact_email_1') ||
    document.getElementById('id_contact_email')
  )
}

function init () {
  const allowContact = document.getElementById('id_allow_contact')
  const accountEmail = document.getElementById('id_contact_email_0_0')
  const otherEmail = document.getElementById('id_contact_email_0_1')
  const emailTextfield = getEmailTextfield()
  let otherEmailChecked = otherEmail ? otherEmail.checked : true

  if (
    accountEmail &&
    otherEmail &&
    !accountEmail.checked &&
    !otherEmail.checked
  ) {
    accountEmail.checked = true
  }

  if (!allowContact.checked) {
    disableContact(true, true)
  } else if (accountEmail && accountEmail.checked) {
    emailTextfield.disabled = true
  }

  allowContact.addEventListener('change', function () {
    if (this.checked) {
      disableContact(false, !otherEmailChecked)
    } else {
      disableContact(true, true)
    }
  })

  if (accountEmail) {
    accountEmail.addEventListener('change', function () {
      if (this.checked) {
        emailTextfield.disabled = true
        otherEmailChecked = false
      }
    })
  }

  if (otherEmail) {
    otherEmail.addEventListener('change', function () {
      if (this.checked) {
        emailTextfield.disabled = false
        otherEmailChecked = true
      }
    })
  }
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
