/*
 * Simulated browser environment for Rhino
 *   By John Resig <http://ejohn.org/>
 * Copyright 2007 John Resig, under the MIT License
 */

// The window Object
window = this;

function Storage() {}
Storage.prototype = {
    get length() {
        var i=0;
        for(var k in this){
            if(Object.prototype.hasOwnProperty.call(this, k)) {
                i+=1;
            }
        }
        return i;
    },
    key: function(index) {
        var i=0;
        for(var k in this){
            if(Object.prototype.hasOwnProperty.call(this, k)) {
                if(i===index) {
                    return this[k];
                }
                i+=1;
            }
        }
    },
    getItem: function(k) {
        return this[k];
    },
    setItem: function(k,data) {
        if(data!== undefined) {
            if(this[k] === undefined) {
                this[k] = data;
                Storage.prototype.length += 1;
            }
        }
    },
    removeItem: function(k) {
        delete this[k]
    },

    clear: function() {
        for(var k in this){
            if(Object.prototype.hasOwnProperty.call(this, k))
            {
                delete this[k];
            }
            //
        }
    },

    toString: function() {
        var s="{";
        for(var k in this){
            if(Object.prototype.hasOwnProperty.call(this, k))
            {
                s+=(k+": "+this[k]+", ");
            }
            //
        }
        s+="}";
        return s;
    }
};

// navigator.localStorage = new Storage();
window.localStorage=new Storage();

//function setTimeout(x,y) {
////alert("----------------"+y);
////alert(y==='0');
//if(y===0) {
////alert("++++++++++++++++++"+y);
//    x();
//}
//alert("\n------------------------------------- setTimeout --------------------------------------------\n")
//alert("setTimeout('"+x+"',"+y+",)")
//alert("\n===================================== setTimeout ============================================\n")
//};
window.attachEvent=function(x,y){
alert('[attachEvent] '+x);
if (y !== undefined && ['onreadystatechange'].indexOf(x)>=0) {
        y();
    }
}
window.document.attachEvent=window.attachEvent;

//eval2=eval;
//eval=function(code) {
////alert(code);
//var res= eval2(code);
////alert("Done!");
//return res;
//}


MimeType = function (description, suffixes, type) {
    this.description=description;
    this.suffixes=suffixes;
    this.type=type;
};


m0= new MimeType('FutureSplash Player', 'spl', "application/futuresplash");
m1= new MimeType('Shockwave Flash', 'swf', "application/x-shockwave-flash");

Plugin = function() {
    this[0]=m1;
    this[1]=m0;
    this.description= "Shockwave Flash 32.0 r0";
    this.filename= "Flash Player.plugin";
    this.version= "32.0.0.101";
    this.name= "Shockwave Flash";
    this.length = 2;
};

pligin=new Plugin();
m0.enabledPlugin=pligin;
m1.enabledPlugin=pligin;

MimeType = function (description, suffixes, type) {
    this.description=description;
    this.suffixes=suffixes;
    this.type=type;
}

navigator.mimeTypes = {
0: m0,
1: m1,
'application/futuresplash': m0,
'application/x-shockwave-flash': m1,
'lenth': 2
}


function Promise(f) {
    this.f=f;
}

Promise.prototype.then = function (f2) {
    this.f(f2);
}

navigator.mediaDevices= {
    enumerateDevices: function () {
        devices=new function () {
            this.length= 3;
            this[0]={kind: 'videoinput', label: '', deviceId: 'q3NLZogBe9MO0G+EQSu/IuQCsGkbJYn0l73zg0TdutI='};
            this[1]={kind: 'audioinput', label: '', deviceId: 'qT4HvK0ZR5M6z7yRj2DNylUFcIs3fIaZLNPNUQatJtk='};
            this[2]={kind: 'audioinput', label: '', deviceId: '/9msAmAB0tNGkuiN3kUQSdopkcR675wZRAt+2hkThkw='};
        };

        return new Promise(function(thenfunc){
        alert(devices);
        return thenfunc(devices);
        })
    }
}


