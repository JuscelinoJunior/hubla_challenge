function showUploadFile() {
  Swal.fire({
    title: 'Upload txt file with sales',
    html:
      '<input type="file" id="file" class="swal2-input">',
    focusConfirm: false,
    preConfirm: () => {
      uploadFile();
    }
  })
}

function uploadFile() {
  const formData = new FormData();
  formData.append("file", document.getElementById("file").files[0]);

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://127.0.0.1:5000/upload_sales");
  // xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(formData);
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
      const objects = JSON.parse(this.responseText);
      if (this.status !== 200) {
        Swal.fire({icon: "error", text: objects["detail"]})
      } else {
        Swal.fire({icon: "success", text: "Sales registered successfully!"});
        loadTable();
      }
    }
  };
}


function loadTable() {
  const xhttp_owners = new XMLHttpRequest();
  xhttp_owners.open("GET", "http://127.0.0.1:5000/sales");
  xhttp_owners.send();
  xhttp_owners.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      console.log(this.responseText);
      let trHTML = '';
      const objects = JSON.parse(this.responseText);
      for (let object of objects) {
        let sale_date = new Date(object['date'])

        trHTML += '<tr>';
        trHTML += '<td>' + object['id'] + '</td>';
        trHTML += '<td>' + object['product'] + '</td>';
        trHTML += '<td>' + object['seller'] + '</td>';
        trHTML += '<td>' + object['type'] + '</td>';
        trHTML += '<td>' + object['value'] + '</td>';
        trHTML += '<td>' + (sale_date.getDay()+1).toString().padStart(2, "0") + "/" + (sale_date.getMonth()+1).toString().padStart(2, "0") + "/" + sale_date.getFullYear() + '</td>';
        trHTML += "</tr>";
      }
      document.getElementById("sales_table").innerHTML = trHTML;
    }
  };
}

loadTable();