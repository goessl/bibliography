var data = [
  {
    "type": "Booklet",
    "id": "la",
    "author": [
      "Maas, Axel"
    ],
    "title": "Linear Algebra",
    "subtitle": "Lecture in WS 2025/26 at the KFU Graz",
    "url": "https://static.uni-graz.at/fileadmin/_Persoenliche_Webseite/maas_axel/la.pdf"
  },
  {
    "type": "Booklet",
    "id": "funki",
    "author": [
      "Behrndt, Jussi",
      "Holzmann, Markus",
      "Schlosser, Peter"
    ],
    "title": "Funktionalanalysis und partielle Differentialgleichungen",
    "subtitle": "Skriptum",
    "note": "Wintersemester 2020/21"
  },
  {
    "type": "Book",
    "id": "dem1",
    "author": [
      "Demtröder, Wolfgang"
    ],
    "title": "Experimentalphysik 1",
    "subtitle": "Mechanik und Wärme",
    "date": "2021-07-30",
    "edition": 9,
    "publisher": "Springer Spektrum Berlin, Heidelberg",
    "isbn": "978-3-662-62728-0",
    "doi": "10.1007/978-3-662-62728-0",
    "url": "https://link.springer.com/book/10.1007/978-3-662-62728-0"
  },
  {
    "type": "Book",
    "id": "arens",
    "author": [
      "Arens, Tilo",
      "Hettlich, Frank",
      "Karpfinger, Christian",
      "Kockelkorn, Ulrich",
      "Lichtenegger, Klaus",
      "Stachel, Hellmuth"
    ],
    "title": "Mathematik",
    "date": "2022-08-04",
    "edition": 5,
    "publisher": "Springer Spektrum Berlin, Heidelberg",
    "isbn": "978-3-662-64389-1",
    "doi": "10.1007/978-3-662-64389-1",
    "url": "https://link.springer.com/book/10.1007/978-3-662-64389-1"
  }
];

//autocolumns would only scan first row
var fields = [...new Set(data.flatMap(Object.keys))];
var authors = [...new Set(data.flatMap(function (e) { return e.author || []; }))].sort();

//define formatting and filtering for each column
var columns = fields.map(function (field) {
  var column = {title: field,
                field: field };
  
  switch (field) {
    case "type":
      column.headerFilter = "list";
      column.headerFilterParams = {valuesLookup: true,
                                   clearable: true,
                                   multiselect: true };
      column.headerFilterFunc = "in";
      break;
    
    case "author":
      column.formatter = function (cell) {
        var values = cell.getValue() || [];
        return (
          "<ul>" +
          values.map(function (a) { return "<li>"+a+"</li>"; }).join("") +
          "</ul>"
        );
      };
      
      column.headerFilter = "list";
      column.headerFilterParams = {values: authors, clearable: true, multiselect: true};
      column.headerFilterFunc = function (headerValue, rowValue) {
        if (!headerValue || !headerValue.length) return true;
        return (rowValue || []).some(function (a) { return headerValue.includes(a); });
      };
      break;
    
    case "url":
      column.formatter = "link";
      column.formatterParams = {label: "link",
                                target: "_blank" };
      break;
    
    case "publisher":
      column.headerFilter = "list";
      column.headerFilterParams = {valuesLookup: true,
                                   clearable: true,
                                   multiselect: true };
      column.headerFilterFunc = "in";
      break;
    
    case "doi":
      column.formatter = "link";
      column.formatterParams = {
        label: function (cell) { return cell.getValue(); },
        url: function (cell) { return "https://doi.org/" + cell.getValue(); },
        target: "_blank"
      };
      column.headerFilter = "input";
      break;
    
    default:
      column.headerFilter = "input";
      break;
  }

  return column;
});

new Tabulator("#bibliography-table", {
  data: data,
  columns: columns
});
