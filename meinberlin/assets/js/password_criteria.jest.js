import { evaluatePassword, init } from './password_criteria'

function buildForm () {
  document.body.innerHTML = `
    <form>
      <input id="id_username" name="username" value="">
      <input id="id_password1" name="password1" type="password">
      <div id="id_password1_criteria"
           data-password-criteria
           data-password-input="#id_password1"
           data-username-input="#id_username"
           data-min-length="10"
           data-met-text="Met"
           data-unmet-text="Not met"
           hidden>
        <ul>
          <li data-criterion="length"><span class="password-criteria__status"></span></li>
          <li data-criterion="username"><span class="password-criteria__status"></span></li>
          <li data-criterion="categories">
            <span class="password-criteria__status"></span>
            <ul>
              <li data-category="uppercase"></li>
              <li data-category="lowercase"></li>
              <li data-category="number"></li>
              <li data-category="special"></li>
            </ul>
          </li>
        </ul>
      </div>
      <button type="submit">Register</button>
    </form>
  `
  const form = document.querySelector('form')
  return {
    password: form.querySelector('#id_password1'),
    username: form.querySelector('#id_username'),
    criteria: form.querySelector('#id_password1_criteria'),
    submit: form.querySelector('[type="submit"]')
  }
}

function type (input, value) {
  input.value = value
  input.dispatchEvent(new Event('input'))
}

describe('evaluatePassword', () => {
  it('checks the minimum length', () => {
    expect(evaluatePassword('Short1!', '', 10).length).toBe(false)
    expect(evaluatePassword('Longenough1!', '', 10).length).toBe(true)
  })

  it('requires at least three of the four character types', () => {
    expect(evaluatePassword('abcdefghij', '', 10).categories).toBe(false)
    expect(evaluatePassword('abcdefghij1', '', 10).categories).toBe(false)
    expect(evaluatePassword('Abcdefghij1', '', 10).categories).toBe(true)
  })

  it('detects the individual character types', () => {
    const result = evaluatePassword('aA1!', '', 10)
    expect(result.categoryDetails).toEqual({
      uppercase: true,
      lowercase: true,
      number: true,
      special: true
    })
  })

  it('rejects the username as a case-insensitive substring', () => {
    expect(evaluatePassword('MaxMustermann1!', 'max', 10).username).toBe(false)
    expect(evaluatePassword('MaxMustermann1!', 'other', 10).username).toBe(true)
  })

  it('passes the username criterion when there is no username yet', () => {
    expect(evaluatePassword('anything', '', 10).username).toBe(true)
  })
})

describe('password criteria widget', () => {
  it('hides the criteria list until the field is focused', () => {
    const { criteria } = buildForm()
    init(document)
    expect(criteria.hidden).toBe(true)
  })

  it('shows the criteria list on focus and hides it again when empty', () => {
    const { criteria, password } = buildForm()
    init(document)
    password.focus()
    expect(criteria.hidden).toBe(false)
    password.blur()
    expect(criteria.hidden).toBe(true)
  })

  it('keeps the criteria list visible once a value is entered', () => {
    const { criteria, password } = buildForm()
    init(document)
    type(password, 'a')
    password.blur()
    expect(criteria.hidden).toBe(false)
  })

  it('disables the submit button until every criterion is met', () => {
    const { password, username, submit, criteria } = buildForm()
    init(document)

    expect(submit.disabled).toBe(true)

    type(username, 'max')
    type(password, 'MaxMustermann1!')
    expect(submit.disabled).toBe(true)

    type(username, 'otheruser')
    expect(submit.disabled).toBe(false)
    expect(criteria.classList.contains('is-valid')).toBe(true)
  })

  it('marks each criterion and pill as met', () => {
    const { password, criteria } = buildForm()
    init(document)

    type(password, 'Longenough1!')

    expect(criteria.querySelector('[data-criterion="length"]').classList.contains('is-met')).toBe(true)
    expect(criteria.querySelector('[data-category="uppercase"]').classList.contains('is-met')).toBe(true)
    expect(criteria.querySelector('[data-category="lowercase"]').classList.contains('is-met')).toBe(true)
    expect(criteria.querySelector('[data-category="number"]').classList.contains('is-met')).toBe(true)
    expect(criteria.querySelector('[data-category="special"]').classList.contains('is-met')).toBe(true)
  })

  it('re-evaluates when the username changes', () => {
    const { password, username, submit } = buildForm()
    init(document)

    type(username, 'otheruser')
    type(password, 'otheruserABC1')
    expect(submit.disabled).toBe(true)

    type(username, 'someoneelse')
    expect(submit.disabled).toBe(false)
  })

  it('does not initialize the same container twice', () => {
    const { password, criteria } = buildForm()
    init(document)
    init(document)
    const item = criteria.querySelector('[data-criterion="length"]')
    type(password, 'Longenough1!')
    expect(item.classList.contains('is-met')).toBe(true)
  })
})
