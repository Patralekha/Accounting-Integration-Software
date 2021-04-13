/*           CHECKS INTERNET CONNECTION           */

var offLine=false;

window.addEventListener("online", connectionUpdate);
window.addEventListener("offline", connectionUpdate);

function connectionUpdate(event) {
  if (navigator.onLine) {
    if (offLine) {
     
      document.getElementById("connectionStatus").innerHTML =
        "<br><span class='btn btn-outline-success' id='statusOnline'>You are back online...</span>";
      setTimeout(function () {
        $("#statusOnline").fadeOut("slow");
      }, 2000);
      offLine = !offLine;
    }
  } else {
    
    document.getElementById("connectionStatus").innerHTML =
      "<br><span class='btn btn-outline-danger'> <i class='fas fa-cloud'></i>Oops!! You are offline!You cannot make any request to the server now!</span>";
      offLine = !offLine;
  }
}

/*  ##############################################################################################      */


function loop(data,str){
  var i;
  var c=1;
  for (i = 1; i <= data['sets']; i++) { 
    if(i==1){
          $(str).append(
                `
                <a class="dropdown-item" onclick="load('','','','','','','',${0},${1000})">Latest 1000</a>
                `
          );

      }else if(i==data['sets']){
        $(str).append(
          `
          <a class="dropdown-item" onclick="load('','','','','','','',${c},${c+data['lastSet']-1})" id="last">${c} - ${c+data['lastSet']-1}</a>
          `
    );
      }else{
        $(str).append(
          `<a class="dropdown-item" onclick="load('','','','','','','',${c},${c+999})" id="last">${c} - ${c+999}</a>`
        );

      }
      c+=1000;
  }
}

//<option value="${c} - ${c+99}">${c} - ${c+99}</option>
//<option value="${c} - ${c+data['lastSet']-1}" id="last">${c} - ${c+data['lastSet']-1}</option>


/*$(document).on('change', 'select', function() {
  //console.log($(this).val()); // the selected options’s value

  // if you want to do stuff based on the OPTION element:
  var opt = $(this).find('option:selected')[0];
  var set=$(this).val();
  
});
*/


function totalRec(){
  var token = "Token ";
  var token1 = sessionStorage.getItem("auth");
  var authorization = token.concat(token1);
  if (sessionStorage.getItem("auth") === null) {
    window.location.href = "login.html";
  }
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/getTotalRecs/",
    headers: { Authorization: authorization },
    success: function (data) {
       //console.log(data);
      loop(data,'#records');
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });


}





window.onload = function(){
  if (sessionStorage.getItem("adminPrivilege") == "true") {
    document.getElementById("admin").style.display = "block";
  }
  //$('#myModal').modal('show');
  totalRec();
  load('','','','','','','',0,1000);
}


function logout() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/logout/",
    success: function (data) {
      sessionStorage.removeItem("name");
      sessionStorage.removeItem("adminPrivilege");
      sessionStorage.removeItem("auth", "");
      window.location.href = "login.html";
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}


/*                   CLIENT SIDE DATA FETCH AND PAGINATED DISPLAY                      */

function load (a,b,c,d,e,f,g,i,j) {
  var token = "Token ";
  var token1 = sessionStorage.getItem("auth");
  var authorization = token.concat(token1);
  if (sessionStorage.getItem("auth") === null) {
    window.location.href = "login.html";
  }


  var body={
    "accName":a,
    "stDate":b,
    "endDate":c,
    "stAmt":d,
    "endAmt":e,
    "de":f,
    "cr":g,
    "start":i,
    "end":j
  };
  if(typeof(a)=="undefined"){
    body={
      "accName":'',
      "stDate":'',
      "endDate":'',
      "stAmt":'',
      "endAmt":'',
      "de":'',
      "cr":'',
      "start":i,
      "end":j
    };
  }
  console.log(i+" "+j);
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/transactions/",
    headers: { Authorization: authorization },
    data:body,
    success: function (data) {
      $("#transactionsTable").dataTable().fnDestroy();
      


var netDebit=[];
var netCredit=[];
var dateList=[];

     
      var buttonCommon = {
        exportOptions: {
          format: {
            body: function (data, row, column, node) {
              // Strip $ from amount column to make it numeric
              return column === 5 ? data.replace(/[$,]/g, "") : data;
            },
          },
        },
      };

      var table = $("#transactionsTable").DataTable({
        orderCellsTop: true,
        fixedHeader: false,
        data:data,
        columns: [
          { data: "accountId"},
          { data: "accountName"},
          { data: "amount"},
          { data: "accountType"},
          { data: "date"},
          { data: null,
            render: function(data,type,row){
              
              var p=data['extraFields'];
              
              if(p!=null)
              {console.log(typeof(p));}
              
              return (data['extraFields']);
            }
          }
        ],
        columnDefs: [
          { width: '60%', targets: 0 },
          { width: '100%', targets: 2 },
          { width: '100%', targets: 3 },
          { width: '100%', targets: 4 },
          { width: '60%', targets: 5 },
         
      ],
      dom: "<Bfrl<t>ip>",
      buttons: [
         'copy','pdf','excel','csv','print'
      ],
       initComplete: function () {
        var count = 0;
        this.api().columns([0,1,2,3,4]).every( function () {
            var title = this.header();
            //replace spaces with dashes
            title = $(title).html().replace(/[\W]/g, '-');
            var column = this;
            var select = $('<select id="' + title + '" class="select2" ></select>')
                .appendTo( $(column.footer()).empty() )
                .on( 'change', function () {
                  //Get the "text" property from each selected data 
                  //regex escape the value and store in array
                  var data1 = $.map( $(this).select2('data'), function( value, key ) {
                    return value.text ? '^' + $.fn.dataTable.util.escapeRegex(value.text) + '$' : null;
                             });
                  
                  //if no data selected use ""
                  if (data1.length === 0) {
                    data1= [""];
                  }
                  
                  //join array into string with regex or (|)
                  var val = data1.join('|');
                  
                  //search for the option(s) selected
                  column
                        .search( val ? val : '', true, false )
                        .draw();
                } );

            column.data().unique().sort().each( function ( d, j ) {
                select.append( '<option value="'+d+'">'+d+'</option>' );
            } );
          
          //use column title as selector and placeholder
          $('#' + title).select2({
            multiple: true,
            closeOnSelect: false,
            placeholder: "Select " + title,
            width: '100%'
          });
          
          //initially clear select otherwise first option is selected
          $('.select2').val(null).trigger('change');
        } );
    },
    
    
    footerCallback: function ( row, data, start, end, display ) {
      var api = this.api(), data;

      // Remove the formatting to get integer data for summation
      var intVal = function ( i ) {
          return typeof i === 'string' ?
              i.replace(/[\$,]/g, '')*1 :
              typeof i === 'number' ?
                  i : 0;
      };

          var cr = 0;
          var dr = 0;

          var data1=data;
      var data2 =api.rows( { search:'applied' } ).data().each(function(value, index) {
        //console.log(value, index);
        if(value['accountType']==='Credit'){
          cr+=parseFloat(value['amount']);
        }else{
          dr+=parseFloat(value['amount']);
        }

       
    });
    //console.log(data2);


      // Total over this page
      var pageTotal = api
          .column( 2,{filter:'applied'} )
          .data()
          .reduce( function (a, b) {
           
              return parseFloat(a) + parseFloat(b);
          }, 0 );


      // Update footer
      $( api.column( 2 ).footer() ).html(
          'Net: '+pageTotal.toFixed(2) +'<br/> Credit:'+ cr.toFixed(2) +'<br/> Debit: '+ dr.toFixed(2)
      );

   
      var dates=api.column( 4,{ search:'applied' } ).data().unique();
      dates.sort();
      netDebit=[];
      netCredit=[];
      dateList=[];
       dateList=dates.toArray();
      dateList.forEach(function(date) {
  
        var debit=0.0;var credit=0.0;
        var g=data2.filter(function(l){

          if(l['date'] === date){
            if(l['accountType']==='Debit'){
              debit+=parseFloat(l['amount']);
            }else{
              credit+=parseFloat(l['amount']);
            }
          }
      });
      netDebit.push(parseFloat(debit.toFixed(2)));
      netCredit.push(parseFloat(credit.toFixed(2)));
      
      var s=date+" "+debit.toFixed(2)+" "+credit.toFixed(2);
      //console.log(netCredit);
     
      
    });
    plotChart(netDebit,netCredit,dateList);
   //console.log('\n');
   
  }
         
      });
     
    
    },
    error: function (response) {
      alert(response["statusText"]);
    },
  });
}

/*  ###########################################################################     */


/*                     SERVER SIDE PAGINATED FETCH                  */

function paginated(a,b,c,d,e,f,g){

  var token = "Token ";
  var token1 = sessionStorage.getItem("auth");
  var authorization = token.concat(token1);
  if (sessionStorage.getItem("auth") === null) {
    window.location.href = "login.html";
  }


  var body={
    "accName":a,
    "stDate":b,
    "endDate":c,
    "stAmt":d,
    "endAmt":e,
    "de":f,
    "cr":g,
  };
  if(typeof(a)=="undefined"){
    body={
      "accName":'',
      "stDate":'',
      "endDate":'',
      "stAmt":'',
      "endAmt":'',
      "de":'',
      "cr":'',
    };
  }
  


  document.getElementById("card1").style.display = "none";
  document.getElementById("card2").style.display = "none";
  document.getElementById("client").style.display = "none";
  document.getElementById("server").style.display = "block";


  var netDebit=[];
  var netCredit=[];
  var dateList=[];
  
       
        var buttonCommon = {
          exportOptions: {
            format: {
              body: function (data, row, column, node) {
                // Strip $ from amount column to make it numeric
                return column === 5 ? data.replace(/[$,]/g, "") : data;
              },
            },
          },
        };

       /* $('#example').on( 'page.dt', function () {
          var info = table.page.info();
          $('#pageInfo').html( 'Showing page: '+info.page+' of '+info.pages );
          } );*/
          $("#transactionsTable").dataTable().fnDestroy();
      
        var table = $("#transactionsTable").DataTable({
          dom: "<Bfrl<t>ip>",
        buttons: [
           'copy','pdf','excel','csv','print'
        ],
          orderCellsTop: true,
          fixedHeader: false,
          responsive: true,
        serverSide: true,
        processing: true,
        orderMulti : true,
        
          ajax: {
            type: "GET",
            url: 'http://127.0.0.1:8000/transactionsPaginated/',
            headers: { Authorization: authorization },
            body:body
        },
          columns: [
            { data: "accountId"},
            { data: "accountName"},
            { data: "amount"},
            { data: "accountType"},
            { data: "date"},
          ],
          columnDefs: [
            { width: '60%', targets: 0 ,orderable: true,searchable:true},
            { width: '60%', targets: 1 ,orderable: true,searchable:true},
            { width: '100%', targets: 2,orderable: true,searchable:true },
            { width: '100%', targets: 3,orderable: true,searchable:true },
            { width: '100%', targets: 4,orderable: true,searchable:true}
        ],


        initComplete: function () {
          var count = 0;
          var min = $('#min').val();
          var max = $('#max').val();
          
          this.api().columns().every( function () {
              var title = this.header();
              //replace spaces with dashes
              title = $(title).html().replace(/[\W]/g, '-');
              var column = this;
              var select = $('<select id="' + title + '" class="select2" ></select>')
                  .appendTo( $(column.footer()).empty() )
                  .on( 'change', function () {
                    //Get the "text" property from each selected data 
                    //regex escape the value and store in array
                    var data1 = $.map( $(this).select2('data'), function( value, key ) {
                      return value.text ? '^' + $.fn.dataTable.util.escapeRegex(value.text) + '$' : null;
                               });
                    
                    //if no data selected use ""
                    if (data1.length === 0) {
                      data1= [""];
                    }
                    
                    //join array into string with regex or (|)
                    var val = data1.join('|');
                    
                    //search for the option(s) selected
                    column
                          .search( val ? val : '', true, false )
                          .draw();
                  } );
  
              column.data().unique().sort().each( function ( d, j ) {
                  select.append( '<option value="'+d+'">'+d+'</option>' );
              } );
            
            //use column title as selector and placeholder
            $('#' + title).select2({
              multiple: true,
              closeOnSelect: false,
              placeholder: "Select " + title,
              width: '100%'
            });
            
            //initially clear select otherwise first option is selected
            $('.select2').val(null).trigger('change');
          } );
      },
      drawCallback:function( settings ) {
        var min = $('#min').val();
        var max = $('#max').val();
        console.log(min);
        console.log(max);
    },
      
      footerCallback: function ( row, data, start, end, display ) {
        var api = this.api(), data;
        
  
        // Remove the formatting to get integer data for summation
        var intVal = function ( i ) {
            return typeof i === 'string' ?
                i.replace(/[\$,]/g, '')*1 :
                typeof i === 'number' ?
                    i : 0;
        };
  
            var cr = 0;
            var dr = 0;
  
            var data1=data;
        var data2 =api.rows( { search:'applied' } ).data().each(function(value, index) {
          //console.log(value, index);
          if(value['accountType']==='Credit'){
            cr+=parseFloat(value['amount']);
          }else{
            dr+=parseFloat(value['amount']);
          }
  
         
      });
      //console.log(data2);
  
  
        // Total over this page
        var pageTotal = api
            .column( 2,{filter:'applied'} )
            .data()
            .reduce( function (a, b) {
             
                return parseFloat(a) + parseFloat(b);
            }, 0 );
  
  
        // Update footer
        $( api.column( 2 ).footer() ).html(
            '$'+pageTotal.toFixed(2) +' ( $'+ cr.toFixed(2) +' Cr)'+' ( $'+ dr.toFixed(2) +' De)'
        );
  
     
        var dates=api.column( 4,{ search:'applied' } ).data().unique();
        dates.sort();
        netDebit=[];
        netCredit=[];
        dateList=[];
         dateList=dates.toArray();
        dateList.forEach(function(date) {
    
          var debit=0.0;var credit=0.0;
          var g=data2.filter(function(l){
  
            if(l['date'] === date){
              if(l['accountType']==='Debit'){
                debit+=parseFloat(l['amount']);
              }else{
                credit+=parseFloat(l['amount']);
              }
            }
        });
        netDebit.push(parseFloat(debit.toFixed(2)));
        netCredit.push(parseFloat(credit.toFixed(2)));
        
        var s=date+" "+debit.toFixed(2)+" "+credit.toFixed(2);
        //console.log(netCredit);
       
        
      });
      plotChart(netDebit,netCredit,dateList);
     //console.log('\n');
     
    }
           
        });
        
}


/*########################################################################################*/

/*         GRAPH /CHART GENERATION FUNCTION              */

function plotChart(netDebit,netCredit,dateList){
  var fdate=$("#filterDate");
 
    var container = $("<div/>").insertBefore(fdate);
  Highcharts.chart('chart', {
    title: {
      text: 'Net debit/credit on a particular date'
  },  
      chart:{
      type:'area'
      },
      xAxis: {
          categories: dateList
      },
       yAxis: {
         allowDecimals:true,
      
          title: {
              text: 'Net Amount'
          }
      },
      series:[{
      name:'Debit',
      data:netDebit,
      color: '#32a850',
      },
      {
        name:'Credit',
        data:netCredit,
        color: '#ba1e28',
        }
    ]
  
  });
  }
  
  
/* #########################################################################*/

/*                     AMOUNT AND DATE RANGE FILTERS              */

$('.input-daterange input').each(function() {
  $(this).datepicker('clearDates');
});

// Extend dataTables search
$.fn.dataTable.ext.search.push(
  function(settings, data, dataIndex) {
    var min = $('#min').val();
    var max = $('#max').val();
    var createdAt = data[4] || 4; // Our date column in the table

    if((min == "" || max == "") ||(moment(createdAt).isSameOrAfter(min) && moment(createdAt).isSameOrBefore(max)))
     {
    return true;
}

    return false;
  }
);


$(document).ready(function () {
  $('.date-range-filter').change(function() {
    //console.log("True");
      var table = $('#transactionsTable').DataTable();
    table.draw();
  });

 
 

  document.getElementById("min").value="";
  document.getElementById("max").value="";
  
  $('#data-table_filter').hide();
  
  });



/* Custom filtering function which will search data in column four between two values */
$.fn.dataTable.ext.search.push(
	function( settings, data, dataIndex ) {
		var min = parseFloat( $('#mina').val(), 10 );
		var max = parseFloat( $('#maxa').val(), 10 );
		var amt = parseFloat( data[2] ) || 0; // use data for the amt column

		if ( ( isNaN( min ) && isNaN( max ) ) ||
			 ( isNaN( min ) && amt <= max ) ||
			 ( min <= amt   && isNaN( max ) ) ||
			 ( min <= amt   && amt <= max ) )
		{
			return true;
		}
		return false;
	}
);

document.addEventListener('keyup', redraw);


function redraw(e){
  var table = $('#transactionsTable').DataTable();
      table.draw();

}
/* #######################################################################################    */

/*                  AMOUNT AND DATE FILTERS CLEARING             */


  function clearAmount(){
    document.getElementById("mina").value="";
    document.getElementById("maxa").value="";
    var table = $('#transactionsTable').DataTable();
    table.draw();
  }


  function clearDates(){
    document.getElementById("min").value="";
    document.getElementById("max").value="";
    var table = $('#transactionsTable').DataTable();
    table.draw();
  }



/*  ################################################################################   */

/*      PROCESS MODAL INPUTS ON FORM SUBMIT AND SEND TO load() OR paginated FUNCTION  */


$(document).ready(function() { 
$( "#filterData" ).submit(function( event ) {
 
 event.preventDefault();
 
  var open=document.getElementById("stAmt").value;
  var close=document.getElementById("endAmt").value;
  var stD=$("input[name=stDate]").val();
  var endD=$("input[name=endDate]").val();
  var accName=document.getElementById("accName").value;
  var de=document.getElementById('ide').checked?"Debit":'';
  var cr=document.getElementById('icr').checked?"Credit":'';
  var t=open+" "+close+" "+stD+" "+endD+" "+accName+" "+de+" "+cr;
  console.log(de);
  console.log(cr);
  console.log(t);
  load(accName,stD,endD,open,close,de,cr,'','');

});

});



function clearForm(){
  document.getElementById('filterData').reset();
  load('','','','','','','',0,1000);
}