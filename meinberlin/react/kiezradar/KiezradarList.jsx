import React, { useState, useEffect, useRef } from 'react'
import django from 'django'
import { Link } from 'react-router-dom'
import Loading from './Loading'
import { alert as Alert } from 'adhocracy4'
import { updateItem } from '../contrib/helpers'

const noSavedKiezradarsText = django.gettext('No saved Kiezes')
const addKiezText = django.gettext('Add Kiez')
const yourKiezradarsText = django.gettext('Your Kiezes')
const errorText = django.gettext('Error')
const errorKiezesText = django.gettext('Failed to fetch Kiezes')
const errorDeleteKiezesText = django.gettext(
  'Failed to delete kiezradar'
)
const editText = django.gettext('Edit')
const deleteText = django.gettext('Delete')
const closeText = django.gettext('Close')
const viewProjectsText = django.gettext('View projects')
const confirmDeletionText = (name) =>
  django.interpolate(
    django.gettext('Confirm deletion of %(name)s'),
    { name },
    true
  )
const confirmDeletionDescriptionText = django.gettext('You will no longer be able to select this kiez in the Kiezradar. In addition, search profiles based on this kiez will also be deleted.')

export default function KiezradarList ({
  apiUrl,
  planListUrl,
  kiezradarFiltersUrl,
  kiezradarNewUrl,
  onKiezradarDelete
}) {
  const [kiezradars, setKiezradars] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [deleteModal, setDeleteModal] = useState(null)

  useEffect(() => {
    const fetchKiezradars = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(apiUrl)

        if (!response.ok) {
          throw new Error(errorKiezesText)
        }

        const data = await response.json()
        setKiezradars(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchKiezradars()
  }, [])

  const handleDelete = async (kiezradar) => {
    try {
      setLoading(true)
      setDeleteModal(null)

      const response = await updateItem({}, apiUrl + kiezradar.id + '/', 'DELETE')

      if (!response.ok) {
        throw new Error(errorDeleteKiezesText)
      }

      setKiezradars((prevKiezradars) =>
        prevKiezradars.filter((prevKiezradar) => prevKiezradar.id !== kiezradar.id)
      )

      onKiezradarDelete(kiezradar)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div aria-live="polite">
      {loading
        ? <Loading />
        : error
          ? (
            <div className="kiezradar__error">
              <Alert type="danger" message={errorText + ': ' + error} />
            </div>
            )
          : (
            <>
              {deleteModal?.kiezradar && (
                <DeleteModal
                  kiezradar={deleteModal.kiezradar}
                  onDelete={() => handleDelete(deleteModal.kiezradar)}
                  onClose={() => setDeleteModal(null)}
                />
              )}
              <h2>
                {kiezradars.length === 0
                  ? yourKiezradarsText
                  : yourKiezradarsText + ' (' + kiezradars.length + ')'}
              </h2>
              <div className="kiezradar-list">
                {kiezradars.length === 0
                  ? (
                    <section>
                      <p>{noSavedKiezradarsText}</p>
                      <Link to={kiezradarNewUrl} className="button">
                        {addKiezText}
                      </Link>
                    </section>
                    )
                  : (
                    <>
                      <section>
                        <ul className="kiezradar-list__list">
                          {kiezradars.map((kiezradar) => (
                            <li key={kiezradar.id} className="kiezradar-list__kiezradar">
                              <article>
                                <header className="kiezradar-list__header">
                                  <div>
                                    <h3 className="kiezradar-list__kiezradar-title">
                                      {kiezradar.name}
                                    </h3>
                                  </div>
                                  <div className="kiezradar-list__header-buttons">
                                    <div className="kiezradar-list__buttons">
                                      <EditLink to={kiezradarFiltersUrl + kiezradar.id} />
                                      <DeleteButton onDelete={() => setDeleteModal({ kiezradar })} />
                                    </div>
                                  </div>
                                </header>
                                <footer className="kiezradar-list__footer">
                                  <a
                                    href={planListUrl + '?kiezradar=' + kiezradar.id}
                                    className="button button--light kiezradar-list__view-projects"
                                  >
                                    {viewProjectsText}
                                  </a>
                                </footer>
                                <div className="kiezradar-list__footer-buttons">
                                  <div className="kiezradar-list__buttons">
                                    <EditLink to={kiezradarFiltersUrl + kiezradar.id} />
                                    <DeleteButton onDelete={() => setDeleteModal({ kiezradar })} />
                                  </div>
                                </div>
                              </article>
                            </li>
                          ))}
                        </ul>
                      </section>
                      <div className="kiezradar-list__button-container">
                        <Link
                          to={kiezradarNewUrl}
                          className="button kiezradar-list__button"
                        >
                          {addKiezText}
                        </Link>
                      </div>
                    </>
                    )}
              </div>
            </>
            )}
    </div>
  )
}

function EditLink ({ to }) {
  return (
    <Link to={to} className="kiezradar-list__button">
      <i className="fa-solid fa-pencil mr-1" />
      {editText}
    </Link>
  )
}

function DeleteButton ({ onDelete }) {
  return (
    <button
      className="kiezradar-list__button"
      onClick={onDelete}
    >
      <i className="fa-classic fa-regular fa-trash-can mr-1" />
      {deleteText}
    </button>
  )
}

function DeleteModal ({ kiezradar, onDelete, onClose }) {
  const dialogRef = useRef(null)

  const closeModal = () => {
    dialogRef.current.close()
    onClose()
  }

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') closeModal()
    }

    document.addEventListener('keydown', handleKeyDown)

    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [])

  useEffect(() => {
    dialogRef.current.showModal()
  }, [])

  return (
    <dialog className="kiezradar__modal" ref={dialogRef} aria-modal="true">
      <button type="button" className="kiezradar__modal-close" aria-label={closeText} onClick={closeModal}>
        <span className="fa fa-times" aria-hidden="true" />
      </button>
      <h3 className="kiezradar__modal-title">{confirmDeletionText(kiezradar.name)}</h3>
      <p className="kiezradar__modal-text">{confirmDeletionDescriptionText}</p>
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
