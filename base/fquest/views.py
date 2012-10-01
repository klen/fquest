# coding: utf-8

from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user
from functools import wraps
from .forms import CharacterCreateForm
from .models import Character, db, Event


fquest = Blueprint(
    'fquest',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/fquest')


def authenticated(func):
    """ Check authorization.
    """
    @wraps(func)
    def wrapper():
        if not current_user.is_authenticated():
            return redirect(url_for('fquest.index'))
        return func()
    return wrapper


@fquest.route('/')
def index():
    " Facebook Quest Main page. "

    return render_template('fquest/index.html')


@fquest.route('/profile/')
@authenticated
def profile():
    " Facebook Quest Profile. "
    if not current_user.characters.count():
        return redirect(url_for('fquest.create'))

    character = current_user.characters.first()
    page = int(request.args.get('page', 1))
    events = Event.query.filter(Event.character_id == character.id)\
        .order_by(Event.created_at.desc()).paginate(page, per_page=20)
    return render_template(
        'fquest/profile.html',
        title="%s — %s" % (character.name, character.display()),
        events=events,
        character=character)


@fquest.route('/character/<facebook_id>/')
def character(facebook_id):
    character = Character.query.filter(Character.facebook_id == facebook_id).first_or_404()
    page = int(request.args.get('page', 1))
    events = Event.query.filter(Event.character_id == character.id)\
        .order_by(Event.created_at.desc()).paginate(page, per_page=20)
    return render_template(
        'fquest/profile.html',
        events=events,
        character=character)


@fquest.route('/edit/')
@authenticated
def edit():
    pass


@fquest.route('/profile/create/', methods=['GET', 'POST'])
@authenticated
def create():
    if current_user.characters.count():
        return redirect(url_for('fquest.profile'))

    form = CharacterCreateForm()
    if form.validate_on_submit():
        key = current_user.keys.first()
        character = Character(
            user=current_user,
            name=current_user.username,
            facebook_id=key.service_id,
            facebook_token=key.access_token,
            strenght=15,
            dexterity=15,
            intellect=15,
            luck=15,
        )
        form.populate_obj(character)
        character.role()
        db.session.add(character)
        db.session.commit()
        return redirect(url_for('fquest.profile'))

    return render_template(
        'fquest/create.html',
        form=form)


@fquest.route('/canvas/')
def canvas():
    return render_template('fquest/canvas.html')


@fquest.route('/realtime', methods=['GET', 'POST'])
def realtime():
    from ..ext import mail
    from flask_mail import Message

    content = str(request.args)

    if request.method == 'POST':
        content = str(request.json)

        try:
            assert request.json and request.json.get('entry')
            for info in request.json.get('entry'):
                character = Character.query.filter(Character.facebook_id == info.get('id')).first()
                if character:
                    Event.fire(character)

        except AssertionError:
            pass

    db.session.commit()

    msg = Message('realtime', body=content, recipients=['horneds@gmail.com'])
    mail.send(msg)

    return request.args.get('hub.challenge', 'OK')
