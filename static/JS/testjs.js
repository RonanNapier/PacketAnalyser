var buttonClick = document.getElementById("btnClick");
buttonClick.addEventListener("click", function(){
    /*
    if (checkFile() === true){
        return true;
    }

     */
});

//Check the inputted file and validate that it is a .pcap extension.
//If succeeded then return true otherwise alert the user that they must upload a .pcap file.
function checkFile(){

    var allowedType = /(\.pcap)$/i;
    var uploadedFile = document.getElementById("btnFile");
    var filePath = uploadedFile.value;
    //var regex = new RegExp("([a-zA-Z0-9\s_\\.\-:])+(" + allowedFile.join('|') + ")$");
    if(!allowedType.exec(filePath)){
        alert("Please upload a file with the extension: .pcap");
    }
    else{
        return true;
    }

};

function doSubmit() {
    console.log("hey");
    var uploadForm = document.getElementById("uploadFile");
    if (checkFile() == true){
        console.log("hey2");
        uploadForm.submit();
    }

    return false;
}


