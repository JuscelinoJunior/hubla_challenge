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
  xhttp.open("POST", "http://0.0.0.0:5050/upload_sales");
  xhttp.send(formData);
  xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
      const objects = JSON.parse(this.responseText);
      if (this.status !== 201) {
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
  xhttp_owners.open("GET", "http://0.0.0.0:5050/sales");
  xhttp_owners.send();
  xhttp_owners.onreadystatechange = function() {
    let tableHTML;
    let sales_table_identifier;
    let node;
    if (this.readyState === 4 && this.status === 200) {
      console.log(this.responseText);
      const sales = JSON.parse(this.responseText);
      i = 0
      let sales_list;
      for ([seller, sales_list] of Object.entries(sales)) {

        sales_table_identifier = "sales_table" + i

        tableHTML = "<div class=\"table-responsive\">\n" +
            `        <h3>${seller}</h3>` +
            "        <table class=\"table\">\n" +
            "          <thead>\n" +
            "            <tr>\n" +
            "              <th scope=\"col\">#</th>\n" +
            "              <th scope=\"col\">Product</th>\n" +
            "              <th scope=\"col\">Type</th>\n" +
            "              <th scope=\"col\">Value</th>\n" +
            "              <th scope=\"col\">Date</th>\n" +
            "            </tr>\n" +
            "          </thead>\n" +
            `          <tbody id=${sales_table_identifier}>\n` +
            "            <tr>\n" +
            "              <th scope=\"row\" colspan=\"5\">Loading...</th>\n" +
            "            </tr>\n" +
            "          </tbody>\n" +
            "        </table>\n" +
            "      </div>"

        node = document.createRange().createContextualFragment(tableHTML);
        document.getElementById("list").appendChild(node);

        let trHTML = '';
        let sum_value = 0;

        sales_list.forEach(function (item) {
          let sale_date = new Date(item.date)

          if (item.type === "Comissão paga") {
            sum_value -= item.value
          } else {
            sum_value += item.value
          }

          trHTML += '<tr>';
          trHTML += '<td>' + item.id + '</td>';
          trHTML += '<td>' + item.product + '</td>';
          trHTML += '<td>' + item.type + '</td>';
          trHTML += '<td>' + item.value + '</td>';
          trHTML += '<td>' + (sale_date.getDay() + 1).toString().padStart(2, "0") + "/" + (sale_date.getMonth() + 1).toString().padStart(2, "0") + "/" + sale_date.getFullYear() + '</td>';
          trHTML += "</tr>";
        })

        i++

        trHTML += `<h5>Total value: ${sum_value}</h5>`
        document.getElementById(sales_table_identifier).innerHTML = trHTML;
      }
    }
  };
}

loadTable();