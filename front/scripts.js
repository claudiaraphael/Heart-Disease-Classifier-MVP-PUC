const API_URL = 'http://127.0.0.1:5000';

/*
  ─────────────────────────────────────────
  TEMA DIA / NOITE
  ─────────────────────────────────────────
*/
function toggleTheme() {
    const body = document.body;
    const moonIcon = document.getElementById('moonIcon');
    const sunIcon  = document.getElementById('sunIcon');

    if (body.classList.contains('dark')) {
        body.classList.replace('dark', 'light');
        moonIcon.style.display = 'none';
        sunIcon.style.display  = 'block';
    } else {
        body.classList.replace('light', 'dark');
        moonIcon.style.display = 'block';
        sunIcon.style.display  = 'none';
    }
}

/*
  ─────────────────────────────────────────
  CARGA INICIAL — lista todos os pacientes
  ─────────────────────────────────────────
*/
document.addEventListener('DOMContentLoaded', () => {
    loadPatients();
});

async function loadPatients() {
    try {
        const response = await fetch(`${API_URL}/pacientes`);
        const data = await response.json();
        renderTable(data.pacientes || []);
    } catch (error) {
        console.error('Erro ao carregar pacientes:', error);
    }
}

/*
  ─────────────────────────────────────────
  SUBMISSÃO DO FORMULÁRIO
  ─────────────────────────────────────────
*/
async function submitForm() {
    const name     = document.getElementById('name').value.trim();
    const age      = document.getElementById('age').value;
    const sex      = document.getElementById('sex').value;
    const cp       = document.getElementById('cp').value;
    const trestbps = document.getElementById('trestbps').value;
    const chol     = document.getElementById('chol').value;
    const fbs      = document.getElementById('fbs').value;
    const restecg  = document.getElementById('restecg').value;
    const thalach  = document.getElementById('thalach').value;
    const exang    = document.getElementById('exang').value;
    const oldpeak  = document.getElementById('oldpeak').value;
    const slope    = document.getElementById('slope').value;
    const ca       = document.getElementById('ca').value;
    const thal     = document.getElementById('thal').value;

    // Validação básica
    if (!name) {
        alert('Por favor, informe o nome do paciente.');
        return;
    }

    const fields = { age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal };
    for (const [key, val] of Object.entries(fields)) {
        if (val === '' || val === null || val === undefined) {
            alert(`Por favor, preencha todos os campos clínicos.`);
            return;
        }
    }

    const formData = new FormData();
    formData.append('name',     name);
    formData.append('age',      age);
    formData.append('sex',      sex);
    formData.append('cp',       cp);
    formData.append('trestbps', trestbps);
    formData.append('chol',     chol);
    formData.append('fbs',      fbs);
    formData.append('restecg',  restecg);
    formData.append('thalach',  thalach);
    formData.append('exang',    exang);
    formData.append('oldpeak',  oldpeak);
    formData.append('slope',    slope);
    formData.append('ca',       ca);
    formData.append('thal',     thal);

    try {
        const response = await fetch(`${API_URL}/paciente`, {
            method: 'POST',
            body: formData,
        });

        if (response.status === 409) {
            alert('Já existe um paciente com esse nome. Utilize um nome diferente.');
            return;
        }

        if (!response.ok) {
            alert('Erro ao processar a requisição. Tente novamente.');
            return;
        }

        const data = await response.json();
        showResult(data);
        clearForm();
        loadPatients();

    } catch (error) {
        console.error('Erro na requisição:', error);
        alert('Não foi possível conectar ao servidor. Verifique se a API está rodando.');
    }
}

/*
  ─────────────────────────────────────────
  EXIBE O CARD DE RESULTADO
  ─────────────────────────────────────────
*/
function showResult(data) {
    const card    = document.getElementById('resultCard');
    const content = document.getElementById('resultContent');

    const isHigh = data.outcome === 1;

    card.className = 'card result-card ' + (isHigh ? 'result-high' : 'result-low');
    card.style.display = 'block';

    content.innerHTML = isHigh
        ? `
            <span class="result-icon">⚠</span>
            <p class="result-title">Alta probabilidade de doença cardíaca</p>
            <p class="result-desc">
                O modelo identificou indicadores clínicos associados a risco elevado de doença cardíaca
                para o paciente <strong>${data.name}</strong>.
                Recomenda-se avaliação médica especializada.
            </p>
          `
        : `
            <span class="result-icon">✓</span>
            <p class="result-title">Baixa probabilidade de doença cardíaca</p>
            <p class="result-desc">
                O modelo não identificou indicadores clínicos significativos de risco cardíaco
                para o paciente <strong>${data.name}</strong>.
                Manutenção de acompanhamento preventivo regular é recomendada.
            </p>
          `;

    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

/*
  ─────────────────────────────────────────
  RENDERIZA A TABELA DE HISTÓRICO
  ─────────────────────────────────────────
*/
function renderTable(pacientes) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    if (pacientes.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="empty-state">
                    Nenhum paciente cadastrado ainda.
                </td>
            </tr>`;
        return;
    }

    pacientes.forEach(p => {
        const isHigh  = p.outcome === 1;
        const sexLabel = p.sex === 1 ? 'Masculino' : 'Feminino';
        const badge   = isHigh
            ? `<span class="badge badge-high">Alto risco</span>`
            : `<span class="badge badge-low">Baixo risco</span>`;

        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${p.name}</td>
            <td>${p.age}</td>
            <td>${sexLabel}</td>
            <td>${p.trestbps} mmHg</td>
            <td>${p.chol} mg/dl</td>
            <td>${p.thalach} bpm</td>
            <td>${badge}</td>
            <td>
                <button class="btn-delete" onclick="deletePatient('${p.name}')" title="Remover paciente">×</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

/*
  ─────────────────────────────────────────
  DELETAR PACIENTE
  ─────────────────────────────────────────
*/
async function deletePatient(name) {
    if (!confirm(`Remover o paciente "${name}" do histórico?`)) return;

    try {
        const response = await fetch(`${API_URL}/paciente?name=${encodeURIComponent(name)}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            loadPatients();
        } else {
            alert('Erro ao remover paciente.');
        }
    } catch (error) {
        console.error('Erro ao deletar paciente:', error);
        alert('Não foi possível conectar ao servidor.');
    }
}

/*
  ─────────────────────────────────────────
  LIMPAR FORMULÁRIO
  ─────────────────────────────────────────
*/
function clearForm() {
    const ids = ['name', 'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'];
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el.tagName === 'SELECT') el.selectedIndex = 0;
        else el.value = '';
    });
}