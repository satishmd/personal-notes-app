var messages = document.querySelectorAll('.messages li');

setTimeout(function() {
    messages.forEach(function(message) {
        message.remove();
    });
}, 3000);


function showEditModal(id) {
    var title = document.getElementById("title-" + id).textContent;
    var body = document.getElementById("body-" + id).textContent;
    document.getElementById('note_id').value = id;
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-body').value = body;
    document.getElementById('btnModal').click();
}

document.getElementById('edit-form').addEventListener('submit', function(event) {
    event.preventDefault();
    event.stopPropagation();

    const formData = new FormData(this);
    fetch('notes/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
      },
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        window.location.href = "/"
      }
    })
    .catch(error => {
      alert('Failed to update note.');
    });
  });