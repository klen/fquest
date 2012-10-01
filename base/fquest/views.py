from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user
from functools import wraps
from .forms import CharacterCreateForm
from .models import Character, db


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

    return render_template(
        'fquest/profile.html', character=current_user.characters.first())


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
    return request.args.get('hub.challenge', 'OK')
