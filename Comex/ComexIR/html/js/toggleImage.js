var session;
// var ip = "192.168.8.101";

$(document).ready(function(){
	init()
	$('#exitApplication').css('cursor','default');

    var locked = false;
    $('.dialogable').on('click touchend', function(){
        if (!locked) {
            locked = true;
            var _this = $(this);
            var aDire = "\""+ _this.attr("name") + "\"";
            createSession( function(){
                lancerDialogue(aDire);
            });
            setTimeout(unlock, 2000);
        }
	});
})

function init(){
	toggleImage(logosogeicon)
}

function createSession(callback){
	try {
		QiSession( function (s) {
			console.log('connected!');
			session = s;
			callback();
		});
		// },disconnected,ip);
	}catch (err) {
	  console.log("Error when initializing QiSession: " + err.message);
	  console.log("Make sure you load this page from the robots server.");
	}
}

function lancerDialogue(aDire){
	session.service('ALDialog').then(function (ald){
		//setFocus sur le bon topic si jamais ca ne marche pas
		ald.forceInput(aDire);
	},function (error){
		alert(error);
		console.log(error);
  });
};

function unlock () {
    locked = false;
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

function disconnected() {
  console.log("disconnected");
}
