import { call_fetch } from "./api.js"; 

async function add_note(){
    const FormAddNote = document.getElementById('note-form-create')
    FormAddNote.addEventListener('submit', async function(event) {
        event.preventDefault();

        const data_note = new FormData(FormAddNote)
        const object_data = Object.fromEntries(data_note)
        
        const response = await call_fetch('POST', 'http://127.0.0.1:8000/notes/', {}, object_data)
        
        if(!response.ok) {
            alert('Algo salió mal')
        } else {
            alert('Agregada con éxito')
        }
        console.log(response)
    })
}

add_note() 