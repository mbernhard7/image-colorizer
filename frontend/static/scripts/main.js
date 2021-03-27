$.getScript("/static/scripts/opencv.js");
var imageName;
var newImageName;
var fileExtension;
apiURL = "https://milesbernhard.pythonanywhere.com";
if (window.location.href=='http://127.0.0.1:8000/'){
    apiURL = "http://127.0.0.1:5000"
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
                $('.error-message').html('')
                $('.file-upload-image').attr('src', e.target.result);
                $('.hidden-image').attr('src', e.target.result);
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
function dataUriToBlob(dataUri, type) {
    const b64 = atob(dataUri.split(',')[1]);
    const u8 = Uint8Array.from(b64.split(''), e => e.charCodeAt());
    return new Blob([u8], {type: type});
}

function colorizeImage() {
    const hiddenCanvas = document.getElementById('hidden-canvas');
    $('.colorize-image').attr('disabled', 'disabled');
    $('.remove-image').attr('disabled', 'disabled');
    $('.file-return-image').show()
    let mat = cv.imread("hidden-image");
    let dst = new cv.Mat();
    var original_width = mat.size().width;
    var original_height = mat.size().height;
    let dsize = new cv.Size(224, 224);
    cv.resize(mat, dst, dsize);
    mat.delete();
    cv.imshow('hidden-canvas',dst);
    dst.delete();
    var file = hiddenCanvas.toDataURL();
    file = dataUriToBlob(file, 'image.' + fileExtension.toLowerCase())
    file = new File([file], 'image.' + fileExtension.toLowerCase(), file)
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
                                $('.hidden-image').attr('src', imgURL).load(function() {  
                                    let mat1 = cv.imread('hidden-image');
                                    $('.hidden-image').attr('src', '')
                                    let dst1  = new cv.Mat();
                                    let dsize1 = new cv.Size(original_width, original_height);
                                    cv.resize(mat1, dst1, dsize1);
                                    mat1.delete();
                                    cv.imshow('hidden-canvas',dst1);
                                    const data1 = hiddenCanvas.toDataURL();
                                    dst1.delete();
                                    $('.file-return-image').attr('src', data1);
                                    $('.download-link').attr('href', data1);
                                });
                                $('.result-class').html('');
                                $('.download').css("display", "block");
                                $('.remove-image').removeAttr("disabled");
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
}

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').css("display", "none");
    $('.file-return-image').css("display", "none");
    $('.hidden-image').attr('src', "");
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