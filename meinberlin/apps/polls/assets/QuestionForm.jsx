var React = require('react')
var django = require('django')
var FlipMove = require('react-flip-move')
var ChoiceForm = require('./ChoiceForm')
var ErrorList = require('../../contrib/assets/ErrorList')

const QuestionForm = (props) => {
  return (
    <section className="commenting">
      <div className="commenting__content commenting__content--border">
        <div className="form-group">
          <label
            htmlFor={'id_questions-' + props.id + '-name'}>
            {django.gettext('Question')}
          </label>
          <textarea
            id={'id_questions-' + props.id + '-name'}
            name={'questions-' + props.id + '-name'}
            value={props.question.label}
            onChange={(e) => { props.onLabelChange(e.target.value) }} />
          <ErrorList errors={props.errors} field="label" />
        </div>

        <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
          {
            props.question.choices.map((choice, index) => {
              var key = choice.id || choice.key
              var label = django.gettext('Choice') + ` #${props.index + 1}`
              var errors = props.errors && props.errors.choices
                ? props.errors.choices[index] : {}
              return (
                <div key={key}>
                  <ChoiceForm
                    id={key}
                    label={label}
                    choice={choice}
                    onLabelChange={(label) => { props.onChoiceLabelChange(index, label) }}
                    onDelete={() => { props.onDeleteChoice(index) }}
                    errors={errors}
                  />
                </div>
              )
            })
          }
        </FlipMove>
        <button
          className="btn btn--light btn--small"
          onClick={props.onAppendChoice}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('Add a new choice')}
        </button>
      </div>

      <div className="commenting__actions btn-group" role="group">
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveUp}
          disabled={!props.onMoveUp}
          title={django.gettext('Move up')}
          type="button">
          <i className="fa fa-chevron-up"
            aria-label={django.gettext('Move up')} />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onMoveDown}
          disabled={!props.onMoveDown}
          title={django.gettext('Move down')}
          type="button">
          <i className="fa fa-chevron-down"
            aria-label={django.gettext('Move down')} />
        </button>
        <button
          className="btn btn--light btn--small"
          onClick={props.onDelete}
          title={django.gettext('Delete')}
          type="button">
          <i className="fa fa-trash"
            aria-label={django.gettext('Delete')} />
        </button>
      </div>
    </section>
  )
}

module.exports = QuestionForm
