var session;
// var ip = "192.168.8.103";
var beforeIdleSeconds = 62;
var idleSeconds = 70;

$(document).ready(function(){
    createSession()
    $(function(){
      var beforeIdleTimer;
      var idleTimer;
      function resetTimer(){
        console.log("resetTimer")
        clearTimeout(beforeIdleTimer);
        clearTimeout(idleTimer);
        idleTimer = setTimeout(whenUserIdle,idleSeconds*1000);
        beforeIdleTimer = setTimeout(beforeIdle,beforeIdleSeconds*1000);
      }
      $(document.body).bind('touchstart',resetTimer);
      $(document.body).bind('touchstart',
          function () {
            if($(this).is(':animated')) {
                console.log("stopAnimation")
               $(this).stop().fadeIn(500);
            }
          }
      );
      resetTimer(); // Start the timer when the page loads
    });
});


function beforeIdle() {
  console.log("beforeIdle")
  $(document.body).fadeOut(10000)
}

function whenUserIdle(){
    console.log("FIN")
    session.service('ALMemory').then(function (alm){
    //setFocus sur le bon topic si jamais ça ne marche pas
    // alert("Iddled")
    alm.raiseEvent("robotState", "777");
},function (error){
    alert(error);
    console.log(error);
});
  // raiseEvent("robotState","1")
}


function disconnected() {
  console.log("disconnected");
}

function getIntFromString (stringAParser){
	console.log(stringAParser);
		return parseInt(stringAParser.replace(/[^0-9\.]/g, ''), 10);
}

function createSession(callback){
	try {
		QiSession( function (s) {
			console.log('connected!');
			session = s;
			callback();
		});/*,disconnected,ip);*/
	}catch (err) {
	  console.log("Error when initializing QiSession: " + err.message);
	  console.log("Make sure you load this page from the robots server.");
	}
};

function lancerDialogue(aDire){
	session.service('ALDialog').then(function (ald){
		//setFocus sur le bon topic si jamais รงa ne marche pas
		ald.forceInput(aDire);
	},function (error){
		alert(error);
		console.log(error);
  });
};

function raiseEvent(key,value){
    session.service('ALMemory').then(function (alm){
		//setFocus sur le bon topic si jamais รงa ne marche pas
		alm.raiseEvent(key, value);
	},function (error){
		alert(error);
		console.log(error);
  });
};

function isInArray(value, array) {
  return array.indexOf(value) > -1;
};

// function backDialog(){
    // if (!locked) {
        // locked = true;
        // var _this = $(this);
        // var redirection = "1;" + _this.attr("redirection");
        // var dialog = "20;" + _this.attr("dialog");
        // session.service('ALMemory').then(function( memory) {
            // memory.raiseEvent("dialogURL",redirection);
            // memory.raiseEvent("dialogEngaged",dialog);
        // }, function (error) {
            // console.log(error);
            // setTimeout(unlock, 2000);
        // });
    // }
// };