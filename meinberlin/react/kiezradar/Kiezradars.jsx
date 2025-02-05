import React, { useState } from 'react'
import django from 'django'
import KiezradarList from './KiezradarList'
import { Route, Routes, useLocation, Link } from 'react-router-dom'
import NewKiezradar from './NewKiezradar'
import EditKiezradar from './EditKiezradar'
import { alert as A4Alert, classNames } from 'adhocracy4'

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
    )
}

export default function Kiezradars (props) {
  const [alert, setAlert] = useState(null)
  const location = useLocation()
  const isNewKiez = location.pathname.includes(props.kiezradarNewUrl)

  const handleAlert = ({ title, message }) => {
    setAlert({ title, message })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <>
      {alert && (
        <Alert
          message={alert.message}
          onClose={() => setAlert(null)}
        />
      )}
      <h1>{translations.titleText}</h1>
      <p>{translations.descriptionText}</p>
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
                onKiezradarDelete={(kiezradar) =>
                  handleAlert({
                    message: translations.kiezDeletedText(kiezradar.name)
                  })}
              />
            }
          />
          <Route
            path={props.kiezradarNewUrl}
            element={
              <NewKiezradar
                {...props}
                onKiezradarSave={(kiezradar) =>
                  handleAlert({
                    message: translations.kiezCreatedText(kiezradar.name)
                  })}
              />
            }
          />
          <Route
            path={props.kiezradarFiltersUrl + ':id/'}
            element={
              <EditKiezradar
                {...props}
                onKiezradarSave={(kiezradar) =>
                  handleAlert({
                    message: translations.kiezSavedText(kiezradar.name)
                  })}
              />
            }
          />
        </Routes>
      </div>
    </>
  )
}

function Alert ({ message, onClose }) {
  return (
    <A4Alert
      type="success"
      message={message}
      onClick={() => onClose()}
    />
  )
}
