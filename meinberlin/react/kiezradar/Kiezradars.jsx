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
  kiezCreatedText: (title) =>
    django.interpolate(
      django.gettext(
        'Your kiez %(title)s has been successfully created. You can find it under “Kiezes & Districts” on the Kiezradar page. By selecting %(title)s you can explore projects from this Kiez. Individual adjustments are possible in the user settings under “Manage Kiezes”.'
      ),
      { title },
      true
    ),
  kiezSavedText: (title) =>
    django.interpolate(
      django.gettext(
        '%(title)s successfully updated. Your changes have been saved.'
      ),
      { title },
      true
    ),
  kiezDeletedText: (title) =>
    django.interpolate(
      django.gettext('%(title)s has been permanently deleted.'),
      { title },
      true
    ),
  errorKiezesText: django.gettext('Failed to fetch Kiezes'),
  limitExceededText: django.gettext('You’ve reached the maximum number of 5 Kiez allowed. To save a new one, you’ll need to delete an existing Kiez.')
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
      {error && (
        <Alert
          type="danger"
          message={error}
          onClick={() => setError(null)}
        />
      )}
      {alert && (
        <Alert
          type="success"
          message={alert.message}
          onClick={() => setAlert(null)}
        />
      )}
      {limitExceeded && (
        <AlertLimit />
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
                          message: translations.kiezSavedText(kiezradar.name)
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

function AlertLimit () {
  const [active, isActive] = useState(true)

  if (!active) {
    return null
  }

  return (
    <Alert
      message={translations.limitExceededText}
      onClick={() => isActive(false)}
    />
  )
}
