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

// async function that takes job_name, company, and descriptions as fields and creates that job in the jobs table.
async function createJob() {
    const response = await fetch(
        "http://127.0.0.1:8000/create_job", {
            "headers": {
                "Authorization": "Bearer " + userToken,
                "Content-Type": "application/json"
            },
            "body": JSON.stringify({
                "job_name": document.getElementById("jobName").value,
                "company": document.getElementById("companyName").value,
                "date_posted": Date(),
                "description": document.getElementById("jobDescription").value
            }),
            "method": "POST"
        }
    )
    const data = await response.json()
}

// async function that lists all jobs in database
async function displayJobs() {
    const response = await fetch("http://127.0.0.1:8000/jobs")
    const data = await response.json()
    let job_listings = ""
    for (i = 0; i < data.length; i++) {
        for (j = 0; j < 4; j++) {
            job_listings += data[i][j]
            if (j < 3) {
                job_listings += " | "
            }
        }
        job_listings += '\n'
    }
    document.getElementById("jobListings").innerHTML = job_listings
}