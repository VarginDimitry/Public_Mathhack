function OpenAnswer() {
	let doc = document.getElementsByClassName('answer-button');
	for (let i = 0; i < doc.length; i++){
		doc[i].addEventListener('click', function () {
			let content = this.nextElementSibling;
			if (content.style.maxHeight){
				content.style.maxHeight = null;
			}
			else {
				content.style.maxHeight = content.scrollHeight + 'px'
			}
		});
	}
}

function CorrectInputPoints() {
	let grades = [document.getElementById('id_task13'), document.getElementById('id_task14'), document.getElementById('id_task15'),
                document.getElementById('id_task16'), document.getElementById('id_task17'),
                document.getElementById('id_task18'), document.getElementById('id_task19')];
	for (let i = 0; i < grades.length; i++) {
	    if (i < 3) {
            grades[i].oninput = function () {
                if (!(grades[i].value === '0' || grades[i].value === '1' || grades[i].value === '2')) {
                    document.getElementById('id_task' + String(i + 13)).value = '';
                }
            };
        } else if (i < 5){
	        grades[i].oninput = function () {
                if (!(grades[i].value === '0' || grades[i].value === '1' || grades[i].value === '2' || grades[i].value === '3')) {
                    document.getElementById('id_task' + String(i + 13)).value = '';
                }
            };
        } else {
	        grades[i].oninput = function () {
                if (!(grades[i].value === '0' || grades[i].value === '1' || grades[i].value === '2' || grades[i].value === '3' || grades[i].value === '4')) {
                    document.getElementById('id_task' + String(i + 13)).value = '';
                }
            };
        }
    }
}

function OpenHeaderMenu() {
	let doc = document.getElementsByClassName('user-name');
	let pointer = document.getElementsByClassName('pointer');
	for (let i = 0; i < doc.length; i++){
		doc[i].addEventListener('click', function () {
			let content = this.nextElementSibling.nextElementSibling;
			if (content.style.maxHeight){
				content.style.maxHeight = null;
				//pointer.rotate(-180*Math.PI/180);
			}
			else {
				content.style.maxHeight = '100px';
				//pointer.rotate(180*Math.PI/180);
			}
		});
	}
}

function SwapTabsInMainMenu(){
	const tabLinks = document.querySelectorAll(".tabs .inner-tab-name");
	const tabPanels = document.querySelectorAll(".tabs-panel");

	for (let el of tabLinks) {
  		el.addEventListener("click", e => {
    		e.preventDefault();

    		document.querySelector(".tabs .tab-name.active").classList.remove("active");
    		document.querySelector(".tabs-panel.active").classList.remove("active");

		    const parentListItem = el.parentElement;
    		parentListItem.classList.add("active");
    		const index = [...parentListItem.parentElement.children].indexOf(parentListItem);

    		const panel = [...tabPanels].filter(el => el.getAttribute("data-index") == index);
    		panel[0].classList.add("active");
  		});
  	}
}

function WidthChangeButton() {
	window.onload = function(){
		document.getElementById('inner-change-button').style.width = document.getElementById('user-image').scrollWidth + 'px';
		if (document.getElementById('reset-button')){
			document.getElementById('reset-button').style.width = document.getElementById('inner-change-button').style.width;
		}
	};
	window.onload();
}

function SetStandardOfChanges() {
	window.onload = function () {
		// display = 'block';
		let name = document.getElementById('start_username');
		let up_input_name = document.getElementById('up_id_username');
		up_input_name.setAttribute('class', name.className);
		/*
		let input_name = document.getElementById('id_username');
		input_name.style.height = up_input_name.style.height;
		*/
		document.getElementById('id_username').style.height = '20px';//document.getElementById('up_id_username').style.height;
	};
	window.onload();
}