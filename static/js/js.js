function CutDiv(divname){
    document.getElementById(divname).style.display = 'none';
}

var ninput = 2

function AddInput(){
    if (ninput>=2){
        
        ninput = ninput+ 1;
        var div = document.getElementById('optionsdiv');
        div.innerHTML += '<div id="optioninputdiv'+ninput+'"><label for="">'+ninput+' : </label><input name="option'+ninput+'" required id="optiondiv'+ninput+'" type="text"></div>'
        console.log(ninput)
        if(ninput>2){
            document.getElementById('removeinputbtn').style.display = 'flex';
        }
}
}

function RemoveInput(){

    var div = document.getElementById('optioninputdiv'+ninput);
    div.remove();
    ninput = ninput - 1;
    
    if(ninput==2){
        document.getElementById('removeinputbtn').style.display = 'none';
    }
    console.log(ninput)
}



function ChangeBtnBg(id,color){
    document.getElementById(id).style.backgroundColor = color;
}

var sidebar = 'hidden';

function SideBarToggle(){
    if (sidebar == 'hidden'){
        document.getElementById('sidebar').style.display = 'flex';
        document.getElementById('sidebartoggelbtn').style.backgroundColor = '#a1e4ff';
        sidebar = 'visible';
    }else{
        document.getElementById('sidebar').style.display = 'none';
        document.getElementById('sidebartoggelbtn').style.backgroundColor = 'transparent';
        sidebar = 'hidden';

    }
   
};
