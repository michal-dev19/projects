// a temporary storage for user's token
let userToken = null

// an asynchronous function, to retrieve data from user, package it, POST it to the server and wait for a 'Promise' (response)
async function registerUser() {
    const response = await fetch(
        "http://127.0.0.1:8000/register", {
            "headers": {"Content-Type": "application/json"}, 
            "body": JSON.stringify({
                "email": document.getElementById("registerEmail").value, 
                "password": document.getElementById("registerPassword").value
            }), 
            "method": "POST"
        }
    )
    const data = await response.json()
    console.log(data)
}

// async function just like registerUser, but this time we are logging the user in, and the return value (or Promise), is a signed token
async function loginUser() {
    const response = await fetch(
        "http://127.0.0.1:8000/login", {
            "headers": {"Content-Type": "application/json"},
            "body": JSON.stringify({
                "email": document.getElementById("loginEmail").value,
                "password": document.getElementById("loginPassword").value
            }),
            "method": "POST"
        }
    )
    const data = await response.json()
    userToken = data
}