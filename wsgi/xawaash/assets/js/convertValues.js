//Author: Maher Kassim
// Tool for converting volumes/weights/length/temperature (to be expanded)
// for use on xawaash.com

function getSubmeasure(value, submeasures){
  for(i = 0; i < submeasures.length; i++){
	if (value >= eval(submeasures[i])){
	  return submeasures[i];
	}
  }
  return "";
}

function setDicts(){
  return [{
  liquid: [
    { english: "US", somali: "Mareykan", french: "Américaine", arabic: "أمريكي", to_metric: "4.92892" },
    { english: "Imperial", somali: "Ingiriis", french: "Impérial Britannique", arabic: "إمبراطوري بريطاني", to_metric: "5.91939" },
    { english: "Metric", somali: "Halbeegga Caalamiga", french: "Métrique", arabic: "متري", to_metric: "1" }
  ],
  weight: [
    { english: "Imperial", somali: "Ingiriis", french: "Impérial Britannique", arabic: "إمبراطوري بريطاني", to_metric: "28349.5" },
    { english: "Metric", somali: "Halbeegga Caalamiga", french: "Métrique", arabic: "متري", to_metric: "1" }
  ], 
  temp: [
	{ english: "kelvin", mult: "1", add: "273.15", unit: " K" },
    { english: "Celsius", mult: "1", add: "0", unit: "° C" },
    { english: "Fahrenheit", mult: "1.8", add: "32", unit: "° F" },
    { english: "Gas Mark", mult: "1.8", add: "32" }
  ], 
  length: [
    { english: "US", somali: "Mareykan", french: "Américaine", arabic: "أمريكي", to_metric: "25.4" },
    { english: "Metric", somali: "Halbeegga Caalamiga", french: "Métrique", arabic: "متري", to_metric: "1" }
  ]}, {
  liquid: [
    { english: "Teaspoon(s)", somali: "Qaaddo Yar", french: "Cuillère(s) à Café", arabic: "ملعقة صغيرة", scale: "1", type: "US", rem: "True", sub: ["1/2", "1/4", "1/8"] },
    { english: "Tablespoon(s)", somali: "Qaado Weyn", french: "Cuillère(s) à Soupe", arabic: "ملعقة كبيرة", scale: "3", type: "US", rem: "True" },
    { english: "Tablespoon(s) (Australian)", somali: "Qaado Weyn (Australian)", french: "Cuillère(s) à Soupe (Australien)", arabic: "ملعقة كبيرة (الاسترالي)", scale: "4", type: "US", rem: "False" },
    { english: "Fluid Ounce(s)", somali: "Wiqiyad dareere", french: "Ounze(s) fluide(s)", arabic: "أونصة سائلية", scale: "6", type: "US", rem: "False" },
    { english: "Cup(s)", somali: "Koob", french: "Tasse(s)", arabic: "كوب", scale: "48", type: "US", rem: "True", sub: ["1/2", "1/3", "1/4"] },
    { english: "Pint(s)", somali: "Baayint", french: "Pinte(s)", arabic: "باينت", scale: "96", type: "US", rem: "False" },
    { english: "Quart(s)", somali: "Kuwart", french: "Litre(s)", arabic: "كوارت", scale: "192", type: "US", rem: "False" },
    { english: "Gallon(s)", somali: "Gaalon", french: "Gallon(s)", arabic: "جالون", scale: "768", type: "US", rem: "False" },
    { english: "Teaspoon(s)", somali: "Qaaddo Yar", french: "Cuillère(s) à Café", arabic: "ملعقة صغيرة", scale: "1", type: "Imperial", rem: "True", sub: ["1/2", "1/4", "1/8"]},
    { english: "Tablespoon(s)", somali: "Qaado Weyn", french: "Cuillère(s) à Soupe", arabic: "ملعقة كبيرة", scale: "3", type: "Imperial", rem: "True" },
    { english: "Fluid Ounce(s)", somali: "Wiqiyad dareere", french: "Ounze(s) fluide(s)", arabic: "أونصة سائلية", scale: "6", type: "Imperial", rem: "False" },
    { english: "Cup(s)", somali: "Koob", french: "Tasse(s)", arabic: "كوب", scale: "48", type: "Imperial", rem: "True", sub: ["1/2", "1/3", "1/4"] },
    { english: "Pint(s)", somali: "Baayint", french: "Pinte(s)", arabic: "باينت", scale: "96", type: "Imperial", rem: "False" },
    { english: "Quart(s)", somali: "Kuwart", french: "Litre(s)", arabic: "كوارت", scale: "192", type: "Imperial", rem: "False" },
    { english: "Gallon(s)", somali: "Gaalon", french: "Gallon(s)", arabic: "جالون", scale: "768", type: "Imperial", rem: "False" },
    { english: "Milliliter(s)", somali: "Mililitir", french: "Millilitre(s)", arabic: "مليلتر", scale: "1", type: "Metric", rem: "False"},
    { english: "Deciliter(s)", somali: "Desilitir", french: "Décilitre(s)", arabic: "ديسيلتر", scale: "100", type: "Metric", rem: "False"},
	{ english: "Cup(s)", somali: "Koob", french: "Tasse(s)", arabic: "كوب متري", scale: "250", type: "Metric", rem: "False"},
    { english: "Liter(s)", somali: "Litir", french: "Liter(s)", arabic: "لتر", scale: "1000", type: "Metric", rem: "False"}
  ],
  weight: [
    { english: "Ounce(s)", somali: "Wiqiyad", french: "Once(s)", arabic: "أونصة", scale: "1", type: "Imperial", rem: "True" },
    { english: "Pound(s)", somali: "Rodol", french: "Livre(s)", arabic: "رطل", scale: "16", type: "Imperial", rem: "True" },
    { english: "Stone(s)", somali: "Stoon", french: "Pierre(s)", arabic: "ستون", scale: "224", type: "Imperial", rem: "True" },
    { english: "Short Ton(s)", somali: "Tan", french: "Tonne(s) courte(s)", arabic: "طن أمريكي", scale: "32000", type: "Imperial", rem: "False" },
    { english: "Long Ton(s)", somali: "Tan (Mareykan)", french: "Tonne(s) longue(s)", arabic: "طن إنجليزي", scale: "35840", type: "Imperial", rem: "False" },
    { english: "Milligram(s)", somali: "Miligaraam", french: "Milligramme(s)", arabic: "ملليجرام", scale: "1", type: "Metric", rem: "False" },
    { english: "Gram(s)", somali: "Garaam", french: "Gramme(s)", arabic: "جرام", scale: "1000", type: "Metric", rem: "False" },
    { english: "Kilogram(s)", somali: "Kiilogaraam", french: "Kilogramme(s)", arabic: "كليوجرام", scale: "1000000", type: "Metric", rem: "False" },
    { english: "Metric Ton(s)", somali: "Tan", french: "Tonne(s)", arabic: "طن", scale: "1000000000", type: "Metric", rem: "False" }
  ],
  temp: [
	{ english: "Gas Mark", somali: "Kulka Gaaska", french: "Thermostat", arabic: "حرارة الغاز", scale: "0", type: "Gas Mark" },
	{ english: "None", somali: "None", french: "Thermostat 1", arabic: "None", scale: "86", type: "Gas Mark" },
    { english: "None", somali: "None", french: "Thermostat 2", arabic: "None", scale: "140", type: "Gas Mark" },
    { english: "None", somali: "None", french: "Thermostat 3", arabic: "None", scale: "194", type: "Gas Mark" },
	{ english: "Gas Mark 1/4 (Cool Oven)", somali: "Kulka Gaaska 1/4", french: "None", arabic: "حرارة الغاز 1/4", scale: "225", type: "Gas Mark" },
	{ english: "Gas Mark 1/2 (Cool Oven)", somali: "Kulka Gaaska 1/2", french: "Thermostat 4", arabic: "حرارة الغاز 1/2", scale: "250", type: "Gas Mark" },
    { english: "Gas Mark 1 (Very Low Oven)", somali: "Kulka Gaaska 1", french: "None", arabic: "حرارة الغاز 1", scale: "275", type: "Gas Mark" },
    { english: "Gas Mark 2 (Very Low Oven)", somali: "Kulka Gaaska 2", french: "Thermostat 5", arabic: "حرارة الغاز 2", scale: "300", type: "Gas Mark" },
    { english: "Gas Mark 3 (Low Oven)", somali: "Kulka Gaaska 3", french: "None", arabic: "حرارة الغاز 3", scale: "325", type: "Gas Mark" },
    { english: "Gas Mark 4 (Moderate Oven)", somali: "Kulka Gaaska 4", french: "Thermostat 6", arabic: "حرارة الغاز 4", scale: "350", type: "Gas Mark" },
    { english: "Gas Mark 5 (Moderate Oven)", somali: "Kulka Gaaska 5", french: "None", arabic: "حرارة الغاز 5", scale: "375", type: "Gas Mark" },
    { english: "Gas Mark 6 (Moderately Hot Oven)", somali: "Kulka Gaaska 6", french: "Thermostat 7", arabic: "حرارة الغاز 6", scale: "400", type: "Gas Mark" },
    { english: "Gas Mark 7 (Fairly Hot Oven)", somali: "Kulka Gaaska 7", french: "None", arabic: "حرارة الغاز 7", scale: "425", type: "Gas Mark" },
    { english: "Gas Mark 8 (Hot Oven)", somali: "Kulka Gaaska 8", french: "Thermostat 8", arabic: "حرارة الغاز 8", scale: "450", type: "Gas Mark" },
    { english: "Gas Mark 9 (Very Hot Oven)", somali: "Kulka Gaaska 9", french: "None", arabic: "حرارة الغاز 9", scale: "475", type: "Gas Mark" },
    { english: "Gas Mark 10 (Extremely Hot Oven)", somali: "Kulka Gaaska 10", french: "Thermostat 9", arabic: "حرارة الغاز 10", scale: "520", type: "Gas Mark" },
    { english: "° Celsius", somali: "° Selsiyas", french: "° Celsius", arabic: "° مئوية", scale: "0", type: "Celsius" },
	{ english: "kelvin", somali: "kelfin", french: "kelvin", arabic: "كلفن", scale: "0", type: "kelvin" },
    { english: "° Fahrenheit", somali: "° Fahrenhayt", french: "° Fahrenheit", arabic: "° فهرنهايت", scale: "0", type: "Fahrenheit" }
  ],
  length: [
	{ english: "Millimeter(s)", somali: "Millimitir", french: "Millimètre(s)", arabic: "ملليمتر", scale: "1", type: "Metric", rem: "False" },
	{ english: "Centimeter(s)", somali: "Sentimitir", french: "Centimètre(s)", arabic: "سنتيمتر", scale: "10", type: "Metric", rem: "False" },
	{ english: "Meter(s)", somali: "Mitir", french: "Mètre(s)", arabic: "متر", scale: "1000", type: "Metric", rem: "False" },
	{ english: "Kilometer(s)", somali: "Kiiloomitir", french: "Kilomètre(s)", arabic: "كيلومتر", scale: "1000000", type: "Metric", rem: "False" },
	{ english: "Inch(es)", somali: "Inji", french: "Pouce(s)", arabic: "بوصة", scale: "1", type: "US", rem: "True" },
	{ english: "Foot", somali: "Tilaab/Tilaabood", french: "Pied(s)", arabic: "قدم", scale: "12", type: "US", rem: "True" },
	{ english: "Yard(s)", somali: "Yaardi", french: "Yard(s)", arabic: "ياردة", scale: "36", type: "US", rem: "True" },
	{ english: "Mile(s)", somali: "Mayl", french: "Mile(s)", arabic: "ميل", scale: "63360", type: "US", rem: "True" },
	{ english: "Nautical Mile(s)", somali: "Mayl Badeed", french: "Mile(s) Nautiques", arabic: "ميل بحري", scale: "72913.4", type: "US", rem: "False" }
  ],
  ing: [
	{ english: "sugar, brown", somali: "", french: "", arabic: "", scale: "0.8" },
	{ english: "sugar, confectioner's", somali: "", french: "", arabic: "", scale: "0.8" },
	{ english: "sugar, powdered", somali: "", french: "", arabic: "", scale: "0.8" },
  ]}];
}

function processInputs(base_id, langType, measureType){
	var userInput = {};

	userInput['fromIndex'] = document.getElementById(base_id + "from_unit").selectedIndex;
	userInput['fromUnit'] = document.getElementById(base_id + "from_unit").options[userInput['fromIndex']].text;
	userInput['toIndex'] = document.getElementById(base_id + "to_unit").selectedIndex;
	userInput['toUnit'] = document.getElementById(base_id + "to_unit").options[userInput['toIndex']].text;
	if (document.getElementById(base_id + "from_unit").options[userInput['fromIndex']].value == "1"){
		userInput['fromUnit'] = 0;
	}
	if (document.getElementById(base_id + "to_unit").options[userInput['toIndex']].value == "1"){
		userInput['toUnit'] = 0;
	}
	var oldValue = document.getElementById(base_id + "quant").value;
	if(!/^[0-9\.\/]*(\s[0-9\.\/]*)?$/.test(oldValue)){
		if(oldValue !== "You cannot enter values for Gas Mark"){
			alert("Invalid input. Please enter only numbers in one of the following formats: 1, 0.5, 1/2, 1 1/2");
		}
		document.getElementById(base_id + "quant").value = "";
		oldValue = "";
	}
	userInput['parsed'] = oldValue.split(' ');
	userInput['frac'] = eval(userInput['parsed'][1]);
	userInput['oldQuant'] = eval(userInput['parsed'][0]);
	if (userInput['frac']) {
		userInput['oldQuant'] += userInput['frac'];
	}
	return userInput;
}

function getData(langType, data, convType, inputs){
	var retrieved = {};
	for(var i = 0; i < data.length; i++){
	  var dictionaryItem = data[i][langType];
	  var type = data[i].type;
	  var convertedType = "";
	  for (var j = 0; j < convType.length; j++){
		var tempType = convType[j]['english'];
		if(tempType == type){
		  convertedType = convType[j][langType];
		  break;
		}
	  }
	  var altDictionaryItem = dictionaryItem + " (" + convertedType + ")";
	  if(inputs['fromUnit'] == dictionaryItem || inputs['fromUnit'] == altDictionaryItem){
		retrieved['fromScale'] = eval(data[i].scale);
		retrieved ['fromType'] = data[i].type;
	  }
	  if(inputs['toUnit'] == dictionaryItem || inputs['toUnit'] == altDictionaryItem){
		retrieved['entryIndex'] = i;
		retrieved['toScale'] = eval(data[i].scale);
		retrieved['toType'] = data[i].type;
		for (var j = 0; j < convType.length; j++){
		  var tempType = convType[j]['english'];
		  if(tempType == retrieved['toType']){
			retrieved['convertedToType'] = convType[j][langType];
			break;
		  }
		}
	  }
	}
	return retrieved;
}

function genericCalc(){
	var resultVal = 0;
	return resultVal
}

function convertVal(measureType, langType){
  var base_id = langType + "_" + measureType + "_";
	
  // Parse user inputs
  var inputs = processInputs(base_id, langType, measureType);

  // Set-up dictionaries
  var dicts = setDicts();
  var data = dicts[1][measureType];
  var convType = dicts[0][measureType];
  
  // Initialize variables for output
  var resultQuant = 0;
  var resultVal = "";
  var resultText = [];
  var convertedToType = "";
  var retrievedData = getData(langType, data, convType, inputs);
  var entryIndex = retrievedData['entryIndex'];
  var fromType = retrievedData['fromType'];
  var toType = retrievedData['toType'];
  var convertedToType = retrievedData['convertedToType'];  
  
  // Check if user input is valid/complete
  if (!inputs['fromUnit'] || !inputs['toUnit'] || (inputs['parsed'] == "" && fromType != "Gas Mark")){
    resultVal = "";
    resultText = [];
  } else {
	if(measureType == "temp"){
		var mult = 1, add = 0, sub = 0, toIndex = 0;
		for(var i = 0; i < convType.length; i++){
		  if(convType[i].english == fromType){
			mult /= parseFloat(convType[i].mult);
			sub = parseFloat(convType[i].add);
		  }
		  if(convType[i].english == toType){
		    toIndex = i;
			mult *= parseFloat(convType[i].mult);
			add = parseFloat(convType[i].add);
		  }
		}
		var quantity = retrievedData['fromScale'] || inputs['oldQuant'];
		resultVal = ( quantity - sub )*mult + add;
		resultString = 0 + parseFloat(resultVal.toFixed(2));
		resultString += convType[toIndex].unit;
		if(toType == "Gas Mark" && data[entryIndex].scale == "0"){
			var closest = 0;
			for(var i = 0; i < data.length; i++){
				var curVal = eval(data[closest].scale);
				var nextVal = eval(data[i].scale);
				if((!closest || Math.abs(resultVal - nextVal) < Math.abs(resultVal - curVal)) && data[i][langType] != "None" && data[i].type == "Gas Mark"){
					closest = i;
				}
			}
			resultString = data[closest][langType];
			resultVal = resultString + ": " + eval(data[closest].scale) + "° F";
		}
		if (fromType == "Gas Mark"){
			if(langType == "english"){
				document.getElementById(base_id + "quant").value="You cannot enter values for Gas Mark";
			} else {
				document.getElementById(base_id + "quant").value="";
			}
		}
		document.getElementById(base_id + "result_box").value=resultVal;
		document.getElementById(base_id + "result_text").innerHTML=resultString;
		return 0;
	}
	
	var typeConversion = 1;
	if(fromType != toType){
	  for(var i = 0; i < convType.length; i++){
	    if(convType[i].english == fromType){
		  typeConversion *= parseFloat(convType[i].to_metric);
		}
		if(convType[i].english == toType){
		  typeConversion /= parseFloat(convType[i].to_metric);
		}
	  }
	}
	
	var quant = inputs['oldQuant']*retrievedData['fromScale']*typeConversion;
	resultQuant = quant/retrievedData['toScale'];
	resultVal = resultQuant;
	var numerator = quant % retrievedData['toScale'];
	var denominator = retrievedData['toScale'];
	var frac_array;
	var whole = 0;
	if(numerator > 0){
		if (inputs['parsed'][0] && inputs['parsed'][0].split('/').length > 1){
		  frac_array = inputs['parsed'][0].split('/');
		} else if (inputs['parsed'][1] && inputs['parsed'][1].split('/').length > 1){
		  frac_array = inputs['parsed'][1].split('/');
		  whole = eval(inputs['parsed'][0]);
		}
		if(frac_array){
		  denominator = eval(frac_array[1])*retrievedData['toScale'];
		  numerator = ((whole*eval(frac_array[1]) + eval(frac_array[0]))*retrievedData['fromScale']*typeConversion) % denominator;
		}
		if (fromType == toType){
		  var gcd_val = gcd(denominator, numerator);
		  if(gcd_val >= 1){
		  	resultVal = Math.floor(resultQuant) || "";
			resultVal += " " + numerator/gcd_val + "/" + denominator/gcd_val;
		  }
		}
	}
	var scale = retrievedData['toScale'];
	var submeasure = "";
	while(quant > 0 && entryIndex >= 0){
	  if(toType == "Metric" || measureType == 'weight'){
		resultVal = quant/scale;
	    resultText.push(quant/scale + " " + data[entryIndex][langType]);
		break;
	  } else {
		var floored = Math.floor(quant/scale)
		if(data[entryIndex].scale == "1"){
		  floored = Math.round(quant/scale);
		}
		var subText = "";
		if(floored != 0){
		  if(data[entryIndex]['sub'] && quant%scale > 0) {
			var submeasureList = data[entryIndex].sub;
			submeasure = getSubmeasure(quant/scale - floored, submeasureList);
		  }
		  subText += floored;
		  if(submeasure){
		    subText += " " + submeasure;
		  }
		  subText += " " + data[entryIndex][langType];
		  resultText.push(subText);
		} else if(data[entryIndex]['sub']) {
		  var submeasureList = data[entryIndex].sub;
		  submeasure = getSubmeasure(quant/scale, submeasureList);
		  if (submeasure) {
		    subText += submeasure + " " + data[entryIndex][langType];
			resultText.push(subText);
		  }
		}
		quant %= scale;
		if(submeasure){
		  quant -= eval(submeasure) * scale;
		  submeasure = "";
		}
		var oldEntryIndex = entryIndex;
		entryIndex--;
		while(entryIndex >= 0 && data[entryIndex].rem == "False"){
		  entryIndex--;
		}
		if(entryIndex >= 0 && data[entryIndex].type == data[oldEntryIndex].type){
		  scale = parseInt(data[entryIndex].scale);
		} else {
		  break;
		}
	  }
	}
  }
  var resultString = resultText.join(" + ");
  if(resultText.length > 0){
	resultString += " (" + convertedToType + ")";
	if (fromType != toType && toType != "Metric"){
	  resultString = "~" + resultString;
	}
  }
  document.getElementById(base_id + "result_box").value=resultVal;
  document.getElementById(base_id + "result_text").innerHTML=resultString;
}

function gcd(x, y) {
	while (y != 0) {
		var z = x % y;
		x = y;
		y = z;
	}
	return x;
}