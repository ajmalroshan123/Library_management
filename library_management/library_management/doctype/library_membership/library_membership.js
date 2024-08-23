// Copyright (c) 2024, Ajmal Roshan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Membership", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on('Library Membership',{
   from_date:function(frm) {

     if (frm.doc.from_date && frm.doc.to_date) {

       if(frm.doc.from_date > frm.doc.to_date){
         frm.set_value("from_date","")
         frappe.throw("The 'From Date' must be earlier than the 'To Date'.")
       }
     }
   },
   to_date:function(frm) {

     if (frm.doc.from_date && frm.doc.to_date) {

       if(frm.doc.from_date > frm.doc.to_date){
         frm.set_value("to_date","")
         frappe.throw("The 'From Date' must be earlier than the 'To Date'.")
       }
     }
   }





});
