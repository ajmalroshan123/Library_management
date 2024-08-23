// Copyright (c) 2024, Ajmal Roshan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Library Transaction", {
// 	refresh(frm) {

// 	},
// });


// frappe.ui.form.on("Library Transaction", {
//     onload(frm) {
//         frm.set_query('library_member', () => {
//             return{
//                 filters: {
//                     last_name : 'Bhai'
//                 }
//             }
//         })
//     }
// });

frappe.ui.form.on('Library Transaction', {
    onload: function (frm) {
        frm.set_query('library_member', function () {
            return {
                filters: [
                    ['Library Member', 'name', 'in', get_valid_members()]
                ]
            };
        });
    }
});

function get_valid_members() {
    var valid_members = [];
    frappe.call({
        method: 'library_management.library_management.doctype.library_transaction.library_transaction.get_valid_library_members',
        async: false,
        callback: function (r) {
            if (r.message) {
                valid_members = r.message;
            }
        }
    });
    return valid_members;
}
