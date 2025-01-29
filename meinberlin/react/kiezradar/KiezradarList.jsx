import React, { useState, useEffect } from 'react'
import django from 'django'
import { Link } from 'react-router-dom'
import Loading from './Loading'
import { alert as Alert } from 'adhocracy4'

const noSavedKiezradarsText = django.gettext('No saved Kiezes')
const addKiezText = django.gettext('Add Kiez')
const yourKiezradarsText = django.gettext('Your Kiezes')
const errorText = django.gettext('Error')
const errorKiezesText = django.gettext('Failed to fetch Kiezes')
const editText = django.gettext('Edit')
const viewProjectsText = django.gettext('View projects')

export default function KiezradarList ({
  apiUrl,
  planListUrl,
  kiezradarFiltersUrl,
  kiezradarNewUrl
}) {
  const [kiezradars, setKiezradars] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

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
                                      <EditLink to={kiezradarFiltersUrl + kiezradar.id}>
                                        {editText}
                                      </EditLink>
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
                                    <EditLink to={kiezradarFiltersUrl + kiezradar.id}>
                                      {editText}
                                    </EditLink>
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
