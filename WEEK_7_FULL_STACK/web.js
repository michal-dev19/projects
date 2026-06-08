async function registerUser() {
    const response = await fetch(
        "http://127.0.0.1:8000/register", {
            "headers": {"Content-Type": "application/json"}, 
            "body": JSON.stringify({
                "email": document.getElementById("email").value, 
                "password": document.getElementById("password").value}), 
            "method": "POST"
            }
        )
    const data = await response.json()
    console.log(data)
}

