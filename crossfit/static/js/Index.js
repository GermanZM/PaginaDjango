setInterval('Index()', 500);

var mov = 0;

function Index(){

	if (mov == 0) {
		document.getElementById('usuariosR').style.transform = 'translateX(12px)';
		document.getElementById('reservasCross').style.transform = 'translateX(12px)';
    	mov = 1;
	} else {

		document.getElementById('usuariosR').style.transform = 'translateX(-12px)';
		document.getElementById('reservasCross').style.transform = 'translateX(-12px)';
		mov = 0;
	}

}