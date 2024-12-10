/* global django */
import React, { useId } from 'react'
import { classNames } from '../contrib/helpers'
import ProjectTopics from './ProjectTopics'
import getTimespan from './get-timespan'
import ImageWithPlaceholder from '../contrib/ImageWithPlaceholder'

const copyrightMissingStr = django.gettext('copyright missing')
const copyrightStr = django.gettext('copyright by')
const altImgStr = django.gettext('Here you can find a decorative picture.')

function truncateText (item) {
  if (item.length > 170) {
    return item.substring(0, 170) + '...'
  } else {
    return item
  }
}

const ProjectTile = ({ project, isHorizontal, topicChoices, isMapTile }) => {
  const labelId = useId()
  const describedById = useId()
  const statusId = useId()
  const statusBarProgress = project.active_phase ? project.active_phase[0] + '%' : null

  return (
    <a
      href={project.url}
      target={project.subtype === 'external' ? '_blank' : '_self'}
      rel="noreferrer"
      aria-labelledby={labelId}
      id={describedById}
      aria-describedby={describedById}
      className={classNames('project-tile', isHorizontal ? 'project-tile--horizontal' : 'project-tile--vertical', isMapTile && 'project-tile--map')}
    >
      <div className="project-tile__image-wrapper image">
        <ProjectTileIcon access={project.access} />
        <ImageWithPlaceholder
          src={project.tile_image}
          alt={project.tile_image_alt_text ?? altImgStr}
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
            <ProjectTopics project={project} topicChoices={topicChoices} />
          </div>}
        <h3 className="project-tile__title" id={labelId}>{project.title}</h3>
        {project.description && !isMapTile && (
          <p className="project-tile__description">
            {truncateText(project.description)}
          </p>
        )}

        {project.active_phase &&
          <>
            <progress
              value={project.active_phase[0]}
              max="100"
              aria-valuenow={project.active_phase[0]}
              aria-valuemin="0"
              aria-valuemax="100"
              className="project-tile__status"
              id={statusId}
            >
              {statusBarProgress}
            </progress>
            <label htmlFor={statusId} className="project-tile__timespan">
              <i className="far fa-clock" aria-hidden="true" />
              {getTimespan(project)}
            </label>
          </>}
      </div>
    </a>
  )
}

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
