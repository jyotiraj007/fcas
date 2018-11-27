//const subsetFactory = require('./subsetFactory');
//const converterFactory = require('./converterFactory');

const fontFactory = function () {

    let factories = this;
    const factoryList = [{
            option: 'subset',
            source: './subsetFactory'
        },
        {
            option: 'convert',
            source: './converterFactory'
        }
    ];

    factoryList.forEach(function(factory){
        console.log('source '+factory.source)
        factories[factory.option]=require(factory.source);
    });

    console.log(JSON.stringify(factories,null,4));

}

module.exports=new fontFactory;