"use strict";

// Class definition
var KTAppEcommerceSalesSaveOrder = function () {
    // Shared variables
    var table;
    var datatable;

    // Private functions
    const initSaveOrder = () => {
        // Init flatpickr
        $('#kt_ecommerce_edit_order_date').flatpickr({
            altInput: true,
            altFormat: "d F, Y",
            dateFormat: "Y-m-d",
        });

        // Init select2 country options
        // Format options
        const optionFormat = (item) => {
            if (!item.id) {
                return item.text;
            }

            var span = document.createElement('span');
            var template = '';

            template += '<img src="' + item.element.getAttribute('data-kt-select2-country') + '" class="rounded-circle h-20px me-2" alt="image"/>';
            template += item.text;

            span.innerHTML = template;

            return $(span);
        }

        // Init Select2 --- more info: https://select2.org/        
        $('#kt_ecommerce_edit_order_billing_country').select2({
            placeholder: "Select a country",
            minimumResultsForSearch: Infinity,
            templateSelection: optionFormat,
            templateResult: optionFormat
        });

        $('#kt_ecommerce_edit_order_shipping_country').select2({
            placeholder: "Select a country",
            minimumResultsForSearch: Infinity,
            templateSelection: optionFormat,
            templateResult: optionFormat
        });

        // Init datatable --- more info on datatables: https://datatables.net/manual/
        table = document.querySelector('#kt_ecommerce_edit_order_product_table');
        datatable = $(table).DataTable({
            'order': [],
            "scrollY": "200px",
            "scrollCollapse": true,
            "paging": false,
            "info": false,
            'columnDefs': [
                { orderable: true, targets: 0 }, // Disable ordering on column 0 (checkbox)
            ]
        });
    }

    // Search Datatable --- official docs reference: https://datatables.net/reference/api/search()
    var handleSearchDatatable = () => {
        const filterSearch = document.querySelector('[data-kt-ecommerce-edit-order-filter="search"]');
        filterSearch.addEventListener('keyup', function (e) {
            datatable.search(e.target.value).draw();
        });
    }

 // Handle shipping form
 const handleShippingForm = () => {
  // Select elements
  const addProductButton = document.getElementById('add_product');

  // Clone and insert the card
  addProductButton.addEventListener('click', e => {
    const addProductCard = document.getElementById('add_product_card');
    const clonedCard = addProductCard.cloneNode(true);
    clonedCard.classList.add('mt-7', 'mt-lg-10'); // Add margin between cards

    // Reset field values
    const inputFields = clonedCard.querySelectorAll('input, select');
    inputFields.forEach(field => {
      if (field.type === 'checkbox') {
        field.checked = false;
      } else {
        field.value = '';
      }
    });

    const generalContainer = document.getElementById('products');
    generalContainer.appendChild(clonedCard);

  });
};



    const handleProductSelect = () => {
        const checkboxes = table.querySelectorAll('[type="checkbox"]');
        const target = document.getElementById('kt_ecommerce_edit_order_selected_products');
        const message = target.querySelector('span');
    
        // Loop through all checkboxes
        checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', e => {
            if (e.target.checked) {
            // Disable other checkboxes
            checkboxes.forEach(otherCheckbox => {
                if (otherCheckbox !== checkbox) {
                otherCheckbox.checked = false;
                }
            });
            }
    
            // Select parent row element
            const parent = checkbox.closest('tr');
    
            // Clone parent element as variable
            const product = parent.querySelector('[data-kt-ecommerce-edit-order-filter="product"]').cloneNode(true);
    
            // Create inner wrapper
            const innerWrapper = document.createElement('div');
    
            // Store inner content
            const innerContent = product.innerHTML;
    
            // Add & remove classes on parent wrapper
            const wrapperClassesAdd = ['col', 'my-2'];
            const wrapperClassesRemove = ['d-flex', 'align-items-center'];
    
            // Define additional classes
            const additionalClasses = ['border', 'border-dashed', 'rounded', 'p-3', 'bg-body'];
    
            // Update parent wrapper classes
            product.classList.remove(...wrapperClassesRemove);
            product.classList.add(...wrapperClassesAdd);
    
            // Remove parent default content
            product.innerHTML = '';
    
            // Update inner wrapper classes
            innerWrapper.classList.add(...wrapperClassesRemove);
            innerWrapper.classList.add(...additionalClasses);
    
            // Apply stored inner content into new inner wrapper
            innerWrapper.innerHTML = innerContent;
    
            // Append new inner wrapper to parent wrapper
            product.appendChild(innerWrapper);
    
            // Get product id
            const productId = product.getAttribute('data-kt-ecommerce-edit-order-id');
    
            if (e.target.checked) {
            // Add product to selected product wrapper
            target.innerHTML = ''; // Clear previous selection
            target.appendChild(product);
            } else {
            // Remove product from selected product wrapper
            const selectedProduct = target.querySelector('[data-kt-ecommerce-edit-order-id="' + productId + '"]');
            if (selectedProduct) {
                target.removeChild(selectedProduct);
            }
            }
    
            // Trigger empty message logic
            detectEmpty();
        });
        });
    
        // Handle empty list message
        const detectEmpty = () => {
        // Select elements
        const products = target.querySelectorAll('[data-kt-ecommerce-edit-order-filter="product"]');
    
        // Detect if element is empty
        if (products.length < 1) {
            // Show message
            message.classList.remove('d-none');
        } else {
            // Hide message
            message.classList.add('d-none');
        }
        }
    };
    
    
        // Submit form handler
    const handleSubmit = () => {
        // Define variables
        let validator;
      
        // Get elements
        const form = document.getElementById('kt_ecommerce_edit_order_form');
        const submitButton = document.getElementById('kt_ecommerce_edit_order_submit');
      
        // Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
        validator = FormValidation.formValidation(
          form,
          {
            fields: {
              'full_name': {
                validators: {
                  notEmpty: {
                    message: 'Полное имя обязательно'
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
              'sell_price': {
                validators: {
                  notEmpty: {
                    message: 'Обязательное поле'
                  }
                }
              }
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
      
        // Handle form submit
        submitButton.addEventListener('click', function (e) {
          e.preventDefault();
      
          const checkboxes = document.querySelectorAll('#kt_ecommerce_edit_order_product_table [type="checkbox"]:checked');

          if (checkboxes.length === 0) {
            // Show error message for no selected checkboxes
            Swal.fire({
              text: "Выберите хотя бы один продукт",
              icon: "error",
              buttonsStyling: false,
              confirmButtonText: "Ок",
              customClass: {
                confirmButton: "btn btn-primary"
              }
            });
            return;
          }
          // Validate form
          validator.validate().then(function (status) {
            if (status == 'Valid') {
              // Show loading indication
              submitButton.setAttribute('data-kt-indicator', 'on');
      
                // Disable submit button whilst loading
              submitButton.disabled = true;

              const products = document.getElementsByName('add_product_card');
              const selectedProducts = [];
              
              products.forEach(product => {
                const checkbox = product.querySelector('[type="checkbox"]:checked');
                
                if (checkbox) {
                  const productId = checkbox.getAttribute('data-product-id');
                  const quantityInput = product.querySelector('[name="products_amount"]');
                  const costPriceInput = product.querySelector('[name="cost_price"]');
                  const dropPriceInput = product.querySelector('[name="drop_price"]');
                  const sellPriceInput = product.querySelector('[name="sell_price"]');
                  const sizeSelect = product.querySelector('[name="sizes"]');
                  
                  const selectedProduct = {
                    product: productId,
                    quantity: quantityInput.value,
                    cost_price: costPriceInput.value,
                    drop_price: dropPriceInput.value,
                    sell_price: sellPriceInput.value,
                    sizes: Array.from(sizeSelect.selectedOptions).map(option => option.value)
                  };
                  
                  selectedProducts.push(selectedProduct);
                }
              });

              const formData = new FormData(form);
              formData.append('order_products', JSON.stringify(selectedProducts));

              let csrftoken = $('input[name="csrfmiddlewaretoken"]').prop('value');
              const headers = {
                  'X-CSRFToken': csrftoken
              };
      
              const jsonData = {};
              for (const [key, value] of formData.entries()) {
                jsonData[key] = value;
              }

              fetch(window.location.href, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(jsonData)
              })
                .then(response => response.json())
                .then(data => {
                  // Handle server response
                  if (data.success) {
                    // Reset form
                    // form.reset();
                    // validator.reset();
      
                    // Reset selected products
                    const selectedProducts = table.querySelectorAll('[type="checkbox"]:checked');
                    selectedProducts.forEach(checkbox => {
                      checkbox.checked = false;
                    });
      
                    // Clear selected products wrapper
                    const selectedProductsWrapper = document.getElementById('kt_ecommerce_edit_order_selected_products');
                    selectedProductsWrapper.innerHTML = '';
      
                    // Show success message
                    Swal.fire({
                      text: "Заказ успешно добавлен.",
                      icon: "success",
                      buttonsStyling: false,
                      confirmButtonText: "Ок",
                      customClass: {
                        confirmButton: "btn btn-primary"
                      }
                    });
                  } else {
                    // Show error message
                    let errorMessage = "Ошибка при создании заказа. Пожалуйста, попробуйте еще раз.";
                    if (data.errors && data.errors.sell_price) {
                      errorMessage = data.errors.sell_price[0];
                    }
                    Swal.fire({
                      text: errorMessage,
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
                  console.log(error);
                  let errorMessage = "Ошибка при отправке запроса. Пожалуйста, попробуйте еще раз.";
                  if (error && error.errors) {
                    errorMessage = Object.values(error.errors).flat().join('<br>');
                  }
                  // Show error message
                  Swal.fire({
                    html: errorMessage,
                    icon: "error",
                    buttonsStyling: false,
                    confirmButtonText: "Ок",
                    customClass: {
                      confirmButton: "btn btn-primary"
                    }
                  });
                })
                .finally(() => {
                  // Hide loading indication
                  submitButton.removeAttribute('data-kt-indicator');
                  submitButton.disabled = false;
                });
            } else {
              // Show error message
              Swal.fire({
                text: "Извините, обнаружены ошибки. Пожалуйста, проверьте заполненные поля и попробуйте еще раз.",
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
      }
  

    return {
        // Public functions
        init: function () {
            // Initialize
            initSaveOrder();
            handleSearchDatatable();
            handleShippingForm();
            handleProductSelect();
            handleSubmit();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTAppEcommerceSalesSaveOrder.init();
});
