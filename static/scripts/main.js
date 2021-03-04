var imageName;
var newImageName;
var fileExtension;

function readURL(input) {
  $('.file-return-content').hide();
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    var file = input.files[0];
    var fileSize = file.size.toString();
    imageName=file.name.toString();
    fileExtension=imageName.split('.').slice(-1)[0]
    newImageName = imageName.replace('.'+fileExtension,'-colorized.'+fileExtension);
    if (fileSize>5000000){
      $('.error-message').html('File larger than 5 MB maximum')
      removeUpload();
    } else {
      reader.onload = function(e) {
        $('.image-upload-wrap').hide();
        $('.error-message').html('')
        $('.file-upload-image').attr('src', e.target.result);
        $('.file-upload-content').show();
        $('.file-upload-btn').hide();
        $('.download-link').attr('download',newImageName);
      };
      reader.readAsDataURL(input.files[0]);
    }
  } else {
    $('.error-message').html('No image file found')
    removeUpload();
  }
}

function colorizeImage() {
  fetch($('.file-upload-image').attr('src'))
  .then(res => res.blob())
  .then(blob => {
    const file = new File([blob], 'image.'+fileExtension, blob)
    if (file) {
      const formData = new FormData()
      formData.append('imageFile', file)
      const options = {
        method: 'POST',
        body: formData,
      };
      fetch('/colorize', options)
      .then(res => {
        if (res.status==200) {
          res.blob()
          .then(blob => {
            const imgURL = URL.createObjectURL(blob);
            $('.file-return-image').attr('src', imgURL);
            $('.download-link').attr('href', imgURL);
            $('.file-return-content').show();
          });
        } else {
          console.error(status+' '+res.text())
        }
      })
      .catch(error => {
      console.error(error)
      })
    } else {
      removeUpload();
    }})
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.file-return-content').hide();
  $('.image-upload-wrap').show();
  $('.file-upload-btn').show();
  imageName="";
  newImageName="";
  fileExtension="";
}

function downloadImage() {
  $('.download-link').attr("style","");
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
  elmnt.className+=" current";
}