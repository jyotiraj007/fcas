
const shelljs = require('shelljs')
// Runnable command in terminal: ./subset -i GreatVibes-Regular.otf -o outputfont -u 0061:0063

function converter(inputFontFile,outPutFontFile,format){
    console.log('input file path',inputFontFile);
    console.log('output file path',outPutFontFile);
    if(process.platform=='darwin'){
        console.log('Mac platform')
        shelljs.exec(`${process.env.PWD}/lib/osx/subset -i ${inputFontFile} -o ${outPutFontFile} ${format}`)
    }else if(process.platform=='linux'){
        console.log('Linux platform')
        shelljs.exec(`${process.env.PWD}/lib/linux/x64//subset -i ${inputFontFile} -o ${outPutFontFile} ${format}`)
    }
}
function convertToWoff(inputFontFile,outPutFontFile){
    converter(inputFontFile,outPutFontFile,'-woff');
}

function convertToTTF(inputFontFile,outPutFontFile){
    converter(inputFontFile,outPutFontFile,'-ttf');
}

function convertToOTF(inputFontFile,outPutFontFile){
    converter(inputFontFile,outPutFontFile,'-otf');
}

function convertToEOT(inputFontFile,outPutFontFile){
    converter(inputFontFile,outPutFontFile,'-eot');
}

function convertToMultipleFormats(inputFontFile,outPutFontFile){
    converter(inputFontFile,outPutFontFile,'-woff -eot -ttf -otf');
}
module.exports={
    convertToWoff,
    convertToTTF,
    convertToEOT,
    convertToOTF,
    convertToMultipleFormats,

}