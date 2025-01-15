/* global django */
import React, { forwardRef, useId } from 'react'
import { classNames, toLocaleDate } from '../contrib/helpers'
import ProjectTilePills from './ProjectTopics'
import getTimespan from './get-timespan'
import ImageWithPlaceholder from '../contrib/ImageWithPlaceholder'

const copyrightMissingStr = django.gettext('copyright missing')
const copyrightStr = django.gettext('copyright by')
const participationEndedStr = django.gettext('Participation ended')
const beginsOnStr = django.gettext('Begins on the')
const participationProjectsStr = django.gettext('Participation projects')
const participationProjectStr = django.gettext('Participation project')

function truncateText (item) {
  if (item.length > 170) {
    return item.substring(0, 170) + '...'
  } else {
    return item
  }
}

// FIXME: change to `ref` when using this component once we are on react v19
//  see https://react.dev/reference/react/forwardRef
const ProjectTile = forwardRef(function ProjectTile ({ project, isHorizontal, topicChoices, isMapTile }, ref) {
  const labelId = useId()
  const describedById = useId()
  const statusId = useId()
  const statusBarProgress = project.active_phase ? project.active_phase[0] + '%' : null
  let state = 'past'

  // Plans are always active since we dont change state for them, we only show
  // projects belonging to them.
  if (project.active_phase || project.type === 'plan') {
    state = 'active'
  } else if (project.future_phase) {
    state = 'future'
  }

  return (
    <a
      href={project.url}
      target={project.subtype === 'external' ? '_blank' : '_self'}
      rel="noreferrer"
      ref={ref}
      aria-labelledby={labelId}
      id={describedById}
      aria-describedby={describedById}
      className={classNames('project-tile', isHorizontal ? 'project-tile--horizontal' : 'project-tile--vertical', isMapTile && 'project-tile--map')}
    >
      <div className="project-tile__image-wrapper image">
        <ProjectTileIcon access={project.access} />
        <ImageWithPlaceholder
          src={project.tile_image}
          alt={project.tile_image_alt_text ?? ''}
          height={490}
          width={isHorizontal ? 490 : 630}
          className="project-tile__image"
        />
        <span className="image__copyright">
          {project.tile_image_copyright ? copyrightStr + ' ' + project.tile_image_copyright : copyrightMissingStr}
        </span>
      </div>

      <div className="project-tile__body">
        {!isMapTile && <span className="project-tile__head">{project.district}</span>}
        {project.topics?.length > 0 &&
          <div className="project-tile__topics">
            <ProjectTilePills project={project} topicChoices={topicChoices} />
          </div>}
        <h3 className="project-tile__title" id={labelId}>{project.title}</h3>
        {project.description && !isMapTile && (
          <p className="project-tile__description">
            {truncateText(project.description)}
          </p>
        )}

        <div className="project-tile__status">
          {state === 'active' && project.type !== 'plan' && (
            <>
              <progress
                value={project.active_phase[0]}
                max="100"
                aria-valuenow={project.active_phase[0]}
                aria-valuemin="0"
                aria-valuemax="100"
                id={statusId}
                className="status-bar"
              >
                {statusBarProgress}
              </progress>
              <label htmlFor={statusId} className="status-bar__timespan">
                <i className="far fa-clock" aria-hidden="true" />
                {getTimespan(project)}
              </label>
            </>
          )}
          {state === 'active' && project.type === 'plan' && (
            <p>
              <i className="fas fa-table-cells" aria-hidden="true" />

              <span className="project-tile__plan__count">{project.published_projects_count}</span>
              {project.published_projects_count === 1
                ? participationProjectStr
                : participationProjectsStr}
            </p>
          )}
          {state === 'past' && <p>{participationEndedStr}</p>}
          {state === 'future' && <p>{beginsOnStr} {toLocaleDate(project.future_phase, undefined, { month: 'numeric', year: 'numeric', day: 'numeric' })}</p>}
        </div>
      </div>
    </a>
  )
})

function ProjectTileIcon ({ access }) {
  const projectType = {
    1: 'public',
    2: 'semiPublic',
    3: 'private'
  }[access]

  switch (projectType) {
    case 'semiPublic':
      return (
        <div className="project-tile__icon" aria-hidden="true">
          <i className="fa fa-eye" />
        </div>
      )

    case 'private':
      return (
        <div className="project-tile__icon" aria-hidden="true">
          <i className="fa fa-lock" />
        </div>
      )

    case 'public':
    default:
      return null
  }
}

export default ProjectTile
