$(document).ready(function(){
	init()
})

function init(){
	toggleImage(logosogeicon)
	// setTimeout(function()
	// {
	// 	toggleImage(logosoge);
	// }, 3000);
}

function hideAll(thesethings){
	$(thesethings).fadeOut(500);
}

function toggleImage(name){
	hideAll(".img");
	var nameID = "#" + name;
	setTimeout(function()
	{
		$(name).fadeToggle(2000);
	}, 500);

}

