$(document).ready(function(){
  $('#id_checkname').click(function(){
    //displayid = this.attr
    //console.log(displayid);
    displayArea = $(this).attr('disp');
    //alert(displayArea);
    $.ajax({
      url: 'checkname',
      data: { fullname : $('#id_name').val(), remark : 'This is my first ajax code.' },
      dataType: 'json',
      success: function (responseText){
        json = responseText;
        //console.log(json);
        html = '';
        if(json.customer){
          html += "<table class='popUpCustomer'>";
          html += "<tr class='row1'><td class='col1'>";
          html += json.customer[0].fields.name;
          html += "<br>";
          html += json.customer[0].fields.addr;
          html += thaiAddr(json.customer[0].fields.soi, ' ซ.');
          html += thaiAddr(json.customer[0].fields.road, ' ถ.');
          html += thaiAddr(json.customer[0].fields.moo, ' ม.');
          html += " ต." + json.customer[0].fields.tumbon;
          html += " อ." + json.customer[0].fields.amphur;
          html += " จ." + json.customer[0].fields.province;
          html += " " + json.customer[0].fields.postcode;
          html += "<br>โทร. " + json.customer[0].fields.tel;
          html += "<br>หมายเหตุ : " + json.customer[0].fields.remark;
          html += "</td><td class='col2'>";
          html += "<input type='button' id='id_setCustomerBack' onclick='setCustomerBack(json.customer[0])' value=' OK '>";
          html += "</td></tr></table>";
          html += "<table class='popUpCar'>";
          html += "<tr class='head'>";
          html += "<td class='col1 colPad'>#</td>";
          html += "<td class='col2'>เลขทะเบียน</td>";
          html += "<td class='col3'>รถ</td>";
          html += "<td class='col4'>รายการ</td>";
          html += "<td class='col5'>อัพเดทล่าสุด</td>";
          html += "<td class='col6'>ภาษีขาด</td>";
          html += "<td class='col7'>ภาษีใหม่</td>";
          html += "<td class='col8'>เลือก</td>";
          html += "</tr>";
          for(i in json.car_list){
            html += "<tr class='row"+ (parseInt(i)%2) +"'>";
            html += "<td class='colPad'>" + (parseInt(i)+1) + "</td>";
            html += "<td>" + json.car_list[i].fields.car_alphabet + " "
              + json.car_list[i].fields.car_number + " "
              + json.car_list[i].fields.car_province + "</td>";
            html += "<td>" + json.car_list[i].fields.car_type + "</td>";
            html += "<td>" +
              doList(json.car_list[i].fields.is_tro, 'ตรอ,') +
              doList(json.car_list[i].fields.is_insure, ' พรบ,') +
              doList(json.car_list[i].fields.is_paytax, ' ภาษี,') +
              doList(json.car_list[i].fields.is_special, ' นอก,') +
              "</td>";
            html += "<td>" + thaiDate(json.car_list[i].fields.update_date) + "</td>";
            html += "<td>" + thaiDate(json.car_list[i].fields.expire_date) + "</td>";
            html += "<td>" + thaiDate(getNextEndTax(json.car_list[i].fields.expire_date)) + "</td>";
            html += "<td><input type='button' name='setVal' onclick='setCustomerCarBack(json.customer[0], json.car_list["+i+"])' value='OK'></td>";
            html += "</tr>";
          }
          html += "</table>";
        }else{
          html += "<table class='popUpCustomer'>";
          html += "<tr class='row1'><td class='col1'>";
          html += "<div align='center'>ไม่พบข้อมูล</div>";
          html += "</tr></td></table>";
        }
        $('#'+displayArea).html(html);
        $('#id_setCustomerBack').focus();
      }
    });
  });
});

function thaiAddr(val, pre){
  addr = '';
  if(val){
    addr = pre + val;
  }
  return addr;
}

function doList(val, tran){
  result = '';
  if(val){
    result = tran;
  }
  return result;
}

function thaiDate(val){
  if(val != '-'){
    monthSet = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
    d = new Date(val);
    return d.getDate() + ' ' + monthSet[parseInt(d.getMonth())] + ' ' + parseInt(d.getFullYear()+543);
  }else{
    return val;
  }
}

function getNextEndTax(val){
  d = new Date(val);
  n = new Date();
  //console.log('d:'+d.getDate()+'-'+d.getMonth()+'-'+d.getFullYear());
  //console.log('n:'+n.getDate()+'-'+n.getMonth()+'-'+n.getFullYear());
  day = parseInt(n.getDate());
  next3m = parseInt(n.getMonth()+3);
  year = parseInt(n.getFullYear());
  // เช็คว่าขาดเกินหลายปีหรือไม่
  //console.log(year - parseInt(d.getFullYear()));
  if(year - parseInt(d.getFullYear()) > 1){
    //console.log('case');
    adjustEndYear = year - parseInt(d.getFullYear()) - 1;
    d.setFullYear(parseInt(d.getFullYear() + adjustEndYear));
  }
  // เช็คว่าถ้า +3 เดือนจะขึ้นปีใหม่ หรือไม่
  if(next3m > 11){
    next3m = next3m - 12;
    year = year + 1;
    if(day > 28 && next3m == 1) day = 28;
    if(day > 30 && (next3m == 0 || next3m == 2 || next3m == 4 || next3m == 6 || next3m == 7 || next3m == 9 || next3m == 11)) day = 30;
  }
  next3Date = new Date(year, next3m, day);
  //console.log('d:'+d.getDate()+'-'+d.getMonth()+'-'+d.getFullYear());
  //console.log('next3Date:'+next3Date.getDate()+'-'+next3Date.getMonth()+'-'+next3Date.getFullYear());
  // เช็คว่าต่อล้วงหน้าได้รึไม่
  if(d < next3Date){
    d.setFullYear(parseInt(d.getFullYear()+1));
    // เช็คว่าต้องเพิ่มปีหรือไม่
    if(d < n) d.setFullYear(parseInt(d.getFullYear()+1));
    return d;
  }else{
    return '-';
  }
}

function setCustomerBack(customer){
    $('#id_name').val(customer.fields.name);
    $('#id_addr').val(customer.fields.addr);
    $('#id_soi').val(customer.fields.soi);
    $('#id_road').val(customer.fields.road);
    $('#id_moo').val(customer.fields.moo);
    $('#id_tumbon').val(customer.fields.tumbon);
    $('#id_amphur').val(customer.fields.amphur);
    $('#id_province').val(customer.fields.province);
    $('#id_postcode').val(customer.fields.postcode);
    $('#id_tel').val(customer.fields.tel);
    $('#id_remark').val(customer.fields.remark);
    $('#id_car_alphabet').focus();
}

function setCustomerCarBack(customer, car){
  setCustomerBack(customer);
  $('#id_car_alphabet').val(car.fields.car_alphabet);
  $('#id_car_number').val(car.fields.car_number);
  $('#id_car_province').val(car.fields.car_province);
  car_type = $('[name="car_type"]');
  for(i=0; i<car_type.length; i++){
    if(car_type[i].value == car.fields.car_type) car_type[i].checked = true;
  }
  $('#id_is_tro').prop('checked', car.fields.is_tro);
  $('#id_is_insure').prop('checked', car.fields.is_insure);
  $('#id_is_paytax').prop('checked', car.fields.is_paytax);
  $('#id_is_special').prop('checked', car.fields.is_special);
  expireDate = getNextEndTax(car.fields.expire_date);
  day = '';
  month = '';
  year = '';
  try{
    day = String(expireDate.getDate());
    if(day.length < 2) day = '0'+day;
    month = String(parseInt(expireDate.getMonth()+1));
    if(month.length < 2) month = '0'+month;
    year = String(parseInt(expireDate.getFullYear())-1957);
  }catch(err){
    //console.log(err.message);
  }
  $('#id_expire_date').val(day+month+year);
  $('#id_expire_date').focus();
}
