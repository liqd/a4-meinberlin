import pytest

from meinberlin.apps.projects.rules import has_no_non_initiator_contributions


@pytest.mark.django_db
def test_no_non_initiator_contributions_with_initiators_no_contributions(
    user_factory, project_factory, organisation
):
    """Test: Project with initiators but without contributions should return True."""
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)

    assert has_no_non_initiator_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_non_initiator_contributions_only_initiator_items(
    user_factory, project_factory, organisation, module_factory, idea_factory
):
    """Test: Project with only initiator items should return True."""
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    idea_factory(module=module, creator=initiator)

    assert has_no_non_initiator_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_non_initiator_contributions_non_initiator_items(
    user_factory, project_factory, organisation, module_factory, idea_factory
):
    """Test: Project with non-initiator items should return False."""
    non_initiator = user_factory()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    idea_factory(module=module, creator=non_initiator)

    assert has_no_non_initiator_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_non_initiator_contributions_non_initiator_comments(
    user_factory,
    project_factory,
    organisation,
    module_factory,
    topic_factory,
    comment_factory,
):
    """Test: Project with non-initiator comments should return False."""
    non_initiator = user_factory()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    topic = topic_factory(module=module)
    comment_factory(content_object=topic, creator=non_initiator)

    assert has_no_non_initiator_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_non_initiator_contributions_only_initiator_comments(
    user_factory,
    project_factory,
    organisation,
    module_factory,
    topic_factory,
    comment_factory,
):
    """Test: Project with only initiator comments should return True."""
    # Remove automatically created initiators
    organisation.initiators.clear()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    # Topic must also be created by the initiator, as it is an Item
    topic = topic_factory(module=module, creator=initiator)
    comment_factory(content_object=topic, creator=initiator)

    assert has_no_non_initiator_contributions.test(initiator, project) is True


@pytest.mark.django_db
def test_no_non_initiator_contributions_non_initiator_votes(
    user_factory,
    project_factory,
    organisation,
    module_factory,
    poll_factory,
    question_factory,
    choice_factory,
    vote_factory,
):
    """Test: Project with non-initiator votes should return False."""
    non_initiator = user_factory()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    poll = poll_factory(module=module)
    question = question_factory(poll=poll, multiple_choice=True)
    choice = choice_factory(question=question)
    vote_factory(choice=choice, creator=non_initiator)

    assert has_no_non_initiator_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_non_initiator_contributions_non_initiator_answers(
    user_factory,
    project_factory,
    organisation,
    module_factory,
    poll_factory,
    question_factory,
    answer_factory,
):
    """Test: Project with non-initiator answers should return False."""
    non_initiator = user_factory()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    poll = poll_factory(module=module)
    question = question_factory(poll=poll, is_open=True)
    answer_factory(question=question, creator=non_initiator)

    assert has_no_non_initiator_contributions.test(initiator, project) is False


@pytest.mark.django_db
def test_no_non_initiator_contributions_non_initiator_ratings(
    user_factory,
    project_factory,
    organisation,
    module_factory,
    idea_factory,
    rating_factory,
):
    """Test: Project with non-initiator ratings should return False."""
    non_initiator = user_factory()
    initiator = user_factory()
    organisation.initiators.add(initiator)
    project = project_factory(organisation=organisation)
    module = module_factory(project=project)
    idea = idea_factory(module=module)
    rating_factory(content_object=idea, creator=non_initiator, value=1)

    assert has_no_non_initiator_contributions.test(initiator, project) is False
