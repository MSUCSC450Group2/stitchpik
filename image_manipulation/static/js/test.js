clist = "#ff0000,#00ff00,#0000ff";

window.onload=function(){

  colors = clist.split(",");

	box=document.getElementById("box");
	
	if(colors != "") {
		for(var i=0; i<colors.length; i++) {
			var temp = document.createElement("input");
			var temp2 = document.createElement("div");
			var temp3 = document.createElement("p");
			temp3.className = "color_number";
			temp2.className = "holder";
			temp2.appendChild(temp3);
			temp2.appendChild(temp);
			temp.id = i;
			temp.type = "text";
			temp.className = "basicColor";
			temp.value = colors[i];
			box.appendChild(temp2);
		}
	}
	var temp = document.createElement("input");
	var temp2 = document.createElement("div");
	var temp3 = document.createElement("p");
	temp3.className = "empty_label";
	temp3.innerHTML = "new color";
	temp2.className = "holder";
	temp2.appendChild(temp3);
	temp2.appendChild(temp);
	temp.type = "text";
	temp.className = "emptyColor";
	temp.value = "";
	box.appendChild(temp2);

	$(".basicColor").bind("change", colorHandler);
	update();
  olist();
}

update = function() {
	$(".basicColor").spectrum({
		preferredFormat: "hex",
		allowEmpty:true
	});
	$(".emptyColor").spectrum({
		preferredFormat: "hex",
		allowEmpty:true
	});
	$(".emptyColor").bind("change", emptyHandler);
	colorLabel();
}

colorHandler = function() {
	if($(this).val() == "") {
		$(this).spectrum("destroy");
		$(this).prev().remove();
		$(this).parent().remove();
		$(this).remove();
	}
	olist();
}

colorLabel = function() {
	$(".color_number").each(function(index,element) {
		this.innerHTML = "Color #"+index;
	});
}

emptyHandler = function() {
	if($(this).val() != "") {
		$(this).attr('class','basicColor');
		var temp2 = document.createElement("div");
		var temp3 = document.createElement("p");
		var temp = document.createElement("input");
		$(this).prev().attr('class','color_number');
		temp3.innerHTML = "new color";
		temp2.className = "holder"
		temp3.className = "empty_label";
		temp.type = "text";
		temp.className = "emptyColor";
		temp.value = "";
		temp2.appendChild(temp3);
		temp2.appendChild(temp);
		box.appendChild(temp2);
		$(this).unbind("change", emptyHandler);
		$(this).bind("change",colorHandler);
		update();
		olist();
	}
}

olist = function() {
	var ostring = "";
  var tlen = $(".basicColor").length;
	$(".basicColor").each(function(index, element) {
		ostring += $(this).val();
    //ostring += "," + index + ",";
    if(index < tlen - 1) {
      ostring += ",";
    }
	});
	$("#out").text(ostring);
}
