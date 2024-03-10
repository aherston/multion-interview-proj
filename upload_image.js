const uriInput = document.querySelector('input[type="text"]');
const formData = new FormData();

formData.append('uri', uriInput.value);

fetch('http://localhost:8000/uploadimage/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(result => {
    console.log('Success:', result);
    document.getElementById('result').textContent = JSON.stringify(result);
    window.location.href = "http://localhost:8080"
})
.catch(error => {
    console.error('Error:', error);
});