const fileInput = document.querySelector('input[type="file"]');
const formData = new FormData();

formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/uploadfile/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(result => {
    console.log('Success:', result);
})
.catch(error => {
    console.error('Error:', error);
});