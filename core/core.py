from flask import Blueprint, render_template

core_bp = Blueprint('core_bp',__name__,template_folder='templates')

@core_bp.route('/')
def index():
        return render_template('core/index.html')

