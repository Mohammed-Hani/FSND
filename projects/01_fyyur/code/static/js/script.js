window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

function toggleSeekDescript(ev) {
    let seeking_description = document.getElementById('seeking_description').parentNode;
    if (ev.target.checked)
        seeking_description.classList.remove('hidden');
    else
        seeking_description.classList.add('hidden');
}
