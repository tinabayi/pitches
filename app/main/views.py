# from flask import render_template,request,redirect,url_for,abort
# from ..models import  User
# from . import main
# from .forms import ReviewForm,UpdateProfile
# from .. import db

# from .forms import ReviewForm

from flask_login import login_required 

from flask import render_template,redirect,url_for, abort
from . import main

from .. import db,photos
from ..models import Pitch,User,Comment
from .forms import ReviewForm,CommentForm
# Pitch= pitches.Pitch

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    all_pitches=Pitch.get_pitches()
    title = 'Home - Welcome to The best pitches Website Online'
    return render_template('index.html', title = title ,all_pitches = all_pitches)


@main.route('/pitch/new', methods = ['GET','POST'])
def new_pitch():
    form = ReviewForm()
    pitches =Pitch.get_pitches()

    if form.validate_on_submit():
       
        description = form.description.data
        new_pitch = Pitch(description=description)
        new_pitch.save_pitches()
        return redirect(url_for('main.index',description=description))
        

    title = 'Welcome to The best pitches Website Online'
    return render_template('pitch.html',title = title, review_form=form, pitches=pitches)


#    @main.route('/pitches')
# def diplay_pitch():
#    all_pitches = Pitch.get_pitches()
#    print(all_pitches)
#    return render_template("pitches.html",all_pitches=all_pitches) 




@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))










@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form) 

# @main.route('/pitch/new', methods = ['GET','POST'])
# @login_required
# def create_pitch():
#    form = PitchForm()
#    # Pitch = pitch.Pitch
#    # movie = get_movie(id)

#    if form.validate_on_submit():
#        # title = form.title.data
#        teaser = form.teaser.data
#        pitch = form.pitch.data
#        new_pitch = Pitch(user_id=current_user.id,teaser=teaser, pitch=pitch)
#        new_pitch.save_pitch()
#        return redirect(url_for('.index',pitch = pitch ))

#    # username = f'{user.username} pitch'
#    return render_template('new_pitch.html', pitch_form=form)


@main.route('/pitches')
def display_pitch():
   all_pitches = Pitch.get_pitches()
   print(all_pitches)
   return render_template("create_pitch.html",all_pitches=all_pitches)



@main.route('/comment/new/<int:id>', methods = ['GET','POST'])
def add_comment(id):
    form = CommentForm()
    comments =Comment.get_comments()


    if form.validate_on_submit():
       
        comment = form.comment.data
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.index',comment=comment))

        title = 'Welcome to The best pitches Website Online'
        return render_template('comment.html',title = title, review_form=form, pitches=pitches,comments=comments)
