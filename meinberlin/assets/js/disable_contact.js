function init () {
  const allowContact = document.getElementById('id_allow_contact')
  const contactPhone = document.getElementById('id_contact_phone')
  const storageConsent = document.getElementById('id_contact_storage_consent')
  // registered users get a radio group, guests only a single email input
  const radios = document.querySelectorAll('input[name="contact_email_0"]')
  const otherRadio = document.querySelector(
    'input[name="contact_email_0"][value="other"]'
  )
  const emailInput = document.querySelector('.js-contact-email')
  const hasAccountRadio = radios.length > 0

  if (hasAccountRadio && !Array.from(radios).some((radio) => radio.checked)) {
    // default to the account email option (radio can be unchecked on re-render)
    const accountRadio = Array.from(radios).find(
      (radio) => radio.value !== 'other'
    )
    accountRadio.checked = true
  }

  function update () {
    const contactDisabled = !allowContact.checked
    radios.forEach((radio) => {
      radio.disabled = contactDisabled
    })
    contactPhone.disabled = contactDisabled
    storageConsent.disabled = contactDisabled
    // the free text input is only usable with the "other" choice
    emailInput.disabled =
      contactDisabled || (hasAccountRadio && !otherRadio.checked)
  }

  allowContact.addEventListener('change', update)
  radios.forEach((radio) => radio.addEventListener('change', update))
  update()
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
