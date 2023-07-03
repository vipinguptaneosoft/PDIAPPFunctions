
$(document).ready(function() {
  $('#input_dataframe').select2();
});
function openPopup() {
    var popup = window.open("create_case_popup.html", "popupWindow", "width=500,height=500");
}

function submitForm() {
    
    var popup = document.getElementById("popup");
popup.style.display = "none"
}


function open_right_panel(task_id, function_id, case_id){
    window.location.replace("/cases/"+case_id+"/task/"+task_id+"/?function="+function_id)
    // $.ajax({
    //     type: 'GET',
    //     url: "/cases/"+case_id+"/task/"+task_id+"/?function="+function_id,
    //     success: function (data) {
    //         console.log(data)
            
    //         task = ``
    //         $('#data_represent').html('')
    //         for (let k in data.function_config) {
    //             console.log(k + ' is ' + data.function_config[k])
    //             task += `<label >${k}</label>
    //             <div >
    //                 <input type="${data.function_config[k]}" class="form-control form-control-modern" name="${k}" required value="" />
    //             </div>`
    //         }
    //         task += `
    //             <input type="hidden" class="form-control form-control-modern" name="function_id" required value="${function_id}" />
    //             <input type="hidden" class="form-control form-control-modern" name="case_id" required value="${case_id}" />
    //             <input type="hidden" class="form-control form-control-modern" name="task_id" required value="${task_id}" />
    //         `
    //         console.log(task)
    //         $('#data_represent').append(task);
    //         $('#step_function_data').html(data.table_tag)
    //        },
    //     error: function (response) {
    //         var err_txt = $('#code-id-error-txt');
    //         if (err_txt.hasClass('d-block')){
    //             err_txt.removeClass('d-block');
    //             err_txt.addClass('d-none');
    //         }
    //         if (err_txt.hasClass('d-none')){
    //             err_txt.addClass('d-block');
    //             err_txt.text(`${response.responseJSON}`);
    //         }
    //     }
    // })
}

function openCaseDetailPage(case_id){
    window.location.replace('/cases/'+case_id)
}

function add_delete_id_case(case_id){
    $('#case_deletion').val(case_id);
}

function add_delete_id_function(case_id, function_id){
    $('#case_deletion').val(case_id);
    $('#function_deletion').val(function_id);
}

function execute_all_steps(case_id){
    start_time = document.getElementById("start_time_id");
    end_time = document.getElementById("end_time_id");
    formated_start_time = new Date(start_time.value).toISOString().replace('T', ' ').replace('Z', " ")
    formated_end_time = new Date(end_time.value).toISOString().replace('T', ' ').replace('Z', " ")
    var loader = document.getElementById("loader");
    var overlay = document.getElementById("overlay");
    loader.style.display = "inline-block";
    overlay.style.display = "block";


    $.ajax({
        type: 'GET',
        url: "/execute_functions/?case="+case_id+"&start_time="+formated_start_time+"&end_time="+formated_end_time,
        success: function (data) {

          // alert("Executed")
          output = data.data
          $('#function_output').html('')
          $('#function_output').append(output)
          loader.style.display = "none";
          overlay.style.display = "none";
           },
        error: function (response) {
          // alert("Error")
          $('#function_output').html('')
          $('#function_output').append(response.responseText)            
          loader.style.display = "none";
          overlay.style.display = "none";
        }
        }
    )
}

var draggedRow = null;
var table = document.getElementById("myTable");

// Add draggable attribute to all rows in the table
for (var i = 0; i < table.rows.length; i++) {
  table.rows[i].draggable = true;
  table.rows[i].addEventListener("dragstart", function(event) {
    // Save reference to the dragged row
    draggedRow = event.target;
  });
}

// Allow dropping of rows before or after other rows
table.addEventListener("dragover", function(event) {
  event.preventDefault();
  var targetRow = event.target.closest("tr");
  if (targetRow) {
    // Highlight the drop target row
    targetRow.classList.add("drag-over");
  }
});

// Reset the drop target row highlight when leaving it
table.addEventListener("dragleave", function(event) {
  var targetRow = event.target.closest("tr");
  if (targetRow) {
    targetRow.classList.remove("drag-over");
  }
});

// Move the dragged row to the drop target position
table.addEventListener("drop", function(event) {
  event.preventDefault();
  var targetRow = event.target.closest("tr");
  if (targetRow && draggedRow !== targetRow) {
    // Determine whether to insert before or after the drop target
    var targetIndex = Array.from(table.rows).indexOf(targetRow);
    var draggedIndex = Array.from(table.rows).indexOf(draggedRow);
    if (draggedIndex < targetIndex) {
      targetRow.parentNode.insertBefore(draggedRow, targetRow.nextSibling);
    } else {
      targetRow.parentNode.insertBefore(draggedRow, targetRow);
    }

    $.ajax({
        type: 'GET',
        url: "/change_sequence/"+draggedRow.id +"/"+targetRow.id+"/",
        success: function (data) {
           },
        error: function (response) {
            }
        }
    )
  }
  // Reset the drop target row highlight
  targetRow.classList.remove("drag-over");
});


function open_edit_popup(event,id_, case_id, function_id, task_id){
  event.preventDefault()
  $.ajax({
    type: 'GET',
    url: "/get_info/?task_detail_id="+id_+"&case_id="+case_id+"&function_id="+function_id+"&task_id="+task_id,
    success: function (data) {
            $('#popup_data_body').html('');
            $('#popup_data_body').append(data['body']);

            $('#popup_data_footer').html('');
            $('#popup_data_footer').append(data['footer'])
       },
    error: function (response) {
        alert("Please add atleast 1 step");
        }
    }
) 
}

function changed_start_time(){
  var start_id = document.getElementById("start_time_id");
  localStorage.setItem('start_time_id', start_id.value);
}

function changed_end_time(){
  var end_id = document.getElementById("end_time_id");
  localStorage.setItem('end_time_id', end_id.value); 
}


window.addEventListener('load', (event) => {
  const current_date = new Date();
  var start_id = document.getElementById("start_time_id");
  var end_id = document.getElementById("end_time_id");
  old_start = localStorage.getItem('start_time_id');
  old_end = localStorage.getItem('end_time_id');
  if (old_start){
    start_id.value = old_start
  }
  else{
    const startdate = current_date
    start_id.value = startdate.toISOString().slice(0,16);
    localStorage.setItem('start_time_id', startdate.toISOString().slice(0,16));
  }
  if (old_end){
    end_id.value = old_end
  }
  else{
    const enddate = new Date(current_date.getTime() + 10*60000);
    end_id.value = enddate.toISOString().slice(0,16);
    localStorage.setItem('end_time_id', enddate.toISOString().slice(0,16)); 
  }

});

function delete_case_detail(task_detail_id, case_detail_id, function_detail_id, task_id){
  var elem = document.getElementById('task_detail_deletion')
  elem.value = task_detail_id
  var elem = document.getElementById('case_detail_deletion')
  elem.value = case_detail_id
  var elem = document.getElementById('function_detail_deletion')
  elem.value = function_detail_id
  var elem = document.getElementById('task_detail_id_deletion')
  elem.value = task_id
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function add_task(case_id){
  var alias = document.getElementById("alias").value;
  var fid = document.getElementById("fid").value;
  var function_input = document.getElementById("function_input").value;
  // var multiple_input_checkbox = document.getElementById("multiple_input_check").checked;
  // var multiple_input_select = document.getElementById("input_dataframe");
  var multiple_input_select = document.getElementById("input_functions_params").textContent
  // console.log(multiple_input_select)
  var external_config = document.getElementById("put_external_config").querySelectorAll("input")
  var values = {}
  for (const input of external_config){
    values[input.name] = input.value
  }
  console.log(values)
  
  // var selectedValues = "";
    
  //   for (var i = 0; i < multiple_input_select.options.length; i++) {
  //     var option = multiple_input_select.options[i];
      
  //     if (option.selected) {
  //       selectedValues += option.value+',';
  //     }
  //   }
  // if (selectedValues.length==0 & function_input){
  //   var err_txt = $('#input_param-error-txt');
  //   if (err_txt.hasClass('d-block')){
  //       err_txt.removeClass('d-block');
  //       err_txt.addClass('d-none');
  //   }
  //   if (err_txt.hasClass('d-none')){
  //       err_txt.addClass('d-block');
  //       err_txt.text(`Please select atleast one input.`);
  //   }
  //   return
  // }
  datas= {"alias": alias, "fid": fid, "case_id": case_id, "function_input": function_input, "input_files": multiple_input_select, "external_config": values}
  console.log(datas)
  $.ajax({
    type: 'POST',
    url: "/add_task/",
    // data: {"alias": alias, "fid": fid, "case_id": case_id},
    headers: {
      "X-CSRFToken": getCookie("csrftoken")
    },
    data:JSON.stringify(datas),
    contentType: 'application/json',
    success: function (data) {
      console.log("HHHHHHHH")
            location.reload()
       },
    error: function (response) {
      console.log(response);
      alert("Please choose different alias  name")
        }
    }
);
  
}


function get_dropdown(case_id){
  console.log("this filedones")
  var multiple_input = document.getElementById("multiple_input_check").checked
  if (multiple_input){
    $.ajax({
      type: 'get',
      url: "/get_multiple_input/?case_id="+case_id,
      data:{},
      contentType: 'application/json',
      success: function (data) {
              console.log(data)
              $('#input_dataframe').html('');
              row = ""
              data.map((item)=>{
                row = row + "<option value='"+item+"'"+">" +item+"</option>"
              })
              $('#input_dataframe').append(row);
          
              var selectElement = document.getElementById("input_dataframe");
              selectElement.removeAttribute("disabled");
              console.log("in success")
      },
      error: function (response) {
        console.log(response);
        alert("Please choose different alias  name")
          }
      }
  );
  }
  else{
    $('#input_dataframe').html('');
    var selectElement = document.getElementById("input_dataframe");
    selectElement.disabled = true;

  }
  
}


function check_for_multiple_input(case_id){
  var function_input = document.getElementById("function_input").value;
  console.log(function_input)
  $.ajax({
    type: 'get',
    url: "/check_for_multiple_input/?function="+function_input+"&case="+case_id,
    data:{},
    contentType: 'application/json',
    success: function (data) {
            console.log(data)
            if (data.length){
              $('#input_dataframe').html('');
            row = ""
            data.map((item)=>{
              row = row + "<option value='"+item+"'"+">" +item+"</option>"
            })
            $('#input_dataframe').append(row);
        
            var selectElement = document.getElementById("input_dataframe");
            selectElement.removeAttribute("disabled");
            }
            // $('#input_dataframe').html('');
            // row = ""
            // data.map((item)=>{
            //   row = row + "<option value='"+item+"'"+">" +item+"</option>"
            // })
            // $('#input_dataframe').append(row);
        
            // var selectElement = document.getElementById("input_dataframe");
            // selectElement.removeAttribute("disabled");
            // console.log("in success")
    },
    error: function (response) {
      console.log(response);
      var selectElement = document.getElementById("input_dataframe");
      selectElement.disabled = true
      $('#input_dataframe').html('');
        }
    }
);  
}

function check_for_multiple_input_in_merge(case_id, k){
  console.log("merge_function_input_"+k)
  var function_input = document.getElementById("merge_function_input_"+k).value;
  console.log(function_input)
  $.ajax({
    type: 'get',
    url: "/check_for_multiple_input/?function="+function_input+"&case="+case_id,
    data:{},
    contentType: 'application/json',
    success: function (data) {
            console.log(data)
            if (data.length){
              $('#merge_input_dataframe_'+k).html('');
            row = ""
            data.map((item)=>{
              row = row + "<option value='"+item+"'"+">" +item+"</option>"
            })
            $('#merge_input_dataframe_'+k).append(row);
        
            var selectElement = document.getElementById("merge_input_dataframe_"+k);
            selectElement.removeAttribute("disabled");
            }
            // $('#input_dataframe').html('');
            // row = ""
            // data.map((item)=>{
            //   row = row + "<option value='"+item+"'"+">" +item+"</option>"
            // })
            // $('#input_dataframe').append(row);
        
            // var selectElement = document.getElementById("input_dataframe");
            // selectElement.removeAttribute("disabled");
            // console.log("in success")
    },
    error: function (response) {
      console.log(response);
      var selectElement = document.getElementById("merge_input_dataframe_"+k);
      selectElement.disabled = true
      $('#merge_input_dataframe_'+k).html('');
        }
    }
);  
}


