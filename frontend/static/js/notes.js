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

async function get_notes() {
    const response = await call_fetch('GET', 'http://127.0.0.1:8000/notes/', {})
    console.log(response)
    const list = document.getElementById('notes-list')
    list.innerHTML = ''

    response.data.forEach(note => {
        const clone = document.getElementById('note-item-template').content.cloneNode(true)
        clone.querySelector('.note-item-title').textContent = note.title
        clone.querySelector('.note-item-content').textContent = note.content

        list.appendChild(clone)
    });
}

add_note() 
get_notes()