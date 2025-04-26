from flask import Blueprint, render_template, redirect, session, current_app, request
from datetime import datetime
from app.utils import admin_required, get_logger

logger = get_logger(__name__)

bp = Blueprint('admin_routes', __name__, url_prefix='/admin', template_folder='templates')

"""
Admin Module Routes:
- Display failed login attempts
- Manage pending user account approvals
- Restrict access to admin users only
"""

@bp.route('/', methods=['GET', 'POST'])
@admin_required
def admin_panel():
    db = current_app.get_db()

    if request.method == 'POST':
        selected_users = request.form.getlist('activate')
        for username in selected_users:
            db.execute("UPDATE User SET Account_Active = 1 WHERE UserName = ?", (username,))
            logger.info("Activated account: %s", username)
        db.commit()
        return redirect('/admin/')

    failed_logins = db.execute("SELECT UserName, Num_Login_attempts FROM User WHERE Num_Login_attempts > 0").fetchall()
    pending_users = db.execute("SELECT UserName FROM User WHERE Account_Active = 0").fetchall()

    return render_template("ho_admin.html", failed_logins=failed_logins, pending_users=pending_users)