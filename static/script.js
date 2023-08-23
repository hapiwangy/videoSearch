document.getElementById("box").addEventListener("mouseenter", function() {
    document.getElementById("tooltip").style.display = "block";
});

document.getElementById("box").addEventListener("mouseleave", function() {
    document.getElementById("tooltip").style.display = "none";
});
