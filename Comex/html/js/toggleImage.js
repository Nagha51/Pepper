function toggleImage(number) {
	number = 1
	var imgID = "#img" + number
	$(imgID).fadeToggle(2000);
}

function init(){
	// $(".img").hide()
	setTimeout(function()
	{
		toggleImage(1);
	}, 500);
}
