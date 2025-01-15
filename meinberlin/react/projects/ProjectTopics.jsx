import django from 'django'
import React from 'react'

const planStr = django.gettext('Plan')

const ProjectTilePills = ({ project, topicChoices }) => {
  const topicList = project.topics.map((val) => {
    return topicChoices[val]
  })

  if (project.type === 'plan' && topicList.length > 1) {
    const additionalPills = topicList.length - 1
    topicList.splice(1, additionalPills, '+1')
  }

  if (project.topics && project.topics.length > 0) {
    return (
      <ul className="pill__list pill__list--inline">
        {project.type === 'plan' && <li className="pill pill--label">{planStr}</li>}
        {topicChoices.filter(topic => project.topics.includes(topic.code)).map(topic =>
          <li key={topic.code} className="pill pill--topic">{topic.name}</li>
        )}
      </ul>
    )
  }
}

export default ProjectTilePills
