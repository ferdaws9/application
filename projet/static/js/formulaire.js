$(document).ready(function() {
	$("#annuler").click(function() {
		window.location.href = '/projet/';
	});
	if (document.getElementById('mdp')) {
		$("#mdp").click(function() {
			window.location.href = changer_mot_de_passe;
		});
	}
	
	
});
