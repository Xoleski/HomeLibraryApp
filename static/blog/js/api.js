const apiBaseURL = "https://master-sheep-really.ngrok-free.app";
const apiClient = axios.create({baseURL: apiBaseURL})


const api = {
    v1: {
        categories: {
            list: async function(){
                try {
                    return await apiClient.get("/api/v1/categories")
                } catch (e) {}
            },
            detail: async function(slug) {
                try {
                    const response = await fetch(`/api/v1/categories/${slug}`);
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return await response.json();
                } catch (e) {
                    console.error("Error fetching category details:", e);
                }
            },
            get: async function(slug) {
                try {
                    return await apiClient.get(`/api/v1/categories/${slug}`)
                } catch (e) {}
            },
            create: async function(data, headers) {
                try {
                    return await apiClient.request({
                        url: "/api/v1/categories",
                        method: "post",
                        data: data,
                        headers: headers
                    });
                } catch (e) {
                    console.error("Failed to create category:", e);
                }
            }
        },
        books_private: {
            list: async function(){
                try {
                    return await apiClient.get("/api/v1/books_private")
                } catch (e) {}
            },
            detail: async function(title, author) {
                console.log(title, author)
                try {
                    const url = `/api/v1/books_private_list?title=${encodeURIComponent(title)}&author=${encodeURIComponent(author)}`;
                    const response = await fetch(url);
//                    const response = await apiClient.get("/api/v1/books_private")
//                    console.log(title=${encodeURIComponent(title)})
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return await response.json();
                } catch (e) {
                    console.error("Error fetching book_private details:", e);
                }
            },
            create: async function(data, headers) {
                try {
                    return await apiClient.request({
                        url: "/api/v1/books_private",
                        method: "post",
                        data: data,
                        headers: headers
                    });
                } catch (e) {
                    console.error("Failed to create books_private:", e);
                }
            },
//            detail: async function(slug) {
//                try {
//                    const response = await fetch(`/api/v1/books_private/${slug}`);
//                    if (!response.ok) {
//                        throw new Error(`HTTP error! Status: ${response.status}`);
//                    }
//                    return await response.json();
//                } catch (e) {
//                    console.error("Error fetching book_private details:", e);
//                }
//            },
            get: async function(slug) {
                try {
                    return await apiClient.get(`/api/v1/books_private/${slug}`)
                } catch (e) {}
            },
//            create: async function(data, headers) {
//                try {
//                    return await apiClient.request({
//                        url: "/api/v1/books_private,
//                        data: data,
//                        headers: headers
//                    });
//                } catch (e) {
//                    console.error("Failed to create book_private:", e);
//                }
//            }
        }
    },
    auth: {
        register: async function(data) {
            try {
                return await apiClient.post("/api/auth/register", data)
            } catch (e) {}
        },
        login: async function(data) {
            try {
                return await apiClient.post("/api/auth/login", data)
            } catch (e) {}
        },
        refresh: async function(data) {
             try {
                return await apiClient.post("/api/auth/refresh", data)
            } catch (e) {}
        },
        google: async function(params) {
            try {
                return await apiClient.get("/api/auth/google" + params)
            } catch (e) {}
        }
    }
}







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

