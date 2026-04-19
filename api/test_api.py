import pytest
import json
from app import app
from model import Session, Paciente

# Para rodar: pytest -v test_api.py


@pytest.fixture
def client():
    """Configura o cliente de teste para a aplicação Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_patient_data():
    """Dados de exemplo de um paciente para os testes."""
    return {
        "name":     "João Silva",
        "age":      52,
        "sex":      1,
        "cp":       0,
        "trestbps": 125,
        "chol":     212,
        "fbs":      0,
        "restecg":  1,
        "thalach":  168,
        "exang":    0,
        "oldpeak":  1.0,
        "slope":    2,
        "ca":       2,
        "thal":     3,
    }


def test_home_redirect(client):
    """Testa se a rota home redireciona para o frontend."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/front/index.html' in response.location


def test_docs_redirect(client):
    """Testa se a rota docs redireciona para o openapi."""
    response = client.get('/docs')
    assert response.status_code == 302
    assert '/openapi' in response.location


def test_get_pacientes_empty(client):
    """Testa a listagem de pacientes quando não há nenhum."""
    response = client.get('/pacientes')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'pacientes' in data
    assert isinstance(data['pacientes'], list)


def test_add_patient_prediction(client, sample_patient_data):
    """Testa a adição de um paciente e a predição de doença cardíaca."""
    # Limpa paciente existente com o mesmo nome, se houver
    session = Session()
    existing = session.query(Paciente).filter(
        Paciente.name == sample_patient_data['name']
    ).first()
    if existing:
        session.delete(existing)
        session.commit()
    session.close()

    response = client.post(
        '/paciente',
        data=json.dumps(sample_patient_data),
        content_type='application/json'
    )

    assert response.status_code == 200
    data = json.loads(response.data)

    # Verifica se todos os campos foram salvos corretamente
    assert data['name']     == sample_patient_data['name']
    assert data['age']      == sample_patient_data['age']
    assert data['sex']      == sample_patient_data['sex']
    assert data['cp']       == sample_patient_data['cp']
    assert data['trestbps'] == sample_patient_data['trestbps']
    assert data['chol']     == sample_patient_data['chol']
    assert data['fbs']      == sample_patient_data['fbs']
    assert data['restecg']  == sample_patient_data['restecg']
    assert data['thalach']  == sample_patient_data['thalach']
    assert data['exang']    == sample_patient_data['exang']
    assert data['oldpeak']  == sample_patient_data['oldpeak']
    assert data['slope']    == sample_patient_data['slope']
    assert data['ca']       == sample_patient_data['ca']
    assert data['thal']     == sample_patient_data['thal']

    # Verifica se a predição foi realizada (0 = sem doença, 1 = com doença)
    assert 'outcome' in data
    assert data['outcome'] in [0, 1]


def test_add_duplicate_patient(client, sample_patient_data):
    """Testa que não é possível adicionar um paciente com nome duplicado."""
    client.post(
        '/paciente',
        data=json.dumps(sample_patient_data),
        content_type='application/json'
    )

    response = client.post(
        '/paciente',
        data=json.dumps(sample_patient_data),
        content_type='application/json'
    )

    assert response.status_code == 409
    data = json.loads(response.data)
    assert 'message' in data
    assert 'já existente' in data['message']


def test_get_patient_by_name(client, sample_patient_data):
    """Testa a busca de um paciente pelo nome."""
    client.post(
        '/paciente',
        data=json.dumps(sample_patient_data),
        content_type='application/json'
    )

    response = client.get(f'/paciente?name={sample_patient_data["name"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == sample_patient_data['name']


def test_get_nonexistent_patient(client):
    """Testa a busca de um paciente que não existe na base."""
    response = client.get('/paciente?name=PacienteInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'mesage' in data


def test_delete_patient(client, sample_patient_data):
    """Testa a remoção de um paciente pelo nome."""
    client.post(
        '/paciente',
        data=json.dumps(sample_patient_data),
        content_type='application/json'
    )

    response = client.delete(f'/paciente?name={sample_patient_data["name"]}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'removido com sucesso' in data['message']


def test_delete_nonexistent_patient(client):
    """Testa a remoção de um paciente que não existe na base."""
    response = client.delete('/paciente?name=PacienteInexistente')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'message' in data


def test_prediction_edge_cases(client):
    """Testa casos extremos de valores para a predição."""
    # Paciente com valores mínimos típicos do dataset
    min_data = {
        "name":     "Paciente Minimo",
        "age":      29,
        "sex":      0,
        "cp":       0,
        "trestbps": 94,
        "chol":     126,
        "fbs":      0,
        "restecg":  0,
        "thalach":  71,
        "exang":    0,
        "oldpeak":  0.0,
        "slope":    0,
        "ca":       0,
        "thal":     1,
    }

    response = client.post(
        '/paciente',
        data=json.dumps(min_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    assert data['outcome'] in [0, 1]

    # Paciente com valores máximos típicos do dataset
    max_data = {
        "name":     "Paciente Maximo",
        "age":      77,
        "sex":      1,
        "cp":       3,
        "trestbps": 200,
        "chol":     564,
        "fbs":      1,
        "restecg":  2,
        "thalach":  202,
        "exang":    1,
        "oldpeak":  6.2,
        "slope":    2,
        "ca":       3,
        "thal":     3,
    }

    response = client.post(
        '/paciente',
        data=json.dumps(max_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'outcome' in data
    assert data['outcome'] in [0, 1]


def cleanup_test_patients():
    """Limpa os pacientes criados durante os testes."""
    session = Session()
    test_patients = session.query(Paciente).filter(
        Paciente.name.in_(['João Silva', 'Paciente Minimo', 'Paciente Maximo'])
    ).all()
    for patient in test_patients:
        session.delete(patient)
    session.commit()
    session.close()


def test_cleanup():
    """Limpa os dados de teste do banco."""
    cleanup_test_patients()