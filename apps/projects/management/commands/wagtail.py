import datetime
import sqlite3


def _parse_dt(s):
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S.%f')
    except TypeError:
        return None


def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_db(path):
    conn = sqlite3.connect(path)
    conn.row_factory = _dict_factory
    return conn.cursor()


def _get_process(db, page_id):
    db.execute('SELECT * FROM meinberlin_process WHERE page_ptr_id=?',
               (page_id,))
    process = db.fetchone()

    db.execute('SELECT * FROM wagtailcore_page WHERE id=?', (page_id,))
    page = db.fetchone()

    db.execute('SELECT * FROM wagtailimages_image WHERE id=?',
               (process['image_id'],))
    image = db.fetchone()

    return {
        'created': _parse_dt(page['first_published_at']),
        'modified': _parse_dt(page['latest_revision_created_at']),
        'slug': page['slug'],
        'name': page['title'],
        'description': process['short_description'],
        'is_draft': not page['live'],
        'image': image['file'],
        'image_author': process['image_copyright'],
        'is_archived': bool(process['archived']),
        'city': process['city'],
    }


def iter_external_processes(db):
    db.execute('SELECT * FROM meinberlin_externalprocess')
    for external_process in db.fetchall():
        data = _get_process(db, external_process['process_ptr_id'])
        data.update({
            'url': external_process['external_url'],
            'is_adhocracy': bool(external_process['is_adhocracy']),
        })
        yield data


def get_adhocracy_process(db, path):
    sql = 'SELECT * FROM meinberlin_adhocracyprocess WHERE embed_url=?'
    db.execute(sql, (path,))
    adhocracy_process = db.fetchone()

    # try different path variations until we find
    if adhocracy_process is None:
        db.execute(sql, (path.rstrip('/'),))
        adhocracy_process = db.fetchone()
    if adhocracy_process is None:
        db.execute(sql, (path + 'VERSION_0000000',))
        adhocracy_process = db.fetchone()
    if adhocracy_process is None:
        db.execute(sql, (path + 'VERSION_0000000/',))
        adhocracy_process = db.fetchone()
    if adhocracy_process is None:
        db.execute(sql, (path + 'VERSION_0000001',))
        adhocracy_process = db.fetchone()
    if adhocracy_process is None:
        db.execute(sql, (path + 'VERSION_0000001/',))
        adhocracy_process = db.fetchone()
    if adhocracy_process is None:
        print('missing wagtail data:', path)
        return {}

    data = _get_process(db, adhocracy_process['process_ptr_id'])
    data.update({
        # TODO: we may want to sanitize the HTML
        'information': adhocracy_process['description'],
        'typ': adhocracy_process['process_type'],  # a3 content type
    })
    return data
