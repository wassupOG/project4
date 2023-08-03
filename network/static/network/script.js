function like (button) {
    const id = button.dataset.id
    const data = {'id': id}

    fetch('/update_likes', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {

        if (result.status === 'login_required') {
            alert('You must be logged in to like posts!')
            return
        }

        const likesDiv = button.lastElementChild
        let likes = parseInt(likesDiv.innerText)

        if (result.status === 'liked') {
            likes += 1
            button.classList.remove('unliked')
            button.classList.add('liked')
        } else if (result.status === 'unliked') {
            likes -= 1
            button.classList.remove('liked')
            button.classList.add('unliked')
        }
        
        likesDiv.innerText = likes
    })
    .catch(error => {
        console.error('Error:', error)
        alert('Log in to like posts!')
    });
}


function post (event) {
    event.preventDefault();
    const id = document.querySelector('#user-id').dataset.id;
    const text = document.querySelector('#post-text').value;

    if (text.trim() === '') {
        alert("Post can't be empty!")
        return
    }

    const data = { 'user_id': id, 'text': text };

    fetch('/submit_post', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            // Clear the textarea after successful submission
            document.getElementById('post-text').value = '';

            // Create a new div for the new post
            const newPostDiv = document.createElement('div');
            newPostDiv.className = 'post';
            newPostDiv.innerHTML = `
            <div class="user-post abs"><a href="#">${result.username}</a></div>
                <div>${result.text}</div>
                    <div class="like-btn abs unliked" data-id="${result.id}">
                        <svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                            <g fill="none" fill-rule="evenodd"><path d="M0 0h24v24H0z"></path><path d="M16 4a5.95 5.95 0 0 0-3.89 1.7l-.12.11-.12-.11A5.96 5.96 0 0 0 7.73 4 5.73 5.73 0 0 0 2 9.72c0 3.08 1.13 4.55 6.18 8.54l2.69 2.1c.66.52 1.6.52 2.26 0l2.36-1.84.94-.74c4.53-3.64 5.57-5.1 5.57-8.06A5.73 5.73 0 0 0 16.27 4zm.27 1.8a3.93 3.93 0 0 1 3.93 3.92v.3c-.08 2.15-1.07 3.33-5.51 6.84l-2.67 2.08a.04.04 0 0 1-.04 0L9.6 17.1l-.87-.7C4.6 13.1 3.8 11.98 3.8 9.73A3.93 3.93 0 0 1 7.73 5.8c1.34 0 2.51.62 3.57 1.92a.9.9 0 0 0 1.4-.01c1.04-1.3 2.2-1.91 3.57-1.91z" fill="currentColor" fill-rule="nonzero"></path></g>
                        </svg><div class="like-count">${result.likes}</div>
                    </div>
                    <div class="abs date-post">${result.date}</div>
            </div>
            `;

            // Get the first post in the container
            const firstPost = document.querySelector('.post');

            // Insert the new post before the first post in the container
            document.querySelector('#posts-container').insertBefore(newPostDiv, firstPost);

            const newButton = document.querySelector('.like-btn')
            newButton.addEventListener('click', () => {
                like(newButton)
            })

        }
    })
    .catch(error => console.error('Error:', error));
}


function follow (event) {
    const element = event.target
    const following_id = element.dataset.id
    const data = {'following_id': following_id}

    fetch('/follow', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {

        if (result.status === 'login_required') {
            alert('You must be logged in to follow users!')
            return
        }

        const followPlate = document.querySelector('#follow-plate')
        const followers = document.querySelector('#followers-count')
        const following = document.querySelector('#following-count')

        if (result.status === 'followed') {
            element.innerText = 'Unfollow'
        } else if (result.status === 'unfollowed') {
            element.innerText = 'Follow'
        }

        followers.innerHTML = `<b>${result.followers_count}</b> followers`
        following.innerHTML = `<b>${result.following_count}</b> following`
        
    })
    .catch(error => {
        console.error('Error:', error)
    });
}


function edit (event) {
    const editLink = event.target
    const post_id = editLink.dataset.id
    const data = {'post_id': post_id}

    fetch('/edit', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Get div with text
        const postedText = document.querySelector(`#text_${post_id}`)

        // Create, populate & sty;e textarea
        const textarea = document.createElement('textarea');
        textarea.value = postedText.innerText;
        textarea.classList.add('textarea-style')

        // Insert & toggle visibility of div
        const ParentElement = postedText.parentNode
        ParentElement.insertBefore(textarea, postedText)
        postedText.style.display = 'none'
        
        // Insert & toggle visibility of 'edit'
        const editParent = editLink.parentNode
        const saveLink = document.createElement('a')
        saveLink.innerText = 'Save'
        editParent.insertBefore(saveLink, editLink)
        editLink.style.display = 'none'

        saveLink.addEventListener('click', () => {
            const updatedText = textarea.value
            const newData = {'updated_text': updatedText, 'post_id': post_id}
            fetch('/save', {
                method: 'POST',
                body: JSON.stringify(newData)
            })
            .then(response => response.json())
            .then(result => {
                postedText.innerText = updatedText
                textarea.remove()
                saveLink.remove()
                postedText.style.display = 'block'
                editLink.style.display = 'block'
            })
            .catch(error => {console.log('Error:', error)})
        })
    })
    .catch(error => {
        console.error('Error:', error)
    });
}



document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', () => {
        like(button)
    })
})


/*
function pagination (event) {
    // Buttons
    const prevBtn = document.querySelector('#previous-btn')
    const nextBtn = document.querySelector('#next-btn')
    const pressedButton = event.target

    // Content container
    const postsContainer = document.querySelector('#posts-container')

    // Div with info
    const divTracker = document.querySelector('#current-page')
    let pageNumber = parseInt(divTracker.dataset.page)
    let maxPages = parseInt(divTracker.dataset.max)

    if (pressedButton.id === 'next-btn') {
        pageNumber += 1
    } else {
        pageNumber -= 1
    }

    divTracker.dataset.page = pageNumber
    data = pageNumber

    fetch('/pagination', {
        method: 'POST',
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(posts => {
        postsContainer.innerHTML = ``
        // Toggle visibility of 'Previous'
        if (pageNumber > 1) {
            prevBtn.style.display = 'block'
        } else {
            prevBtn.style.display = 'none'
        }

        if (pageNumber === maxPages) {
            nextBtn.style.display = 'none'
        } else {
            nextBtn.style.display = 'block'
        }
    })
    .catch(error => {
        console.error('Error:', error)
    });
}
*/


