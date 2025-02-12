import React, { useEffect, useRef } from 'react'
import django from 'django'

const closeText = django.gettext('Close')
const deleteText = django.gettext('Delete')

export default function DeleteModal ({ title, message, onDelete, onClose }) {
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
      className="kiezradar__modal"
      ref={dialogRef}
      aria-labelledby="modal-title"
      onKeyDown={(event) => {
        if (event.key === 'Escape') closeModal()
      }}
    >
      <button type="button" className="kiezradar__modal-close" aria-label={closeText} onClick={closeModal}>
        <span className="fa fa-times" aria-hidden="true" />
      </button>
      <h3 id="modal-title" className="kiezradar__modal-title">{title}</h3>
      <p className="kiezradar__modal-text">{message}</p>
      <div className="kiezradar__modal-buttons">
        <button className="link" onClick={closeModal}>
          {closeText}
        </button>
        <button className="button kiezradar__modal-button-open" onClick={onDelete}>
          {deleteText}
        </button>
      </div>
    </dialog>
  )
}
