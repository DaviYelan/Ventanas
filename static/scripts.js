// scripts.js

function generateAttention(ventanilla) {
    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ventanilla: ventanilla })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al generar atenciones');
            }
            return response.json();
        })
        .then(data => {
            const resultsDiv = document.querySelector(`#ventanilla-${ventanilla} .results`);
            resultsDiv.innerHTML = '';
            data.new_attentions.forEach(attention => {
                resultsDiv.innerHTML += `<p>${attention.user.name} - ${attention.user.action} (${attention.duration}s) - Nota: ${attention.nota}</p>`;
            });
            document.getElementById(`total-persons-${ventanilla}`).innerText = data.total_persons;
            document.getElementById(`total-time-${ventanilla}`).innerText = data.total_time;
            document.getElementById(`final-nota-${ventanilla}`).innerText = data.final_nota;
            document.getElementById(`generate-${ventanilla}`).disabled = true;
        })
        .catch(error => alert(error.message));
}

function saveAttention(ventanilla) {
    const totalPersons = document.getElementById(`total-persons-${ventanilla}`).innerText;
    const totalTime = document.getElementById(`total-time-${ventanilla}`).innerText;
    const finalNota = document.getElementById(`final-nota-${ventanilla}`).innerText;

    fetch('/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ventanilla: ventanilla, total_persons: totalPersons, total_time: totalTime, final_nota: finalNota })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al guardar atención');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            const recordsTable = document.getElementById(`records-${ventanilla}`);
            const newRow = document.createElement('tr');
            newRow.innerHTML = `
            <td>${data.day}</td>
            <td>${totalPersons}</td>
            <td>${totalTime}</td>
            <td>${finalNota}</td>
            <td>${new Date().toLocaleDateString()}</td>
        `;
            recordsTable.appendChild(newRow);
            document.getElementById(`total-persons-${ventanilla}`).innerText = '0';
            document.getElementById(`total-time-${ventanilla}`).innerText = '0';
            document.getElementById(`final-nota-${ventanilla}`).innerText = 'N/A';
            document.querySelector(`#ventanilla-${ventanilla} .results`).innerHTML = '';
            document.getElementById(`generate-${ventanilla}`).disabled = false;
            newRow.addEventListener('click', () => {
                deleteAttention(ventanilla, data.day, newRow);
            });
        })
        .catch(error => alert(error.message));
}

function deleteAllAttention(ventanilla) {
    fetch('/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ventanilla: ventanilla })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al eliminar todas las atenciones');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            document.querySelector(`#ventanilla-${ventanilla} .results`).innerHTML = '';
            document.getElementById(`total-persons-${ventanilla}`).innerText = '0';
            document.getElementById(`total-time-${ventanilla}`).innerText = '0';
            document.getElementById(`final-nota-${ventanilla}`).innerText = 'N/A';
            document.getElementById(`generate-${ventanilla}`).disabled = false;
            document.getElementById(`records-${ventanilla}`).innerHTML = '';
        })
        .catch(error => alert(error.message));
}

function deleteAttention(ventanilla, day, row) {
    if (confirm("¿Seguro que deseas eliminar esta fila?")) {
        fetch('/delete_record', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ventanilla: ventanilla, day: day })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al eliminar el registro');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message);
                row.remove();
            })
            .catch(error => alert(error.message));
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.records tbody tr').forEach(row => {
        const ventanilla = row.closest('.ventanilla').id.split('-')[1];
        const day = row.children[0].innerText;
        row.addEventListener('click', () => {
            deleteAttention(ventanilla, day, row);
        });
    });
});
