"use strict";

// Class definition
var KTModalEditStorage = function () {
	var submitButton;
	var validator;
	var form;
	var modal;
	var modalEl;
	var addContactButton;


    const initFormRepeater = () => {
        $('#contact_options').repeater({
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
		const allConditionTypes = document.querySelectorAll('[storage-contacts="contact_option"]');
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
		
						const contactOptionsContainer = document.getElementById('contact_options');
						const contactOptionItems = contactOptionsContainer.querySelectorAll('[data-repeater-item]');
						
						const contactOptions = [];
						
						contactOptionItems.forEach(item => {
							const optionTypeElement = item.querySelector('[name^="contact_options["][name$="[type]"]');
							const optionValueElement = item.querySelector('[name^="contact_options["][name$="[value]"]');
							const optionDescriptionElement = item.querySelector('[name^="contact_options["][name$="[description]"]');
						
							const optionType = optionTypeElement ? optionTypeElement.value : '';
							const optionValue = optionValueElement ? optionValueElement.value : '';
							const optionDescription = optionDescriptionElement ? optionDescriptionElement.value : '';
						
							contactOptions.push({
								'type': optionType,
								'value': optionValue,
								'description': optionDescription
							});
						});
						
						formData.delete('contact_options'); // Remove the previous contact_options data
						formData.append('contact_options', JSON.stringify(contactOptions));
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
									text: "Склад успешно изменен.",
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

		addContactButton.addEventListener('click', function (e) {
			e.preventDefault();
			let type = document.getElementById('newContactType').value;
			$.ajax({
				type: 'POST',
				url: `/vendor/storage/add_contact/`,
				data: {
					contact_type: type,
					csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
				},
				dataType: 'json',
				success: function (response) {
					if (response.success) {
						Swal.fire({
							text: "Контакт успешно добавлен!",
							icon: "success",
							buttonsStyling: false,
							confirmButtonText: "Ок",
							customClass: {
								confirmButton: "btn btn-primary"
							}
						}).then(function () {
							window.location.reload();
						});
					} else {
						Swal.fire({
							text: "Не удалось добавить контакт.",
							icon: "error",
							buttonsStyling: false,
							confirmButtonText: "Ок",
							customClass: {
								confirmButton: "btn btn-primary"
							}
						});
					}
				},
				error: function () {
					Swal.fire({
						text: "Произошла ошибка при добавлении контакта.",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "Ок",
						customClass: {
							confirmButton: "btn btn-primary"
						}
					});
				}
			});
		});

		$('a.delete-employee').on('click', function (e) {
			e.preventDefault();
		
			const employeeId = $(this).data('employee-id');
		
			Swal.fire({
				text: "Вы уверены, что хотите удалить этого сотрудника?",
				icon: "warning",
				showCancelButton: true,
				buttonsStyling: false,
				confirmButtonText: "Да, удалить!",
				cancelButtonText: "Отмена",
				customClass: {
					confirmButton: "btn btn-danger",
					cancelButton: "btn btn-active-light"
				}
			}).then(function (result) {
				if (result.isConfirmed) {
					$.ajax({
						type: 'POST',
						url: `/vendor/employee/${employeeId}/delete/`,
						data: {
							csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
						},
						dataType: 'json',
						success: function (response) {
							if (response.success) {
								// Обновляем интерфейс после успешного удаления
								Swal.fire({
									text: "Сотрудник успешно удален!",
									icon: "success",
									buttonsStyling: false,
									confirmButtonText: "Ок",
									customClass: {
										confirmButton: "btn btn-primary"
									}
								}).then(function () {
									// Перезагружаем страницу для обновления данных
									window.location.reload();
								});
							} else {
								Swal.fire({
									text: "Не удалось удалить сотрудника.",
									icon: "error",
									buttonsStyling: false,
									confirmButtonText: "Ок",
									customClass: {
										confirmButton: "btn btn-primary"
									}
								});
							}
						},
						error: function () {
							Swal.fire({
								text: "Произошла ошибка при удалении сотрудника.",
								icon: "error",
								buttonsStyling: false,
								confirmButtonText: "Ок",
								customClass: {
									confirmButton: "btn btn-primary"
								}
							});
						}
					});
				}
			});
		});
	}

	return {
		init: function () {
			modalEl = document.querySelector('#kt_modal_new_storage');
			if (!modalEl) {
				return;
			}
			modal = new bootstrap.Modal(modalEl);

			form = document.querySelector('#kt_modal_new_storage_form');
			submitButton = document.getElementById('kt_modal_new_storage_submit');
			addContactButton = document.getElementById('confirmAddContact');

			initFormRepeater();
			initConditionsSelect2();
			handleForm();
		}
	};
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
	KTModalEditStorage.init();
});