from flask import Blueprint, render_template
from flask_login import login_required
from models.cliente import Cliente

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    total_clientes = Cliente.query.filter_by(status='ativo').count()

    stats = {
        'os_abertas': 0,
        'os_concluidas_mes': 0,
        'a_receber': 0,
        'contas_vencidas': 0,
        'total_clientes': total_clientes,
    }
    return render_template('dashboard/index.html', stats=stats, pagina='dashboard')
