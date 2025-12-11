import React, { useEffect, useRef, useState } from 'react'
import django from 'django'

const closeText = django.gettext('Close')

export default function Modal ({ title, message, buttonText, onConfirm, onClose, children }) {
  const dialogRef = useRef(null)
  const [isOpen, setIsOpen] = useState(false)

  const closeModal = () => {
    if (dialogRef.current) {
      dialogRef.current.close()
      setIsOpen(false)
      onClose()
    }
  }

  useEffect(() => {
    if (dialogRef.current) {
      dialogRef.current.showModal()
      setIsOpen(true)
    }
  }, [])

  // Focus trap
  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog || !isOpen) return

    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        closeModal()
      }
      if (e.key === 'Tab') {
        const focusableElements = dialog.querySelectorAll(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        const firstElement = focusableElements[0]
        const lastElement = focusableElements[focusableElements.length - 1]

        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault()
          lastElement.focus()
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault()
          firstElement.focus()
        }
      }
    }

    dialog.addEventListener('keydown', handleKeyDown)

    // Focus first button when modal opens
    const firstButton = dialog.querySelector('button')
    if (firstButton) {
      setTimeout(() => firstButton.focus(), 100)
    }

    return () => {
      dialog.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen])

  return (
    <dialog
      className="modal"
      ref={dialogRef}
      aria-modal="true"
      aria-labelledby="modal__title"
      aria-describedby="modal__description"
    >
      <button
        type="button"
        className="modal__close"
        aria-label={closeText}
        onClick={closeModal}
      >
        <span className="fa fa-times" aria-hidden="true" />
      </button>
      <h2 id="modal__title" className="modal__title title-3">{title}</h2>
      <p id="modal__description" className="modal__text">{message}</p>
      {children && <div className="modal__content">{children}</div>}
      <div className="modal__buttons">
        <button className="link" onClick={closeModal}>
          {closeText}
        </button>
        <button className="button modal__confirm-button" onClick={onConfirm}>
          {buttonText}
        </button>
      </div>
    </dialog>
  )
}
