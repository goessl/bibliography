var url = new URL('../bibliography.json', window.location.href).href;

fetch(url)
  .then(function(response) { return response.json(); })
  .then(function(data) {

//autocolumns would only scan first row
var allFields = new Set(data.flatMap(Object.keys));
var priority = ['type', 'id', 'author', 'editor', 'title', 'subtitle', 'date', 'note', 'edition', 'publisher', 'isbn', 'doi', 'url'];
var fields = [
  ...priority.filter(function(f) { return allFields.has(f); }),
  ...[...allFields].filter(function(f) { return !priority.includes(f); })
];
var authors = [...new Set(data.flatMap(function(e) { return e.author || []; }))].sort();
var editors = [...new Set(data.flatMap(function(e) { return e.editor || []; }))].sort();

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
    case "editor":
      column.formatter = function(cell) {
        var ul = document.createElement('ul');
        (cell.getValue() || []).forEach(function(a) {
          var li = document.createElement('li');
          li.textContent = a;
          ul.appendChild(li);
        });
        return ul;
      };
      column.headerFilter = "list";
      column.headerFilterParams = {values: field==='author'?authors:editors, clearable: true, multiselect: true};
      column.headerFilterFunc = function (headerValue, rowValue) {
        if(!headerValue || !headerValue.length) {
            return true;
        }
        return (rowValue || []).some(function (a) { return headerValue.includes(a); });
      };
      break;
    
    case "url":
      column.formatter = function(cell) {
        var val = cell.getValue();
        if(!val) {
            return '';
        }
        var a = document.createElement('a');
        a.href = val;
        a.textContent = 'link';
        a.target = '_blank';
        return a;
      };
      break;
    
    case "publisher":
      column.headerFilter = "list";
      column.headerFilterParams = {valuesLookup: true,
                                   clearable: true,
                                   multiselect: true };
      column.headerFilterFunc = "in";
      break;
    
    case "doi":
      column.formatter = function(cell) {
        var val = cell.getValue();
        if(!val) {
            return '';
        }
        var a = document.createElement('a');
        a.href = 'https://doi.org/' + val;
        a.textContent = val;
        a.target = '_blank';
        return a;
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

});
