const fileInput = document.querySelector('input[type="file"]');
const formData = new FormData();

formData.append('file', fileInput.files[0]);

fetch('http://127.0.0.1:8000/items/5?q=somequery', {
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