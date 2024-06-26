const categoryCreateForm = document.getElementById("create-category");
const book_privateCreateForm = document.getElementById("create-book-private");



function parseJwt (token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
}


async function refreshTokenPair(callback) {
    const refreshToken = localStorage.getItem("refreshToken");
    if (refreshToken === undefined || refreshToken === null) {
        window.location.href = "/login";
    }
    try {
        const refreshTokenPayload = parseJwt(refreshToken);
        if (Date.now() >= refreshTokenPayload.exp * 1000) {
            localStorage.removeItem("refreshToken");
            window.location.href = "/login";
        }
    } catch (e) {
        window.location.href = "/login";
    }

    const response = await api.auth.refresh({refresh_token: refreshToken});
    if (response === undefined || response === null) {
        window.location.href = "/login";
    } else {
        localStorage.setItem("accessToken", response.data.access_token);
        localStorage.setItem("refreshToken", response.data.refresh_token);
        localStorage.setItem("tokenType", response.data.token_type);

        if (callback !== undefined) {
            await callback()
        }
    }

}


async function getAccessToken() {
   let accessToken = localStorage.getItem("accessToken");
    if (accessToken === undefined || accessToken === null) {
        await refreshTokenPair()
    }
    try {
        const accessTokenPayload = parseJwt(accessToken);
        if (Date.now() >= accessTokenPayload.exp * 1000) {
            localStorage.removeItem("accessToken");
            await refreshTokenPair()
        }
    } catch (e) {
        await refreshTokenPair()
    }
   accessToken = localStorage.getItem("accessToken");

   return accessToken
}




categoryCreateForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const categoryNameInput = document.getElementById("categoryName");
    const accessToken = await getAccessToken()
    const tokenType = localStorage.getItem("tokenType");
    const response = await api.v1.categories.create({name: categoryNameInput.value}, {Autharization: `${tokenType} ${accessToken}`})
    console.log(categoryNameInput.value)
    console.log(response)
    if (response !== undefined) {
        console.log("Category created:", categoryName.value)
        categoryNameInput.value ="";
        await renderCategoryDropdownList()
    } else {
        console.error("Failed to create category");
    }
});


//book_privateCreateForm.addEventListener("submit", async (e) => {
//    e.preventDefault();
//    const book_privateTitleInput = document.getElementById("book_privateTitle");
//    const book_privateAuthorInput = document.getElementById("book_privateAuthor");
//    const book_privateCategory_idInput = document.getElementById("book_privateCategory_id");
//    const book_privateGeneral_book_idInput = document.getElementById("book_privateGeneral_book_id");
////    const book_privatecreated_atInput = document.getElementById("book_privatecreated_at");
//    const book_privatepictureInput = document.getElementById("book_privatepicture");
//    const book_privateuser_emailInput = document.getElementById("book_privateuser_email");
//
//    const accessToken = await getAccessToken()
//    const tokenType = localStorage.getItem("tokenType");
//    const response = await api.v1.books_private.create({title: book_privateTitleInput.value,
//                                                        author: book_privateAuthorInput.value,
//                                                        category_id: book_privateCategory_idInput.value,
//                                                        general_book_id: book_privateGeneral_book_idInput.value,
////                                                        created_at: book_privatecreated_atInput.value,
//                                                        picture: book_privatepictureInput.value,
//                                                        user_email: book_privateuser_emailInput.value,
//                                                        },
//                                                        {Autharization: `${tokenType} ${accessToken}`})
//    console.log(book_privateTitleInput.value)
//    console.log(response)
//    if (response !== undefined) {
//        console.log("Book created:", book_privateTitle.value)
//        book_privateTitleInput.value ="";
//        book_privateAuthorInput.value ="";
//        book_privateCategory_idInput.value ="";
//        book_privateGeneral_book_idInput.value ="";
////        book_privatecreated_atInput.value ="";
//        book_privatepictureInput.value ="";
//        book_privateuser_emailInput.value ="";
////        await renderCategoryDropdownList()
//    } else {
//        console.error("Failed to create book");
//    }
//});

book_privateCreateForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const book_privateTitleInput = document.getElementById("book_privateTitle");
    const book_privateAuthorInput = document.getElementById("book_privateAuthor");
    const book_privateCategory_idInput = document.getElementById("book_privateCategory_id");
    const book_privateGeneral_book_idInput = document.getElementById("book_privateGeneral_book_id");
//    const book_privateSlugInput = document.getElementById("book_privateSlug");

    const accessToken = await getAccessToken();
    const tokenType = localStorage.getItem("tokenType");

    const bookData = {
        title: book_privateTitleInput.value,
        author: book_privateAuthorInput.value,
        category_id: parseInt(book_privateCategory_idInput.value),
        general_book_id: parseInt(book_privateGeneral_book_idInput.value),
//        slug: book_privateSlugInput.value,
    };

    try {
        const response = await api.v1.books_private.create(bookData, {Autharization: `${tokenType} ${accessToken}`});
        console.log(bookData)
        console.log(response)
        console.log(tokenType)
        console.log(accessToken)
        if (response !== undefined) {
            console.log("Book created:", book_privateTitleInput.value);
            book_privateTitleInput.value = "";
            book_privateAuthorInput.value = "";
            book_privateCategory_idInput.value = "";
            book_privateGeneral_book_idInput.value = "";
//            book_privateSlugInput.value = "";
            var modal = bootstrap.Modal.getInstance(document.getElementById('modal-report2'));
            modal.hide();
        } else {
            console.error("Failed to create book on");
        }
    } catch (error) {
        console.error("Failed to create book", error);
    }
});


async function renderGeneralBookCards(slug) {
    const response = await api.v1.categories.detail(slug);
    if (response) {
        const contentDiv = document.getElementById("general-books-list");
        contentDiv.innerHTML = "";
        response.general_books.forEach(function (general_book) {
            const card = document.createElement('div');
            card.classList.add('col-12', 'mb-3');
            card.innerHTML = `
                <button class="card btn btn-link text-left p-0">
                    <div class="card-body">
                        <h3 class="card-title">НАЗВАНИЕ: ${general_book.title}</h3>
                        <p class="text-secondary">АВТОР: ${general_book.author}</p>
                        <div class="tags">
                            ТЭГИ: ${general_book.tags_general.map(tag => `<span class="tag">${tag.name}</span>`).join(' ')}
                        </div>
                    </div>
                </button>`;

            card.querySelector('.card').addEventListener('click', () => {
                const title = encodeURIComponent(general_book.title);
                const author = encodeURIComponent(general_book.author);
                const slug = encodeURIComponent(general_book.slug);
                window.location.href = `/${slug}?title=${title}&author=${author}`;
            });

            contentDiv.appendChild(card);
        });
    }
}



async function renderBookPrivateCards(title, author, slug) {
    const response = await api.v1.books_private.detail(title, author, slug);
    if (response) {
        const contentDiv = document.getElementById("books-private-list");
        contentDiv.innerHTML = "";
        response.books_private.forEach(function (book_private) {
            const card = document.createElement('div');
            card.classList.add('col-12', 'mb-3');
            card.innerHTML = `
                <div class="card">
                    <div class="card-body">
                        <h3 class="card-title">НАЗВАНИЕ КНИГИ: ${book_private.title}</h3>
                        <p class="text-secondary">АВТОР КНИГИ: ${book_private.author}</p>
                        <p class="text-secondary">ПОЛЬЗОВАТЕЛЬ: ${book_private.user_id}</p>
                        <div class="tags">
                            ТЭГИ: ${book_private.tags_private.map(tag => `<span class="tag">${tag.name}</span>`).join(' ')}
                        </div>
                    </div>
                </div>`;
            contentDiv.appendChild(card);
        });
    }
}






async function renderCategoryDropdownList() {
    const response = await api.v1.categories.list();
    if (response.status === 200) {
        let categoryDropdown = document.getElementById("category-dropdown-list");
        categoryDropdown.innerHTML = "";
        response.data.forEach(function (category) {
            const categoryLink = document.createElement("a");
            categoryLink.className = "dropdown-item";
            categoryLink.setAttribute("rel", "noopener");
            categoryLink.href = `/${category.slug}`;
            categoryLink.textContent = category.name;
//            categoryLink.addEventListener("click", async (event) => {
//                await renderCategoryDetail(category.slug);
//            });
            console.log(category.slug)
            categoryDropdown.appendChild(categoryLink);
        });
    }
}



document.addEventListener("DOMContentLoaded", async () => {
    await getAccessToken();
    await renderCategoryDropdownList();
    let categorySlug = document.location.pathname.split("/")[1];
    console.log(categorySlug)
    let searchParams = new URLSearchParams(window.location.search);
    let title = searchParams.get("title");
    let author = searchParams.get("author");
//    let slug = searchParams.get("slug");
//    general_bookLink.href = `/${general_book.slug}`

    if (categorySlug) {
        try {
            await renderGeneralBookCards(categorySlug);
            if (title && author) {
                try {
                    await renderBookPrivateCards(title, author);
                } catch (e) {
                    console.error("Failed to render private book cards:", e);
                }
            }

        } catch (e) {
            console.error("Failed to render general book cards:", e);
        }
    }
});







//document.addEventListener("DOMContentLoaded", async () => {
//    await getAccessToken()
//    await renderGeneralBookCards();
//    let general_bookSlug = document.location.pathname.split("/")[1];
//    if (general_bookSlug) {
//        try {
//            await renderBookPrivateCards(general_bookSlug);
//        } catch (e) {
//            console.error("Failed to render book private cards:", e);
//        }
//    }
//});


//categoryCreateForm.addEventListener("submit", async (e) => {
//    e.preventDefault();
//
//    const categoryNameInput = document.getElementById("categoryName");
//    const categoryName = categoryNameInput.value.trim();
//
//    if (categoryName === "") {
//        console.error("Category name cannot be empty");
//        return;
//    }
//
//    const accessToken = await getAccessToken();
//    const tokenType = localStorage.getItem("tokenType");
//
//    try {
//        const response = await api.v1.categories.create(
//            { name: categoryName },
//            { Authorization: `${tokenType} ${accessToken}` }
//        );
//
//        if (response !== undefined) {
//            categoryNameInput.value = "";
//            await renderCategoryDropdownList();
//        }
//    } catch (e) {
//        console.error("Failed to create category:", e);
//    }
//})

//async function renderGeneralBookCards(slug) {
//    const response = await api.v1.categories.detail(slug);
//    if (response) {
//        const contentDiv = document.getElementById("general-books-list");
//        contentDiv.innerHTML = "";
//        response.general_books.forEach(function (general_book) {
//            const card = document.createElement('div');
//            card.classList.add('col-12', 'mb-3');
//            card.innerHTML = `<div class="card">
//                <div class="card-body">
//                    <h3 class="card-title">НАЗВАНИЕ: ${general_book.title}</h3>
//                    <p class="text-secondary">АВТОР: ${general_book.author}</p>
//                    <div class="tags">
//                        ТЭГИ: ${general_book.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
//                    </div>
//                </div>
//            </div>`;
//
//            card.addEventListener('click', () => {
//                const title = encodeURIComponent(general_book.title);
//                const author = encodeURIComponent(general_book.author);
//                window.location.href = `/books?title=${title}&author=${author}`;
//            });
//
//            contentDiv.appendChild(card);
//        });
//    }
//}

//async function renderGeneralBookCards(slug) {
//    const response = await api.v1.categories.detail(slug);
//    if (response) {
//        const contentDiv = document.getElementById("general-books-list");
//        contentDiv.innerHTML = "";
//        response.general_books.forEach(function (general_book) {
//            const card = document.createElement('div');
//            card.classList.add('col-12', 'mb-3');
//            card.innerHTML = `
//                <button class="card btn btn-link text-left p-0">
//                    <div class="card-body">
//                        <h3 class="card-title">НАЗВАНИЕ: ${general_book.title}</h3>
//                        <p class="text-secondary">АВТОР: ${general_book.author}</p>
//                        <div class="tags">
//                            ТЭГИ: ${general_book.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
//                        </div>
//                    </div>
//                </button>`;
//
//            card.querySelector('.card').addEventListener('click', () => {
//                const title = encodeURIComponent(general_book.title);
//                const author = encodeURIComponent(general_book.author);
//                window.location.href = `/books?title=${title}&author=${author}`;
//            });
//
//            contentDiv.appendChild(card);
//        });
//    }
//}



//async function renderGeneralBookCards(slug) {
//    const response = await api.v1.categories.detail(slug);
//    if (response) {
//        const contentDiv = document.getElementById("general-books-list");
//        contentDiv.innerHTML = "";
//        response.general_books.forEach(function (general_book) {
//            contentDiv.innerHTML += `<div class="col-12 mb-3">
//                <div class="card">
//                  <div class="card-body">
//                    <h3 class="card-title">НАЗВАНИЕ:    ${general_book.title}</h3>
//                    <p class="text-secondary">АВТОР:    ${general_book.author}</p>
//                    <div class="tags">
//                        ТЭГИ:    ${general_book.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
//                    </div>
//                  </div>
//                </div>
//              </div>`;
//        });
//    }
//}


//async function renderBookPrivateCards(slug) {
//    const response = await api.v1.general_books.detail(slug);
//    if (response) {
//        const contentDiv = document.getElementById("books-private-list");
//        contentDiv.innerHTML = "";
//        response.data.forEach(function (general_book) {
//            const general_bookLink = document.createElement("a");
//            general_bookLink.className = "card";
//            general_bookLink.setAttribute("rel", "noopener");
//            general_bookLink.href = `/${general_book.slug}`;
//            general_bookLink.textContent = general_book.title;
////            general_bookLink.addEventListener("click", async (event) => {
////                await renderCategoryDetail(category.slug);
////            });
//            console.log(general_book.slug)
//            contentDiv.appendChild(general_bookLink);
//        });
//        response.books_private.forEach(function (book_private) {
//            contentDiv.innerHTML += `<div class="col-12 mb-3">
//                <div class="card">
//                  <div class="card-body">
//                    <h3 class="card-title">НАЗВАНИЕ:    ${book_private.title}</h3>
//                    <p class="text-secondary">АВТОР:    ${book_private.author}</p>
//                    <div class="tags">
//                        ТЭГИ:    ${book_private.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
//                    </div>
//                  </div>
//                </div>
//              </div>`;
//        });
//    }
//}





//async function renderGeneralBookCards(slug) {
//    const response = await api.v1.categories.detail(slug);
//    if (response.status === 200) {
//        const category = response.data;
//        document.getElementById("category-name").textContent = category.name;
//
//        let generalBooksList = document.getElementById("general-books-list");
//        generalBooksList.innerHTML = "";
//        category.general_books.forEach(generalBook => {
//            const generalBookItem = document.createElement("div");
//            generalBookItem.className = "general-book-item";
//            generalBookItem.innerHTML = `
//                <h3>${generalBook.title}</h3>
//                <p>${generalBook.body}</p>
//                <div class="tags">
//                    ${generalBook.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
//                </div>
//            `;
//            generalBooksList.appendChild(generalBookItem);
//        });
//    }
//}

//async function renderGeneralBookCards(slug) {
//    const response = await api.v1.categories.detail(slug);
//    if (response.status === 200) {
//        const contentDiv = document.getElementById("content");
//        contentDiv.innerHTML = "";
//        response.data.general_books.map(function (general_book) {
//            contentDiv.innerHTML += `<div class="col-md-6 col-lg-3">
//                <div class="card">
//                  <div class="card-body">
//                    <h3 class="card-title"></h3>
//                    <p class="text-secondary">${general_book.title}</p>
//                  </div>
//                </div>
//              </div>`
//        })
//    }
//}



//async function renderCategoryDropdownList() {
//    const response = await api.v1.categories.list();
//    if (response.status === 200) {
//        let categoryDropdown = document.getElementById("category-dropdown-list");
//        categoryDropdown.innerHTML = "";
//        response.data.map(function (category) {
//            const categoryLink = document.createElement("a");
//            categoryLink.className = "dropdown-item";
//            categoryLink.setAttribute( "rel", "noopener");
//            categoryLink.href = `/${category.id}`
//            categoryLink.textContent = category.name;
//            categoryDropdown.appendChild(categoryLink);
//        })
//    }
//}



//async function renderCategoryDetail(slug) {
//    const response = await api.v1.categories.detail(slug);
//    if (response.status === 200) {
//        const category = response;
//        document.getElementById("category-name").textContent = category.name;
//
//        let generalBooksList = document.getElementById("general-books-list");
//        generalBooksList.innerHTML = "";
//        category.general_books.forEach(generalBook => {
//            const generalBookItem = document.createElement("div");
//            generalBookItem.className = "general-book-item";
//            generalBookItem.innerHTML = `
//                <h3>${generalBook.title}</h3>
//                <p>${generalBook.body}</p>
//                <div class="tags">
//                    ${generalBook.tags.map(tag => `<span class="tag">${tag.name}</span>`).join('')}
//                </div>
//            `;
//            console.log(general_books.title)
//            generalBooksList.appendChild(generalBookItem);
//        });
//    }
//}

//document.addEventListener("DOMContentLoaded", async () => {
//    await getAccessToken()
//    await renderCategoryDropdownList();
//    let categorySlug = document.location.pathname.split("/")[1];
//    let general_bookSlug = document.location.pathname.split("/")[1];
//    if (categorySlug) {
//        try {
////            await renderCategoryDetail(categorySlug);
//            await renderGeneralBookCards(categorySlug);
//                if (general_bookSlug) {
//                    try {
//                        await renderBookPrivateCards(general_bookSlug);
//                    } catch (e) {
//                        console.error("Failed to render private book cards:", e);
//                    }
//                }
//        } catch (e) {
//            console.error("Failed to render general book cards:", e);
//        }
//    }
//});