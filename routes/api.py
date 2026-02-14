from flask import Blueprint, jsonify
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect
import requests

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/cep/<cep>')
@login_required
def buscar_cep(cep):
    """Proxy para ViaCEP - evita problemas de CORS"""
    cep_limpo = cep.replace('-', '').replace('.', '').strip()
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return jsonify({'erro': True, 'msg': 'CEP invalido'}), 400

    try:
        r = requests.get(f'https://viacep.com.br/ws/{cep_limpo}/json/', timeout=10)
        data = r.json()
        if data.get('erro'):
            return jsonify({'erro': True, 'msg': 'CEP nao encontrado'}), 404
        return jsonify({
            'erro': False,
            'logradouro': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'uf': data.get('uf', ''),
        })
    except Exception as e:
        return jsonify({'erro': True, 'msg': f'Erro na busca: {str(e)}'}), 500


@api_bp.route('/cnpj/<cnpj>')
@login_required
def buscar_cnpj(cnpj):
    """Proxy para BrasilAPI - busca dados do CNPJ"""
    cnpj_limpo = cnpj.replace('.', '').replace('/', '').replace('-', '').strip()
    if len(cnpj_limpo) != 14 or not cnpj_limpo.isdigit():
        return jsonify({'erro': True, 'msg': 'CNPJ invalido'}), 400

    try:
        r = requests.get(f'https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}', timeout=15)
        if r.status_code != 200:
            # Tenta API alternativa (ReceitaWS)
            r2 = requests.get(f'https://receitaws.com.br/v1/cnpj/{cnpj_limpo}', timeout=15)
            if r2.status_code == 200:
                data2 = r2.json()
                if data2.get('status') == 'ERROR':
                    return jsonify({'erro': True, 'msg': 'CNPJ nao encontrado'}), 404
                return jsonify({
                    'erro': False,
                    'razao_social': data2.get('nome', ''),
                    'nome_fantasia': data2.get('fantasia', ''),
                    'telefone': data2.get('telefone', ''),
                    'email': data2.get('email', ''),
                    'cep': data2.get('cep', '').replace('.', ''),
                    'logradouro': data2.get('logradouro', ''),
                    'numero': data2.get('numero', ''),
                    'complemento': data2.get('complemento', ''),
                    'bairro': data2.get('bairro', ''),
                    'cidade': data2.get('municipio', ''),
                    'uf': data2.get('uf', ''),
                })
            return jsonify({'erro': True, 'msg': 'CNPJ nao encontrado'}), 404

        data = r.json()
        return jsonify({
            'erro': False,
            'razao_social': data.get('razao_social', ''),
            'nome_fantasia': data.get('nome_fantasia', ''),
            'telefone': data.get('ddd_telefone_1', ''),
            'email': data.get('email', ''),
            'cep': str(data.get('cep', '')).replace('.', ''),
            'logradouro': data.get('logradouro', ''),
            'numero': data.get('numero', ''),
            'complemento': data.get('complemento', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('municipio', ''),
            'uf': data.get('uf', ''),
        })
    except Exception as e:
        return jsonify({'erro': True, 'msg': f'Erro na busca: {str(e)}'}), 500
