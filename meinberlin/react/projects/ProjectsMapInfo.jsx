import React, { useState } from 'react'
import django from 'django'
import Alert from 'adhocracy4/adhocracy4/static/Alert'
import { classNames } from 'adhocracy4'

const translations = {
  dontForget: django.gettext("Don't forget"),
  projectsNotShown: django.gettext('Projects without spacial reference are not shown on the map. Please have a look at the project list.')
}

const ProjectsMapInfo = ({ className }) => {
  const [shouldShow, setShouldShow] = useState(sessionStorage.getItem('hideProjectsMapInfo') !== 'true')
  if (!shouldShow) {
    return null
  }

  return (
    <div className={classNames(className, 'projects-map-info')}>
      <Alert
        type="info"
        alertAttribute="off"
        onClick={() => {
          setShouldShow(false)
          sessionStorage.setItem('hideProjectsMapInfo', 'true')
        }}
        message={(
          <p>
            <strong>{translations.dontForget}</strong><br />
            {translations.projectsNotShown}
          </p>
    )}
      />
    </div>
  )
}

export default ProjectsMapInfo
