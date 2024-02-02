btnBack = document.querySelector("#btnBack")
btnAddUser = document.querySelector('#btnAddUser')
btnEditPost = document.querySelector("#btnEditPost")
btnCancel = document.querySelector('#btnCancel')
btnAddTag = document.querySelector('#btnAddTag')
btnShowTags = document.querySelector('#btnShowTags')
btnAddPost = document.querySelector("#btnAddPost")

function addPost(){
    window.location.href="/users/{{user.id}}/posts/new"
}

btnAddPost.addEventListener('click', addPost)

function back(){
    window.location.href = "/"
}

btnBack.addEventListener('click', back)

function edit() {
    window.location.href = "/posts/{{post.id}}/edit";
}

btnEditPost.addEventListener('click', edit)

        
function cancel(){
    window.location.href = "/"
}

btnCancel.addEventListener('click', cancel)

function addUser(){
    window.location.href = '/users/new'
}

btnAddUser.addEventListener('click', addUser)

function addNewTag(){
    window.location.href = '/tags/new'
}

btnAddTag.addEventListener('click', addNewTag)


function showTags(){
    window.location.href = '/tags'

}

btnShowTags.addEventListener('click', showTags)

function addPost(){
    window.location.href="/users/{{user.id}}/posts/new"
}

btnAddPost.addEventListener('click', addPost)