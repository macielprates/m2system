from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.cliente import Cliente
from app import db

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')


@clientes_bp.route('/')
@login_required
def lista():
    busca = request.args.get('busca', '').strip()
    tipo = request.args.get('tipo', '')
    status = request.args.get('status', '')
    perfil = request.args.get('perfil', '')

    query = Cliente.query

    if busca:
        filtro = f'%{busca}%'
        query = query.filter(
            db.or_(
                Cliente.nome.ilike(filtro),
                Cliente.cpf_cnpj.ilike(filtro),
                Cliente.telefone.ilike(filtro),
                Cliente.celular.ilike(filtro),
                Cliente.email.ilike(filtro),
                Cliente.cidade.ilike(filtro),
            )
        )

    if tipo:
        query = query.filter_by(tipo=tipo)

    if status:
        query = query.filter_by(status=status)

    if perfil:
        query = query.filter(Cliente.perfis.ilike(f'%{perfil}%'))

    clientes = query.order_by(Cliente.nome).all()

    return render_template(
        'clientes/lista.html',
        clientes=clientes,
        busca=busca,
        tipo=tipo,
        status=status,
        perfil=perfil,
        pagina='clientes',
    )


@clientes_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    if request.method == 'POST':
        return _salvar_cliente(None)
    return render_template('clientes/form.html', cliente=None, pagina='clientes')


@clientes_bp.route('/<int:id>')
@login_required
def ver(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/ver.html', cliente=cliente, pagina='clientes')


@clientes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        return _salvar_cliente(cliente)
    return render_template('clientes/form.html', cliente=cliente, pagina='clientes')


@clientes_bp.route('/<int:id>/status/<novo_status>', methods=['POST'])
@login_required
def alterar_status(id, novo_status):
    if novo_status not in ('ativo', 'inativo', 'bloqueado'):
        flash('Status invalido.', 'danger')
        return redirect(url_for('clientes.ver', id=id))

    cliente = Cliente.query.get_or_404(id)
    cliente.status = novo_status
    db.session.commit()

    nomes = {'ativo': 'ativado', 'inativo': 'desativado', 'bloqueado': 'bloqueado'}
    flash(f'Cliente "{cliente.nome}" {nomes[novo_status]} com sucesso.', 'success')
    return redirect(url_for('clientes.ver', id=id))


@clientes_bp.route('/<int:id>/excluir', methods=['POST'])
@login_required
def excluir(id):
    cliente = Cliente.query.get_or_404(id)

    # TODO: Verificar vinculos com OS quando modulo estiver pronto
    # Por enquanto permite excluir qualquer cliente
    try:
        nome = cliente.nome
        db.session.delete(cliente)
        db.session.commit()
        flash(f'Cliente "{nome}" excluido permanentemente.', 'success')
        return redirect(url_for('clientes.lista'))
    except Exception as e:
        db.session.rollback()
        flash(f'Nao foi possivel excluir: este cliente possui vinculos no sistema.', 'danger')
        return redirect(url_for('clientes.ver', id=id))


# ============ RELATORIOS ============

@clientes_bp.route('/<int:id>/ficha')
@login_required
def relatorio_ficha(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/relatorio_ficha.html', cliente=cliente)


@clientes_bp.route('/relatorio/whatsapp')
@login_required
def relatorio_whatsapp():
    clientes = Cliente.query.filter(
        Cliente.status == 'ativo',
        Cliente.celular.isnot(None),
        Cliente.celular != ''
    ).order_by(Cliente.nome).all()
    return render_template('clientes/relatorio_whatsapp.html', clientes=clientes)


@clientes_bp.route('/relatorio/selecionados', methods=['POST'])
@login_required
def relatorio_selecionados():
    ids = request.form.getlist('cliente_ids')
    if not ids:
        flash('Selecione pelo menos um cliente.', 'warning')
        return redirect(url_for('clientes.lista'))
    clientes = Cliente.query.filter(Cliente.id.in_(ids)).order_by(Cliente.nome).all()
    return render_template('clientes/relatorio_selecionados.html', clientes=clientes)


# ============ FUNCOES INTERNAS ============

def _salvar_cliente(cliente):
    is_novo = cliente is None

    if is_novo:
        cliente = Cliente()
        cliente.id_usuario_cad = current_user.id
        cliente.status = 'ativo'

    # Dados basicos
    cliente.tipo = request.form.get('tipo', 'PF')
    cliente.nome = request.form.get('nome', '').strip().upper()
    cliente.nome_fantasia = request.form.get('nome_fantasia', '').strip().upper() or None
    cliente.cpf_cnpj = _limpar_documento(request.form.get('cpf_cnpj', ''))
    cliente.rg_ie = request.form.get('rg_ie', '').strip() or None

    # Perfis
    perfis_selecionados = request.form.getlist('perfis')
    if not perfis_selecionados:
        perfis_selecionados = ['cliente']
    cliente.perfis = ','.join(perfis_selecionados)

    # Contato
    cliente.telefone = _limpar_telefone(request.form.get('telefone', ''))
    cliente.celular = _limpar_telefone(request.form.get('celular', ''))
    cliente.email = request.form.get('email', '').strip().lower() or None

    # Endereco
    cliente.cep = request.form.get('cep', '').strip() or None
    cliente.logradouro = request.form.get('logradouro', '').strip().upper() or None
    cliente.numero = request.form.get('numero', '').strip() or None
    cliente.complemento = request.form.get('complemento', '').strip().upper() or None
    cliente.bairro = request.form.get('bairro', '').strip().upper() or None
    cliente.cidade = request.form.get('cidade', '').strip().upper() or None
    cliente.uf = request.form.get('uf', '').strip().upper() or None

    # Observacoes
    cliente.observacoes = request.form.get('observacoes', '').strip() or None

    # Validacoes
    if not cliente.nome:
        flash('O nome do cliente e obrigatorio.', 'danger')
        return render_template('clientes/form.html', cliente=cliente, pagina='clientes')

    if not cliente.cpf_cnpj:
        flash('O CPF/CNPJ e obrigatorio.', 'danger')
        return render_template('clientes/form.html', cliente=cliente, pagina='clientes')

    # Verificar CPF/CNPJ duplicado
    existente = Cliente.query.filter_by(cpf_cnpj=cliente.cpf_cnpj).first()
    if existente and existente.id != cliente.id:
        flash('Ja existe um cliente com este CPF/CNPJ.', 'danger')
        return render_template('clientes/form.html', cliente=cliente, pagina='clientes')

    try:
        if is_novo:
            db.session.add(cliente)
        db.session.commit()
        flash(
            f'Cliente "{cliente.nome}" {"cadastrado" if is_novo else "atualizado"} com sucesso.',
            'success'
        )
        return redirect(url_for('clientes.ver', id=cliente.id))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao salvar: {str(e)}', 'danger')
        return render_template('clientes/form.html', cliente=cliente, pagina='clientes')


def _limpar_documento(doc):
    if not doc:
        return None
    return doc.replace('.', '').replace('-', '').replace('/', '').strip() or None


def _limpar_telefone(tel):
    if not tel:
        return None
    return tel.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').strip() or None
