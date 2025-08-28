import React, { useState } from 'react'
import django from 'django'
import { Link } from 'react-router-dom'
import Loading from './Loading'
import { alert as Alert } from 'adhocracy4'
import { updateItem } from '../contrib/helpers'
import Modal from '../contrib/Modal'

const noSavedKiezradarsText = django.gettext('No saved Kiezes')
const addKiezText = django.gettext('Add Kiez')
const yourKiezradarsText = django.gettext('Your Kiezes')
const errorText = django.gettext('Error')
const errorDeleteKiezesText = django.gettext(
  'Failed to delete kiezradar'
)
const editText = django.gettext('Edit')
const deleteText = django.gettext('Remove')
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
  kiezradars,
  limitExceeded,
  onKiezradarDelete
}) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [deleteModal, setDeleteModal] = useState(null)

  const handleDelete = async (kiezradar) => {
    try {
      setLoading(true)
      setDeleteModal(null)

      const response = await updateItem({}, apiUrl + kiezradar.id + '/', 'DELETE')

      if (!response.ok) {
        throw new Error(errorDeleteKiezesText)
      }

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
                <Modal
                  title={confirmDeletionText(deleteModal.kiezradar.name)}
                  message={confirmDeletionDescriptionText}
                  buttonText={deleteText}
                  onConfirm={() => handleDelete(deleteModal.kiezradar)}
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
                                    href={planListUrl + '?kiezradars=' + kiezradar.name}
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
                        {limitExceeded
                          ? (
                            <button className="button" disabled>
                              {addKiezText}
                            </button>
                            )
                          : (
                            <Link
                              to={kiezradarNewUrl}
                              className="button"
                            >
                              {addKiezText}
                            </Link>)}
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
      <i className="far fa-trash-alt mr-1" />
      {deleteText}
    </button>
  )
}
