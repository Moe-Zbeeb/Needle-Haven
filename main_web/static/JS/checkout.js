function showConfirmation() {
    var confirmationTab = document.getElementById('confirmationTab');
    confirmationTab.style.display = 'flex';
    setTimeout(function() {
        confirmationTab.style.opacity = '0';
    }, 3000);
}

document.getElementById('submitBtn').addEventListener('click', function(event) {
    // Get the form element
    const form = document.getElementById('myForm');
    
    // Check if all required fields are filled
    const allFilled = [...form.elements].every(input => {
        if (input.type !== 'submit' && input.type !== 'button') {
            return input.value.trim() !== '';
        }
        return true;
    });

    if (allFilled) {
        // If all fields are filled, submit the form
        document.getElementById('myForm').submit();
    } else {
        // If any fields are empty, prevent form submission and show an error message
        event.preventDefault();
        document.getElementById('errorMessage').style.display = 'block';
    }
});




    model_path = '/home/rawad/Documents/Amazon/Needle-Haven/main_models_classes/eps/growth_prediction_model.pkl'