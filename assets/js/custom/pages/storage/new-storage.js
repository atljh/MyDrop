"use strict";

// Class definition
var KTModalNewStorage = function () {
	var submitButton;
	var cancelButton;
	var validator;
	var form;
	var modal;
	var modalEl;

	// Init form inputs
	// var initForm = function() {
	// 	// Team assign. For more info, plase visit the official plugin site: https://select2.org/
    //     $(form.querySelector('[name="team_assign"]')).on('change', function() {
    //         // Revalidate the field when an option is chosen
    //         validator.revalidateField('team_assign');
    //     });
	// }
    const initFormRepeater = () => {
        $('#kt_ecommerce_add_product_options').repeater({
            initEmpty: false,

            defaultValues: {
                'text-input': 'foo'
            },

            show: function () {
                $(this).slideDown();

                // Init select2 on new repeated items
                initConditionsSelect2();
            },

            hide: function (deleteElement) {
                $(this).slideUp(deleteElement);
            }
        });
    }

	// Init condition select2
	const initConditionsSelect2 = () => {
		// Tnit new repeating condition types
		const allConditionTypes = document.querySelectorAll('[data-kt-ecommerce-catalog-add-product="product_option"]');
		allConditionTypes.forEach(type => {
			if ($(type).hasClass("select2-hidden-accessible")) {
				return;
			} else {
				$(type).select2({
					minimumResultsForSearch: -1
				});
			}
		});
	}
	// Handle form validation and submittion
	var handleForm = function() {
		// Stepper custom navigation

		// Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
		validator = FormValidation.formValidation(
			form,
			{
				fields: {
					'name': {
						validators: {
							notEmpty: {
								message: 'Название обязательно'
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

		// Action buttons
		submitButton.addEventListener('click', function (e) {
			e.preventDefault();

			// Validate form before submit
			if (validator) {
				validator.validate().then(function (status) {
					console.log('validated!');

					if (status == 'Valid') {
						submitButton.setAttribute('data-kt-indicator', 'on');

						// Disable button to avoid multiple click 
						submitButton.disabled = true;

						let csrftoken = $('input[name="csrfmiddlewaretoken"]').prop('value');

						const headers = {
							'X-CSRFToken': csrftoken
						};
		
						// Serialize form data
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
									text: "Склад добавлен успешно!",
									icon: "success",
									buttonsStyling: false,
									confirmButtonText: "Oк",
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
									confirmButtonText: "Ок",
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
				text: "Are you sure you would like to cancel?",
				icon: "warning",
				showCancelButton: true,
				buttonsStyling: false,
				confirmButtonText: "Yes, cancel it!",
				cancelButtonText: "No, return",
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
						text: "Your form has not been cancelled!.",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "Ok, got it!",
						customClass: {
							confirmButton: "btn btn-primary",
						}
					});
				}
			});
		});
	}

	return {
		// Public functions
		init: function () {
			// Elements
			modalEl = document.querySelector('#kt_modal_new_storage');

			if (!modalEl) {
				return;
			}

			modal = new bootstrap.Modal(modalEl);

			form = document.querySelector('#kt_modal_new_storage_form');
			submitButton = document.getElementById('kt_modal_new_storage_submit');
			cancelButton = document.getElementById('kt_modal_new_storage_cancel');

			initFormRepeater();
			initConditionsSelect2();
			handleForm();
		}
	};
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
	KTModalNewStorage.init();
});