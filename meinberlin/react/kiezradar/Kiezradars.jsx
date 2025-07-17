import React, { useEffect, useState } from 'react'
import django from 'django'
import KiezradarList from './KiezradarList'
import { Route, Routes, useLocation, Link } from 'react-router-dom'
import NewKiezradar from './NewKiezradar'
import EditKiezradar from './EditKiezradar'
import { alert as Alert, classNames } from 'adhocracy4'
import Loading from './Loading'

const translations = {
  titleText: django.gettext('Kiez selection'),
  descriptionText: django.gettext(
    'Set up your Kiez to get notified when new projects in your area get published.'
  ),
  manageKiezesText: django.gettext('Manage Kiezes'),
  createKiezText: django.gettext('Create a Kiez'),
  kiezCreatedTitle: (title) =>
    django.interpolate(
      django.gettext('Your Kiez %(title)s has been successfully created'),
      { title },
      true
    ),
  kiezCreatedText: (title) =>
    django.interpolate(
      django.gettext(
        'You can find %(title)s under “Kiezes & Districts” on the Kiezradar page. By selecting %(title)s you can explore projects from this Kiez. Individual adjustments are possible under “Manage Kiezes”.'
      ),
      { title },
      true
    ),
  kiezSavedTitle: (title) =>
    django.interpolate(
      django.gettext('%(title)s successfully updated'),
      { title },
      true
    ),
  kiezSavedText: django.gettext('Your changes have been saved.'),
  kiezDeletedTitle: (title) =>
    django.interpolate(
      django.gettext('%(title)s has been deleted successfully.'),
      { title },
      true
    ),
  kiezDeletedText: (title) =>
    django.interpolate(
      django.gettext('The Kiez %(title)s will no longer be shown in the Kiezradar under the "Kieze & Bezirke" filter.'),
      { title },
      true
    ),
  errorText: django.gettext('Error'),
  errorKiezesText: django.gettext('Failed to fetch Kiezes'),
  limitExceededTitle: django.gettext('You have reached the limit of saved Kieze'),
  limitExceededText: django.gettext('You are using the maximum number of 5 Kieze. To create a new Kiez, you must delete an existing one.')
}

export default function Kiezradars (props) {
  const [loading, setLoading] = useState(false)
  const [kiezradars, setKiezradars] = useState([])
  const [error, setError] = useState(null)
  const [alert, setAlert] = useState(null)
  const location = useLocation()
  const isNewKiez = location.pathname.includes(props.kiezradarNewUrl)

  useEffect(() => {
    const fetchKiezradars = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await fetch(props.apiUrl)

        if (!response.ok) {
          throw new Error(translations.errorKiezesText)
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

  const handleAlert = ({ title, message }) => {
    setAlert({ title, message })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const limitExceeded = kiezradars.length === 5

  return (
    <>
      {limitExceeded && (
        <Alert
          title={translations.limitExceededTitle}
          message={translations.limitExceededText}
        />
      )}
      {error && (
        <Alert
          type="danger"
          title={translations.errorText}
          message={error}
          onClick={() => setError(null)}
        />
      )}
      {alert && (
        <Alert
          type="success"
          title={alert.title}
          message={alert.message}
          onClick={() => setAlert(null)}
        />
      )}
      <h1>{translations.titleText}</h1>
      <p>{translations.descriptionText}</p>
      <div aria-live="polite">
        {loading
          ? <Loading />
          : (
            <div className="kiezradar">
              <nav>
                <ul className="kiezradar__nav">
                  <li className="kiezradar__nav-item">
                    <Link
                      to={props.kiezradarFiltersUrl}
                      className={classNames(
                        'kiezradar__link',
                        !isNewKiez && 'kiezradar__link--active'
                      )}
                    >
                      {translations.manageKiezesText}
                    </Link>
                  </li>
                  <li className="kiezradar__nav-item">
                    <Link
                      to={props.kiezradarNewUrl}
                      className={classNames(
                        'kiezradar__link',
                        isNewKiez && 'kiezradar__link--active'
                      )}
                    >
                      {translations.createKiezText}
                    </Link>
                  </li>
                </ul>
              </nav>
              <Routes>
                <Route
                  path={props.kiezradarFiltersUrl}
                  element={
                    <KiezradarList
                      {...props}
                      kiezradars={kiezradars}
                      limitExceeded={limitExceeded}
                      onKiezradarDelete={(kiezradar) => {
                        setKiezradars((prevKiezradars) => prevKiezradars.filter((prevKiezradar) => prevKiezradar.id !== kiezradar.id))

                        handleAlert({
                          title: translations.kiezDeletedTitle(kiezradar.name),
                          message: translations.kiezDeletedText(kiezradar.name)
                        })
                      }}
                    />
                  }
                />
                <Route
                  path={props.kiezradarNewUrl}
                  element={
                    <NewKiezradar
                      {...props}
                      limitExceeded={limitExceeded}
                      onKiezradarSave={(kiezradar) => {
                        setKiezradars((prevKiezradars) =>
                          [...prevKiezradars, kiezradar]
                        )

                        handleAlert({
                          title: translations.kiezCreatedTitle(kiezradar.name),
                          message: translations.kiezCreatedText(kiezradar.name)
                        })
                      }}
                    />
                  }
                />
                <Route
                  path={props.kiezradarFiltersUrl + ':id/'}
                  element={
                    <EditKiezradar
                      {...props}
                      kiezradars={kiezradars}
                      limitExceeded={limitExceeded}
                      onKiezradarSave={(kiezradar) => {
                        setKiezradars((prevKiezradars) =>
                          prevKiezradars.map((item) =>
                            item.id === kiezradar.id ? kiezradar : item
                          )
                        )

                        handleAlert({
                          title: translations.kiezSavedTitle(kiezradar.name),
                          message: translations.kiezSavedText
                        })
                      }}
                    />
                  }
                />
              </Routes>
            </div>)}
      </div>
    </>
  )
}
