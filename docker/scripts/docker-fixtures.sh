#!/bin/bash
set -e

# Extract the current date variables similar to the Makefile
START_NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
END_NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+30 days")
START_2=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+31 days")
END_2=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+61 days")
START_3=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+62 days")
END_3=$(date -u +"%Y-%m-%dT%H:%M:%SZ" -d "+92 days")

# set start date of active phase to today
sed -i "s/2022-12-31T23:00:00Z/$START_NOW/g" meinberlin/fixtures/phases.json
sed -i "s/2023-01-31T22:59:00Z/$END_NOW/g" meinberlin/fixtures/phases.json
# set start date of upcoming phase to today + 31
sed -i "s/2023-01-31T23:00:00Z/$START_2/g" meinberlin/fixtures/phases.json
sed -i "s/2023-02-28T22:59:00Z/$END_2/g" meinberlin/fixtures/phases.json
# set start date of last phase to today + 62
sed -i "s/2023-02-28T23:00:00Z/$START_3/g" meinberlin/fixtures/phases.json
sed -i "s/2023-03-31T21:59:00Z/$END_3/g" meinberlin/fixtures/phases.json

python manage.py loaddata meinberlin/fixtures/site-dev.json
python manage.py loaddata meinberlin/fixtures/users.json
python manage.py loaddata meinberlin/fixtures/accounts.json
python manage.py loaddata meinberlin/fixtures/administrative_districts.json
python manage.py loaddata meinberlin/fixtures/map-preset.json
python manage.py loaddata meinberlin/fixtures/organisations.json
python manage.py loaddata meinberlin/fixtures/projects.json
python manage.py loaddata meinberlin/fixtures/modules.json
python manage.py loaddata meinberlin/fixtures/phases.json
python manage.py loaddata meinberlin/fixtures/maps.json
python manage.py loaddata meinberlin/fixtures/polls.json
python manage.py loaddata meinberlin/fixtures/live_questions.json
python manage.py loaddata meinberlin/fixtures/categories.json
python manage.py loaddata meinberlin/fixtures/documents.json
python manage.py loaddata meinberlin/fixtures/labels.json
python manage.py loaddata meinberlin/fixtures/maptopicprop.json
python manage.py loaddata meinberlin/fixtures/moderationtasks.json
python manage.py loaddata meinberlin/fixtures/topicprio.json
python manage.py loaddata meinberlin/fixtures/votes.json

git restore meinberlin/fixtures/phases.json