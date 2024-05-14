const baseURL = "http://127.0.0.1:8080"
const apiClient = axios.create({
    baseURL: baseURL
})


const api = {
    v1: {
        categories: {
            list: async function(){
                try {
                    return await apiClient.get("/api/v1/categories")
                } catch (e) {
                    console.log(e)
                }
            },
            get: async function(categoryID) {
                try {
                    return await apiClient.get(`/api/v1/categories/${categoryID}`)
                } catch (e) {
                    console.log(e)
                }
            }
        }
    }
}

async function renderGeneralBookCards(categoryID) {
    const response = await api.v1.categories.get(categoryID);
    if (response.status === 200) {
        const contentDiv = document.getElementById("content");
        contentDiv.innerHTML = "";
        response.data.general_books.map(function (general_book) {
            contentDiv.innerHTML += `<div class="col-md-6 col-lg-3">
                <div class="card">
                  <div class="card-body">
                    <h3 class="card-title"></h3>
                    <p class="text-secondary">${general_book.title}</p>
                  </div>
                </div>
              </div>`
        })
    }
}

//async function renderArticleCards(categoryID) {
//    const response = await api.v1.categories.get(categoryID);
//    if (response.status === 200) {
//        const contentDiv = document.getElementById("content");
//        contentDiv.innerHTML = "";
//        response.data.articles.map(function (acticle) {
//            contentDiv.innerHTML += `<div class="col-md-6 col-lg-3">
//                <div class="card">
//                  <div class="card-body">
//                    <h3 class="card-title"></h3>
//                    <p class="text-secondary">${acticle.title}</p>
//                  </div>
//                </div>
//              </div>`
//        })
//    }
//}

async function renderCategoryDropdownList() {
    const response = await api.v1.categories.list();
    if (response.status === 200) {
        let categoryDropdown = document.getElementById("category-dropdown-list");
        categoryDropdown.innerHTML = "";
        response.data.map(function (category) {
            const categoryLink = document.createElement("a");
            categoryLink.className = "dropdown-item";
            categoryLink.setAttribute( "rel", "noopener");
            categoryLink.href = `/${category.id}`
            categoryLink.textContent = category.name;
            categoryDropdown.appendChild(categoryLink);
        })
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await renderCategoryDropdownList();
    let categoryID = document.location.pathname.split("/")[1];
    try {
        categoryID = parseInt(categoryID);
        await renderGeneralBookCards(categoryID)
    } catch (e) {}
})








//const baseURL = "http://0.0.0.0:8080"
//const apiClient = axios.create({
//    baseURL: baseURL
//})
//
//
//const api = {
//    v1: {
//        categories: {
//            list: async function(){
//                try {
//                    return await apiClient.get("/api/v1/categories")
//                } catch (e) {
//                    console.log(e)
//                }
//            }
//        }
//    }
//}
//
//async function renderCategoryDropDownList() {
//    const response = await api.v1.categories.list();
//    if (response.status === 200) {
//        let categoryDropdown = document.getElementById("category-dropdown-list");
//        categoryDropdown.innerHTML = "";
//        response.data.map(function (category) {
//            const categoryLink = document.createElement("a");
//            categoryLink.className = "dropdown-item";
//            categoryLink.setAttribute("rel", "noopener");
//            categoryLink.href = `/${category.id}`;
//            categoryLink.textContent = category.name;
//            categoryDropdown.appendChild(categoryLink);
//        })
//    }
//}
//
//document.addEventListener('DOMContentLoaded', async () => {
//    await renderCategoryDropDownList
//})
//

//const api = {
//    v1: {
//        categories: {
//            list: async function(): {
//                try {
//                    return await apiClient.get(
//                        "/api/v1/categories"
//                    )
//                } catch (e) {
//                    if (e.response.status === 401) {
//                        window.location.href = '/login'
//                    }
//                    return e.response
//                }
//            }
//        }
//    }
//}


//async function _request(method, url, data):{
//    const accessToken: = sessionStorage.getItem(key: 'token');
//    try {
//        return await this.request({method: method, url: url, data: data, headers: {'Authorization': 'Bearer ${accessToken}'}});
//    } catch (e) {
//        if (e.response.status === 401) {
//            window.location.href = '/login'
//        }
//        return e.response
//    }
//}

