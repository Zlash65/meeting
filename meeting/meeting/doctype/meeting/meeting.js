// Copyright (c) 2017, frappe and contributors
// For license information, please see license.txt

var attendeeList =[];
if(cur_frm.doc.attendees != undefined){
	attendeeList = getName();
}

function getName(){
	var x = [];
	for(i=0;i<cur_frm.doc.attendees.length;i++){
		x.push(cur_frm.doc.attendees[i].attendee);
	}
	return x;
}

frappe.ui.form.on("Meeting", {
	send_emails: function(frm){
		if(frm.doc.status==="Planned"){
			frappe.call({
				method: "meeting.api.send_invitation_emails",
				args: {
					meeting: frm.doc.name
				},
				callback: function(r){
					
				}
			});
		}
	}
});

frappe.ui.form.on('Meeting Attendee', {
	attendee: function(frm, cdt, cdn) {
		var attendee = frappe.model.get_doc(cdt, cdn);
		
		if(attendeeList.includes(attendee.attendee)){
			x = attendeeList.length;
			cur_frm.get_field("attendees").grid.grid_rows[x].remove();
			frappe.msgprint("Attendee already in list");
		}
		else if(attendee.attendee!=null && attendee.attendee!="")
		{
			attendeeList.push(attendee.attendee);
			frappe.call({
				method: "meeting.meeting.doctype.meeting.meeting.get_full_name",
				args: {
					attendee: attendee.attendee
				},
				callback: function(r){
					frappe.model.set_value(cdt, cdn, "full_name", r.message);
				}
			});
		}
	},
	attendees_remove: function(frm){
		var x = getName();
		removed = attendeeList.filter( function( el ) {
			return x.indexOf( el ) < 0;
		});
		for(i=0;i<attendeeList.length;i++){
			if(removed[0] == attendeeList[i]){
				attendeeList.splice(i,1);
				break;
			}
		}
	}
});