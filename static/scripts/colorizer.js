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
  const img = $('.file-upload-image');
  fetch(img.attr('src'))
  .then(res => res.blob())
  .then(blob => {
    const file = new File([blob], 'dot.png', blob)
    if (file) {
      const formData = new FormData()
      formData.append('imageFile', file)
      const options = {
        method: 'POST',
        body: formData,
      };
      fetch('https://cs121-image-colorizer.herokuapp.com/colorize', options)
      .then(res => {
        const status = response.headers.get("status");
        if (status==200) {
            $('.file-return-image').attr('src', 'data:image/jpg;base64,'+data);
            $('.file-return-content').show();
            console.log(res);
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
}