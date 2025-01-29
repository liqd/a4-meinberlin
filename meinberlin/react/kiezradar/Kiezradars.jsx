import React, { useState } from 'react'
import django from 'django'
import KiezradarList from './KiezradarList'
import { Route, Routes, useLocation, Link } from 'react-router-dom'
import { classNames } from '../contrib/helpers'
import NewKiezradar from './NewKiezradar'
import EditKiezradar from './EditKiezradar'
import { alert as Alert } from 'adhocracy4'

const titleText = django.gettext('Kiez selection')
const descriptionText = django.gettext(
  'Set up your Kiez to get notified when new projects in your area get published.'
)
const manageKiezesText = django.gettext('Manage Kiezes')
const createKiezText = django.gettext('Create a Kiez')
const kiezDeletedText = django.gettext('The Kiez has been permanently deleted.')

export default function Kiezradars (props) {
  const [deleteAlert, setDeleteAlert] = useState(null)
  const location = useLocation()
  const isNewKiez = location.pathname.includes(props.kiezradarNewUrl)

  return (
    <>
      {deleteAlert && <Alert type="success" message={kiezDeletedText} onClick={() => setDeleteAlert(false)} />}
      <h1>{titleText}</h1>
      <p>{descriptionText}</p>
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
                {manageKiezesText}
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
                {createKiezText}
              </Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route
            path={props.kiezradarFiltersUrl}
            element={<KiezradarList {...props} onKiezradarDelete={() => setDeleteAlert(true)} />}
          />
          <Route
            path={props.kiezradarNewUrl}
            element={<NewKiezradar {...props} />}
          />
          <Route
            path={props.kiezradarFiltersUrl + ':id/'}
            element={<EditKiezradar {...props} />}
          />
        </Routes>
      </div>
    </>
  )
}
