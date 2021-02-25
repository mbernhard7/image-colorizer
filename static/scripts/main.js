function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function colorizeImage() {
  
  if ($('.file-upload-image') && $('.file-upload-image').attr('src')!=="#"){    
    var image = $('.file-upload-image').attr('src')
    const formData = new FormData()
    formData.append('imageFile', image)
    console.log(image)
    fetch('/colorize', {
      method: 'POST',
      body: formData
    })
    .then(res => {
      console.log(res)
    })
    .catch(error => {
      console.error(error)
    })

  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}

git add .                       
git commit -m "testing image upload"
git push -u origin main             
git push heroku main