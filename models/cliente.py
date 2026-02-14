from app import db
from datetime import datetime


class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(2), default='PF')  # PF, PJ, PR (Produtor Rural)
    nome = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200))
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=False)
    rg_ie = db.Column(db.String(30))

    # Status: ativo, inativo, bloqueado
    status = db.Column(db.String(20), default='ativo')

    # Perfis: cliente, tecnico, fornecedor, vendedor (separados por virgula)
    perfis = db.Column(db.String(200), default='cliente')

    # Contato
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(150))

    # Endereco
    cep = db.Column(db.String(10))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))

    # Controle
    observacoes = db.Column(db.Text)
    dt_cadastro = db.Column(db.DateTime, default=datetime.now)
    dt_alteracao = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    id_usuario_cad = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def iniciais(self):
        partes = self.nome.split()
        if len(partes) >= 2:
            return (partes[0][0] + partes[-1][0]).upper()
        return self.nome[:2].upper()

    def cpf_cnpj_formatado(self):
        doc = self.cpf_cnpj or ''
        doc = doc.replace('.', '').replace('-', '').replace('/', '')
        if len(doc) == 11:
            return f'{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:]}'
        elif len(doc) == 14:
            return f'{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:]}'
        return self.cpf_cnpj or ''

    def celular_formatado(self):
        cel = self.celular or ''
        cel = cel.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if len(cel) == 11:
            return f'{cel[:2]} {cel[2:7]}-{cel[7:]}'
        elif len(cel) == 10:
            return f'{cel[:2]} {cel[2:6]}-{cel[6:]}'
        return self.celular or ''

    def telefone_principal(self):
        return self.celular or self.telefone or ''

    def tipo_descricao(self):
        tipos = {'PF': 'Pessoa Fisica', 'PJ': 'Pessoa Juridica', 'PR': 'Produtor Rural'}
        return tipos.get(self.tipo, self.tipo)

    def status_descricao(self):
        desc = {'ativo': 'Ativo', 'inativo': 'Inativo', 'bloqueado': 'Bloqueado'}
        return desc.get(self.status, self.status)

    def lista_perfis(self):
        if not self.perfis:
            return ['cliente']
        return [p.strip() for p in self.perfis.split(',') if p.strip()]

    def perfis_descricao(self):
        nomes = {
            'cliente': 'Cliente',
            'tecnico': 'Tecnico',
            'fornecedor': 'Fornecedor',
            'vendedor': 'Vendedor',
            'transportador': 'Transportador',
        }
        return [nomes.get(p, p.capitalize()) for p in self.lista_perfis()]

    def endereco_completo(self):
        partes = []
        if self.logradouro:
            s = self.logradouro
            if self.numero:
                s += f', {self.numero}'
            if self.complemento:
                s += f' - {self.complemento}'
            partes.append(s)
        if self.bairro:
            partes.append(self.bairro)
        if self.cidade:
            s = self.cidade
            if self.uf:
                s += f'/{self.uf}'
            partes.append(s)
        return ' - '.join(partes)

    def __repr__(self):
        return f'<Cliente {self.id} - {self.nome}>'
