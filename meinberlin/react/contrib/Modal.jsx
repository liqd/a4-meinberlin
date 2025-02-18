import React, { useEffect, useRef } from 'react'
import django from 'django'

const closeText = django.gettext('Close')

export default function Modal ({ title, message, buttonText, onConfirm, onClose, children }) {
  const dialogRef = useRef(null)

  const closeModal = () => {
    if (dialogRef.current) {
      dialogRef.current.close()
      onClose()
    }
  }

  useEffect(() => {
    if (dialogRef.current) {
      dialogRef.current.showModal()
    }
  }, [])

  return (
    <dialog
      className="modal"
      ref={dialogRef}
      aria-labelledby="modal__title"
      onKeyDown={(event) => {
        if (event.key === 'Escape') closeModal()
      }}
    >
      <button type="button" className="modal__close" aria-label={closeText} onClick={closeModal}>
        <span className="fa fa-times" aria-hidden="true" />
      </button>
      <h3 id="modal__title" className="modal__title">{title}</h3>
      <p className="modal__text">{message}</p>
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
