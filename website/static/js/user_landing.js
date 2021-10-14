// select DOM elements
const time = document.getElementById('time'),
    greeting = document.getElementById('greeting'),
    username = document.getElementById('username'),
    focus = document.getElementById('focus');

// Options
const showAmPm = true;

// Show time
function showTime() {
    // let today = new Date(2021, 06, 10, 20, 33, 30),
    let today = new Date(),
        // today.getHours returns a number between 0 and 23
        hour = today.getHours(),
        min = today.getMinutes(),
        sec = today.getSeconds();

    // set AM or PM
    const amPm = hour >= 12 ? 'PM' : 'AM';

    // 12hr format
    hour = hour % 12 || 12;

    //output the time
    time.innerHTML = `${hour}<span>:</span>${addZero(min)}<span>:</span>${addZero(sec)} ${showAmPm ? amPm : ''}`;

    // call showTime every sec(1000msec)
    setTimeout(showTime, 1000);
}

// Add Zeros
function addZero(n) {
    return (parseInt(n, 10) < 10 ? '0' : '') + n;
}

// Set Background and Greeting
function setBGreet() {
    // let today = new Date(2021, 06, 10, 20, 33, 30),
    let today = new Date(),
        hour = today.getHours();

    if (hour < 12) {
        // Morning
        document.body.style.backgroundImage = "url('../img/morning.jpeg')";
        greeting.textContent = 'Good Morning';
    } else if (hour < 18) {
        // Afternoon
        document.body.style.backgroundImage = "url('../img/afternoon.jpeg')";
        greeting.textContent = 'Good Afternoon';
    } else {
        // Evening
        document.body.style.backgroundImage = "url('../img/evening.jpeg')";
        greeting.textContent = 'Good Evening';
        //document.body.style.color = 'white';
    }
}

// Get Name 
function getName() {
    // want to check if there is a local storage item called name
    if (localStorage.getItem('username') === null) {
        username.textContent = '[Enter Name]';
        username.blur();
    } else {
        username.textContent = localStorage.getItem('username');
    }
}

// Set Name
function setName(e) {
    if (e.type === 'keypress') {
        // Make sure enter is pressed
        if (e.which == 13 || e.keyCode == 13) {
            localStorage.setItem('username', e.target.innerText);
            username.blur();
        }
    } else {
        localStorage.setItem('username', e.target.innerText);
    }
}

// Get Focus 
function getFocus() {
    // want to check if there is a local storage item called name
    if (localStorage.getItem('focus') === null) {
        focus.textContent = '[Enter Focus]';
    } else {
        focus.textContent = localStorage.getItem('focus');
    }
}

// Set Name
function setFocus(e) {
    if (e.type === 'keypress') {
        // Make sure enter is pressed
        if (e.which == 13 || e.keyCode == 13) {
            localStorage.setItem('focus', e.target.innerText);
            focus.blur();
        }
    } else {
        localStorage.setItem('focus', e.target.innerText);
    }
}

username.addEventListener('keypress', setName);
username.addEventListener('blur', setName);
focus.addEventListener('keypress', setFocus);
focus.addEventListener('blur', setFocus);

// run showTime
showTime();
setBGreet();
getName();
getFocus();



