var imageName;
var newImageName;
var fileExtension;
apiURL = "https://milesbernhard.pythonanywhere.com";
if (window.location.href=='http://127.0.0.1:8000/'){
    apiURL = "http://127.0.0.1:5000"
}

function uploadClick() {
    removeUpload();
    $('.file-upload-input').trigger( 'click' )
}

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
                $('.error-message').html('');
                $('.file-upload-image').attr('src', e.target.result);
                $('.colorize-image').removeAttr("disabled");
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
    const hiddenCanvas = document.getElementById('hidden-canvas');
    $('.colorize-image').attr('disabled', 'disabled');
    $('.file-upload-btn').attr('disabled', 'disabled');
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
                    mode: 'cors',
                    body: formData,
                    headers: {
                        'Access-Control-Allow-Origin': '*'
                    }
                };
                fetch(apiURL+'/colorize', options)
                    .then(res => {
                        if (res.ok) {
                            res.json().then(data => {
                                fetch(data['image']).then(response => response.blob())
                                    .then(blob => {
                                        const imgURL = URL.createObjectURL(blob);
                                        $('.file-return-image').attr('src', imgURL)
                                        $('.download-link').attr('href', imgURL);
                                        $('.result-class').html('');
                                        $('.download').css("display", "block");
                                        $('.file-upload-btn').removeAttr("disabled");
                                    });
                            });
                        } else {
                            res.text().then(text => {
                                console.log(text)
                                var parser = new DOMParser();
                                var htmlDoc = parser.parseFromString(text, 'text/html');
                                $('.error-message').html(htmlDoc.getElementsByTagName('title')[0].textContent);
                            });
                            removeUpload();
                        }
                    })
                    .catch(error => {
                        console.error(error);
                        $('.error-message').html(error)
                        removeUpload();
                    })
            } else {
                removeUpload();
            }
        });
}

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-return-image').css("display", "none");
    $('.result-class').html("");
    $('.file-return-image').attr('src', '/static/images/loading.gif');
    $('.file-upload-image').attr('src', '/static/images/noimage.png');
    $('.download').css("display", "none");
    $('.image-upload-wrap').css("display", "block");
    $('.colorize-image').attr('disabled', 'disabled');
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