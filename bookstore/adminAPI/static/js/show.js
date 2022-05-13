function Show(){
    c = document.getElementById('ta');
    className = 'pop-up-off';
    if (c.classList.contains(className))
        c.classList.remove(className);
    else
        c.classList.add(className); 
}