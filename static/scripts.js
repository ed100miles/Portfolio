console.log('JS loaded okay')

function loadbar(){
    setInterval(()=> {
        document.getElementById("wordProgressBar").value
        = document.getElementById("wordProgressBar").value + 1;
        if (document.getElementById("wordProgressBar").value === 100){
            document.getElementById("wordProgressBar").value = 1
        }
    }, 50)
}
