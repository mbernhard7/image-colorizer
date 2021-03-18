var imageName;
var newImageName;
var fileExtension;

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        var file = input.files[0];
        var fileSize = file.size.toString();
        imageName = file.name.toString();
        fileExtension = imageName.split('.').slice(-1)[0]
        newImageName = imageName.replace('.' + fileExtension, '-colorized.' + fileExtension);
        fileExtension = fileExtension.replace('jpg', 'jpeg').replace('JPG', 'JPEG')
        if (fileSize > 5000000) {
            $('.error-message').html('File larger than 5 MB maximum')
            removeUpload();
        } else {
            reader.onload = function(e) {
                $('.image-upload-wrap').css("display", "none");
                $('.error-message').html('')
                $('.file-upload-image').attr('src', e.target.result);
                $('.file-upload-content').css("display", "block");
                $('.file-upload-btn').css("display", "none");
                $('.download-link').attr('download', newImageName);
            };
            reader.readAsDataURL(input.files[0]);
        }
    } else {
        $('.error-message').html('No image file found')
        removeUpload();
    }
}

function colorizeImage() {
    $('.colorize-image').attr('disabled', 'disabled');
    $('.remove-image').attr('disabled', 'disabled');
    $('.file-return-image').show()
    fetch($('.file-upload-image').attr('src'))
        .then(res => res.blob())
        .then(blob => {
            const file = new File([blob], 'image.' + fileExtension.toLowerCase(), blob)
            if (file) {
                const formData = new FormData()
                formData.append('imageFile', file)
                const options = {
                    method: 'POST',
                    body: formData,
                };
                fetch('/colorize', options)
                    .then(res => {
                        if (res.status == 200) {
                            res.json().then(data => {
                                fetch(data['image']).then(response => response.blob())
                                    .then(blob => {
                                        const imgURL = URL.createObjectURL(blob);
                                        $('.file-return-image').attr('src', imgURL);
                                        $('.result-class').html(data['prediction'] + ' , ' + data['probability'] + '% sure');
                                        $('.download-link').attr('href', imgURL);
                                        $('.download').css("display", "block");
                                        $('.remove-image').removeAttr("disabled");
                                    });
                            });
                        } else {
                            console.error(status + ' ' + res.text())
                            $('.error-message').html('Error: ' + status)
                            removeUpload();
                        }
                    })
                    .catch(error => {
                        console.error(error)
                        $('.error-message').html(error)
                        removeUpload();
                    })
            } else {
                removeUpload();
            }
        })
}

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').css("display", "none");
    $('.file-return-image').css("display", "none");
    $('.result-class').html("");
    $('.file-return-image').attr('src', '/static/images/loading.gif');
    $('.download').css("display", "none");
    $('.image-upload-wrap').css("display", "block");
    $('.file-upload-btn').css("display", "block");
    $('.colorize-image').removeAttr("disabled");
    $('.remove-image').removeAttr("disabled");
    imageName = "";
    newImageName = "";
    fileExtension = "";
}

function downloadImage() {
    document.getElementsByClassName('download-link')[0].click();
}

function openPage(pageName, elmnt) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].className = tabcontent[i].className.replace(" current", "");
    }

    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" current", "");
    }

    document.getElementById(pageName).className += " current";
    elmnt.className += " current";
}