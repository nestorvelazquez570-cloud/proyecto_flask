from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.user import db, User
from forms import EditProfileForm
from routes.auth import login_required

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def index():
    """Página de bienvenida que lista todos los usuarios."""
    users = User.query.all()
    return render_template('index.html', users=users)

@users_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    """Ver perfil de un usuario (solo accesible si está autenticado)."""
    user = User.query.get_or_404(id)
    # Opcional: solo el propio usuario puede ver su perfil
    if session.get('user_id') != user.id:
        flash('No tienes permiso para ver este perfil.', 'danger')
        return redirect(url_for('users.index'))
    return render_template('profile.html', user=user)

@users_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    """Editar perfil de usuario."""
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para editar este perfil.', 'danger')
        return redirect(url_for('users.index'))

    form = EditProfileForm(obj=user)  # precargar datos
    if form.validate_on_submit():
        # Verificar si el nuevo email o username ya existen en otro usuario
        existing = User.query.filter(
            (User.username == form.username.data) | (User.email == form.email.data)
        ).filter(User.id != user.id).first()
        if existing:
            flash('El nombre de usuario o email ya está en uso.', 'danger')
            return render_template('edit_profile.html', form=form, user=user)

        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('users.profile', id=user.id))
    return render_template('edit_profile.html', form=form, user=user)

@users_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    """Eliminar usuario (solo el propio usuario)."""
    user = User.query.get_or_404(id)
    if session.get('user_id') != user.id:
        flash('No tienes permiso para eliminar este usuario.', 'danger')
        return redirect(url_for('users.index'))

    db.session.delete(user)
    db.session.commit()
    session.pop('user_id', None)  # cerrar sesión después de eliminar
    flash('Usuario eliminado.', 'info')
    return redirect(url_for('auth.login'))