// Copyright (c) 2017, frappe and contributors
// For license information, please see license.txt

var attendeeList =[];
for(i=0;i<cur_frm.doc.attendees.length;i++){
	attendeeList.push(cur_frm.doc.attendees[i].attendee);
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
	}
});