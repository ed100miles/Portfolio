var right=document.getElementById('scrabbleWords').style.height;
var left=document.getElementById('scrabbleForm').style.height;
if(left>right)
{
    document.getElementById('scrabbleWords').style.height=left;
}
else
{
    document.getElementById('scrabbleForm').style.height=right;
}
