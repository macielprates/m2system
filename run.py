from app import create_app

app = create_app()

if __name__ == '__main__':
    print()
    print('=' * 50)
    print('  M2 INFORMATICA - Sistema de Gestao')
    print('  Abra no navegador: http://localhost:5000')
    print('=' * 50)
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
