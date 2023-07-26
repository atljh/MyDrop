"use strict";

// Class definition
var KTModalCustomersAdd = function () {
    var submitButton;
    var cancelButton;
	var closeButton;
    var validator;
    var form;
    var modal;

    // Init form inputs
    var handleForm = function () {
        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
		validator = FormValidation.formValidation(
			form,
			{
				fields: {
                    'name': {
						validators: {
							notEmpty: {
								message: 'ФИО обязательно'
							}
						}
					},
					'phone_number': {
						validators: {
							notEmpty: {
								message: 'Номер телефона обязателен'
							}
						}
					},
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap5({
						rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
					})
				}
			}
		);

		// Revalidate country field. For more info, plase visit the official plugin site: https://select2.org/
        $(form.querySelector('[name="country"]')).on('change', function() {
            // Revalidate the field when an option is chosen
            validator.revalidateField('country');
        });

		// Action buttons
		submitButton.addEventListener('click', function (e) {
			e.preventDefault();

			// Validate form before submit
			if (validator) {
				validator.validate().then(function (status) {
					console.log('validated!');

					if (status == 'Valid') {
						submitButton.setAttribute('data-kt-indicator', 'on');

						// Disable submit button whilst loading
						submitButton.disabled = true;
						
						let csrftoken = $('input[name="csrfmiddlewaretoken"]').prop('value');

						const headers = {
							'X-CSRFToken': csrftoken
						};
						const formData = new FormData(form);

						// Perform POST request to the server
						fetch(window.location.href, {
							method: 'POST',
							body: formData,
							headers: headers
						})
						.then(response => response.json())
						.then(data => {
							// Process the response as needed
							if (data.success) {
								Swal.fire({
									text: "Сотрудник добавлен успешно!",
									icon: "success",
									buttonsStyling: false,
									confirmButtonText: "Понятно",
									customClass: {
										confirmButton: "btn btn-primary"
									}
								}).then(function (result) {
									if (result.isConfirmed) {
										// Enable submit button after loading
										submitButton.disabled = false;
		
										// Redirect to customers list page
										window.location = form.getAttribute("data-kt-redirect");
									}
								});
							} else {
								Swal.fire({
									text: "Упс, что-то пошло не так.",
									icon: "error",
									buttonsStyling: false,
									confirmButtonText: "Понятно",
									customClass: {
										confirmButton: "btn btn-primary"
									}
								});
							}
						})
						.catch(error => {
							console.error('Error:', error);
							Swal.fire({
								text: "Упс, что-то пошло не так.",
								icon: "error",
								buttonsStyling: false,
								confirmButtonText: "Понятно",
								customClass: {
									confirmButton: "btn btn-primary"
								}
							});
						});
					}
				});
			}
		});

        cancelButton.addEventListener('click', function (e) {
            e.preventDefault();

            Swal.fire({
                text: "Вы уверены что хотите отменить?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: "Да, отменить",
                cancelButtonText: "Нет, вернутся",
                customClass: {
                    confirmButton: "btn btn-primary",
                    cancelButton: "btn btn-active-light"
                }
            }).then(function (result) {
                if (result.value) {
                    form.reset(); // Reset form	
                    modal.hide(); // Hide modal				
                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Сотрудник не сохранен.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Понятно",
                        customClass: {
                            confirmButton: "btn btn-primary",
                        }
                    });
                }
            });
        });

		closeButton.addEventListener('click', function(e){
			e.preventDefault();

            Swal.fire({
                text: "Вы уверены что хотите отменить?",
                icon: "warning",
                showCancelButton: true,
                buttonsStyling: false,
                confirmButtonText: "Да, отменить",
                cancelButtonText: "Нет, вернутся",
                customClass: {
                    confirmButton: "btn btn-primary",
                    cancelButton: "btn btn-active-light"
                }
            }).then(function (result) {
                if (result.value) {
                    form.reset(); // Reset form	
                    modal.hide(); // Hide modal				
                } else if (result.dismiss === 'cancel') {
                    Swal.fire({
                        text: "Сотрудник не сохранен.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Понятно",
                        customClass: {
                            confirmButton: "btn btn-primary",
                        }
                    });
                }
            });
		})
    }

    return {
        // Public functions
        init: function () {
            // Elements
            modal = new bootstrap.Modal(document.querySelector('#kt_modal_add_customer'));

            form = document.querySelector('#kt_modal_add_customer_form');
            submitButton = form.querySelector('#kt_modal_add_customer_submit');
            cancelButton = form.querySelector('#kt_modal_add_customer_cancel');
			closeButton = form.querySelector('#kt_modal_add_customer_close');

            handleForm();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
	KTModalCustomersAdd.init();
});