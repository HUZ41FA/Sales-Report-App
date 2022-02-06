let csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value
let alertBox = document.getElementById('alert-box')
let myDropzone = new window.Dropzone('#my-dropzone', {
    url:'/reports/upload/',
    init: function(){
        this.on('sending', function(file, xhr, formData){
            console.log('Sending')
            formData.append('csrfmiddlewaretoken', csrf)
        }),
        this.on('success', function(file, response){
            console.log(response)
            let ex = response.ex
            if (ex){
                alertBox.innerHTML = `<div class="alert alert-danger" role="alert">
                File already exists
              </div>`
            }else{
                alertBox.innerHTML = `<div class="alert alert-success" role="alert">
                        Your file has been uploaded
              </div>`
            }
        })
    },
    maxFiles: 30, 
    maxFilesize : 30,
    acceptedFiles :'.csv',
})