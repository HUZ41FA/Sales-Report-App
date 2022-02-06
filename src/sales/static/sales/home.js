let reportBtn = document.getElementById('report-btn')
let img = document.getElementById('img')
let modalBody = document.getElementById('modal-body')
let reportForm = document.getElementById('report-form')

let reportName = document.getElementById('id_name')
let reportRemarks = document.getElementById('id_remarks')
let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value 
let alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
    <div class="alert alert-${type}" role="alert">
        ${msg}
    </div>
    `
}

if(img){
    reportBtn.classList.remove('not-visible')
}

reportBtn.addEventListener("click", ()=>{
    img.setAttribute('class', 'w-100')
    modalBody.prepend(img)



    reportForm.addEventListener("submit", e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)

        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                console.log(response)
                handleAlerts('success', 'Report saved')
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger', 'There was an error')
            },
            processData: false,
            contentType: false,
        })
    })
    
})