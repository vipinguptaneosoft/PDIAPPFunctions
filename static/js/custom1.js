$(document).ready(function() {
    $('#createTask').on('show.bs.modal', function() {
      $('#add_input_function').modal('hide');
    });
    
    $('#add_input_function').on('hidden.bs.modal', function() {
      $('#createTask').modal('show');
    });
  });
  


function add_input_function(){
    input_function = document.getElementById('function_input').value
    multiple_input_select = document.getElementById('input_dataframe')
    var selectedValues = [];
    
    for (var i = 0; i < multiple_input_select.options.length; i++) {
      var option = multiple_input_select.options[i];
      
      if (option.selected) {
        selectedValues.push(option.value);
      }
    }

    console.log(input_dataframe,input_function)
    row = ""
    for (var i = 0; i < selectedValues.length; i++) {
        row = row + selectedValues[i]+",<br>"

      }
    $('#input_functions_params').append(row);
    // document.getElementById('input_functions_params')
        // console.log(data)
    $('#add_input_function').modal('hide');

    // $.ajax({
    //     type: 'get',
    //     url: "/get_function_via_id/?function_id="+input_function,
    //     data:{},
    //     contentType: 'application/json',
    //     success: function (data) {
    //         console.log(data)
    //         row = ""
    //         for (var i = 0; i < selectedValues.length; i++) {
    //             row = row +data.sequence+"==>"+ data.function_name+"==>"+selectedValues[i]+",<br>"

    //           }

    //         $('#input_functions_params').append(row);
    //         // document.getElementById('input_functions_params')
    //             console.log(data)
    //         $('#add_input_function').modal('hide');
            
    //     },
    //     error: function (response) {
    //       console.log(response);
    //         }
    //     }
    // );




    // row = ""
    // row = row + "<option value='"+input_dataframe+"'"+">" +input_function+"</option>"
    // $('#input_functions_params').append(row);
    // document.getElementById('input_functions_params')
}

function get_external_config(){
  function_id = document.getElementById('fid').value
  $.ajax({
    type: 'get',
    url: "/get_external_config/?function_id="+function_id,
    data:{},
    contentType: 'application/json',
    success: function (data) {
        console.log(data)
        $('#put_external_config').html('')
        row = ""
        for (key in data) {
          row +=' <label>'+key+'</label>' +
                '<input type="'+data[key]+'" class="form-control form-control-modern" name="'+key+'" required>'
          }

        $('#put_external_config').append(row);
        // document.getElementById('input_functions_params')
            console.log(data)
        // $('#add_input_function').modal('hide');
        
    },
    error: function (response) {
      console.log(response);
        }
    }
);
}

function put_task_values_to_edit(data){}


function get_predefined_task_data(task_id, case_id){
  $.ajax({
    type: 'get',
    url: "/task/"+task_id+"/?case_id="+case_id,
    data:{},
    contentType: 'application/json',
    success: function (data) {
        console.log(data)
        $('#put_external_config').html('')
        row = ""
        for (key in data) {
          row +=' <label>'+key+'</label>' +
                '<input type="'+data[key]+'" class="form-control form-control-modern" name="'+key+'" required>'
          }

        $('#put_external_config').append(row);
        // document.getElementById('input_functions_params')
            console.log(data)
        // $('#add_input_function').modal('hide');
        
    },
    error: function (response) {
      console.log(response);
        }
    }
);
}


