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
            get_notes()
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
        const item = clone.querySelector('.note-item')
        const titleItem = clone.querySelector('.note-item-title')
        const contentItem = clone.querySelector('.note-item-content')

        titleItem.textContent = note.title
        contentItem.textContent = note.content

        const BtnEdit = clone.querySelector('.note-item-edit-btn')
        const BtnDelete = clone.querySelector('.note-item-delete-btn')
        const BtnCancel = clone.querySelector('.note-item-cancel-btn')
        const FormEdit = clone.querySelector('.note-item-edit-form')

        const inputTitleEdit = clone.querySelector('.note-item-edit-title-input')
        const inputContentEdit = clone.querySelector('.note-item-edit-content-input')

        BtnEdit.addEventListener('click', function(){
            inputTitleEdit.value = note.title
            inputContentEdit.value = note.content
            item.classList.add('is-editing')
        })

        BtnCancel.addEventListener('click', function(){
            item.classList.remove('is-editing')
        })

        FormEdit.addEventListener('submit', async function(event){
            event.preventDefault();
            const objeto = {
                'title': inputTitleEdit.value, 
                'content': inputContentEdit.value
            }
            
            const response = await edit_note(note.id, objeto)
            
            item.classList.remove('is-editing')

            if(!response.ok) {
            alert('Algo salió mal')
        } else {
            titleItem.textContent = inputTitleEdit.value
            contentItem.textContent = inputContentEdit.value

            note.title = titleItem.textContent
            note.content = contentItem.textContent
            alert('Editada con éxito')
        }
            console.log(response)
        })

        BtnDelete.addEventListener('click', async function () {
            const response = await delete_note(note.id)
            
            if(!response.ok) {
            alert('Algo salió mal')
        } else {
            item.remove()
            alert('Eliminada con éxito')
        }
            console.log(response)
        })

        list.appendChild(clone)
    });
}

async function edit_note(note_id, body) {
    return await call_fetch('PATCH', `http://127.0.0.1:8000/notes/${note_id}`, {}, body)
}

async function delete_note(note_id) {
    return await call_fetch('DELETE', `http://127.0.0.1:8000/notes/${note_id}`)
}

add_note()
get_notes()