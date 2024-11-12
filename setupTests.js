import '@testing-library/jest-dom'

if (typeof window.URL.createObjectURL === 'undefined') {
  window.URL.createObjectURL = () => {}
}

Element.prototype.scrollIntoView = jest.fn()
