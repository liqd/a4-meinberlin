import React from 'react'

const ProjectTopics = ({ project, topicChoices }) => {
  const topicList = project.topics.map((val) => {
    return topicChoices[val]
  })

  if (project.topics && project.topics.length > 0) {
    return (
      <ul className="pill__list pill__list--inline">
        {topicList.map(topic =>
          <li key={topic} className="pill pill--topic">{topic}</li>
        )}
      </ul>
    )
  }
}

export default ProjectTopics
