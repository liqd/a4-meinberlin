import React from 'react'
import django from 'django'
import KiezradarList from './KiezradarList'
import { Route, Routes, useLocation, Link } from 'react-router-dom'
import { classNames } from '../contrib/helpers'
import NewKiezradar from './NewKiezradar'
import EditKiezradar from './EditKiezradar'

const titleText = django.gettext('Kiez selection')
const descriptionText = django.gettext(
  'Set up your Kiez to get notified when new projects in your area get published.'
)
const manageKiezesText = django.gettext('Manage Kiezes')
const createKiezText = django.gettext('Create a Kiez')

export default function Kiezradars (props) {
  const location = useLocation()
  const isNewKiez = location.pathname.includes(props.kiezradarNewUrl)

  return (
    <>
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
            element={<KiezradarList {...props} />}
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
